# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Dedicated toggle for THIS module's fixed-amount discount button - kept
    # fully independent of the standard module_pos_discount field (that one
    # belongs to Odoo's own core "pos_discount" app, the PERCENTAGE-based
    # Global Discount). Keeping them separate lets a POS enable the amount
    # button, the percentage button, both, or neither, independently.
    iface_discount_amount = fields.Boolean(string='Discount Amount', help='Allow the cashier to give a fixed-amount discount on the whole order.')
    discount_amount = fields.Float(string='Discount Amount', help='The default discount Amount when clicking on the Discount button', default=10.0)
    discount_product_id = fields.Many2one('product.product', string='Discount Product',
        domain="[('sale_ok', '=', True)]", help='The product used to apply the discount on the ticket.')

    @api.model
    def _default_discount_value_on_module_install(self):
        configs = self.env['pos.config'].search([])
        # NOTE (20.0 build): the original 17.0 domain also OR'ed in
        # ('rescue', '=', True) to catch "rescue" sessions. Real-install
        # testing on Odoo 20 found that pos.session.rescue no longer
        # exists on this build, so it was dropped here - state != 'closed'
        # already covers the actual safety requirement below (don't touch
        # a config that has any non-closed session). If your Odoo 20
        # install does have a pos.session.rescue (or differently named
        # equivalent) field, add it back the same way.
        open_configs = (
            self.env['pos.session']
            .search([('state', '!=', 'closed')])
            .mapped('config_id')
        )
        # Do not modify configs where an opened session exists.
        product = self.env.ref("point_of_sale.product_product_consumable", raise_if_not_found=False)
        for conf in (configs - open_configs):
            conf.discount_product_id = product if conf.iface_discount_amount and product and (not product.company_id or product.company_id == conf.company_id) else False

    def open_ui(self):
        for config in self:
            if not self.current_session_id and config.iface_discount_amount and not config.discount_product_id:
                raise UserError(_('A discount product is needed to use the Discount Amount feature. Go to Point of Sale > Configuration > Settings to set it.'))
        return super().open_ui()

    def _get_special_products(self):
        res = super()._get_special_products()
        return res | self.env['pos.config'].search([]).mapped('discount_product_id')

    def _get_available_product_domain(self):
        domain = super()._get_available_product_domain()
        # OR-combine with plain prefix-notation domain syntax instead of
        # odoo.osv.expression.OR(): that helper (and the whole odoo.osv
        # package) no longer exists in this Odoo 20 build - see the
        # module description for details. Prefix notation ('|' followed
        # by two complete, self-contained domains) needs no import and
        # works the same on every Odoo version.
        return ['|'] + domain + [('id', '=', self.discount_product_id.id)]
