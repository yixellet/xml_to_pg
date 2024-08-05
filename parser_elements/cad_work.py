from .fio import fio

def cadWork(element):
    '''
    Извлекает сведения о кадастровых работах
    '''
    
    work = {}
    if element.find('work_type') != None:
        work['work_type'] = element.find('work_type').text
    else:
        work['work_type'] = None
    if element.find('cadastral_engineer_agreement') != None:
        work['cadastral_engineer_agreement'] = element.find('cadastral_engineer_agreement').text
    else:
        work['cadastral_engineer_agreement'] = None
    if element.find('cadastral_engineer_registry_number') != None:
        work['cadastral_engineer_registry_number'] = element.find('cadastral_engineer_registry_number').text
    else:
        work['cadastral_engineer_registry_number'] = None
    if element.find('cadastral_engineer_date') != None:
        work['cadastral_engineer_date'] = element.find('cadastral_engineer_date').text
    else:
        work['cadastral_engineer_date'] = None
    
    work['fio_cad_engineer'] = fio(element.find('fio_cad_ingineer'))
    
    return work
