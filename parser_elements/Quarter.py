from .Geometry import Geometry

class Quarter():
    """Извлекает инфо о кадастровом квартале
    """

    OBJECT_TYPE = 'quarters'

    def __init__(self, root_element) -> None:
        """_summary_

        Args:
            root_element (_type_): cadastral_block
        """
        self.root_element = root_element
        self.data = {
            'content': self.OBJECT_TYPE
        }

    def parse(self):
        self.data['cad_number'] = self.root_element.find('cadastral_number').text
        area_quarter = self.root_element.find('area_quarter')
        self.data['area'] = float(area_quarter.find('area').text)
        self.data['unit'] = area_quarter.find('unit').text

        geometry = Geometry(self.root_element.find('spatial_data'), 'quarters', self.data['cad_number'])
        contour = geometry.extract_single_contour()
        self.data.update(contour)
