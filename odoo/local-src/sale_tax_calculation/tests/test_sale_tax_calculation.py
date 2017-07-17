# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleTaxCalculation(TransactionCase):

    def setUp(self):
        super(TestSaleTaxCalculation, self).setUp()

        self.tax_model = self.env['account.tax']
        self.tax_on_product = self.tax_model.create({
            'name': 'Unittest product tax',
            'price_include': False,
            'amount_type': 'percent',
            'amount': '10',
        })
        self.tax_on_account_on_product = self.tax_model.create({
            'name': 'Unittest account product tax',
            'price_include': False,
            'amount_type': 'percent',
            'amount': '20',
        })
        self.tax_on_account_on_product_category = self.tax_model.create({
            'name': 'Unittest account product category tax',
            'price_include': False,
            'amount_type': 'percent',
            'amount': '30',
        })
        self.tax_on_fiscal_position = self.tax_model.create({
            'name': 'Unittest fiscal position tax',
            'price_include': False,
            'amount_type': 'percent',
            'amount': '40',
        })
        self.tax_on_account_on_product_on_fiscal_position = (
            self.tax_model.create({
                'name': 'Unittest account product fiscal position tax',
                'price_include': False,
                'amount_type': 'percent',
                'amount': '50',
            })
        )

        user_type = self.env.ref('account.data_account_type_payable')
        self.account_model = self.env['account.account']
        self.account = self.account_model.create({
            'name': 'Unittest account',
            'code': '123456',
            'user_type_id': user_type.id,
            'reconcile': True,
        })
        self.account_on_fiscal_position = self.account_model.create({
            'name': 'Unittest account on fiscal position',
            'code': '456789',
            'user_type_id': user_type.id,
            'reconcile': True,
        })

        self.fiscal_position_for_tax = (
            self.env['account.fiscal.position'].create({
                'company_id': self.env.user.company_id.id,
                'name': 'Unittest fiscal position for tax',
                'tax_ids': [(0, False, {
                    'tax_src_id': self.tax_on_product.id,
                    'tax_dest_id': self.tax_on_fiscal_position.id,
                })],
            })
        )
        self.fiscal_position_for_account = (
            self.env['account.fiscal.position'].create({
                'company_id': self.env.user.company_id.id,
                'name': 'Unittest fiscal position for tax',
                'account_ids': [(0, False, {
                    'account_src_id': self.account.id,
                    'account_dest_id': self.account_on_fiscal_position.id,
                })],
            })
        )

        self.product_category = self.env['product.category'].create({
            'name': 'Unittest category',
            'property_account_income_categ_id': False,
        })

        self.p1 = self.env['product.product'].create({
            'name': 'Unittest P1',
            'categ_id': self.product_category.id,
            'list_price': 100.,
            'taxes_id': [(5, False)],
        })

        self.partner = self.env['res.partner'].create({
            'name': 'Unittest partner',
        })

    def create_sale_order(self, fiscal_position=False):
        sale = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'fiscal_position_id': (
                fiscal_position.id
                if fiscal_position
                else None
            ),
            'order_line': [
                (0, False, {
                    'name': self.p1.name,
                    'product_id': self.p1.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                }),
            ]
        })
        for line in sale.order_line:
            line.product_id_change()
        return sale

    def test_01_no_tax(self):
        sale = self.create_sale_order()

        product = sale.order_line.product_id
        self.assertFalse(product.taxes_id)
        self.assertFalse(product.property_account_income_id)

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertFalse(sale.order_line.tax_id)
        self.assertEqual(sale.amount_total, 100)

    def test_02_tax_on_product(self):
        self.p1.write({
            'taxes_id': [(6, False, [self.tax_on_product.id])],
        })
        sale = self.create_sale_order()

        product = sale.order_line.product_id
        self.assertEqual(product.taxes_id.ids, [self.tax_on_product.id])
        self.assertFalse(product.property_account_income_id)

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertEqual(sale.order_line.tax_id.ids, [self.tax_on_product.id])
        self.assertEqual(sale.amount_total, 110)

    def test_03_tax_on_product_with_fiscal_position(self):
        self.p1.write({
            'taxes_id': [(6, False, [self.tax_on_product.id])],
        })
        sale = self.create_sale_order(self.fiscal_position_for_tax)

        product = sale.order_line.product_id
        self.assertEqual(product.taxes_id.ids, [self.tax_on_product.id])
        self.assertFalse(product.property_account_income_id)

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertEqual(
            sale.order_line.tax_id.ids,
            [self.tax_on_fiscal_position.id]
        )
        self.assertEqual(sale.amount_total, 140)

    def test_04_no_tax_on_product_no_tax_on_account(self):
        self.p1.write({
            'property_account_income_id': self.account.id,
        })
        sale = self.create_sale_order()

        product = sale.order_line.product_id
        self.assertFalse(product.taxes_id)
        self.assertEqual(product.property_account_income_id, self.account)
        self.assertFalse(product.property_account_income_id.tax_ids)

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertFalse(sale.order_line.tax_id)
        self.assertEqual(sale.amount_total, 100)

    def test_05_no_tax_on_product_but_tax_on_product_account(self):
        self.p1.write({
            'property_account_income_id': self.account.id,
        })
        self.account.write({
            'tax_ids': [(6, False, [self.tax_on_account_on_product.id])],
        })
        sale = self.create_sale_order()

        product = sale.order_line.product_id
        self.assertFalse(product.taxes_id)
        self.assertEqual(product.property_account_income_id, self.account)
        self.assertEqual(
            product.property_account_income_id.tax_ids.ids,
            [self.tax_on_account_on_product.id]
        )

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertEqual(
            sale.order_line.tax_id.ids,
            [self.tax_on_account_on_product.id]
        )
        self.assertEqual(sale.amount_total, 120)

    def test_06_no_tax_on_product_but_tax_on_product_account_with_fiscal_pos(
            self
    ):
        self.p1.write({
            'property_account_income_id': self.account.id,
        })
        self.account.write({
            'tax_ids': [(6, False, [self.tax_on_account_on_product.id])],
        })
        self.account_on_fiscal_position.write({
            'tax_ids':
                [(6, False, [
                    self.tax_on_account_on_product_on_fiscal_position.id
                ])],
        })
        sale = self.create_sale_order(self.fiscal_position_for_account)

        product = sale.order_line.product_id
        self.assertFalse(product.taxes_id)
        self.assertEqual(product.property_account_income_id, self.account)
        self.assertEqual(
            product.property_account_income_id.tax_ids.ids,
            [self.tax_on_account_on_product.id]
        )

        product_category = product.categ_id
        self.assertFalse(product_category.property_account_income_categ_id)

        self.assertEqual(
            sale.order_line.tax_id.ids,
            [self.tax_on_account_on_product_on_fiscal_position.id]
        )
        self.assertEqual(sale.amount_total, 150)

    def test_07_no_tax_on_product_but_tax_on_category_account(self):
        self.product_category.write({
            'property_account_income_categ_id': self.account.id,
        })
        self.account.write({
            'tax_ids':
                [(6, False, [self.tax_on_account_on_product_category.id])],
        })
        sale = self.create_sale_order()

        product = sale.order_line.product_id
        self.assertFalse(product.taxes_id)
        self.assertFalse(product.property_account_income_id)

        product_category = product.categ_id
        self.assertEqual(
            product_category.property_account_income_categ_id,
            self.account
        )
        self.assertEqual(
            product_category.property_account_income_categ_id.tax_ids.ids,
            [self.tax_on_account_on_product_category.id]
        )

        self.assertEqual(
            sale.order_line.tax_id.ids,
            [self.tax_on_account_on_product_category.id]
        )
        self.assertEqual(sale.amount_total, 130)
