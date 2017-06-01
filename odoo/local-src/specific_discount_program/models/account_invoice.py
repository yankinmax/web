# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    gift_quotation = fields.Boolean('This quotation is a gift', readonly=True)

    generated_voucher_ids = fields.One2many(
        comodel_name='sale.discount.program',
        inverse_name='source_invoice_id'
    )

    @api.multi
    def create_voucher(self):
        self.ensure_one()
        try:
            months_validity = int(self.env['ir.config_parameter'].get_param(
                'voucher_default_validity', '0'))
        except ValueError:
            raise UserError(
                "Configuration parameter 'voucher_default_validity' "
                "is invalid.\n This parameter value has to be an Integer.")

        expiration_date = None
        if months_validity:
            expiration_date = date.today() + relativedelta(
                months=months_validity
            )
        self.sudo().write({
            'generated_voucher_ids': [(0, False, {
                'combinable': True,
                'voucher_code': self.env['ir.sequence'].next_by_code(
                    'discount.program.voucher_code'
                ),
                'gift_voucher': True,
                'voucher_amount': (self.invoice_line_ids[0].quantity *
                                   self.invoice_line_ids[0].price_unit),
                'max_use': 1,
                'expiration_date': expiration_date,
                'note_message_for_action':
                    _("You received a gift voucher !")
            })]
        })

    @api.one
    def gift_quotation_invoice_validation(self):
        if self.gift_quotation:
            if not (
                len(self.invoice_line_ids) == 1 and
                self.invoice_line_ids[0].product_id == self.env.ref(
                                'specific_discount_program.gift_card')
            ):
                return False
            else:
                return True
        else:
            raise UserWarning(
                "Only 1 (one) Gift card product "
                "is allowed for gift quotations.")

    @api.multi
    def action_invoice_open(self):
        gift_quotation_invoices = self.filtered(lambda i: i.gift_quotation)
        other_invoices = self - gift_quotation_invoices
        super(AccountInvoice, other_invoices).action_invoice_open()
        for invoice in gift_quotation_invoices:
            if invoice.gift_quotation_invoice_validation():
                # We don't raise validation error if gift quotation invoice
                # was modified but leave it as draft instead, so we don't
                # block confirmation of correct invoices
                super(AccountInvoice, invoice).action_invoice_open()

    @api.multi
    def action_invoice_paid(self):
        super(AccountInvoice, self).action_invoice_paid()
        for invoice in self:
            if invoice.gift_quotation:
                invoice.create_voucher()


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
