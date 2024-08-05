from .contours import contours

def coastlines(root):
    """
    Извлекает инфо о границах зон из КПТ
    """
    cadastral_blocks = root.find('cadastral_blocks')
    cadastral_block = cadastral_blocks.find('cadastral_block')

    if cadastral_block.find('coastline_boundaries') != None:
        result = []
        for boundary in cadastral_block.find('coastline_boundaries').findall('coastline_record'):
            record = {}
            if boundary.find('b_object_coastline') != None:
                b_object_coastline = boundary.find('b_object_coastline')
            else:
                b_object_coastline = boundary.find('b_object_zones_and_territories')
            b_object = b_object_coastline.find('b_object')
            record['registration_number'] = b_object.find('reg_numb_border').text
            record['registration_date'] = boundary.find('record_info').find('registration_date').text
            record['water'] = b_object_coastline.find('water').find('water_object_name').text
            record.update(contours(boundary.find('b_contours_location').find('contours')))

            record['content'] = 'coastlines'
            record['geometryType'] = 'MultiLineString'
            result.append(record)
    else:
        result = None


    return result
