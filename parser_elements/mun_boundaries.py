from .contours import contours

def mun_boundaries(root):
    """
    Извлекает инфо о границах муниципальных образований из КПТ
    """
    cadastral_blocks = root.find('cadastral_blocks')
    cadastral_block = cadastral_blocks.find('cadastral_block')

    if cadastral_block.find('municipal_boundaries') != None:
        result = []
        for boundary in cadastral_block.find('municipal_boundaries').findall('municipal_boundary_record'):
            record = {}
            b_object = boundary.find('b_object_municipal_boundary').find('b_object')
            record['registration_number'] = b_object.find('reg_numb_border').text
            record['registration_date'] = boundary.find('record_info').find('registration_date').text
            record['type_boundary'] = b_object.find('type_boundary').find('value').text
            record.update(contours(boundary.find('b_contours_location').find('contours')))

            record['content'] = 'municipal_boundaries'
            record['geometryType'] = 'MultiPolygon'
            result.append(record)
    else:
        result = None


    return result
