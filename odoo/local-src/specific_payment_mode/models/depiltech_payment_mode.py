# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class DepiltechPaymentMode(models.Model):
    _name = 'depiltech.payment.mode'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )

    calculator_link = fields.Char(
        string='Calculator link',
        translate=True,
    )

    use_as_default = fields.Boolean(
        string='Use as default',
    )

    deny_to_confirm_order = fields.Boolean(
        string='Deny to confirm order',
    )

    compute_calculator = fields.Boolean(
        string='Compute calculator',
    )

    days_before_payment = fields.Integer(
        string='Days before payment',
    )
