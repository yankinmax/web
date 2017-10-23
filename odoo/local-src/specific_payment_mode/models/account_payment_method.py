# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from odoo import models, fields, api, _


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

        if self.env.user.company_id != self.env.ref('base.main_company'):
            raise UserError(
                _('You must be connected '
                  'on "Depil Tech Holding" company to generate payment modes.')
            )

        wizard_model = self.env['account.payment.mode.generator']

        values = {
            'account_payment_method_id': self.id,
        }
        values.update(wizard_model.get_default_values(self))
        # We must be a sudo here, because except admin user,
        # some objects (journals) are readable only for the connected company
        wizard = wizard_model.sudo().create(values)

        action_data = self.env.ref(
            'specific_payment_mode.account_payment_mode_generator_action'
        ).read()[0]
        action_data['res_id'] = wizard.id
        return action_data
