import xml.etree.ElementTree as ET
from datetime import date
import re
from parser_elements.Quarter import Quarter
from parser_elements.LandRecord import LandRecord
from parser_elements.Zone import Zone
from parser_elements.ParserElements import ParserElements as PE
from insert_into_table import insert_into_table

class Parser():
    
    FILE_TYPES = {
        'extract_about_property_land': {
            'name': 'Кадастровая выписка о земельном участке'
        },
        'extract_about_property_construction': {
            'name': 'Кадастровая выписка об объекте капитального строительства'
        },
        'extract_about_boundary': {
            'name': 'Кадастровая выписка об административной границе'
        },
        'extract_about_property_build': {
            'name': 'Кадастровая выписка о здании'
        },
        'extract_about_property_property_complex': {
            'name': 'Кадастровая выписка о предприятии как имущественном комплексе'
        },
        'extract_about_property_room': {
            'name': 'Кадастровая выписка о помещении'
        },
        'extract_about_property_under_construction': {
            'name': 'Кадастровая выписка об объекте незавершенного строительства'
        },
        'extract_about_property_unified_real_estate_complex': {
            'name': 'Кадастровая выписка о едином недвижимом комплексе'
        },
        'extract_about_zone': {
            'name': 'Выписка о зоне с особыми условиями использования территорий'
        },
        'extract_cadastral_plan_territory': {
            'name': 'Кадастровый план территории'
        }
    }

    def __init__(self, xml):
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
    
    def getFileType(self) -> dict[str, str, str, date]:
        """
        Выполняет первичную проверку XML документа по корневому тегу,
        является ли он выпиской из ЕГРН.
        Если корневой тег документа соответствует одному из тегов,
        перечисленных в константе FILE_TYPES, функция генерирует словарь
        следующего формата:
        {
            'tag': <корневой тег>,
            'name': <тип документа (на русском языке)>,
            'cadastral_number': <кадастровый (регистрационный) номер
                объекта, описанного в документе>,
            'date_formation': <дата формирования настоящего документа>
        }
        """
        result = None
        if self.root.tag in self.FILE_TYPES.keys():
            result = {'tag': self.root.tag, 
                      'name': self.FILE_TYPES[self.root.tag]['name'],
                      'date_formation': date.fromisoformat(PE.parse_details_statement(self.root)['date_formation'])}
            if self.root.tag == 'extract_cadastral_plan_territory':
                quarter = Quarter(self.root)
                quarter.parse()
                result.update({
                    'cad_number': quarter.data['cadastral_number']})
            elif self.root.tag == 'extract_about_property_land':
                object = self.root.find('land_record').find('object')
                result.update({
                    'cad_number': PE.parse_common_data(object)['cad_number']})
        return result
    
    def parse(self, cur, conn, schema):
        result = {}
        details = PE.parse_details_statement(self.root)
        result.update(details)
        if self.root.tag == 'extract_about_property_land':
            record= LandRecord(self.root.tag.find('land_record'))
            record.parse()
            data = record.data
            data.update(details)
            insert_into_table(cur, conn, result, schema)
        if self.root.tag == 'extract_about_zone':
            ztcs = self.root.find('zone_territory_coastline_surveying')
            z_and_t = ztcs.find('zones_and_territories')
            if z_and_t:
                record= Zone(z_and_t)
                record.parse()
                data = record.data
                data.update(details)
                insert_into_table(cur, conn, result, schema)
        if self.root.tag == 'extract_cadastral_plan_territory':
            cad_blocks = self.root.find('cadastral_blocks')
            if cad_blocks:
                for block in cad_blocks.findall('cadastral_block'):
                    quarter = Quarter(block)
                    quarter.parse()
                    result.update(quarter.data)
                    insert_into_table(cur, conn, result, schema)
                    record_data = block.find('record_data')
                    if record_data:
                        base_data = record_data.find('base_data')
                        land_records = base_data.find('land_records')
                        if land_records:
                            for land_record in land_records:
                                record = LandRecord(land_record)
                                record.parse()
                                data = record.data
                                data.update(details)
                                insert_into_table(cur, conn, data, schema)
                    zones = block.find('zones_and_territories_boundaries')
                    if zones:
                        for zone in zones.findall('zones_and_territories_record'):
                            record = Zone(zone, 'extract_cadastral_plan_territory')
                            record.parse()
                            data = record.data
                            data.update(details)
                            insert_into_table(cur, conn, data, schema)