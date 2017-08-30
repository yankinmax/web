# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'utm.mixin']

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist')

    partner_company_type = fields.Selection(
        related='partner_id.company_type',
        readonly=True,
    )

    can_edit_marketing_values = fields.Boolean(
        compute='_compute_can_edit_marketing_values',
        default=lambda self: (
            self.env['crm.lead'].can_edit_marketing_values_value()
        ),
    )

    @api.depends()
    def _compute_can_edit_marketing_values(self):
        can_edit_marketing_values = (
            self.env['crm.lead'].can_edit_marketing_values_value()
        )
        for invoice in self:
            invoice.can_edit_marketing_values = can_edit_marketing_values
