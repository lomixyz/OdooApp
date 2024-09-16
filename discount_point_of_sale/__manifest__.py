# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Point of Sale Discount Amount',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'sequence': -99,
    'author': 'Allam Bushra',
    'website': "https://lomisoft.odoo.com",
    'summary': 'Simple Discounts in the Point of Sale ',
    'description': """

This module allows the cashier to quickly give percentage-based
discount to a customer.

""",
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/pos_config_views.xml',
        ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'discount_point_of_sale/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
