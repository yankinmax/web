# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    gift_quotation = fields.Boolean('This quotation is a gift')


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    can_edit_qty = fields.Boolean(
        compute='_compute_can_edit_qty'
    )

    @api.depends('product_id', 'product_id.no_quantity')
    def _compute_can_edit_qty(self):
        """ Quantity is not editable if product has the no_quantity flag.
        """
        for line in self:
            line.can_edit_qty = not line.product_id.no_quantity
