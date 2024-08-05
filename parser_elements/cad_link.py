import re

def cadLink(element, type):
    '''
    Кадастровые номера связанных объектов
    '''

    if element.find(type) != None:
        io = element.find(type)
        array = []
        if type in ('facility_cad_number', 'united_cad_number'):
            array = io.find('cad_number').text
        else:
            for e in io.findall(type[:-1]):
                cn = e.find('cad_number').text
                cns = re.split(r'[,;]\s*', cn)
                array = array + cns
    else:
        array = None

    return array
