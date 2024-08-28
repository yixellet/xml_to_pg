from xml.etree.ElementTree import Element
from typing import Union
import re
from shapely import Point, LineString, Polygon, MultiLineString, MultiPolygon, union, normalize, to_wkt, geometry, make_valid, prepare, within, LinearRing

from constants.msk_zones import MSK_ZONES
from constants.geometry_types import GEOMETRY_TYPES

class Geometry():
    """
    Инструмент для извлечения геометрической информации об объектах ЕГРН
    """

    def __init__(self, element: Union[Element, None], 
                 object: str, 
                 cad_number: str) -> None:
        """Инициализация экземпляра класса Geometry

        :param element: Элемент XML документа, корневой для геометрии, 
        элементы типа contours_location и spatial_data
        :type element: Element
        :param object: Тип разбираемого объекта. Может принимать 
        значения lands, zones, constructions, buildings, borders, coastlines, quarters
        :type object: str
        :param cad_number: Кадастровый (регистрационный) номер
        :type cad_number: str
        """
        self.root_element = element
        self.object_type = object
        self.cad_number = cad_number
    
    def define_geometry_type(self, 
                             coords_array: Union[list[Point], None] = None) -> int:
        """Определяет тип геометрии (линия или полигон)

        :param coords_array: Список строк формата (x y)
        :type coords_array: list
        :return: Возвращает 1 - для линии, 2 - для полигона
        :rtype: int
        """
        
        match self.object_type:
            case 'constructions':
                if coords_array:
                    firstPoint = coords_array[0]
                    lastPoint = coords_array[-1]
                    if firstPoint.x() == lastPoint.x() and firstPoint.y() == lastPoint.y():
                        return GEOMETRY_TYPES[2]
                    else:
                        return GEOMETRY_TYPES[1]
                else:
                    GEOMETRY_TYPES[2]
            case 'coastlines':
                return GEOMETRY_TYPES[1]
            case _:
                return GEOMETRY_TYPES[2]

    def define_msk_zone(self, point: Union[Point, None] = None, 
                        sk_id: str = '') -> str:
        """Определяет зону в МСК-30 (Астраханская область)

        :param point: Точка
        :type point: QgsPointXY
        :param sk_id: Обозначение системы координат в XML документе
        :type sk_id: str, optional
        :return: Сокращенное обозначение СК
        :rtype: str
        """
        cad_number_splitted = re.split(r'[-:]', self.cad_number)
        region_code = cad_number_splitted[0]    # '30'
        # TODO: Разработать алгоритм определения МСК других субъектов
        if point:
            east = point[0]
            nord = point[1]
            return region_code + '.' + str(east)[0]
        return 'no_geometry'

    @staticmethod
    def extract_sk_id(entity_spatial: Element) -> Union[str, None]:
        """
        Извлекает из XML документа обозначение системы координат

        :param entity_spatial: Элемент типа entity_spatial
        :type entity_spatial: Element
        :return: Обозначение СК в документе или None
        :rtype: Union[str, None]
        """
        sk_id = entity_spatial.find('sk_id')
        if sk_id:
            return sk_id.text
        
        return None

    def extract_single_contour(self, 
                               root_element: Element = None, 
                               contours_count: int = 1,
                               to_wgs: bool = False) -> \
        dict[str, Union[str, MultiLineString, MultiPolygon]]:
        """
        Извлекает геометрическую информацию из одного конкретного контура
        (элемент contour или spatial_data)
        
        :param root_element: Элемент XML документа, корневой для геометрии, 
        элементы типа contour и spatial_data
        :type root_element: Element
        :param to_wgs: Флаг, определяющий необходимость пересчета координат
        в WGS-84, defaults to False
        :type to_wgs: bool, optional
        :return: Словарь {'geom': QgsGeometry, 'crs': str}
        :rtype: dict
        """
        if self.object_type == 'quarters':
            root_element = self.root_element
        entity_spatial = root_element.find('entity_spatial')
        spatials_elements = entity_spatial.find('spatials_elements')
        if spatials_elements:
            spatials_elements_array = spatials_elements.findall('spatial_element')
            first_spatial_element = []  # [ (x, y), (x,y), ... ]
            other_spatial_elements = [] # [ ( (x, y), (x,y), ... ), ... ]
            for i in range(len(spatials_elements_array)-1):
                ordinates = spatials_elements_array[i].find('ordinates')
                points_arr = []
                for ordinate in ordinates.findall('ordinate'):
                    points_arr.append(
                            (float(ordinate.find('y').text), 
                             float(ordinate.find('x').text)))
                if i == 0:
                    first_spatial_element += points_arr
                    geometry_type = self.define_geometry_type(points_arr)
                    msk_zone = self.define_msk_zone(
                        points_arr[0], 
                        self.extract_sk_id(entity_spatial))
                else:
                    other_spatial_elements.append(tuple(points_arr))
            if contours_count > 1:
                contour_geometry = [(tuple(first_spatial_element), other_spatial_elements)]
            else:
                if self.object_type == 'quarters':
                    contour_geometry = MultiPolygon([(tuple(first_spatial_element), other_spatial_elements)])
                else:
                    if len(other_spatial_elements) != 0:
                        result = {}
                        parts_count = 1
                        current_shell = first_spatial_element
                        for other_element in other_spatial_elements:
                            shell_poly = Polygon(current_shell)
                            checking_poly = Polygon(other_element)
                            prepare(checking_poly)
                            is_hole = within(checking_poly, shell_poly)
                            if is_hole:
                                if parts_count not in result:
                                    result[parts_count] = [current_shell, [other_element]]
                                else:
                                    result[parts_count][1].append(other_element)
                            else:
                                parts_count += 1
                                current_shell = other_element
                                result[parts_count] = [current_shell, []]
                        contour_geometry = []
                        for g in result.values():
                            contour_geometry.append((tuple(g[0]), g[1]))
                    else:
                        contour_geometry = [(tuple(first_spatial_element), other_spatial_elements)]
            return {
                'geom': contour_geometry, 
                'crs': msk_zone, 
                'geometry_type': geometry_type}
        else:
            return {
                'geom': None, 
                'crs': 'no_geometry', 
                'geometry_type': 'no_geometry'}

    def extract_geometry(self, to_wgs: bool = False) -> \
        list[dict[str, Union[MultiLineString, MultiPolygon, None]]]:
        """Извлекает геометрию, преобразует координаты
        
        :param to_wgs: Флаг, указывающий на необходимость преобразования
        геометрии в систему координат WGS-84, defaults to False
        :type to_wgs: bool, optional

        :returns: Возвращает список словарей формата {'geom': <QgsGeometry>,
        'msk_zone': <зона МСК-30 (1 или 2)>}
        :rtype: list 
        """
        self.null_result = {'geom': None, 'crs': 'no_geometry', 'geometry_type': 'no_geometry'}
        if self.root_element == None:
            
            return [self.null_result]

        temp_result = {}
        result = []
        geometry_type = None

        contours = self.root_element.find('contours')
        contours_array = contours.findall('contour')
        for contour in contours_array:
            geom_contour = self.extract_single_contour(contour, len(contours_array))
            geometry_type = geom_contour['geometry_type']
            if geometry_type == 'no_geometry':
                result.append(self.null_result)
            else:
                if geom_contour['crs'] not in temp_result:
                    temp_result[geom_contour['crs']] = geom_contour['geom']
                else:
                    temp_result[geom_contour['crs']].append(geom_contour['geom'][0])
        
        for key, value in temp_result.items():
            result.append({'crs': key, 'geom': MultiPolygon(value)})
        return result