# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.models import MAGIC_COLUMNS


class DiscountProgramAction(models.Model):
    _name = 'sale.discount.program.action'

    _order = 'program_id, sequence, id'

    program_id = fields.Many2one(
        'sale.discount.program', required=True, ondelete='cascade'
    )

    name = fields.Char(compute='_compute_name')

    type_action = fields.Selection([
        ('voucher', 'Voucher'),
        ('product_add', 'Add Product'),
        ('product_discount', 'Discount on product'),
        ('change_pricelist', 'Change sale order pricelist'),
    ], required=True)

    sequence = fields.Integer(string='Sequence', default=10)

    product_add_id = fields.Many2one('product.product')
    product_add_force_price = fields.Boolean('Specify product price')
    product_add_price = fields.Float(
        string='Product Price',
        digits=dp.get_precision('Product Price')
    )
    allow_negative_total = fields.Boolean(default=True)

    product_discount_selection = fields.Selection([
        ('most_expensive_no_discount', 'Most expensive without discount'),
        ('fixed_product', 'On a specified product'),
    ])

    discount_product_id = fields.Many2one('product.product')

    discount_percent = fields.Float(
        'Discount',
        digits=dp.get_precision('Discount')
    )

    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')

    @api.depends('type_action')
    def _compute_name(self):
        selection_dict = dict(self._fields['type_action'].selection)
        for action in self:
            if action.type_action:
                try:
                    name = getattr(
                        action, '_get_%s_name' % action.type_action
                    )()
                except AttributeError:
                    name = None

                if name is not None:
                    action.name = name
                else:
                    action.name = selection_dict[action.type_action]

    @api.onchange('type_action')
    def onchange_type_action(self):
        """ Reset all configurations columns.
        """
        ignore_field = MAGIC_COLUMNS + ['type_action']
        for field in self._fields.values():
            if field.name not in ignore_field and not field.compute:
                self[field.name] = False

        self._compute_name()

    @api.multi
    def _apply_product_add(self, sale):

        line_vals = {
            'source_program_id': self.program_id.id,
            'product_id': self.product_add_id.id,
            'product_uom_qty': 1,
            'sequence': max((sale.order_line.mapped('sequence') or [0])) + 1,
        }

        if self.product_add_force_price:
            price_unit = self.product_add_price
            if price_unit < 0 and not self.allow_negative_total:
                if sale.amount_total + price_unit < 0:
                    price_unit = -1 * sale.amount_total

            line_vals.update({
                'price_unit': price_unit,
                'price_program': True,
            })

        sale.write({
            'order_line': [(
                (0, False, line_vals)
            )]
        })

    @api.multi
    def _get_product_add_name(self):
        self.ensure_one()
        if self.product_add_id:
            return _("Add product: %s") % self.product_add_id.name

    @api.multi
    def _get_discount_target(self, sale):
        lines = sale.order_line.filtered(
            lambda l: not l.discount_program and l.price_unit
        )
        if self.product_discount_selection == 'most_expensive_no_discount':
            sol = None
            for line in lines:
                if not sol or line.price_unit > sol.price_unit:
                    sol = line

            return sol

        elif self.product_discount_selection == 'fixed_product':
            return lines.filtered(
                lambda l: l.product_id == self.discount_product_id
            )
        else:
            raise NotImplementedError()

    @api.multi
    def _apply_product_discount(self, sale):
        lines = self._get_discount_target(sale)
        if lines:
            for line in lines:
                discount = self.discount_percent
                if line.discount:
                    discount += line.discount

                line.write({
                    'discount': discount,
                    'discount_program': True,
                })

    @api.multi
    def _get_product_discount_name(self):
        self.ensure_one()

        selection_dict = {
            k: v for k, v
            in self._fields['product_discount_selection'].selection
        }

        if self.product_discount_selection and self.discount_percent:
            if self.product_discount_selection == 'fixed_product':
                target = self.discount_product_id.name

            else:
                target = selection_dict[self.product_discount_selection]

            return _("Discount: %s%% on %s") % (
                self.discount_percent,
                target
            )

    @api.multi
    def _apply_change_pricelist(self, sale):
        sale.pricelist_id = self.pricelist_id
        sale.pricelist_program = True
        for line in sale.order_line.filtered(
            lambda l: not l.price_program
        ):
            line.product_uom_change()
            line._onchange_discount()

    @api.multi
    def _get_change_pricelist_name(self):
        self.ensure_one()
        if self.pricelist_id:
            return _("Change pricelist to %s") % self.pricelist_id.name

    @api.multi
    def apply(self, sale):
        self.ensure_one()

        apply_method = getattr(self, '_apply_%s' % self.type_action)
        apply_method(sale)
