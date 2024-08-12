from xml.etree.ElementTree import Element

from .ParserElements import ParserElements as PE
from .Geometry import Geometry

class BoundaryRecord():
    """
    Инструмент для извлечения информации об отдельном земельном участке
    """

    OBJECT_TYPE = 'boundaries'

    def __init__(self, root_element: Element) -> None:
        self.root_element = root_element
        self.data = {
            'content': self.OBJECT_TYPE
        }
        self.geometry = None
    
    def parse(self):
        """
        reg_numb_border
        type_boundary
        -- record_info
        decisions_requisites
        map_plan_information
        contours_location
        special_notes
        """

        boundary_record = self.root_element.find('boundary_record')

        boundary_record_content = None

        if boundary_record.find('municipal_boundary'):
            boundary_record_content = boundary_record.find('municipal_boundary')

        if boundary_record.find('subject_boundary'):
            boundary_record_content = boundary_record.find('subject_boundary')

        if boundary_record.find('inhabited_locality_boundary'):
            boundary_record_content = boundary_record.find('inhabited_locality_boundary')

        # Реестровый номер границы
        self.data['reg_numb_border'] = boundary_record_content.find('reg_numb_border').text

        # Тип границы
        type_boundary = boundary_record_content.find('type_boundary')
        if type_boundary:
            self.data['type_boundary'] = PE.parse_dict(type_boundary)

        # Record info
        record_info = self.root_element.find('record_info')
        if record_info:
            self.data.update(PE.parse_record_info(record_info))
        
        # Contours location
        geometry = Geometry(self.root_element.find('contours_location'),
                            self.OBJECT_TYPE,
                            self.data['cad_number'])
    
        contour = geometry.extract_geometry()
        self.geometry = contour
    
    def parse_params(self) -> None:
        """Параметры земельного участка"""

        element = self.root_element.find('params')
        
        # Категория разрешенного использования
        self.data['category'] = PE.parse_dict(
            element.find('category').find('type'))

        # Площадь
        a = element.find('area')
        self.data['area'] = float(a.find('value').text)
        
        if a.find('inaccuracy') != None:
            self.data['area_inaccuracy'] = float(a.find('inaccuracy').text)
        
        if a.find('type') != None:
            self.data['area_type'] = PE.parse_dict(a.find('type'))

        # Вид разрешенного использования
        if element.find('permitted_use') != None:
            pue = element.find('permitted_use').find('permitted_use_established')
            if pue.find('by_document') != None:
                self.data['land_use_by_document'] = pue.find('by_document').text
            if pue.find('land_use') != None:
                self.data['land_use'] = dict(pue.find('land_use'))
            if pue.find('land_use_mer') != None:
                self.data['land_use_mer'] = dict(pue.find('land_use_mer'))

        # Вид разрешенного использования по градостроительному регламенту
        if element.find('permittes_uses_grad_reg') != None:
            pugr = element.find('permittes_uses_grad_reg')
            if pugr.find('reg_numb_border') != None:
                self.data['gr_reg_numb_border'] = pugr.find('reg_numb_border').text
            if pugr.find('land_use') != None:
                self.data['gr_land_use'] = dict(pugr.find('land_use'))
            if pugr.find('permitted_use_text') != None:
                self.data['gr_permitted_use_text'] = pugr.find('permitted_use_text').text
