# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp
from openerp.models import MAGIC_COLUMNS


class DiscountProgramCondition(models.Model):
    _name = 'sale.discount.program.condition'

    program_id = fields.Many2one(
        'sale.discount.program', required=True, ondelete='cascade'
    )

    name = fields.Char(compute='_compute_name')

    type_condition = fields.Selection([
        ('product_category', 'Product Category'),
    ], required=True)

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
    )

    product_min_qty = fields.Integer('Product minimal quantity')

    product_min_price_unit = fields.Float(
        'Minimal product unit price',
        digits=dp.get_precision('Product Price'),
    )

    @api.depends('type_condition')
    def _compute_name(self):
        # TODO: call method by type_condition that can be inherited.
        selection_dict = {
            k: v for k, v in self._fields['type_condition'].selection
        }
        for condition in self:
            condition.name = selection_dict[condition.type_condition]

    @api.onchange('type_condition')
    def onchange_type_condition(self):
        """ Reset all configurations columns.
        """
        ignore_field = MAGIC_COLUMNS + ['type_condition']
        for field in self._fields.values():
            if field.name not in ignore_field and not field.compute:
                self[field.name] = False

    @api.multi
    def _check_product_category(self, sale):
        """ This condition type check number of products for the specified
        product category in the sale.
        """
        lines = sale.order_line.filtered(
            lambda l: l.product_id.categ_id == self.product_category_id
        )
        if not lines:
            return False

        if self.product_min_price_unit:
            lines = lines.filtered(
                lambda l: l.price_unit >= self.product_min_price_unit
            )
        if not lines:
            return False

        if self.product_min_qty:
            # TODO: compute with UOM
            if sum(lines.mapped('product_uom_qty')) < self.product_min_qty:
                return False

        return True

    @api.multi
    def check(self, sale):
        self.ensure_one()

        check_method = getattr(self, '_check_%s' % self.type_condition)
        return check_method(sale)
