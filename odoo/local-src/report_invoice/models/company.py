# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    early_payment_discount = fields.Boolean(
        "Early payment discount?", default=False,
        help="Enable early payment discount for invoice from the given company"
    )

    early_payment_discount_apply_on_company_id = fields.Many2one(
        comodel_name='res.company',
        string='Apply on',
        help='Apply early payment discount on company',
    )
