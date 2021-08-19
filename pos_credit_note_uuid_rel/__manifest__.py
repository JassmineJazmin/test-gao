# -*- coding: utf-8 -*-
{
    'name': 'POS - CFDI Relacionado en Devoluciones',
    'summary': "Set the UUID Rel Attribute in Refunds.",
    'description': 'Ref. UUID Origen',

    'author': 'German Ponce Dominguez',
    'website': 'http://poncesoft.blogspot.com',
    "support": "german.poncce@outlook.com",

    'category': 'Point of Sale',
    'version': '13.0.0.1.0',
    'depends': ['point_of_sale', 'l10n_mx_edi', 'pos_customer_uso_cfdi'],

    'data': [
        # 'views/assets.xml',
        'views/pos_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],

    'license': "AGPL-3",

    'installable': True,
    'application': True,

    'images': ['static/description/banner.png'],
}
