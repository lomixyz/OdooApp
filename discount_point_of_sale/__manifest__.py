# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Point of Sale Discount Amount',
    'version': '17.0.1.0.4',
    'category': 'Sales/Point of Sale',
    'sequence': -99,
    'author': 'Allam Bushra',
    'website': 'https://www.linkedin.com/in/lomixyz/',
    'summary': 'Give a fixed AMOUNT discount (not a percentage) on the whole order from the POS screen',
    'description': """
Point of Sale Discount Amount
==============================

IMPORTANT: this is an AMOUNT discount, not a percentage discount.
Odoo's Point of Sale already ships with a built-in "Global Discount"
feature, and that one is percentage-based (e.g. 10% off). This module
adds a SEPARATE, complementary "Discount Amount" button so the cashier
can instead subtract a flat number (e.g. 10.00 off, in the store's
currency) with one tap - useful for vouchers, rounding adjustments, or
any manager-approved fixed-value discount that a percentage can't
express. Both features can be enabled at the same time; this module
does not replace or modify Odoo's percentage-based discount.

* One click opens a numeric popup for the discount amount.
* The discount is split proportionally across each tax group present
  on the order, so taxes stay correct.
* Re-applying the button removes the previous discount line first, so
  the cashier can adjust the amount as many times as needed.
* The discount amount can never exceed the order's discountable
  subtotal, so the order total can't go negative by mistake.
* Its own dedicated "Discount Amount" toggle in Settings, completely
  independent from Odoo's standard "Global Discounts" (percentage)
  checkbox - turn on one, the other, or both, and only the matching
  button(s) appear on the POS screen.

Configuration: Point of Sale > Configuration > Settings > turn on
"Discount Amount" to enable this module's fixed-amount button (set a
Discount Product and a default amount), and/or turn on the standard
"Global Discounts" checkbox to enable Odoo's own percentage-based
discount button - independently of each other.
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
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
}
