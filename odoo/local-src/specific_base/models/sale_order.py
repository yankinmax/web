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
