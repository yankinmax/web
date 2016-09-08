# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestDiscountProgram(TransactionCase):

    def setUp(self):
        super(TestDiscountProgram, self).setUp()

        # TODO: manage tax if OCA
        taxes = self.env['account.tax'].search([])
        taxes.write({'price_include': True})

        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.product_category_model = self.env['product.category']
        self.program_model = self.env['sale.discount.program']
        self.sale_model = self.env['sale.order']

        for program in self.program_model.search([]):
            program.unlink()

        self.client = self.partner_model.create({
            'name': 'Default client',
        })

        self.product_category = self.product_category_model.create({
            'name': 'Unittest product category',
        })
        self.p1 = self.product_model.create({
            'name': 'Unittest P1',
            'categ_id': self.product_category.id,
        })

        self.p2 = self.product_model.create({
            'name': 'Unittest P2',
            'categ_id': self.product_category.id,
        })

    def test_add_product(self):
        product_to_add = self.product_model.create({
            'name': 'Unittest gift product',
            'uom_id': self.ref('product.product_uom_unit'),
        })

        program = self.program_model.create({
            'name': 'Unittest gift product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product_category',
                    'product_category_id': self.product_category.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'add_product',
                    'product_add_id': product_to_add.id,
                })
            ]
        })

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        sale.apply_discount_programs()

        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(
            self.p1 | product_to_add,
            sale.order_line.mapped('product_id')
        )

        # Modify condition: Need 2 self.p1 to add the new product
        program.condition_ids[0].product_min_qty = 2
        sale.apply_discount_programs()

        self.assertEqual(1, len(sale.order_line))
        self.assertEqual(self.p1, sale.order_line.product_id)

        sale.order_line.product_uom_qty = 4

        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(
            self.p1 | product_to_add,
            sale.order_line.mapped('product_id')
        )

    def test_reward_product(self):
        promotion = self.program_model.create({
            'name': 'Unittest reward product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product_category',
                    'product_category_id': self.product_category.id,
                    'product_min_price_unit': 400,
                    'product_min_qty': 1,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'product_discount',
                    'product_discount_selection': 'most_expensive_no_discount',
                    'discount_percent': 20,
                })
            ]
        })

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'price_unit': 150,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        sale.apply_discount_programs()

        # condition is not respected
        self.assertEqual(1, len(sale.order_line))
        self.assertEqual(150, sale.amount_total)

        # Add a product from the same category
        sale.write({
            'order_line': [(0, False, {
                'product_id': self.p2.id,
                'product_uom_qty': 1,
                'price_unit': 400,
            })]
        })

        sale.apply_discount_programs()
        self.assertEqual(3, len(sale.order_line))
        # 400 - 20% + 150
        self.assertEqual(470, sale.amount_total)

        # Add quantity condition => At least 2 products with PU > 300
        promotion.condition_ids.product_min_qty = 2

        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(550, sale.amount_total)

        # Change price_unit of first line
        sale.order_line[0].price_unit = 500

        sale.apply_discount_programs()
        self.assertEqual(3, len(sale.order_line))

        # Most expensive: 500
        # => 500 - 20% + 400
        self.assertEqual(800, sale.amount_total)

        # Add second discount in actions (10 % on second most expensive)
        promotion.write({
            'action_ids': [(0, False, {
                'type_action': 'product_discount',
                'product_discount_selection': 'most_expensive_no_discount',
                'discount_percent': 10,
            })]
        })

        sale.apply_discount_programs()
        self.assertEqual(4, len(sale.order_line))

        # 500 - 20% + 400 - 10%
        self.assertEqual(760, sale.amount_total)
