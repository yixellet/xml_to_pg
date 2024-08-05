from xml.etree.ElementTree import Element
from typing import Union
import re
from shapely import Point, LineString, Polygon

from ..constants.msk_zones import MSK_ZONES
from ..constants.geometry_types import GEOMETRY_TYPES

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
            east = point.x()
            nord = point.y()
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

    def extract_geometry(self, to_wgs: bool = False) -> \
        list[dict[str, Union[QgsGeometry, None]]]:
        """Извлекает геометрию, преобразует координаты
        
        :param to_wgs: Флаг, указывающий на необходимость преобразования
        геометрии в систему координат WGS-84, defaults to False
        :type to_wgs: bool, optional

        :returns: Возвращает список словарей формата {'geom': <QgsGeometry>,
        'msk_zone': <зона МСК-30 (1 или 2)>}
        :rtype: list 
        """
        if self.root_element == None:
            msk_zone = self.define_msk_zone()
            geometry_type = self.define_geometry_type()
            null_result = [
                {'geom': None, 'crs': msk_zone, 'geometry_type': geometry_type}]
            return null_result

        temp_result = {}

        contours = self.root_element.find('contours')
        for contour in contours.findall('contour'):
            geom_contour = self.extract_single_contour(contour)
            if geom_contour['crs'] not in temp_result:
                temp_result[geom_contour['crs']] = geom_contour
            else:
                temp_result[geom_contour['crs']]['geom'].addPartGeometry(geom_contour['geom'])
        return list(temp_result.values())

    def extract_single_contour(self, 
                               root_element: Element = '', to_wgs: bool = False) -> \
        dict[str, Union[str, QgsGeometry]]:
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

        result = {}
        if self.object_type == 'quarters':
            root_element = self.root_element

        entity_spatial = root_element.find('entity_spatial')
        msk_zone = ''
        geometry_type = ''
        spatials_elements = entity_spatial.find('spatials_elements')
        if spatials_elements:
            contour = None
            for se_idx, spatial_element \
                    in enumerate(spatials_elements.findall('spatial_element')):
                ords = spatial_element.find('ordinates')
                ordinates_arr = []
                for ordinate in ords.findall('ordinate'):
                    nord = float(ordinate.find('x').text)
                    east = float(ordinate.find('y').text)
                    ordinates_arr.append(Point(east, nord))
                
                geometry_type = self.define_geometry_type(ordinates_arr)
                if se_idx == 0:
                    msk_zone = self.define_msk_zone(
                        ordinates_arr[0], 
                        self.extract_sk_id(entity_spatial))
                    if geometry_type == GEOMETRY_TYPES[1]:
                        contour = LineString(ordinates_arr)
                    if geometry_type == GEOMETRY_TYPES[2]:
                        contour = Polygon(ordinates_arr)
                else:                
                    if geometry_type == GEOMETRY_TYPES[1]:
                        contour.addPartGeometry(
                            QgsGeometry.fromPolyline(ordinates_arr))
                    if geometry_type == GEOMETRY_TYPES[2]:
                        contour_part = QgsGeometry.fromPolygonXY(
                            [ordinates_arr])
                        if se_idx == 0:
                            contour.addPartGeometry(contour_part)
                        else:
                            polygon_geometry_engine = \
                                QgsGeometry.createGeometryEngine(contour_part.constGet())
                            polygon_geometry_engine.prepareGeometry()
                            if polygon_geometry_engine.within(contour.constGet()):
                                contour.addRing(list(reversed(ordinates_arr)))
                            else:
                                contour.addPartGeometry(contour)
            result['geom'] = contour
            result['crs'] = msk_zone
            result['geometry_type'] = geometry_type
        else:
            result = {'geom': None, 'crs': msk_zone, 'geometry_type': geometry_type}
        return result
