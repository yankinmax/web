# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_substance_ids = fields.Many2many(
        'product.substance',
        string='Substances',
    )
    chemistry = fields.Selection(
        related='product_id.chemistry',
        readonly=True,
    )
    tested_sample = fields.Text(
        string='Tested Samples',
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for line in self.product_id.product_substance_line_ids:
            self.product_substance_ids |= line.product_substance_id

    def _fix_substances_values(self, vals):
        """Fix for `product_substance_ids` m2m BSMTS-140.

        We set the field value w/ an onchange in SO line.
        When you create a new line you save the order
        the value is converted to something like:

        u'product_substance_ids': [
            #  _, SUB ID, _
            [1, 1, {u'product_uom_id': 20}],
            [1, 4, {u'product_uom_id': 20}],
            [1, 7, {u'product_uom_id': 20}],
        ]

        or we can have pure ids w/out any command like:

            [1, 4, 7]

        so, here we fix this to proper m2m write values.

        See https://github.com/odoo/odoo/issues/19239
        """
        sub_ids = vals.get('product_substance_ids', [])
        if not sub_ids:
            return
        # if you add value manually instead of onchange
        # you get the correct form: [6, False, [9, 1, 4, 7]]
        fixed = []
        got_pure_ids = all([isinstance(x, int) for x in sub_ids])
        if got_pure_ids:
            # we got a list of ids [9, 4, 7]
            fixed = [(6, 0, sub_ids)]
        else:
            # merge all values here and pass only one command at the end
            all_ids = []
            for x in sub_ids:
                if x[0] == 6:
                    all_ids.extend(x[-1])
                elif x[0] != 6 and len(x) > 1 and not x[1] in all_ids:
                    # include missing ones w/ bad form
                    all_ids.append(x[1])
            fixed = [(6, 0, all_ids)]
        if fixed:
            vals['product_substance_ids'] = fixed

    @api.model
    def create(self, vals):
        self._fix_substances_values(vals)
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        self._fix_substances_values(vals)
        res = super(SaleOrderLine, self).write(vals)
        return res

    def _is_service_task(self):
        return (self.product_id.type == 'service' and
                self.product_id.track_service in ('task', 'completed_task'))
