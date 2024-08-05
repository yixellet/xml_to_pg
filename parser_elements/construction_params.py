from .dict import dict

def constructionParams(el):
    '''
    Извлекает Характеристики ОКС
    '''

    land = {}
    element = el.find('params')

    # Назначение
    land['purpose'] = element.find('purpose').text

    # Количество этажей    
    if element.find('floors') != None:
        land['floors'] = element.find('floors').text
    else:
        land['floors'] = None

    # Количество подземных этажей    
    if element.find('underground_floors') != None:
        land['underground_floors'] = element.find('underground_floors').text
    else:
        land['underground_floors'] = None

    # Название    
    if element.find('name') != None:
        land['name'] = element.find('name').text
    else:
        land['name'] = None

    # Год завершения строительства    
    if element.find('year_built') != None:
        land['year_built'] = element.find('year_built').text
    else:
        land['year_built'] = None

    # Год ввода в эксплуатацию по завершении строительства
    if element.find('year_commisioning') != None:
        land['year_commisioning'] = element.find('year_commisioning').text
    else:
        land['year_commisioning'] = None

    # Основная характеристика
    land['area'] = None
    land['built_up_area'] = None
    land['extension'] = None
    land['depth'] = None
    land['occurence_depth'] = None
    land['volume'] = None
    land['height'] = None
    if element.find('base_parameters') != None:
        for param in element.find('base_parameters').findall('base_parameter'):
            for child in param:
                land[child.tag] = child.text
    
    return land
