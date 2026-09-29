/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { parseFloat } from "@web/views/fields/parsers";

export class DiscountPoSFixed extends Component {
    static template = "discount_point_of_sale.DiscountPoSFixed";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    async click() {
        var self = this;
        const { confirmed, payload } = await this.popup.add(NumberPopup, {
            title: _t("Discount Amount"),
            startingValue: this.pos.config.pos_discount_amount,
            isInputSelected: true,
        });
        if (confirmed) {
            const val = Math.max(0, parseFloat(payload) || 0);
            await self.apply_discount(val);
        }
    }

    async apply_discount(amount) {
        const order = this.pos.get_order();
        const lines = order.get_orderlines();
        const product = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
        if (product === undefined) {
            await this.popup.add(ErrorPopup, {
                title: _t("No discount product found"),
                body: _t(
                    "The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."
                ),
            });
            return;
        }

        // Remove existing discounts
        lines
            .filter((line) => line.get_product() === product)
            .forEach((line) => order._unlinkOrderline(line));

        if (amount <= 0) {
            return;
        }

        // Group the order lines by tax group and compute each group's
        // discountable base first, so we can split the requested amount
        // proportionally across tax groups (instead of applying the full
        // amount once per group, which would over-discount any order that
        // spans more than one tax group).
        const linesByTax = order.get_orderlines_grouped_by_tax_ids();
        const groups = [];
        for (const [tax_ids, taxLines] of Object.entries(linesByTax)) {
            // Note that tax_ids_array is an Array of tax_ids that apply to these lines
            // That is, the use case of products with more than one tax is supported.
            const tax_ids_array = tax_ids
                .split(",")
                .filter((id) => id !== "")
                .map((id) => Number(id));

            const baseToDiscount = order.calculate_base_amount(
                tax_ids_array,
                taxLines.filter((ll) => ll.isGlobalDiscountApplicable())
            );

            if (baseToDiscount > 0) {
                groups.push({ baseToDiscount });
            }
        }

        const totalBase = groups.reduce((sum, group) => sum + group.baseToDiscount, 0);
        if (totalBase <= 0) {
            return;
        }

        // Never let the discount exceed the order's total discountable
        // subtotal, so the order total can't go negative by mistake.
        const cappedAmount = Math.min(amount, totalBase);

        for (const group of groups) {
            // We add the price as manually set to avoid recomputation when changing customer.
            const share = cappedAmount * (group.baseToDiscount / totalBase);
            const discount = -share;
            if (discount < 0) {
                order.add_product(product, {
                    price: discount,
                    lst_price: discount,
                    merge: false,
                });
            }
        }
    }
}

ProductScreen.addControlButton({
    component: DiscountPoSFixed,
    condition: function () {
        // iface_discount_amount is this module's own dedicated toggle -
        // deliberately independent of module_pos_discount (Odoo's
        // standard PERCENTAGE-based Global Discount checkbox), so the two
        // discount buttons can be shown/hidden independently of each
        // other: enable one, the other, or both.
        const { iface_discount_amount, discount_product_id } = this.pos.config;
        return iface_discount_amount && discount_product_id;
    },
});
