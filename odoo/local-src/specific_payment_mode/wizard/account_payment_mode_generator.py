# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentModeGenerator(models.TransientModel):

    _name = 'account.payment.mode.generator'

    account_payment_mode_ids = fields.Many2many(
        'account.payment.mode', string='Existing payment modes')

    account_payment_method_id = fields.Many2one('account.payment.method',
                                                string='Payment method')

    @api.model
    def default_get(self, fields):
        res = super(AccountPaymentModeGenerator, self).default_get(fields)
        payment_method_id = (res.get('account_payment_method_id')
                             or self.env.context.get('active_id'))
        if payment_method_id:
            res['account_payment_mode_ids'] = self.with_context(
                active_test=False).env['account.payment.mode'].search([
                    ('payment_method_id', '=', payment_method_id)]).ids
        return res

    @api.multi
    def generate_payment_modes(self):
        payment_method_id = self.env.context.get('active_id')
        if not payment_method_id:
            raise UserError(_('No active payment method found.'))

        account_payment_method = self.env[
            'account.payment.method'].browse(payment_method_id)
        companies = account_payment_method.children_company_ids
        self.account_payment_mode_ids = self.with_context(
            active_test=False).env['account.payment.mode'].search(
                [('payment_method_id', '=', payment_method_id)])

        vals = []
        errors = []
        for company in companies:
            # Check if exists
            company_payment_mode = self.account_payment_mode_ids.filtered(
                lambda m: m.company_id == company)
            # If payment mode exists and is active, do nothing
            if company_payment_mode and company_payment_mode.active:
                continue
            else:
                aj_obj = self.env['account.journal']
                bank_journal = aj_obj.search(
                    [('type', '=', 'bank'), ('company_id', '=', company.id)])
                if bank_journal:
                    sale_journals = aj_obj.search([
                        ('type', 'in', ('sale_refund', 'sale')),
                        ('company_id', '=', company.id)])
                    values = {
                        'name': account_payment_method.name,
                        'company_id': company.id,
                        'payment_method_id': account_payment_method.id,
                        'bank_account_link': 'variable',
                        'variable_journal_ids': [(6, False, bank_journal.ids)],
                        'workflow_process_id': self.env.ref(
                            'sale_automatic_workflow.automatic_validation').id,
                        'default_journal_ids': [(6, False, sale_journals.ids)]
                    }
                    if company_payment_mode:
                        values['active'] = True
                        company_payment_mode.write(values)
                    else:
                        vals.append(values)
                else:
                    errors.append(_(
                        'No bank journal found for company %s '
                        % company.name))

        # Inactive obsolete payment modes
        obsolete_modes = self.account_payment_mode_ids.filtered(
            lambda m: m.company_id not in companies and m.active)
        used_modes = self.env['account.invoice'].search([
            ('payment_mode_id', 'in', obsolete_modes.ids),
            ('state', 'not in', ('paid', 'cancel'))
        ]).mapped('payment_mode_id')
        if used_modes:
            for mode in used_modes:
                errors.append(_('Payment mode %s from company %s is '
                                'used on an open invoice.' % (
                                    mode.name, mode.company_id.name)))

        if errors:
            raise UserError('.\n'.join(errors))

        for v in vals:
            self.env['account.payment.mode'].create(v)

        obsolete_modes.write({'active': False})
