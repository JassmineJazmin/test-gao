# -*- coding: utf-8 -*-
{
    'name': 'POS Customer Extend',
    'summary': "Set Default Customer in POS and CFDI Use.",
    'description': 'Set Default Customer in POS',

    'author': 'German Ponce Dominguez',
    'website': 'http://poncesoft.blogspot.com',
    "support": "german.poncce@outlook.com",

    'category': 'Point of Sale',
    'version': '13.0.0.1.0',
    'depends': ['point_of_sale','l10n_mx_edi'],

    'data': [
        'views/assets.xml',
        'views/pos_config_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],

    'license': "OPL-1",

    'installable': True,
    'application': True,

    'images': ['static/description/banner.png'],
}
