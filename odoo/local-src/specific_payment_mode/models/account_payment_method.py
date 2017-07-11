# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountPaymentMethod(models.Model):

    _inherit = 'account.payment.method'

    company_ids = fields.Many2many('res.company',
                                   'account_payment_method_res_company_rel',
                                   string='Allowed companies')

    children_company_ids = fields.Many2many(
        'res.company', 'account_payment_method_res_company_children_rel',
        compute='_compute_children_company_ids', store=True
    )

    @api.depends('company_ids', 'company_ids.child_ids')
    def _compute_children_company_ids(self):
        for method in self:
            companies = self.env['res.company'].search(
                [('id', 'child_of', method.company_ids.ids)])
            method.children_company_ids = companies.ids
