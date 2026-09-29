# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Point of Sale Discount Amount',
    'version': '20.0.1.0.5',
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

NOTE ON A FIXED CONFLICT (this 20.0 build): an earlier version of
views/res_config_settings_views.xml used position="replace" on the
built-in div#warning_text_pos_discount (which belongs to Odoo's own
core "pos_discount" module) to inject its fields. That caused a
ParseError ("Element <div id="warning_text_pos_discount"> cannot be
located in parent view") whenever the standard percentage-based Global
Discount was also enabled, because pos_discount's own view re-applies
against that same div on every (re)install and found it already
removed. Fixed by no longer touching that div - see the NOTE in
views/res_config_settings_views.xml for the full explanation.

NOTE ON THIS 20.0 BUILD: Odoo 20 had not reached general availability
at the time this build was prepared. Real-install testing found two backend issues, both fixed in this
build: (1) Odoo 20 removed the odoo.osv package entirely
(odoo.osv.expression, used here to OR-combine two product domains, no
longer exists - the ORM internals now live under odoo.orm). Fixed by
dropping the import and OR-combining the two domains with plain prefix
notation (['|'] + domain_a + domain_b) instead, which needs no helper
import and works unchanged on every Odoo version - see
models/pos_config.py. (2) pos.session no longer has a 'rescue' field on
this build, which made _default_discount_value_on_module_install's
search domain raise "Invalid field pos.session.rescue" on install.
Fixed by dropping that OR clause and keeping only the state != 'closed'
check, which covers the actual safety requirement (don't touch a
config with any non-closed session) - see the NOTE in that method if
your install does have an equivalent field and you want it back. The
rest of the backend (the pos.config / res.config.settings fields and
their settings-screen view) uses only long-stable Odoo APIs and needed
no further changes. The Point of Sale FRONTEND, however, is the part of
Odoo that changed the most starting around 18.0 - the Owl components,
the control-button registration API (ProductScreen.addControlButton)
and the in-browser order/orderline model were all reworked in that
period, and no real Odoo 20 point_of_sale module source was available
to verify against while preparing this build (unlike the security
model for the companion hr_face_mood_attendance 20.0 build, which was
cross-checked against Odoo's own official "account" module). The
JavaScript in static/src/ here is therefore a best-effort port that
still uses the 17.0-era API shape and MUST be tested against a real
Odoo 20 point_of_sale install before going anywhere near production -
if the Discount Amount button does not appear, or the popup/lines do
not behave as expected, the control-button registration API and the
order/orderline method names (get_orderlines_grouped_by_tax_ids,
calculate_base_amount, isGlobalDiscountApplicable) are the first
things to re-check against the installed point_of_sale addon's actual
source.

This 20.0 build's technical module name is the same as the 17.0 build
(discount_point_of_sale) - matching how Odoo's own official modules
never encode the Odoo series in the technical name, only in the
manifest 'version' field. Keep the 17.0 and 20.0 builds in separate
addons paths / git branches, never installed side by side under the
same name on one database.
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
