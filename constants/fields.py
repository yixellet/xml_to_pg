"""Поля для атрибутивной информации, их типы и комментарии"""

FIELDS = {
    'lands': {
        'name': 'lands',
        'desc': 'Земельные участки',
        'geom_types': ['MultiPolygon'],
        'unique': 'cad_number',
        'fields':{
            'registration_number': {'name': 'registration_number',
            'desc': 'Регистрационный номер выписки',
            'type': 'text'},
            'date_formation': {'name': 'date_formation',
            'desc': 'Дата формирования выписки',
            'type': 'timestamp with time zone'},
            'cancel_date': {'name': 'cancel_date',
            'desc': 'Дата снятия с учета/регистрации',
            'type': 'timestamp with time zone'}, 
            'subtype': {'name': 'subtype',
            'desc': 'Подтип',
            'type': 'text'}, 
            'common_land_cad_number': {'name': 'common_land_cad_number',
            'desc': 'Кадастровый номер единого землепользования',
            'type': 'text'},
            'cad_number': {'name': 'cad_number',
            'desc': 'Кадастровый номер',
            'type': 'text'}, 
            'type': {'name': 'type',
            'desc': 'Тип',
            'type': 'text'}, 
            'area_inaccuracy': {'name': 'area_inaccuracy',
            'desc': 'Погрешность площади',
            'type': 'real'}, 
            'area': {'name': 'area',
            'desc': 'Площадь',
            'type': 'real'}, 
            'area_type': {'name': 'area_type',
            'desc': 'Тип площади',
            'type': 'text'}, 
            'land_use_by_document': {'name': 'land_use_by_document',
            'desc': 'Вид разрешенного использования земельного участка по документу',
            'type': 'text'}, 
            'land_use': {'name': 'land_use',
            'desc': 'Вид разрешенного использования земельного участка в соответствии с ранее использовавшимся классификатором',
            'type': 'text'}, 
            'land_use_mer': {'name': 'land_use_mer',
            'desc': 'Вид разрешенного использования земельного участка в соответствии с классификатором',
            'type': 'text'}, 
            'category': {'name': 'category',
            'desc': 'Категория земель',
            'type': 'text'}
        }
    },
    'quarters': {
        'name': 'quarters',
        'desc': 'Кадастровые кварталы',
        'geom_types': ['MultiPolygon'],
        'unique': 'cad_number',
        'fields':{
            'date_formation': {'name': 'date_formation',
            'desc': 'Дата формирования выписки',
            'type': 'timestamp with time zone'}, 
            'cad_number': {'name': 'cad_number',
            'desc': 'Кадастровый номер',
            'type': 'text'},
            'area': {'name': 'area',
            'desc': 'Площадь',
            'type': 'real'}
        }
    },
    'boundaries': {
        'name': 'boundaries',
        'desc': 'Муниципальные границы',
        'geom_types': ['MultiPolygon'],
        'unique': 'reg_numb_border',
        'fields':{
            'registration_number': {'name': 'registration_number',
            'desc': 'Регистрационный номер выписки',
            'type': 'text'}, 
            'date_formation': {'name': 'date_formation',
            'desc': 'Дата формирования выписки',
            'type': 'timestamp with time zone'},
            'registration_date': {'name': 'registration_date',
            'desc': 'Дата регистрации',
            'type': 'timestamp with time zone'},
            'reg_numb_border': {'name': 'reg_numb_border',
            'desc': 'Регистрационный номер',
            'type': 'text'}, 
            'cancel_date': {'name': 'cancel_date',
            'desc': 'Дата снятия с учета/регистрации',
            'type': 'timestamp with time zone'}, 
            'type_boundary': {'name': 'type_boundary',
            'desc': 'Тип',
            'type': 'text'}
        }
    },
    'zones': {
        'name': 'zones',
        'desc': 'Зоны и территории',
        'geom_types': ['MultiPolygon'],
        'unique': 'reg_numb_border',
        'fields':{
            'registration_number': {'name': 'registration_number',
            'desc': 'Регистрационный номер выписки',
            'type': 'text'}, 
            'date_formation': {'name': 'date_formation',
            'desc': 'Дата формирования выписки',
            'type': 'timestamp with time zone'},
            'registration_date': {'name': 'registration_date',
            'desc': 'Дата регистрации',
            'type': 'timestamp with time zone'},
            'reg_numb_border': {'name': 'reg_numb_border',
            'desc': 'Регистрационный номер',
            'type': 'text'}, 
            'type_boundary': {'name': 'type_boundary',
            'desc': 'Тип',
            'type': 'text'},
            'type_zone': {'name': 'type_zone',
            'desc': 'Тип',
            'type': 'text'},
            'cancel_date': {'name': 'cancel_date',
            'desc': 'Дата снятия с учета/регистрации',
            'type': 'timestamp with time zone'}, 
            'name_by_doc': {'name': 'name_by_doc',
            'desc': 'Наименование по документу',
            'type': 'text'}, 
            'name_by_pkk': {'name': 'name_by_pkk',
            'desc': 'Наименование по ПКК',
            'type': 'text'}
        }
    },
    'coastlines': {
        'name': 'coastlines',
        'desc': 'Береговые линии',
        'geom_types': ['MultiLineString'],
        'unique': 'reg_numb_border',
        'fields':{
            'registration_number': {'name': 'registration_number',
            'desc': 'Регистрационный номер выписки',
            'type': 'text'}, 
            'date_formation': {'name': 'date_formation',
            'desc': 'Дата формирования выписки',
            'type': 'timestamp with time zone'},
            'registration_date': {'name': 'registration_date',
            'desc': 'Дата регистрации',
            'type': 'timestamp with time zone'},
            'reg_numb_border': {'name': 'reg_numb_border',
            'desc': 'Регистрационный номер',
            'type': 'text'}, 
            'cancel_date': {'name': 'cancel_date',
            'desc': 'Дата снятия с учета/регистрации',
            'type': 'timestamp with time zone'}, 
            'water': {'name': 'water',
            'desc': 'Наименование водного объекта',
            'type': 'text'}
        }
    }
}
