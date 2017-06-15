# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class DepiltechPaymentMode(models.Model):
    _name = 'depiltech.payment.mode'
    _order = 'name'

    name = fields.Char(
        required=True,
        translate=True,
    )

    calculator_link = fields.Char(
        translate=True,
    )

    use_as_default = fields.Boolean()

    deny_to_confirm_order = fields.Boolean()

    compute_calculator = fields.Boolean()

    days_before_payment = fields.Integer()
