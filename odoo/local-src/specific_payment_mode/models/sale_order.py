# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.addons.decimal_precision as dp

from openerp.exceptions import ValidationError

from openerp import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    depiltech_payment_mode = fields.Many2one(
        comodel_name='depiltech.payment.mode',
        string='Payment mode',
    )

    provision = fields.Integer()
    month_number = fields.Integer()
    monthly_payment = fields.Float(
        digits=dp.get_precision('Account')
    )

    @api.model
    def _check_provision(self, provision, month_number, monthly_payment):
        if provision or month_number or monthly_payment:
            if provision < 10 or provision > 1000:
                raise ValidationError(_(
                    'Provision must be an integer between 10 and 1000'
                ))

    @api.model
    def _check_month_number(self, provision, month_number, monthly_payment):
        if provision or month_number or monthly_payment:
            if month_number < 0 or month_number > 20:
                raise ValidationError(_(
                    'Month number must be an integer between 0 and 20'
                ))

    @api.model
    def _check_monthly_payment(self, provision, month_number, monthly_payment):
        if provision or month_number or monthly_payment:
            if monthly_payment < 0:
                raise ValidationError(_(
                    'Monthly payment must be a positive float'
                ))

    @api.model
    def _check_payment_rules(self, provision, month_number, monthly_payment):
        self._check_provision(provision, month_number, monthly_payment)
        self._check_month_number(provision, month_number, monthly_payment)
        self._check_monthly_payment(provision, month_number, monthly_payment)

    @api.model
    def create(self, values):
        self._check_payment_rules(
            values.get('provision', False),
            values.get('month_number', False),
            values.get('monthly_payment', False),
        )
        return super(SaleOrder, self).create(values)

    @api.multi
    def write(self, values):
        super(SaleOrder, self).write(values)
        context = self.env.context or {}
        if not context.get('no_check_payment_rules'):
            for order in self:
                self._check_payment_rules(
                    order.provision, order.month_number, order.monthly_payment
                )
        return True

    def _compute_provision(self):
        return self.amount_total - (self.month_number * self.monthly_payment)

    def _compute_month_number(self):
        return (self.amount_total - self.provision) / self.monthly_payment

    def _compute_monthly_payment(self):
        return (self.amount_total - self.provision) / self.month_number

    @api.onchange('provision')
    def _onchange_provision(self):
        if (
            not self.provision
            or self.month_number and self.monthly_payment
        ):
            self.with_context(no_check_payment_rules=True).update({
                'month_number': False, 'monthly_payment': False
            })
        elif self.month_number and not self.monthly_payment:
            self.monthly_payment = self._compute_monthly_payment()
        elif not self.month_number and self.monthly_payment:
            self.month_number = self._compute_month_number()
            self.monthly_payment = self._compute_monthly_payment()
        self._check_provision(
            self.provision, self.month_number, self.monthly_payment
        )

    @api.onchange('month_number')
    def _onchange_month_number(self):
        if (
            not self.month_number
            or self.provision and self.monthly_payment
        ):
            self.with_context(no_check_payment_rules=True).update({
                'provision': False, 'monthly_payment': False
            })
        elif self.provision and not self.monthly_payment:
            self.monthly_payment = self._compute_monthly_payment()
        elif not self.provision and self.monthly_payment:
            self.provision = self._compute_provision()
        self._check_month_number(
            self.provision, self.month_number, self.monthly_payment
        )

    @api.onchange('monthly_payment')
    def _onchange_monthly_payment(self):
        if (
            not self.monthly_payment
            or self.provision and self.month_number
        ):
            self.with_context(no_check_payment_rules=True).update({
                'provision': False, 'month_number': False
            })
        elif self.provision and not self.month_number:
            self.month_number = self._compute_month_number()
            self.monthly_payment = self._compute_monthly_payment()
        elif not self.provision and self.month_number:
            self.provision = self._compute_provision()
        self._check_monthly_payment(
            self.provision, self.month_number, self.monthly_payment
        )

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        self.write({
            'provision': False,
            'month_number': False,
            'monthly_payment': False,
        })

    @api.multi
    def onchange(self, values, field_name, field_onchange):
        new_field_onchange = field_onchange or {}
        for field in ['provision', 'month_number', 'monthly_payment']:
            if field_name != field and field in new_field_onchange.keys():
                del new_field_onchange[field]
        return super(SaleOrder, self).onchange(
            values, field_name, new_field_onchange
        )
