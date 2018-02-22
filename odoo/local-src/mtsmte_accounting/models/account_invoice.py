# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    comment = fields.Text(
        default=False,
    )

    @api.multi
    def invoice_validate(self):
        # Override the default method that prevent to have 2 invoices
        # with the same reference, it should be allowed with BVR/ESR
        # as a supplier can use the same number for several invoices.
        # This is done as a specific customization as there is no clean
        # way to disable the check respecting the `super` chain.
        # In next version, hopefully it can be integrated in l10n_ch_base_bank
        # with https://github.com/odoo/odoo/pull/15891
        return self.write({'state': 'open'})


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount
        )
        invoice.comment = ""
        return invoice
