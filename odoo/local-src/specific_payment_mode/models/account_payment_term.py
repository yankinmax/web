# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        readonly=True,
        ondelete='cascade',
        string='Sale order'
    )
