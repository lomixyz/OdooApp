# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # pos.config fields
    # Dedicated toggle for this module's fixed-amount discount, independent
    # of Odoo's own pos_module_pos_discount (the standard percentage-based
    # Global Discount checkbox) - see views/res_config_settings_views.xml
    # for why they must stay decoupled.
    pos_iface_discount_amount = fields.Boolean(related='pos_config_id.iface_discount_amount', readonly=False)
    pos_discount_amount = fields.Float(related='pos_config_id.discount_amount', readonly=False)
    pos_discount_product_id = fields.Many2one('product.product', compute='_compute_pos_discount_product_id', store=True, readonly=False)

    @api.depends('company_id', 'pos_iface_discount_amount', 'pos_config_id')
    def _compute_pos_discount_product_id(self):
        default_product = self.env.ref("point_of_sale.product_product_consumable", raise_if_not_found=False) or self.env['product.product']
        for res_config in self:
            discount_product = res_config.pos_config_id.discount_product_id or default_product
            if res_config.pos_iface_discount_amount and (not discount_product.company_id or discount_product.company_id == res_config.company_id):
                res_config.pos_discount_product_id = discount_product
            else:
                res_config.pos_discount_product_id = False
