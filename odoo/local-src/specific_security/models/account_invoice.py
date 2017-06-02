# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api
from odoo.exceptions import UserError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group(
            'specific_security.group_invoice_creation'
        ) and not self.env.context.get('refund', False):
            raise UserError('You are not allowed to create an invoice.')

        return super(AccountInvoice, self).create(vals)


class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""

    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        return super(AccountInvoiceRefund,
                     self.with_context(refund=True)).invoice_refund()
