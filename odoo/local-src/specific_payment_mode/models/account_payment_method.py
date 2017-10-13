# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


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

    journal_type = fields.Selection(
        selection=[
            ('cash', 'Cash'),
            ('bank', 'Bank'),
        ],
        string='Journal type',
        required=True,
        default='bank',
    )

    @api.multi
    def generate_payment_modes(self):
        self.ensure_one()
        wizard_model = self.env['account.payment.mode.generator']

        values = {
            'account_payment_method_id': self.id,
        }
        values.update(wizard_model.get_default_values(self))
        wizard = wizard_model.create(values)

        action_data = self.env.ref(
            'specific_payment_mode.account_payment_mode_generator_action'
        ).read()[0]
        action_data['res_id'] = wizard.id
        return action_data
