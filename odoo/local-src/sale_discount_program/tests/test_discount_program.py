# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import timedelta, date

from openerp.tests.common import TransactionCase, post_install, at_install


class TestDiscountProgram(TransactionCase):

    def setUp(self):
        super(TestDiscountProgram, self).setUp()

        # TODO: manage tax if OCA
        taxes = self.env['account.tax'].search([])
        taxes.write({'price_include': True})

        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.product_category_model = self.env['product.category']
        self.pricelist_model = self.env['product.pricelist']
        self.program_model = self.env['sale.discount.program']
        self.sale_model = self.env['sale.order']

        # TODO: remove if OCA
        self.phototherapist = self.env['res.company.phototherapist'].create({
            'name': 'Unittest phototherapist',
            'company_id': self.env.user.company_id.id
        })

        for program in self.program_model.search([]):
            program.unlink()

        self.client = self.partner_model.create({
            'name': 'Default client',
        })

        self.product_category = self.product_category_model.create({
            'name': 'Unittest product category',
        })

        self.sub_category = self.product_category_model.create({
            'name': 'Unittest product sub category',
            'parent_id': self.product_category.id,
        })

        self.p1 = self.product_model.create({
            'name': 'Unittest P1',
            'categ_id': self.product_category.id,
        })

        self.p2 = self.product_model.create({
            'name': 'Unittest P2',
            'categ_id': self.product_category.id,
        })

        self.promo_pricelist = self.pricelist_model.create({
            'name': 'Unittest code promo',
            'discount_policy': 'without_discount',
            'item_ids': [(0, False, {
                'applied_on': '3_global',
                'compute_price': 'percentage',
                'percent_price': 10,
            })]
        })
        self.env.user.write({
            'groups_id': [(4, self.ref('sale.group_discount_per_so_line'))]
        })

    @post_install(True)
    @at_install(False)
    def test_product_add(self):

        product_to_add = self.product_model.create({
            'name': 'Unittest gift product',
            'list_price': 100,
            'uom_id': self.ref('product.product_uom_unit'),
        })

        program = self.program_model.create({
            'name': 'Unittest gift product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product',
                    'product_id': self.p1.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'product_add',
                    'product_add_id': product_to_add.id,
                })
            ]
        })
        self.assertEqual(
            'Product: Unittest P1',
            program.condition_ids[0].name
        )

        self.assertEqual(
            'Add product: Unittest gift product',
            program.action_ids[0].name
        )

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'phototherapist_id': self.phototherapist.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p2.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        # Not the good product
        sale.apply_discount_programs()

        self.assertEqual(1, len(sale.order_line))
        self.assertEqual(self.p2, sale.order_line.product_id)

        # Change the quotation product to p1
        sale.order_line.product_id = self.p1

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

        self.assertEqual(100, sale.order_line[1].price_unit)

        # Test to specify price
        program.action_ids.product_add_force_price = True
        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(0, sale.order_line[1].price_unit)

        program.action_ids.product_add_price = 90
        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(90, sale.order_line[1].price_unit)

    @post_install(True)
    @at_install(False)
    def test_condition_sub_category(self):
        program = self.program_model.create({
            'name': 'Unittest gift product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product_category',
                    'product_category_id': self.product_category.id,
                })
            ],
        })

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'phototherapist_id': self.phototherapist.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })
        self.assertTrue(program.is_applicable(sale))

        # Test with a sub category
        self.p1.categ_id = self.sub_category.id
        self.assertTrue(program.is_applicable(sale))

        self.sub_category.parent_id = False
        self.assertFalse(program.is_applicable(sale))

    @post_install(True)
    @at_install(False)
    def test_condition_product_distinct_qty(self):
        program = self.program_model.create({
            'name': 'Unittest gift product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product_category',
                    'product_category_id': self.product_category.id,
                    'product_min_qty': 2,
                })
            ],
        })

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'phototherapist_id': self.phototherapist.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'product_uom_qty': 2,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })
        self.assertTrue(program.is_applicable(sale))

        program.condition_ids.product_qty_type = 'distinct'
        self.assertFalse(program.is_applicable(sale))

        sale.write({
            'order_line': [
                (0, False, {
                    'product_id': self.p2.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        self.assertTrue(program.is_applicable(sale))

        # Two lines with same product should not work
        sale.order_line.write({'product_id': self.p1.id})
        self.assertFalse(program.is_applicable(sale))

    @post_install(True)
    @at_install(False)
    def test_product_discount(self):
        program = self.program_model.create({
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

        self.assertEqual(
            'Product Category: Unittest product category',
            program.condition_ids[0].name
        )

        self.assertEqual(
            'Discount: 20.0% on Most expensive without discount',
            program.action_ids[0].name
        )

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
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
        self.assertEqual(2, len(sale.order_line))
        # 400 - 20% + 150
        self.assertEqual(470, sale.amount_total)
        self.assertEqual(20, sale.order_line[1].discount)
        self.assertEqual(True, sale.order_line[1].discount_program)

        # Add quantity condition => At least 2 products with PU > 300
        program.condition_ids.product_min_qty = 2

        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(550, sale.amount_total)

        # Change price_unit of first line
        sale.order_line[0].price_unit = 500

        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))

        # Most expensive: 500
        # => 500 - 20% + 400
        self.assertEqual(800, sale.amount_total)
        sale.order_line[0].discount = 20
        sale.order_line[1].discount = False

        # Add second discount in actions (10 % on second most expensive)
        program.write({
            'action_ids': [(0, False, {
                'type_action': 'product_discount',
                'product_discount_selection': 'most_expensive_no_discount',
                'discount_percent': 10,
            })]
        })

        sale.apply_discount_programs()
        self.assertEqual(2, len(sale.order_line))

        # 500 - 20% + 400 - 10%
        self.assertEqual(760, sale.amount_total)
        sale.order_line[0].discount = 20
        sale.order_line[1].discount = 10

    @post_install(True)
    @at_install(False)
    def test_voucher_code(self):

        program = self.program_model.create({
            'voucher_code': 'UNITTEST_VOUCHER',
            'partner_id': self.client.id,
            'voucher_amount': 150,
        })

        self.assertEqual(False, program.automatic)
        self.assertEqual(1, program.max_use)
        self.assertEqual(0, program.nb_use)
        self.assertEqual(False, program.used)
        self.assertEqual(True, program.code_valid)

        self.assertEqual(1, len(program.action_ids))
        self.assertEqual('product_add', program.action_ids.type_action)
        self.assertEqual(-150, program.action_ids.product_add_price)

        program.voucher_amount = 200

        self.assertEqual(1, len(program.action_ids))
        self.assertEqual('product_add', program.action_ids.type_action)
        self.assertEqual(-200, program.action_ids.product_add_price)

        program.action_ids.product_add_price = -100

        self.assertEqual(100, program.voucher_amount)

        program.sale_confirmed()

        self.assertEqual(1, program.max_use)
        self.assertEqual(1, program.nb_use)
        self.assertEqual(True, program.used)

        self.assertEqual(False, program.code_valid)

        # If max_use = 0, there is no limit
        program.max_use = 0
        self.assertEqual(True, program.code_valid)

        program.max_use = 1
        self.assertEqual(False, program.code_valid)

        program.sale_cancelled()
        self.assertEqual(1, program.max_use)
        self.assertEqual(0, program.nb_use)

        self.assertEqual(True, program.code_valid)

        program.expiration_date = date.today() - timedelta(days=1)

        self.assertEqual(False, program.code_valid)

    @post_install(True)
    @at_install(False)
    def test_voucher_negative_total(self):

        program = self.program_model.create({
            'voucher_code': 'UNITTEST_VOUCHER',
            'partner_id': self.client.id,
            'voucher_amount': 150,
        })

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'phototherapist_id': self.phototherapist.id,
            'program_code_ids': [(6, False, [program.id])],
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'price_unit': 100,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        self.assertEqual(100, sale.amount_total)

        sale.apply_discount_programs()
        self.assertEqual(0, sale.amount_total)
        self.assertEqual(-100, sale.order_line[1].price_unit)

        program.action_ids[0].allow_negative_total = True

        sale.apply_discount_programs()
        self.assertEqual(-50, sale.amount_total)
        self.assertEqual(-150, sale.order_line[1].price_unit)

    @post_install(True)
    @at_install(False)
    def test_pricelist_visible_discount_with_code_promo(self):
        code = self.program_model.create({
            'promo_code': 'TEST_PROMO_CODE',
            'action_ids': [(0, False, {
                'type_action': 'change_pricelist',
                'pricelist_id': self.promo_pricelist.id,
            })]
        })
        code.combinable = True

        self.p1.list_price = 100

        sale = self.sale_model.create({
            'partner_id': self.client.id,
            'phototherapist_id': self.phototherapist.id,
            'program_code_ids': [(6, False, [code.id])],
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                    'product_uom_qty': 1,
                    'product_uom': self.ref('product.product_uom_unit'),
                })
            ]
        })

        self.assertEqual(0, sale.order_line.discount)
        self.assertEqual(100, sale.order_line.price_unit)
        self.assertEqual(100, sale.amount_total)

        sale.apply_discount_programs()

        self.assertEqual(10, sale.order_line.discount)
        self.assertEqual(100, sale.order_line.price_unit)
        self.assertEqual(90, sale.amount_total)

        # Automatic program that applied a discount.
        self.program_model.create({
            'program_name': 'Test program discount',
            'action_ids': [(0, False, {
                'type_action': 'product_discount',
                'product_discount_selection': 'most_expensive_no_discount',
                'discount_percent': 20,
            })]
        })

        sale.apply_discount_programs()

        self.assertEqual(30, sale.order_line.discount)
        self.assertEqual(100, sale.order_line.price_unit)
        self.assertEqual(70, sale.amount_total)

        # We remove the code and create an automatic that change the pricelist
        # to test the case where pricelist is applied after the discount.
        sale.program_code_ids = False

        self.program_model.create({
            'program_name': 'Test pricelist program',
            'action_ids': [(0, False, {
                'type_action': 'change_pricelist',
                'pricelist_id': self.promo_pricelist.id,
            })]
        })

        sale.apply_discount_programs()

        self.assertEqual(30, sale.order_line.discount)
        self.assertEqual(100, sale.order_line.price_unit)
        self.assertEqual(70, sale.amount_total)

    @post_install(True)
    @at_install(False)
    def test_product_add_and_pricelist(self):
        self.program_model.create({
            'name': 'Unittest reward product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product_category',
                    'product_category_id': self.product_category.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'product_add',
                    'product_add_id': self.p2.id,
                    'product_add_force_price': True,
                    'product_add_price': 0
                }),
                (0, False, {
                    'type_action': 'change_pricelist',
                    'pricelist_id': self.promo_pricelist.id,
                })
            ]
        })

        self.p1.write({
            'list_price': 150,
            'taxes_id': [(5,)],
        })

        self.p2.write({
            'list_price': 100,
            'taxes_id': [(5,)],
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
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
        self.assertEqual(2, len(sale.order_line))
        self.assertEqual(self.p1, sale.order_line[0].product_id)
        self.assertEqual(150, sale.order_line[0].price_unit)
        # 10% with pricelist
        self.assertEqual(10, sale.order_line[0].discount)
        self.assertEqual(135, sale.order_line[0].price_subtotal)

        self.assertEqual(self.p2, sale.order_line[1].product_id)
        self.assertEqual(0, sale.order_line[1].price_unit)

    @post_install(True)
    @at_install(False)
    def test_and_conditions(self):
        program = self.program_model.create({
            'name': 'Unittest conditions_and program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product',
                    'product_id': self.p1.id,
                }),
                (0, False, {
                    'type_condition': 'product',
                    'product_id': self.p2.id,
                })
            ],
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.client.id,
            'order_line': [
                (0, False, {
                    'product_id': self.p1.id,
                })
            ]
        })

        # Default is OR for conditions
        self.assertTrue(program.is_applicable(sale))

        # Switching to and
        program.conditions_and = True
        self.assertFalse(program.is_applicable(sale))

        # Add the second needed product
        sale.write({
            'order_line': [
                (0, False, {
                    'product_id': self.p2.id,
                })
            ]
        })

        self.assertTrue(program.is_applicable(sale))
