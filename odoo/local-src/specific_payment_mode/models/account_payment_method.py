# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPaymentMethod(models.Model):

    _inherit = 'account.payment.method'

    company_ids = fields.Many2many('res.company',
                                   'account_payment_method_res_company_rel',
                                   string='Allowed companies')

    depiltech_payment_mode = fields.Many2one(
        comodel_name='depiltech.payment.mode',
        string='Depiltech payment mode',
        domain=[('deny_to_confirm_order', '=', False)]
    )
