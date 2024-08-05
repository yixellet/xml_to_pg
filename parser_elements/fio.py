def fio(element):
    '''
    Извлекает ФИО в одну строку
    '''    
    fio = element.find('surname').text + ' ' + element.find('name').text
    if element.find('patronymic') != None:
        fio += ' ' + element.find('patronymic').text

    return fio
