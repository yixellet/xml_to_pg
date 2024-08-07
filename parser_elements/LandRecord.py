from xml.etree.ElementTree import Element

from .ParserElements import ParserElements as PE
from .Geometry import Geometry

class LandRecord():
    """
    Инструмент для извлечения информации об отдельном земельном участке
    """

    OBJECT_TYPE = 'lands'

    def __init__(self, root_element: Element) -> None:
        self.root_element = root_element
        self.data = {
            'content': self.OBJECT_TYPE
        }
        self.geometry = None
    
    def parse(self):
        """
        -- record_info
        -- object
        apartment_building
        cad_links
        -- params
        address_location
        cad_works
        zones_and_boundaries
        survey_boundaries
        natural_objects
        government_land_supervision
        cost
        object_parts
        restrictions_encumbrances
        -- contours_location
        special_notes
        """

        # Record info
        record_info = self.root_element.find('record_info')
        if record_info:
            self.data.update(PE.parse_record_info(record_info))
        
        # Object
        object = self.root_element.find('object')
        self.data.update(PE.parse_common_data(object))
        subtype = object.find('subtype')
        if subtype:
            self.data['subtype'] = PE.parse_dict(subtype)
        self.parse_params()

        # Cad links
        cad_links = self.root_element.find('cad_links')
        if cad_links:
            common_land = cad_links.find('common_land')
            if common_land:
                common_land_cad_number = common_land.find('common_land_cad_number')
                if common_land_cad_number:
                    self.data['common_land_cad_number'] = \
                        common_land_cad_number.find('cad_number').text
        
        # Address location
        address_location = self.root_element.find('address_location')
        if address_location:
            self.data.update(
                PE.parse_address(self.root_element.find('address_location')))
        
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
