# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_partner_id = fields.Many2one('res.partner')
    sponsor_id = fields.Many2one('partner.sponsor')

    discount_program_ids = fields.Many2many(
        comodel_name='sale.discount.program'
    )

    @api.multi
    def create_partner_voucher(self, partner_id):
        self.ensure_one()
        months_validity = int(self.env['ir.config_parameter'].get_param(
            'voucher_default_validity', '0'
        ))

        expiration_date = None
        if months_validity:
            expiration_date = date.today() + relativedelta(
                months=months_validity
            )

        self.sudo().write({
            'discount_program_ids': [(0, False, {
                'partner_id': partner_id,
                'combinable': False,
                'voucher_code': self.env['ir.sequence'].next_by_code(
                    'discount.program.voucher_code'
                ),
                'voucher_amount': self.get_voucher_amount(),
                'max_use': 1,
                'expiration_date': expiration_date,
            })]
        })

    @api.multi
    def get_voucher_amount(self):
        """ Compute the amount for the voucher based on invoice amount.
        """
        self.ensure_one()
        icp = self.env['ir.config_parameter']
        percent = float(icp.get_param('voucher_percent', '10'))
        max_amount = int(icp.get_param('voucher_max_amount', '100'))

        amount = min(
            self.amount_total * percent / 100,
            max_amount
        )
        return amount

    @api.multi
    def confirm_paid(self):
        super(AccountInvoice, self).confirm_paid()

        for invoice in self:
            # Bon d'achat si la commande a utilisé le programme de
            # parainnage et si le parrain est toujours valide
            if invoice.sponsor_id.active:
                invoice.create_partner_voucher(
                    invoice.sponsor_id.partner_id.id
                )

            # Bon d'achat en cas de première commande
            sales = invoice.sale_partner_id.sale_order_ids.filtered(
                lambda s: s.state in ('sale', 'done')
            )
            if len(sales) == 1 and sales.invoice_ids == self:
                invoice.create_partner_voucher(invoice.sale_partner_id.id)

    @api.multi
    def refund(self, *args, **kwargs):
        result = super(AccountInvoice, self).refund(*args, **kwargs)

        # Delete unused vouchers
        for program in self.mapped('discount_program_ids'):
            if program.nb_use == 0:
                program.sudo().unlink()

        return result
