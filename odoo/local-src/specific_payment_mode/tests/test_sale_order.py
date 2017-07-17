# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError

from odoo.tests.common import TransactionCase, post_install, at_install


class TestSaleOrder(TransactionCase):

    def setUp(self):
        super(TestSaleOrder, self).setUp()

        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.sale_model = self.env['sale.order']

        self.phototherapist = self.env['res.company.phototherapist'].create({
            'name': 'Unittest phototherapist',
            'company_id': self.env.user.company_id.id
        })

        self.partner1 = self.partner_model.create({
            'name': 'partner',
            'company_type': 'agency_customer',
        })

        self.p1 = self.product_model.create({'name': 'Unittest P1'})

        self.sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'depiltech_payment_mode': self.ref('specific_payment_mode.other'),
            'date_of_first_monthly_payment': '2017-01-15',
            'day_of_payment': 31,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 2500,
                'tax_id': [(5,)]
            })]
        })

    @post_install(True)
    @at_install(False)
    def test_01_payment_rules_constraints(self):
        # Check provision check
        self.sale.write({'provision': 50, 'monthly_payment': 100.})

        with self.assertRaises(ValidationError):
            self.sale.provision = -10
        with self.assertRaises(ValidationError):
            self.sale.provision = 2510

        with self.assertRaises(ValidationError):
            self.sale.monthly_payment = -10
        with self.assertRaises(ValidationError):
            self.sale.monthly_payment = 2510

        # Reset values
        self.sale.write({'provision': False, 'monthly_payment': False})

        # Check month_number check
        self.sale.write({'provision': 100, 'month_number': 5})

        with self.assertRaises(ValidationError):
            self.sale.month_number = -1
        with self.assertRaises(ValidationError):
            self.sale.month_number = 21

        icp = self.env['ir.config_parameter']
        icp.set_param('max_month_number', 22)

        self.sale.month_number = 21

    @post_install(True)
    @at_install(False)
    def test_02_payment_rules_initial_values(self):
        # Check initial values
        self.assertEqual(self.sale.amount_total, 2500)

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

    @post_install(True)
    @at_install(False)
    def test_03_payment_rules_amount_total(self):
        self.sale.write({
            'provision': 1000,
            'month_number': 5,
            'monthly_payment': 300.,
        })

        self.assertEqual(self.sale.provision, 1000)
        self.assertEqual(self.sale.month_number, 5)
        self.assertEqual(self.sale.monthly_payment, 300.)

        # Check amount_total modification
        self.sale._onchange_amount_total()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

    @post_install(True)
    @at_install(False)
    def test_04_payment_rules_provision(self):
        # Check provision modification with only month_number
        self.sale.write({
            'provision': 1000,
            'month_number': 5,
        })
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 1000)
        self.assertEqual(self.sale.month_number, 5)
        self.assertEqual(self.sale.monthly_payment, 300.)

        # Check provision modification with month_number and monthly_payment
        self.sale.provision = 800
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 800)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

        # Check provision modification with only monthly_payment
        self.sale.write({
            'monthly_payment': 400.,
            'provision': 450,
        })
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 450)
        self.assertEqual(self.sale.month_number, 5)
        self.assertEqual(self.sale.monthly_payment, 410.)

        # Check provision modification with False value
        self.sale.provision = False
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

    @post_install(True)
    @at_install(False)
    def test_05_payment_rules_month_number(self):
        # Check month_number modification with only provision
        self.sale.write({
            'provision': 500,
            'month_number': 10,
        })
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, 500)
        self.assertEqual(self.sale.month_number, 10)
        self.assertEqual(self.sale.monthly_payment, 200.)

        # Check month_number modification with False value
        self.sale.month_number = False
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

        # Check month_number modification with only monthly_payment
        self.sale.monthly_payment = 200.
        self.sale.month_number = 8
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, 900)
        self.assertEqual(self.sale.month_number, 8)
        self.assertEqual(self.sale.monthly_payment, 200.)

    @post_install(True)
    @at_install(False)
    def test_06_payment_rules_monthly_payment(self):
        # Check monthly_payment modification with only provision
        self.sale.write({
            'provision': 1000,
            'monthly_payment': 100.5,
        })
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, 1000)
        self.assertEqual(self.sale.month_number, 14)
        self.assertEqual(self.sale.monthly_payment, 107.14)

        # Check monthly_payment modification with False value
        self.sale.monthly_payment = False
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

        # Check monthly_payment modification with only month_number
        self.sale.month_number = 10
        self.sale.monthly_payment = 200.
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, 500)
        self.assertEqual(self.sale.month_number, 10)
        self.assertEqual(self.sale.monthly_payment, 200.)

    @post_install(True)
    @at_install(False)
    def test_07_payment_terms(self):
        self.sale.write({
            'date_of_first_monthly_payment': '2020-01-31',
            'month_number': 10,
            'monthly_payment': 200.,
        })
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, 500)
        self.assertEqual(self.sale.month_number, 10)
        self.assertEqual(self.sale.monthly_payment, 200.)

        # Compute days number to check days calculation
        from_date = fields.Datetime.from_string(
            fields.Datetime.now()  # = confirmation_date
        )
        to_date = fields.Datetime.from_string('2020-01-31')

        time_delta = to_date - from_date
        days = math.ceil(
            time_delta.days + float(time_delta.seconds) / 86400)
        if not days:
            days = 0

        # Check generated payment terms
        self.sale.action_confirm()
        payment_term = self.sale.payment_term_id
        payment_term_lines = payment_term.line_ids

        self.assertEqual(self.sale, payment_term.sale_order_id)
        self.assertEqual(self.sale.name, payment_term.name)
        self.assertTrue(payment_term.sequential_lines)
        self.assertFalse(payment_term.active)

        self.assertEqual(len(payment_term_lines), 1 + 10)

        self.assertEqual(payment_term_lines[0].value_amount, 500)
        self.assertEqual(payment_term_lines[0].value, 'fixed')
        self.assertEqual(payment_term_lines[0].days, 0)
        self.assertEqual(payment_term_lines[0].months, 0)
        self.assertFalse(payment_term_lines[0].payment_days)
        self.assertEqual(
            payment_term_lines[0].option, 'day_after_invoice_date'
        )
        self.assertEqual(payment_term_lines[0].sequence, 1)

        self.assertEqual(payment_term_lines[1].value_amount, 200)
        self.assertEqual(payment_term_lines[1].value, 'fixed')
        self.assertEqual(payment_term_lines[1].days, days)
        self.assertEqual(payment_term_lines[1].months, 0)
        self.assertEqual(payment_term_lines[1].payment_days, '31')
        self.assertEqual(
            payment_term_lines[1].option, 'day_after_invoice_date'
        )
        self.assertEqual(payment_term_lines[1].sequence, 2)

        for i in range(2, 9 + 1):
            self.assertEqual(payment_term_lines[i].value_amount, 200)
            self.assertEqual(payment_term_lines[i].value, 'fixed')
            self.assertEqual(payment_term_lines[i].days, 0)
            self.assertEqual(payment_term_lines[i].months, 1)
            self.assertEqual(payment_term_lines[i].payment_days, '31')
            self.assertEqual(
                payment_term_lines[i].option, 'day_after_invoice_date'
            )
        self.assertEqual(payment_term_lines[i].sequence, i + 1)

        self.assertEqual(payment_term_lines[10].value_amount, 0)
        self.assertEqual(payment_term_lines[10].value, 'balance')
        self.assertEqual(payment_term_lines[10].days, 0)
        self.assertEqual(payment_term_lines[10].months, 1)
        self.assertEqual(payment_term_lines[10].payment_days, '31')
        self.assertEqual(
            payment_term_lines[10].option, 'day_after_invoice_date'
        )
        self.assertEqual(payment_term_lines[10].sequence, 11)

        # Create invoice
        order_context = {
            'active_model': 'sale.order',
            'active_ids': self.sale.ids,
            'active_id': self.sale.id
        }
        payment_wiz = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'all',
        })
        payment_wiz.with_context(order_context).create_invoices()

        invoice = self.sale.invoice_ids[0]

        # Validate invoice
        invoice.action_invoice_open()

        # Check account move
        move = invoice.move_id
        move_lines = move.line_ids.filtered(
            lambda l: l.debit
        ).sorted(
            lambda l: (l.date_maturity, l.id)
        )

        self.assertEqual(move_lines[0].balance, 500)
        self.assertEqual(move_lines[0].date_maturity, fields.Date.today())

        self.assertEqual(move_lines[1].balance, 200)
        self.assertEqual(move_lines[1].date_maturity, '2020-01-31')

        self.assertEqual(move_lines[2].balance, 200)
        self.assertEqual(move_lines[2].date_maturity, '2020-02-29')

        self.assertEqual(move_lines[3].balance, 200)
        self.assertEqual(move_lines[3].date_maturity, '2020-03-31')

        self.assertEqual(move_lines[4].balance, 200)
        self.assertEqual(move_lines[4].date_maturity, '2020-04-30')

        self.assertEqual(move_lines[5].balance, 200)
        self.assertEqual(move_lines[5].date_maturity, '2020-05-31')

        self.assertEqual(move_lines[6].balance, 200)
        self.assertEqual(move_lines[6].date_maturity, '2020-06-30')

        self.assertEqual(move_lines[7].balance, 200)
        self.assertEqual(move_lines[7].date_maturity, '2020-07-31')

        self.assertEqual(move_lines[8].balance, 200)
        self.assertEqual(move_lines[8].date_maturity, '2020-08-31')

        self.assertEqual(move_lines[9].balance, 200)
        self.assertEqual(move_lines[9].date_maturity, '2020-09-30')

        self.assertEqual(move_lines[10].balance, 200)
        self.assertEqual(move_lines[10].date_maturity, '2020-10-31')

    @post_install(True)
    @at_install(False)
    def test_08_payment_terms_with_pnf(self):
        pnf3 = self.env.ref('specific_payment_mode.pnf3')
        self.sale.write({
            'depiltech_payment_mode': pnf3.id,
            'provision': 500,
            'month_number': 10,
            'monthly_payment': 200.,
        })

        # Check generated payment terms
        self.sale.action_confirm()
        payment_term = self.sale.payment_term_id
        payment_term_lines = payment_term.line_ids

        self.assertEqual(self.sale, payment_term.sale_order_id)
        self.assertEqual(self.sale.name, payment_term.name)
        self.assertTrue(payment_term.sequential_lines)
        self.assertFalse(payment_term.active)

        self.assertEqual(len(payment_term_lines), 2)

        self.assertEqual(payment_term_lines[0].value_amount, 500)
        self.assertEqual(payment_term_lines[0].value, 'fixed')
        self.assertEqual(payment_term_lines[0].days, 0)
        self.assertEqual(payment_term_lines[0].months, 0)
        self.assertFalse(payment_term_lines[0].payment_days)
        self.assertEqual(
            payment_term_lines[0].option, 'day_after_invoice_date'
        )
        self.assertEqual(payment_term_lines[0].sequence, 1)

        self.assertEqual(payment_term_lines[1].value_amount, 0)
        self.assertEqual(payment_term_lines[1].value, 'balance')
        self.assertEqual(payment_term_lines[1].days, pnf3.days_before_payment)
        self.assertEqual(payment_term_lines[1].months, 0)
        self.assertFalse(payment_term_lines[0].payment_days)
        self.assertEqual(
            payment_term_lines[1].option, 'day_after_invoice_date'
        )
        self.assertEqual(payment_term_lines[1].sequence, 2)

        # Create invoice
        order_context = {
            'active_model': 'sale.order',
            'active_ids': self.sale.ids,
            'active_id': self.sale.id
        }
        payment_wiz = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'all',
        })
        payment_wiz.with_context(order_context).create_invoices()

        invoice = self.sale.invoice_ids[0]

        # Validate invoice
        invoice.action_invoice_open()

        # Check account move
        move = invoice.move_id
        move_lines = move.line_ids.filtered(
            lambda l: l.debit
        ).sorted(
            lambda l: (l.date_maturity, l.id)
        )

        today = fields.Date.today()
        self.assertEqual(move_lines[0].balance, 500)
        self.assertEqual(move_lines[0].date_maturity, today)

        self.assertEqual(move_lines[1].balance, 2000)
        self.assertEqual(
            fields.Date.from_string(move_lines[1].date_maturity),
            fields.Date.from_string(today) + relativedelta(
                days=pnf3.days_before_payment
            )
        )
