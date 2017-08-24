# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math
import odoo.addons.decimal_precision as dp

from odoo.exceptions import ValidationError
from odoo.tools import float_compare

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_mode_id = fields.Many2one(
        required=True,
    )

    depiltech_payment_mode = fields.Many2one(
        comodel_name='depiltech.payment.mode',
        string='Depiltech payment mode',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )

    compute_calculator = fields.Boolean(
        related='depiltech_payment_mode.compute_calculator',
        readonly=True,
        store=False,
    )

    calculator_link = fields.Char(
        related='depiltech_payment_mode.calculator_link',
        readonly=True,
        store=False,
    )

    provision = fields.Float(
        digits=dp.get_precision('Account'),
        required=True,
        default=0.0,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )
    month_number = fields.Integer(
        required=True,
        default=0,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )
    first_monthly_payment = fields.Float(
        digits=dp.get_precision('Account'),
        required=True,
        default=0.0,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )
    first_monthly_payment_readonly = fields.Float(
        related='first_monthly_payment',
        readonly=True,
    )
    monthly_payment = fields.Float(
        digits=dp.get_precision('Account'),
        required=True,
        default=0.0,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )
    date_of_first_monthly_payment = fields.Date(
        required=True,
        default=lambda s: fields.Date.today(),
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
    )
    day_of_payment = fields.Integer(
        compute='_compute_day_of_payment',
        readonly=True,
        store=True,
    )
    # This field is only used to deactivate check payment rules,
    # in some cases on write method
    no_check_payment_rules = fields.Boolean(
        store=False
    )

    payment_term_id = fields.Many2one(
        copy=False,
    )

    @api.one
    @api.depends('date_of_first_monthly_payment')
    def _compute_day_of_payment(self):
        day_of_payment = False
        if self.date_of_first_monthly_payment:
            day_of_payment = fields.Date.from_string(
                self.date_of_first_monthly_payment
            ).day
        self.day_of_payment = day_of_payment

    def get_to_be_check(self):
        context = self.env.context or {}
        return (
            self.partner_company_type == 'agency_customer' and
            not self.no_check_payment_rules and
            # Context used on specific_discount_program for unit tests
            not context.get('no_check_payment_rules')
        )

    @api.one
    @api.constrains('state', 'depiltech_payment_mode', 'partner_company_type')
    def _check_state(self):
        # If partner company type is a agency customer,
        # check state
        if self.get_to_be_check():
            forbidden_payment_modes = self.env[
                'depiltech.payment.mode'
            ].search(
                [('deny_to_confirm_order', '=', True)],
            )
            is_not_ok = (
                self.state == 'sale' and
                self.depiltech_payment_mode in forbidden_payment_modes
            )
            if is_not_ok:
                raise ValidationError(_(
                    'Depiltech payment mode invalid to confirm sale order'
                ))
            if not self.depiltech_payment_mode:
                raise ValidationError(_(
                    'Payment mode configuration in error '
                    '(no validated depiltech payment mode defined)'
                ))

    @api.one
    @api.constrains('provision', 'amount_total', 'partner_company_type')
    def _check_provision(self):
        # If partner company type is a agency customer,
        # check provision
        if self.get_to_be_check():
            provision_ok = (
                self.provision < 0 or
                float_compare(
                    self.provision,
                    self.amount_total,
                    precision_digits=2
                ) == 1
            )
            if provision_ok:
                raise ValidationError(_(
                    'Provision must be a float '
                    'between 0 and %.2f' % self.amount_total
                ))

    @api.one
    @api.constrains('month_number', 'partner_company_type')
    def _check_month_number(self):
        # If partner company type is a agency customer,
        # check month number
        if self.get_to_be_check():
            icp = self.env['ir.config_parameter']
            max_month_number = int(icp.get_param('max_month_number', '0'))
            if self.month_number < 0 or self.month_number > max_month_number:
                raise ValidationError(_(
                    'Month number must be an integer between 0 and %d' %
                    max_month_number
                ))

    @api.one
    @api.constrains(
        'first_monthly_payment', 'amount_total', 'partner_company_type'
    )
    def _check_first_monthly_payment(self):
        if self.get_to_be_check():
            is_not_ok = (
                self.first_monthly_payment < 0 or
                float_compare(
                    self.first_monthly_payment,
                    self.amount_total,
                    precision_digits=2
                ) == 1
            )
            if is_not_ok:
                raise ValidationError(_(
                    'First monthly payment must be a float '
                    'between 0 and %.2f' % self.amount_total
                ))

    @api.one
    @api.constrains('monthly_payment', 'amount_total', 'partner_company_type')
    def _check_monthly_payment(self):
        if self.get_to_be_check():
            is_not_ok = (
                self.monthly_payment < 0 or
                float_compare(
                    self.monthly_payment,
                    self.amount_total,
                    precision_digits=2
                ) == 1
            )
            if is_not_ok:
                raise ValidationError(_(
                    'Next monthly payment must be a float '
                    'between 0 and %.2f' % self.amount_total
                ))

    @api.one
    @api.constrains('day_of_payment', 'partner_company_type')
    def _check_day_of_payment(self):
        if self.get_to_be_check():
            if self.day_of_payment < 1 or self.day_of_payment > 31:
                raise ValidationError(_(
                    'Day of payment must be an integer between 1 and 31'
                ))

    def _compute_provision(self):
        return self.amount_total - (
            self.month_number * self.monthly_payment
        )

    def _compute_month_number(self):
        return (self.amount_total - self.provision) / self.monthly_payment

    def _compute_monthly_payment(self):
        return (self.amount_total - self.provision) / self.month_number

    @api.onchange('payment_mode_id')
    def _onchange_payment_mode_id(self):
        self.depiltech_payment_mode = (
            self.payment_mode_id.payment_method_id.depiltech_payment_mode
            if self.payment_mode_id
            else self.env['depiltech.payment.mode'].search(
                [('use_as_default', '=', True)],
                limit=1
            )
        )

    @api.onchange('provision')
    def _onchange_provision(self):
        if self.compute_calculator:
            if (
                not self.provision
                or (self.month_number and self.monthly_payment)
            ):
                self.no_check_payment_rules = True
                self.month_number = False
                self.monthly_payment = False
                self.first_monthly_payment = self.monthly_payment
                self.no_check_payment_rules = False
            elif self.month_number and not self.monthly_payment:
                self.monthly_payment = self._compute_monthly_payment()
                self.first_monthly_payment = self.monthly_payment
            elif not self.month_number and self.monthly_payment:
                self.month_number = self._compute_month_number()
                self.monthly_payment = self._compute_monthly_payment()
                self.first_monthly_payment = self.monthly_payment
        self._check_provision()

    @api.onchange('month_number')
    def _onchange_month_number(self):
        if self.compute_calculator:
            if (
                not self.month_number
                or (self.provision and self.monthly_payment)
            ):
                self.no_check_payment_rules = True
                self.provision = False
                self.monthly_payment = False
                self.first_monthly_payment = self.monthly_payment
                self.no_check_payment_rules = False
            elif self.provision and not self.monthly_payment:
                self.monthly_payment = self._compute_monthly_payment()
                self.first_monthly_payment = self.monthly_payment
            elif not self.provision and self.monthly_payment:
                self.provision = self._compute_provision()
        self._check_month_number()

    @api.onchange('monthly_payment')
    def _onchange_monthly_payment(self):
        if self.compute_calculator:
            if (
                not self.monthly_payment
                or (self.provision and self.month_number)
            ):
                self.no_check_payment_rules = True
                self.provision = False
                self.month_number = False
                self.no_check_payment_rules = False
            elif self.provision and not self.month_number:
                self.month_number = self._compute_month_number()
                self.monthly_payment = self._compute_monthly_payment()
            elif not self.provision and self.month_number:
                self.provision = self._compute_provision()
            self.first_monthly_payment = self.monthly_payment
        self._check_monthly_payment()

    @api.onchange('first_monthly_payment')
    def _onchange_first_monthly_payment(self):
        self._check_first_monthly_payment()

    @api.onchange('day_of_payment')
    def _onchange_day_of_payment(self):
        self._check_day_of_payment()

    @api.onchange('amount_total', 'depiltech_payment_mode')
    def _onchange_amount_total(self):
        self.no_check_payment_rules = True
        self.provision = False
        self.month_number = False
        self.monthly_payment = False
        self.first_monthly_payment = False
        self.no_check_payment_rules = False

    @api.multi
    def onchange(self, values, field_name, field_onchange):
        new_field_onchange = field_onchange or {}
        # If onchange is triggered by one of these fields,
        # we don't want to trigger onchange for others
        #
        # Example:
        # If onchange is triggered by provision field,
        # we don't want to trigger onchange
        # on month_number and monthly_payment fields
        for field in ['provision', 'month_number', 'monthly_payment']:
            if field_name != field and field in new_field_onchange.keys():
                del new_field_onchange[field]
        return super(SaleOrder, self).onchange(
            values, field_name, new_field_onchange
        )

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        # If partner company type is a agency customer,
        # we reset custom payment terms
        if self.partner_company_type == 'agency_customer':
            self.payment_term_id = False
        return result

    @api.multi
    def action_cancel(self):
        # If partner company type is a agency customer,
        # we unlink custom payment terms
        if self.partner_company_type == 'agency_customer':
            self.payment_term_id.sudo().unlink()
        return super(SaleOrder, self).action_cancel()

    @api.multi
    def action_confirm(self):
        # If partner company type isn't a agency customer,
        # don't create custom payment terms
        if self.partner_company_type != 'agency_customer':
            return super(SaleOrder, self).action_confirm()
        # Creation of custom payment terms
        values = {
            'name': self.name,
            'company_id': self.company_id.id,
            'active': False,
            'sequential_lines': True,
            'sale_order_id': self.id,
            'line_ids': []
        }
        # PNF payment case
        if not self.compute_calculator:
            # In PNF payment case, we have only 2 payments :
            # - the provision
            values['line_ids'].append(
                (0, False, {
                    'sequence': 1,
                    'value': 'fixed',
                    'value_amount': self.provision,
                    'days': 0,
                    'option': 'day_after_invoice_date',
                }),
            )
            # - the balance
            values['line_ids'].append(
                (0, False, {
                    'sequence': 2,
                    'value': 'balance',
                    'days': self.depiltech_payment_mode.days_before_payment,
                    'option': 'day_after_invoice_date',
                }),
            )
        # Other payment case
        else:
            if self.month_number > 0:
                # First line is the provision
                values['line_ids'].append(
                    (0, False, {
                        'sequence': 1,
                        'value': 'fixed',
                        'value_amount': self.provision,
                        'days': 0,
                        'option': 'day_after_invoice_date',
                    }),
                )
                # Calculation of compute days provides from :
                # hr_holidays._get_number_of_days()
                from_date = fields.Datetime.from_string(
                    fields.Datetime.now()  # = confirmation_date
                )
                to_date = fields.Datetime.from_string(
                    self.date_of_first_monthly_payment
                )

                time_delta = to_date - from_date
                days = math.ceil(
                    time_delta.days + float(time_delta.seconds) / 86400)
                if not days:
                    days = 0

                # Add the first month payment
                # If we have only one month, the payment will be in the balance
                if self.month_number > 1:
                    # If we add more than one month number,
                    # we create here the first payment
                    values['line_ids'].append(
                        (0, False, {
                            'sequence': 2,
                            'value': 'fixed',
                            'value_amount': self.monthly_payment,
                            'days': days,
                            'payment_days': self.day_of_payment,
                            'option': 'day_after_invoice_date',
                        }),
                    )

                # We create here payments for all month
                # (except the first and the last month)
                for month in range(2, self.month_number):
                    values['line_ids'].append(
                        (0, False, {
                            'sequence': month + 1,
                            'value': 'fixed',
                            'value_amount': self.monthly_payment,
                            'months': 1,
                            'payment_days': self.day_of_payment,
                            'option': 'day_after_invoice_date',
                        }),
                    )

                # The last month payment is the balance
                values['line_ids'].append(
                    (0, False, {
                        'sequence': self.month_number + 1,
                        'value': 'balance',
                        'months': 1,
                        'payment_days': self.day_of_payment,
                        'option': 'day_after_invoice_date',
                    }),
                )
            else:
                # First line is the provision, but also the only line
                values['line_ids'].append(
                    (0, False, {
                        'sequence': 1,
                        'value': 'balance',
                        'days': 0,
                        'option': 'day_after_invoice_date',
                    }),
                )
        try:
            payment_term = (
                self.env['account.payment.term'].sudo().create(values)
            )
        except ValidationError:
            raise ValidationError(
                _('Invalid data for the calculator.'))
        self.payment_term_id = payment_term.id
        return super(SaleOrder, self).action_confirm()
