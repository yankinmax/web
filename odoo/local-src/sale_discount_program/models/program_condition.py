# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.models import MAGIC_COLUMNS


class DiscountProgramCondition(models.Model):
    _name = 'sale.discount.program.condition'

    _order = 'program_id, sequence, id'

    program_id = fields.Many2one(
        'sale.discount.program', required=True, ondelete='cascade'
    )

    name = fields.Char(compute='_compute_name')

    type_condition = fields.Selection([
        ('product_category', 'Product Category'),
        ('product', 'Product'),
    ], required=True)

    sequence = fields.Integer(string='Sequence', default=10)

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )

    product_min_qty = fields.Integer('Product minimal quantity')
    product_max_qty = fields.Integer('Product maximal quantity')
    product_qty_type = fields.Selection([
        ('quantity', 'Quantity is the sum of matching products quantities'),
        ('distinct', 'Quantity is the number of distinct matching products'),
    ])

    product_min_price_unit = fields.Float(
        'Minimal product unit price',
        digits=dp.get_precision('Product Price'),
    )

    @api.depends('type_condition')
    def _compute_name(self):
        selection_dict = dict(self._fields['type_condition'].selection)
        for condition in self:
            if condition.type_condition:
                try:
                    name = getattr(
                        condition, '_get_%s_name' % condition.type_condition
                    )()
                except AttributeError:
                    name = None

                if name is not None:
                    condition.name = name
                else:
                    condition.name = selection_dict[condition.type_condition]

    @api.onchange('type_condition')
    def onchange_type_condition(self):
        """ Reset all configurations columns.
        """
        ignore_field = MAGIC_COLUMNS + ['type_condition']
        for field in self._fields.values():
            if field.name not in ignore_field and not field.compute:
                self[field.name] = False

        self._compute_name()

    @api.multi
    def _check_product_category(self, sale):
        """ This condition type check number of products for the specified
        product category in the sale.
        """
        allowed_categories = self.env['product.category'].search([
            ('id', 'child_of', self.product_category_id.id)
        ])
        return self._order_lines_conditions(sale.order_line.filtered(
            lambda l: l.product_id.categ_id in allowed_categories
        ))

    @api.multi
    def _get_product_category_name(self):
        self.ensure_one()
        if self.product_category_id:
            return _("Product Category: %s") % self.product_category_id.name

    @api.multi
    def _check_product(self, sale):
        """ This condition type check number of specified product.
        """
        return self._order_lines_conditions(sale.order_line.filtered(
            lambda l: l.product_id == self.product_id
        ))

    @api.multi
    def _get_product_name(self):
        self.ensure_one()
        if self.product_id:
            return _("Product: %s") % self.product_id.name

    @api.multi
    def _order_lines_conditions(self, order_lines):
        if not order_lines:
            return False

        if self.product_min_price_unit:
            order_lines = order_lines.filtered(
                lambda l: l.price_unit >= self.product_min_price_unit
            )
        if not order_lines:
            return False

        if self.product_min_qty or self.product_max_qty:
            # TODO: compute with UOM
            if self.product_qty_type == 'distinct':
                qty = len(order_lines.mapped('product_id'))
            else:
                qty = sum(order_lines.mapped('product_uom_qty'))

            if self.product_min_qty and qty < self.product_min_qty:
                return False

            if self.product_max_qty and qty > self.product_max_qty:
                return False

        return True

    @api.multi
    def check(self, sale):
        self.ensure_one()

        check_method = getattr(self, '_check_%s' % self.type_condition)
        return check_method(sale)
