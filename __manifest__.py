# -*- coding: utf-8 -*-
{
    'name': "E-Gov-IOT-Pro",
    'author': "Meditech-Insight",
    'description': '',
    'version': '0.2',
    'depends': ['base', 'auth_oauth'],
    'data': [

        'security/ir.model.access.csv',
        'views/main_menu.xml',
        'views/mdm_board_iot.xml',
        'views/health_promoting_hospital_view.xml',
        'data/cron.xml',
        'views/main_flex_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}
