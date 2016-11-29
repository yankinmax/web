# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import ValidationError

from openerp.tests.common import TransactionCase, post_install, at_install


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
        })

        self.p1 = self.product_model.create({'name': 'Unittest P1'})

        self.sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 2500,
                'tax_id': [(5,)]
            })]
        })

    @post_install(True)
    @at_install(False)
    def test_payment_rules_constraints(self):
        # Check provision check
        self.sale.provision = 50
        with self.assertRaises(ValidationError):
            self.sale.write({'provision': 0, 'monthly_payment': 100.})
        with self.assertRaises(ValidationError):
            self.sale.provision = 1010
        self.sale.write({'provision': False, 'monthly_payment': False})

        # Check month_number check
        self.sale.write({'provision': 100, 'month_number': 5})
        with self.assertRaises(ValidationError):
            self.sale.month_number = -1
        with self.assertRaises(ValidationError):
            self.sale.month_number = 21

    @post_install(True)
    @at_install(False)
    def test_payment_rules_initial_values(self):
        # Check initial values
        self.assertEqual(self.sale.amount_total, 2500)

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

    @post_install(True)
    @at_install(False)
    def test_payment_rules_amount_total(self):
        self.sale.write({
            'monthly_payment': 300.,
            'month_number': 5,
            'provision': 1000,
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
    def test_payment_rules_provision(self):
        # Check modification with only month_number
        self.sale.write({
            'month_number': 5,
            'provision': 1000,
        })
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 1000)
        self.assertEqual(self.sale.month_number, 5)
        self.assertEqual(self.sale.monthly_payment, 300.)

        # Check modification with month_number and monthly_payment
        self.sale.provision = 800
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 800)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

        # Check modification with only monthly_payment
        self.sale.write({
            'monthly_payment': 400.,
            'provision': 450,
        })
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, 450)
        self.assertEqual(self.sale.month_number, 5)
        self.assertEqual(self.sale.monthly_payment, 410.)

        # Check modification with False value
        self.sale.with_context(no_check_payment_rules=True).provision = False
        self.sale._onchange_provision()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

    @post_install(True)
    @at_install(False)
    def test_payment_rules_month_number(self):
        # Check modification with only provision
        self.sale.write({
            'provision': 500,
            'month_number': 10,
        })
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, 500)
        self.assertEqual(self.sale.month_number, 10)
        self.assertEqual(self.sale.monthly_payment, 200.)

        # Check modification with False value
        self.sale.month_number = False
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, False)
        self.assertEqual(self.sale.month_number, False)
        self.assertEqual(self.sale.monthly_payment, False)

        # Check modification with only monthly_payment
        self.sale.with_context(no_check_payment_rules=True).write({
            'monthly_payment': 200.,
            'month_number': 8,
        })
        self.sale._onchange_month_number()

        self.assertEqual(self.sale.provision, 900)
        self.assertEqual(self.sale.month_number, 8)
        self.assertEqual(self.sale.monthly_payment, 200.)

    @post_install(True)
    @at_install(False)
    def test_payment_rules_monthly_payment(self):
        # Check modification with only provision
        self.sale.write({
            'provision': 1000,
            'monthly_payment': 100.5,
        })
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, 1000)
        self.assertEqual(self.sale.month_number, 14)
        self.assertEqual(self.sale.monthly_payment, 107.14)

        # Check modification with False value
        self.sale.monthly_payment = False
        self.sale._onchange_monthly_payment()

        # Check modification with only month_number
        self.sale.with_context(no_check_payment_rules=True).write({
            'month_number': 20,
            'monthly_payment': 100.,
        })
        self.sale._onchange_monthly_payment()

        self.assertEqual(self.sale.provision, 500)
        self.assertEqual(self.sale.month_number, 20)
        self.assertEqual(self.sale.monthly_payment, 100.)
