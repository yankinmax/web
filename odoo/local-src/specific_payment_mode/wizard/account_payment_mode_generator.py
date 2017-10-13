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
        string='Payment modes to activate',
        domain=[('active', '=', False)],
        readonly=1)

    to_deactivate_payment_mode_ids = fields.Many2many(
        'account.payment.mode',
        'account_payment_mode_generator_deactivate_rel',
        string='Payment modes to deactivate',
        readonly=1)

    company_modes_to_create_ids = fields.Many2many(
        'res.company', string='Payment modes to create', readonly=1)

    account_payment_method_id = fields.Many2one('account.payment.method',
                                                string='Payment method',
                                                readonly=1)

    journal_type = fields.Selection(
        related='account_payment_method_id.journal_type',
        readonly=True,
    )

    journal_to_update_add_ids = fields.Many2many(
        comodel_name='account.journal',
        relation='account_payment_mode_generator_journal_to_add_rel',
        string='Journals on which payment method must be added',
        readonly=True,
    )

    journal_to_update_delete_ids = fields.Many2many(
        comodel_name='account.journal',
        relation='account_payment_mode_generator_journal_to_delete_rel',
        string='Journals on which payment method must be deleted',
        readonly=True,
    )

    errors = fields.Text('Errors', readonly=1)

    company_on_errors_ids = fields.Many2many(
        'res.company', string='Companies on error', readonly=1)

    @api.model
    def get_default_values(self, payment_method):
        values = {}

        allowed_companies = payment_method.company_ids.mapped(
            'children_company_ids')
        payment_modes = payment_method.sudo().with_context(
            active_test=False).payment_mode_ids
        modes_to_activate = payment_modes.filtered(
            lambda m: not m.active and m.company_id in allowed_companies)
        modes_to_deactivate = payment_modes.filtered(
            lambda m: m.active and m.company_id not in allowed_companies)
        company_modes_to_create = allowed_companies - payment_modes.mapped(
            'company_id')
        errors = []
        companies_on_error = []
        new_errors, new_companies_on_error = (
            self._check_if_deactivable(modes_to_deactivate)
        )
        errors += new_errors
        companies_on_error += new_companies_on_error
        new_errors, new_companies_on_error = self._check_if_creatable(
            company_modes_to_create,
            payment_method.journal_type
        )
        errors += new_errors
        companies_on_error += new_companies_on_error

        journal_to_update_add, journal_to_update_delete = (
            self._get_journal_to_update(payment_method, allowed_companies)
        )

        if errors:
            values['errors'] = '.\n'.join(errors)
            if companies_on_error:
                values['company_on_errors_ids'] = [
                    (6, 0, companies_on_error),
                ]
            company_modes_to_create = company_modes_to_create.filtered(
                lambda c: c.id not in companies_on_error
            )
        elif (len(modes_to_activate) == 0
              and len(modes_to_deactivate) == 0
              and len(company_modes_to_create) == 0
              and len(journal_to_update_add) == 0
              and len(journal_to_update_delete) == 0):
            values['errors'] = _('There is nothing to do.')

        if modes_to_activate:
            values['to_activate_payment_mode_ids'] = [
                (6, 0, modes_to_activate.ids),
            ]
        if modes_to_deactivate:
            values['to_deactivate_payment_mode_ids'] = [
                (6, 0, modes_to_deactivate.ids),
            ]
        if company_modes_to_create:
            values['company_modes_to_create_ids'] = [
                (6, 0, company_modes_to_create.ids),
            ]
        if journal_to_update_add:
            values['journal_to_update_add_ids'] = [
                (6, 0, journal_to_update_add.ids),
            ]
        if journal_to_update_delete:
            values['journal_to_update_delete_ids'] = [
                (6, 0, journal_to_update_delete.ids),
            ]

        return values

    def _get_journal_to_update(self, payment_method, allowed_companies):

        journal_to_update_add = self.env['account.journal']
        for company in allowed_companies:
            journal = self._get_variable_journal(
                company, payment_method.journal_type
            )

            if payment_method not in journal.inbound_payment_method_ids:
                journal_to_update_add |= journal

        journal_to_update_delete = self.env['account.journal'].search([
            ('company_id', 'not in', allowed_companies.ids),
            ('inbound_payment_method_ids', 'in', payment_method.id),
            ('type', '=', payment_method.journal_type),
        ])

        return journal_to_update_add, journal_to_update_delete

    def _check_if_deactivable(self, payment_modes):
        errors = []
        companies_on_error = []
        modes_used_on_invoices = self.env['account.invoice'].search([
            ('payment_mode_id', 'in', payment_modes.ids),
            ('state', 'not in', ('paid', 'cancel'))
        ]).mapped('payment_mode_id')
        if modes_used_on_invoices:
            for mode in modes_used_on_invoices:
                errors.append(_('Payment mode %s from company %s is '
                                'used on an open invoice.' % (
                                    mode.name, mode.company_id.name)))
                companies_on_error.append(mode.company_id.id)
        modes_used_on_sales = self.env['sale.order'].search([
            ('payment_mode_id', 'in', payment_modes.ids),
            '|', ('invoice_status', '!=', 'invoiced'),
            ('state', '!=', 'cancel')
        ]).mapped('payment_mode_id')
        if modes_used_on_sales:
            for mode in modes_used_on_sales:
                errors.append(_('Payment mode %s from company %s is used on '
                                'sales order which are not totally invoiced '
                                'or cancelled.' % (mode.name,
                                                   mode.company_id.name)))
                companies_on_error.append(mode.company_id.id)
        return errors, companies_on_error

    def _get_variable_journal(self, company, journal_type):
        aj_obj = self.env['account.journal']
        # We must be a sudo here, because except admin user,
        # journals are readable only for the connected company
        return aj_obj.sudo().search([
            ('type', '=', journal_type),
            ('company_id', '=', company.id),
        ])

    def _check_if_creatable(self, companies, journal_type):
        errors = []
        companies_on_error = []
        for company in companies:
            variable_journal = self._get_variable_journal(
                company, journal_type
            )
            if not variable_journal:
                errors.append(
                    _('No %s journal found for company %s ')
                    % (journal_type, company.name)
                )
                companies_on_error.append(company.id)
        return errors, companies_on_error

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
        if self.journal_to_update_add_ids:
            self._add_method_in_journals()
        if self.journal_to_update_delete_ids:
            self._delete_method_in_journals()

    def _create_payment_modes(self, companies):
        vals = []
        for company in companies:
            aj_obj = self.env['account.journal']
            variable_journal = self._get_variable_journal(
                company, self.journal_type
            )
            if not variable_journal:
                raise UserError(
                    _('No %s journal found for company %s ')
                    % (self.journal_type, company.name)
                )

            sale_journals = aj_obj.search([
                ('type', '=', 'sale'),
                ('company_id', '=', company.id)])
            values = {
                'name': self.account_payment_method_id.name,
                'company_id': company.id,
                'payment_method_id': self.account_payment_method_id.id,
                'bank_account_link': 'variable',
                'variable_journal_ids': [(6, False, variable_journal.ids)],
                'workflow_process_id': self.env.ref(
                    'sale_automatic_workflow.automatic_validation').id,
                'default_journal_ids': [(6, False, sale_journals.ids)]
            }
            vals.append(values)

        for v in vals:
            self.env['account.payment.mode'].sudo().create(v)

    def _activate_payment_modes(self, modes):
        modes.write({'active': True})

    def _deactivate_payment_modes(self, modes):
        modes.write({'active': False})

    def _add_method_in_journals(self):
        self.journal_to_update_add_ids.write({
            'inbound_payment_method_ids':
                [(4, self.account_payment_method_id.id)]
        })

    def _delete_method_in_journals(self):
        self.journal_to_update_delete_ids.write({
            'inbound_payment_method_ids':
                [(3, self.account_payment_method_id.id)]
        })
