from .cad_work import cadWork
from .address import address
from .record_info import recordInfo
from .common_data import commonData
from .cad_link import cadLink
from .contours import contours, getMskZone, defineGeometryType
from .construction_params import constructionParams

from ..cadaster_import_utils import logMessage

def parseEapc(root):
    '''
    Парсит КВОКС
    '''
    result = {}
    cr = root.find('construction_record')

    result['content'] = 'construction'

    # Даты государственной регистрации
    result.update(recordInfo(cr.find('record_info')))

    object = cr.find('object')
    # Кадастровый номер и вид объекта недвижимости
    result.update(commonData(object))

    # Параметры участка
    result.update(constructionParams(cr))

    # Сведения о кадастровом инженере
    if cr.find('cad_works') != None:
        cad_works = []
        for work in cr.find('cad_works').findall('cad_work'):
            w = cadWork(work)
            cad_works.append(w)
        result['cad_works'] = str(cad_works)
    else:
        result['cad_works'] = None

    # Связь с кадастровыми номерами
    if cr.find('cad_links') != None:
        result['ascendant_cad_numbers'] = str(cadLink(cr.find('cad_links'), 'ascendant_cad_numbers'))
        result['descendant_cad_numbers'] = str(cadLink(cr.find('cad_links'), 'descendant_cad_numbers'))
        result['land_cad_numbers'] = str(cadLink(cr.find('cad_links'), 'land_cad_numbers'))
        result['room_cad_numbers'] = str(cadLink(cr.find('cad_links'), 'room_cad_numbers'))
        result['car_parking_space_cad_numbers'] = str(cadLink(cr.find('cad_links'), 'car_parking_space_cad_numbers'))
        result['facility_cad_number'] = str(cadLink(cr.find('cad_links'), 'facility_cad_number'))
        result['united_cad_number'] = str(cadLink(cr.find('cad_links'), 'united_cad_number'))
        #result['old_numbers'] = str(cadLink(cr.find('cad_links'), 'old_numbers'))
    else:
        result['ascendant_cad_numbers'] = None
        result['descendant_cad_numbers'] = None
        result['land_cad_numbers'] = None
        result['room_cad_numbers'] = None
        result['car_parking_space_cad_numbers'] = None
        result['facility_cad_number'] = None
        #result['old_numbers'] = None
        result['united_cad_number'] = None

    # Сведения об адресном ориентире
    #logMessage(result['cad_number'])
    if cr.find('address_location') != None:
        result.update(address(cr.find('address_location')))
    else:
        result['address_type'] = None
        result['address'] = None
        result['rel_position'] = None

    # Описание местоположения границ ЗУ
    if cr.find('contours') != None:
        xml_contours = cr.find('contours')
        result['geom'] = contours(xml_contours)
        xml_entity_spatial = xml_contours.find('contour').find('entity_spatial')
        result['msk_zone'] = getMskZone(xml_entity_spatial)
        xml_spatial_element = xml_entity_spatial.find('spatials_elements').find('spatial_element')
        result['geometryType'] = defineGeometryType(xml_spatial_element)
    else:
        result['geom'] = None

    return result