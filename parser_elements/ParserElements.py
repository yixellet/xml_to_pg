from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Union
from json import dumps

class ParserElements():
    """
    Инструменты парсинга элементов, общих для всех типов XML
    """
    def __init__(self) -> None:
        pass

    def parse_dict(root: Element,
                   export_element: str = 'value') -> str:
        """
        Извлекает данные, представленные в форме словаря

        :param export_value: Что необходимо извлечь из словаря 
        (code или value), по умолчанию value
        :type export_value: str, optional
        :return: Возвращает строку - код или значение
        :rtype: str
        """
        data = root.find(export_element)
        if data != None:
            return data.text
        else:
            return ''

    @classmethod
    def parse_common_data(self, root: Element) -> dict[str, str]:
        """Извлекает кадастровый номер и тип объекта"""
        result = {}
        cd = root.find('common_data')
        result['cad_number'] = cd.find('cad_number').text
        quarter_cad_number = cd.find('quarter_cad_number')
        if quarter_cad_number:
            result['quarter_cad_number'] = quarter_cad_number.text
        result['type'] = self.parse_dict(cd.find('type'))

        return result
    
    def parse_record_info(element: Element) -> dict[str, Union[datetime, None]]:
        """Извлекает даты государственной регистрации 
        (постановки/снятия с учета (регистрации))

        :param element: Корневой элемент
        :type element: Element
        :return: _description_
        :rtype: dict[str, datetime]
        """
        result = {}
        result['registration_date'] = \
            datetime.fromisoformat(element.find('registration_date').text)
        cancel_date = element.find('cancel_date')
        if cancel_date != None:
            result['cancel_date'] = datetime.fromisoformat(cancel_date.text)
        
        dates_changes = element.find('dates_changes')
        if dates_changes:
            for date_change in dates_changes.findall('date_change'):
                result['date_change'] = datetime.fromtimestamp(date_change.text)

        return result

    def getAddressPart(element, type):
        e = element.find(type)
        if e.find('type_{}'.format(type)):
            typeStr = e.find('type_{}'.format(type)).text
        else:
            typeStr = ''
        if e.find('name_{}'.format(type)):
            nameStr = e.find('name_{}'.format(type)).text
        else:
            nameStr = ''
        return typeStr + ' ' + nameStr

    @classmethod
    def parse_address(self, element):
        '''
        Извлекает адрес
        '''    
        
        obj = {}

        # Тип адреса
        if element.find('address_type') != None:
            obj['address_type'] = self.parse_dict(element.find('address_type'))
        
        # Адрес (местоположение)
        addr = element.find('address')
        ad = {}
        if addr.find('note') != None:
            ad['note'] = addr.find('note').text
        if addr.find('readable_address') != None:
            ad['readable_address'] = addr.find('readable_address').text
        
        if addr.find('address_fias') != None:
            af = addr.find('address_fias')
            afobj = {}
            ls = af.find('level_settlement')
            if ls.find('fias') != None:
                afobj['objectid'] = ls.find('fias').text
            if ls.find('okato') != None:
                afobj['okato'] = ls.find('okato').text
            if ls.find('kladr') != None:
                afobj['kladr'] = ls.find('kladr').text
            if ls.find('oktmo') != None:
                afobj['oktmo'] = ls.find('oktmo').text
            if ls.find('postal_code') != None:
                afobj['postal_code'] = ls.find('postal_code').text
            if ls.find('region') != None:
                afobj['region'] = ls.find('region').text
            if ls.find('district') != None:
                afobj['district'] = self.getAddressPart(ls, 'district')
            if ls.find('city') != None:
                afobj['city'] = self.getAddressPart(ls, 'city')
            if ls.find('urban_district') != None:
                afobj['urban_district'] = self.getAddressPart(ls, 'urban_district')
            if ls.find('soviet_village') != None:
                afobj['soviet_village'] = self.getAddressPart(ls, 'soviet_village')
            if ls.find('locality') != None:
                afobj['locality'] = self.getAddressPart(ls, 'locality')
            
            if af.find('detailed_level') != None:
                dl = af.find('detailed_level')
                if dl.find('street') != None:
                    afobj['street'] = self.getAddressPart(dl, 'street')
                if dl.find('Level1') != None:
                    afobj['Level1'] = self.getAddressPart(dl, 'Level1')
                if dl.find('Level2') != None:
                    afobj['Level2'] = self.getAddressPart(dl, 'Level2')
                if dl.find('Level3') != None:
                    afobj['Level3'] = self.getAddressPart(dl, 'Level3')
                if dl.find('apartment') != None:
                    afobj['apartment'] = self.getAddressPart(dl, 'apartment')
                if dl.find('other') != None:
                    afobj['other'] = dl.find('other').text

            ad['address_fias'] = afobj

        obj['address'] = dumps(ad)

        # Местоположение относительно ориентира
        if element.find('rel_position') != None:
            rp = element.find('rel_position')
            objj = {}
            if rp.find('in_boundaries_mark') != None:
                objj['in_boundaries_mark'] = rp.find('in_boundaries_mark').text
            if rp.find('ref_point_name') != None:
                objj['ref_point_name'] = rp.find('ref_point_name').text
            if rp.find('location_description') != None:
                objj['location_description'] = rp.find('location_description').text
            obj['rel_position'] = dumps(objj)

        return obj

    def parse_details_statement(element):
        '''
        Извлекает сведения о выписке / КПТ
        '''
        result = {}
        ds = element.find('details_statement')

        # "Высшие реквизиты" - номер и дата выписки
        gtr = ds.find('group_top_requisites')
        if gtr.find('registration_number') != None:
            result['registration_number'] = gtr.find('registration_number').text
        result['date_formation'] = gtr.find('date_formation').text

        # "Низшие реквизиты" - должность и имя регистратора
        if ds.find('group_lower_requisites') != None:
            result['position'] = ds.find('group_lower_requisites').find('full_name_position').text
            result['name'] = ds.find('group_lower_requisites').find('initials_surname').text
        
        return result
