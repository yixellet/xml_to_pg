from xml.etree.ElementTree import Element

from .ParserElements import ParserElements as PE
from .Geometry import Geometry

class Zone():
    """
    Инструмент для извлечения информации об отдельной зоне
    """

    OBJECT_TYPE = 'zones'

    def __init__(self, root_element: Element, 
                 root_tag: str = 'extract_about_zone') -> None:
        self.root_element = root_element
        self.root_tag = root_tag
        self.data = {
            'content': self.OBJECT_TYPE
        }
        self.geometry = None
        match self.root_tag:
            case 'extract_cadastral_plan_territory':
                self.contours_tag = 'b_contours_location'
            case 'extract_about_zone':
                self.contours_tag = 'contours_location'
    
    def parse(self):
        """
        -- reg_numb_border
        -- type_boundary
        -- record_info
        -- object
        decisions_requisites
        content_restrict_encumbrances
        permitted_uses
        map_plan_information
        -- contours_location
        included_parcels
        """

        # Record info
        record_info = self.root_element.find('record_info')
        if record_info:
            self.data.update(PE.parse_record_info(record_info))
        
        # Object
        if self.root_tag == 'extract_cadastral_plan_territory':
            
            b_object_zt = self.root_element.find('b_object_zones_and_territories')
            b_object = b_object_zt.find('b_object')
            self.parse_b_object(b_object)
            self.parse_object_info(b_object_zt)

        if self.root_tag == 'extract_about_zone':
            zt = self.root_element.find('zones_and_territories')
            self.parse_b_object(zt)
            self.parse_object_info(zt.find('object'))

        # Contours location
        geometry = Geometry(self.root_element.find(self.contours_tag),
                            self.OBJECT_TYPE,
                            self.data['reg_numb_border'])
        contour = geometry.extract_geometry()
        self.geometry = contour
    
    def parse_b_object(self, element: Element) -> None:
        """Извлекает значения полей reg_numb_border и type_boundary

        :param element: Корневой элемент
        :type element: Element
        """
        self.data['reg_numb_border'] = element.find('reg_numb_border').text
        self.data['type_boundary'] = PE.parse_dict(element.find('type_boundary'))

    def parse_object_info(self, element):

        type_zone = element.find('type_zone')
        if type_zone:
            self.data['type_zone'] = PE.parse_dict(type_zone)
        description = element.find('description')
        if description:
            self.data['description'] = description.text

        name_by_doc = element.find('name_by_doc')
        if name_by_doc:
            self.data['name_by_doc'] = name_by_doc.text

        number = element.find('number')
        if number:
            self.data['number'] = number.text

        index = element.find('index')
        if index:
            self.data['index'] = index.text

        authority_decision = element.find('authority_decision')
        if authority_decision:
            self.data['authority_decision'] = authority_decision.text

        other = element.find('other')
        if other:
            self.data['other'] = other.text
