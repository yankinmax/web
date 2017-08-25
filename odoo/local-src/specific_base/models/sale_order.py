# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def get_default_payment_term_id(self):
    #     return self.env.ref('account.account_payment_term_immediate').id

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        required=True,
        ondelete='restrict',
        string='Phototherapist')
    payment_term_id = fields.Many2one('account.payment.term')
    # default=get_default_payment_term_id)

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
        for order in self:
            order.can_edit_marketing_values = can_edit_marketing_values

    @api.model
    def create(self, values):
        if not values.get('validity_date', False):
            values['validity_date'] = fields.Date.to_string(
                datetime.now() + timedelta(days=90))

        return super(SaleOrder, self).create(values)

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        res = super(SaleOrder, self)._prepare_invoice()
        res['phototherapist_id'] = self.phototherapist_id.id
        return res
