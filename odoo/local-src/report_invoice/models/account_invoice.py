# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.invoice'

    has_early_payment_discount = fields.Boolean(
        compute='_compute_has_early_payment_discount'
    )

    early_payment_discount = fields.Monetary(
        string='Early Payment Discount', store=True, readonly=True,
        compute='_compute_amount')
    amount_untaxed_discount = fields.Monetary(
        string='Untaxed Amount', store=True, readonly=True,
        compute='_compute_amount')
    amount_tax_discount = fields.Monetary(
        string='Tax', store=True, readonly=True, compute='_compute_amount')
    amount_total_discount = fields.Monetary(
        string='Total', store=True, readonly=True, compute='_compute_amount')

    @api.one
    @api.depends('company_id', 'partner_id')
    def _compute_has_early_payment_discount(self):
        """ Discount is applicable if the client is
        a center with active discount and if the invoice
        is emited by the holding """
        res = False
        if self.company_id == self.env.ref('base.main_company'):
            cp_customer = self.env['res.company'].search(
                [('partner_id', '=', self.partner_id.id)])
            res = cp_customer.early_payment_discount
        self.has_early_payment_discount = res

    @api.one
    @api.depends('has_early_payment_discount')
    def _compute_amount(self):
        super(Invoice, self)._compute_amount()

        IrConfig = self.env['ir.config_parameter']
        discount = IrConfig.get_param('early.payment.discount.rate')
        discount = float(discount) if discount else 0.0
        discount_factor = 1. - discount
        self.early_payment_discount = self.amount_untaxed * -discount
        self.amount_untaxed_discount = self.amount_untaxed * discount_factor
        self.amount_tax_discount = self.amount_tax * discount_factor
        self.amount_total_discount = self.amount_total * discount_factor
