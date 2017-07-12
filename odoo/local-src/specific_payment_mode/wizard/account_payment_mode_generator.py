# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentModeGenerator(models.TransientModel):

    _name = 'account.payment.mode.generator'

    to_activate_payment_mode_ids = fields.Many2many(
        'account.payment.mode',
        'account_payment_mode_generator_activate_rel',
        readonly=1)

    to_deactivate_payment_mode_ids = fields.Many2many(
        'account.payment.mode',
        'account_payment_mode_generator_deactivate_rel',
        readonly=1)

    company_modes_to_create_ids = fields.Many2many('res.company', readonly=1)

    account_payment_method_id = fields.Many2one('account.payment.method',
                                                string='Payment method',
                                                readonly=1)

    errors = fields.Text('Errors', readonly=1)

    @api.model
    def default_get(self, fields):
        res = super(AccountPaymentModeGenerator, self).default_get(fields)
        payment_method_id = (res.get('account_payment_method_id')
                             or self.env.context.get('active_id'))
        if payment_method_id:
            payment_method = self.env['account.payment.method'].browse(
                payment_method_id)
            allowed_companies = payment_method.children_company_ids
            payment_modes = payment_method.with_context(
                active_test=False).payment_mode_ids
            modes_to_activate = payment_modes.filtered(
                lambda m: not m.active and m.company_id in allowed_companies)
            modes_to_deactivate = payment_modes.filtered(
                lambda m: m.active and m.company_id not in allowed_companies)
            company_modes_to_create = allowed_companies - payment_modes.mapped(
                'company_id')
            errors = []
            errors += self._check_if_deactivable(modes_to_deactivate)
            errors += self._check_if_creatable(company_modes_to_create)
            if errors:
                res['errors'] = '.\n'.join(errors)
            elif (len(modes_to_activate) == 0
                  and len(modes_to_deactivate) == 0
                  and len(company_modes_to_create) == 0):
                res['errors'] = _('There is nothing to do.')
            else:
                res['to_activate_payment_mode_ids'] = modes_to_activate.ids
                res['to_deactivate_payment_mode_ids'] = modes_to_deactivate.ids
                res['company_modes_to_create_ids'] = \
                    company_modes_to_create.ids
        return res

    def _check_if_deactivable(self, payment_modes):
        errors = []
        modes_used_on_invoices = self.env['account.invoice'].search([
            ('payment_mode_id', 'in', payment_modes.ids),
            ('state', 'not in', ('paid', 'cancel'))
        ]).mapped('payment_mode_id')
        if modes_used_on_invoices:
            for mode in modes_used_on_invoices:
                errors.append(_('Payment mode %s from company %s is '
                                'used on an open invoice.' % (
                                    mode.name, mode.company_id.name)))
        modes_used_on_sales = self.env['sale.order'].search([
            ('payment_mode_id', 'in', payment_modes.ids),
            ('state', '!=', 'draft')
        ]).mapped('payment_mode_id')
        if modes_used_on_sales:
            for mode in modes_used_on_sales:
                errors.append(_('Payment mode %s from company %s is '
                                'used on confirmed sales.' % (
                                    mode.name, mode.company_id.name)))
        return errors

    def _check_if_creatable(self, companies):
        errors = []
        for company in companies:
            aj_obj = self.env['account.journal']
            bank_journal = aj_obj.search(
                [('type', '=', 'bank'), ('company_id', '=', company.id)])
            if not bank_journal:
                errors.append(_(
                    'No bank journal found for company %s '
                    % company.name))
        return errors

    @api.multi
    def generate_payment_modes(self):
        if self.company_modes_to_create_ids:
            self._create_payment_modes(self.company_modes_to_create_ids)
        to_activate = self.with_context(
            active_test=False).to_activate_payment_mode_ids
        if to_activate:
            self._activate_payment_modes(to_activate)
        if self.to_deactivate_payment_mode_ids:
            self._deactivate_payment_modes(self.to_deactivate_payment_mode_ids)

    def _create_payment_modes(self, companies):

        vals = []

        for company in companies:

            aj_obj = self.env['account.journal']
            bank_journal = aj_obj.search(
                [('type', '=', 'bank'), ('company_id', '=', company.id)])
            if not bank_journal:
                raise UserError(_('No bank journal found for company %s '
                                  % company.name))

            sale_journals = aj_obj.search([
                ('type', 'in', ('sale_refund', 'sale')),
                ('company_id', '=', company.id)])
            values = {
                'name': self.account_payment_method_id.name,
                'company_id': company.id,
                'payment_method_id': self.account_payment_method_id.id,
                'bank_account_link': 'variable',
                'variable_journal_ids': [(6, False, bank_journal.ids)],
                'workflow_process_id': self.env.ref(
                    'sale_automatic_workflow.automatic_validation').id,
                'default_journal_ids': [(6, False, sale_journals.ids)]
            }
            vals.append(values)

        for v in vals:
            self.env['account.payment.mode'].create(v)

    def _activate_payment_modes(self, modes):
        modes.write({'active': True})

    def _deactivate_payment_modes(self, modes):
        modes.write({'active': False})
