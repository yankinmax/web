# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import fields

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, post_install, at_install


class TestProgram(TransactionCase):

    def setUp(self):
        super(TestProgram, self).setUp()

        self.env['sale.config.settings'].create({
            'group_discount_per_so_line': 1,
        }).execute()

        self.invoice_model = self.env['account.invoice']
        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.program_model = self.env['sale.discount.program']
        self.sale_model = self.env['sale.order']
        self.sponsor_model = self.env['partner.sponsor']
        self.settings_model = self.env['sale.config.settings']
        self.pricelist_model = self.env['product.pricelist']
        self.account_model = self.env['account.account']
        self.mail_mail_model = self.env['mail.mail']

        for sponsor in self.sponsor_model.search([]):
            sponsor.unlink()

        for program in self.program_model.search([]):
            program.unlink()

        self.sponsor_pricelist = self.env.ref(
            'specific_discount_program.pricelist_sponsorship'
        )

        self.promo_pricelist = self.pricelist_model.create({
            'name': 'Unittest code promo',
            'discount_policy': 'with_discount',
            'item_ids': [(0, False, {
                'applied_on': '3_global',
                'compute_price': 'percentage',
                'percent_price': 10,
            })]
        })

        self.promo_pricelist_without_discount = self.pricelist_model.create({
            'name': 'Unittest code promo (without discount)',
            'discount_policy': 'without_discount',
            'item_ids': [(0, False, {
                'applied_on': '3_global',
                'compute_price': 'percentage',
                'percent_price': 10,
            })]
        })

        self.phototherapist = self.env['res.company.phototherapist'].create({
            'name': 'Unittest phototherapist',
            'company_id': self.env.user.company_id.id
        })

        self.p1 = self.product_model.create({'name': 'Unittest P1'})

        self.partner1 = self.partner_model.create({
            'name': 'Sponsor partner',
            'city': 'Test city',
            'company_type': 'agency_customer',
        })

        self.assertEqual(0, self.sponsor_model.search_count([]))

        self.sale_sponsor = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1
            })]
        })
        self.sale_sponsor.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()
        created_voucher = self.program_model.search([
            ('partner_id', '=', self.partner1.id)
        ])
        created_voucher.unlink()

        # Create Sale Journal
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Sale Journal - Test',
            'code': 'STSJ',
            'type': 'sale',
            'company_id': self.env.user.company_id.id
        })

    @post_install(True)
    @at_install(False)
    def test_vouchers(self):
        sponsor = self.sponsor_model.search([])
        self.assertEqual(1, len(sponsor))
        self.assertEqual(
            'Sponsor partner - Test city', sponsor[0].name
        )

        partner2 = self.partner_model.create({
            'name': 'Other partner',
            'sponsor_id': sponsor.id,
            'company_type': 'agency_customer',
        })

        # Simulate sponsor program by setting pricelist_id to sponsor pricelist
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner2.id,
            'pricelist_id': self.sponsor_pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
            })]
        })
        sale.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        self.assertEqual(2, self.program_model.search_count([
            ('voucher_code', '!=', False)
        ]))

        # One voucher for the client
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        # One voucher for the sponsor
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

        # Simulate that sponsor used his voucher but the client does not
        sponsor_voucher = self.program_model.search([
            ('partner_id', '=', self.partner1.id)
        ])
        sponsor_voucher.nb_use = 1

        # Cancel the sale.order
        sale.action_cancel()

        # Unused voucher has been deleted
        self.assertEqual(1, self.program_model.search_count([
            ('voucher_code', '!=', False)
        ]))

        self.assertEqual(0, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

        # Another sale for partner 2 will create only one voucher
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner2.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
            })]
        })
        sale.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        self.assertEqual(2, self.program_model.search_count([
            ('voucher_code', '!=', False)
        ]))

        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

    @post_install(True)
    @at_install(False)
    def test_voucher_cancel_both(self):
        sponsor = self.sponsor_model.search([])
        partner2 = self.partner_model.create({
            'name': 'Other partner',
            'sponsor_id': sponsor.id,
            'company_type': 'agency_customer',
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner2.id,
            'pricelist_id': self.sponsor_pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
            })]
        })
        sale.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        self.assertEqual(2, self.program_model.search_count([
            ('voucher_code', '!=', False)
        ]))

        # One voucher for the client
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        # One voucher for the sponsor
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

        # Cancel the sale.order
        sale.action_cancel()

        # Unused voucher has been deleted
        self.assertEqual(0, self.program_model.search_count([
            ('voucher_code', '!=', False)
        ]))

    @post_install(True)
    @at_install(False)
    def test_sponsor_became_invalid(self):
        sponsor = self.sponsor_model.search([])
        self.assertEqual(1, len(sponsor))

        partner2 = self.partner_model.create({
            'name': 'Other partner',
            'sponsor_id': sponsor.id,
            'company_type': 'agency_customer',
        })

        # Simulate sponsor program by setting pricelist_id to sponsor pricelist
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner2.id,
            'pricelist_id': self.sponsor_pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1
            })]
        })

        # Sponsor sale is cancelled so this partner can not be a sponsor
        # anymore
        self.sale_sponsor.action_cancel()

        sale.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        # Voucher for client
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        # No voucher on sponsor partner created.
        self.assertEqual(0, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

    @post_install(True)
    @at_install(False)
    def test_voucher_limit(self):
        icp = self.env['ir.config_parameter']
        icp.set_param('voucher_max_count', 2)

        v1 = self.program_model.create({
            'voucher_code': 'UNITTEST_V1',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        v2 = self.program_model.create({
            'voucher_code': 'UNITTEST_V2',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        v3 = self.program_model.create({
            'voucher_code': 'UNITTEST_V3',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'program_code_ids': [(6, False, [v1.id, v2.id, v3.id])],
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
                'price_unit': 500,
            })]
        })

        with self.assertRaises(UserError):
            sale.apply_discount_programs()

        icp.set_param('voucher_max_count', 3)
        sale.apply_discount_programs()

        self.assertEqual(3, len(sale.applied_program_ids))

    @post_install(True)
    @at_install(False)
    def test_promo_limit(self):
        v1 = self.program_model.create({
            'promo_code': 'UNITTEST_V1',
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        v2 = self.program_model.create({
            'promo_code': 'UNITTEST_V2',
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'program_code_ids': [(6, False, [v1.id, v2.id])],
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
                'price_unit': 500,
            })]
        })

        with self.assertRaises(UserError):
            sale.apply_discount_programs()

        sale.write({
            'program_code_ids': [(6, False, [v1.id])],
        })
        sale.apply_discount_programs()

        self.assertEqual(1, len(sale.applied_program_ids))

    @post_install(True)
    @at_install(False)
    def test_voucher_and_promo_limit(self):
        icp = self.env['ir.config_parameter']
        icp.set_param('voucher_max_count', 10)

        v1 = self.program_model.create({
            'promo_code': 'UNITTEST_V1',
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        v2 = self.program_model.create({
            'voucher_code': 'UNITTEST_V2',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
            'note_message_for_action': 'Unittest message',
        })

        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'program_code_ids': [(6, False, [v1.id, v2.id])],
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
                'price_unit': 500,
            })]
        })

        with self.assertRaises(UserError):
            sale.apply_discount_programs()

    @post_install(True)
    @at_install(False)
    def test_discount_manually_percent_max(self):
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
        })

        with self.assertRaises(ValidationError):
            # Default discount manually percent maximum is 10.0
            sale.discount_manually_percent = 15.23

        # Fix discount manually percent maximum to 15.23
        settings = self.settings_model.create({
            'discount_manually_percent_max': 15.23
        })
        settings.execute()
        sale.discount_manually_percent = 15.23

        with self.assertRaises(ValidationError):
            # Default discount manually percent maximum is now 15.23
            sale.discount_manually_percent = 20.

    @post_install(True)
    @at_install(False)
    def test_discount_manually_percent(self):
        # Create a program with gift product
        product_to_add = self.product_model.create({
            'name': 'Unittest gift product',
            'list_price': 100,
            'uom_id': self.ref('product.product_uom_unit'),
        })
        self.program_model.create({
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
                    'note_message': 'Unittest message',
                })
            ]
        })

        # Create sale order
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
                'price_unit': 500,
            })]
        })
        sale.apply_discount_programs()
        # Without manually discount, discount for lines is 0
        self.assertEqual(sale.order_line[0].discount, 0.)
        self.assertEqual(sale.order_line[1].discount, 0.)

        sale.discount_manually_percent = 10.
        sale.apply_discount_programs()
        # With manually discount, discount for "normal" lines is 10.0
        self.assertEqual(sale.order_line[0].discount, 10.)
        # With manually discount, discount for "program" lines is 0.0
        self.assertEqual(sale.order_line[1].discount, 0.)

        # Check that discount is reset correctly
        sale.discount_manually_percent = 5.
        sale.apply_discount_programs()
        # With manually discount, discount for "normal" lines is 5.0
        self.assertEqual(sale.order_line[0].discount, 5.)
        # With manually discount, discount for "program" lines is 0.0
        self.assertEqual(sale.order_line[1].discount, 0.)

    @post_install(True)
    @at_install(False)
    def test_discount_manually_percent_with_another_discount(self):
        # Create a program with discount on product
        self.program_model.create({
            'name': 'Unittest reward product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product',
                    'product_id': self.p1.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'product_discount',
                    'product_discount_selection': 'most_expensive_no_discount',
                    'discount_percent': 20,
                    'note_message': 'Unittest message',
                })
            ]
        })

        # Create sale order
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1,
                'price_unit': 500,
            })]
        })
        sale.apply_discount_programs()
        # Without manually discount, discount for lines is 20.0 (by program)
        self.assertEqual(sale.order_line[0].discount, 20.)
        self.assertEqual(sale.order_line[0].price_unit, 500)
        self.assertEqual(sale.order_line[0].price_subtotal, 400)

        sale.discount_manually_percent = 10.
        sale.apply_discount_programs()
        # With manually discount, discount for lines is 30.0
        # (by program and manually discount)
        self.assertEqual(sale.order_line[0].discount, 30.)
        self.assertEqual(sale.order_line[0].price_unit, 500)
        self.assertEqual(sale.order_line[0].price_subtotal, 350)

    @post_install(True)
    @at_install(False)
    def test_discount_manually_percent_with_pricelist_discount(self):
        # Create product with list_price (used on pricelist)
        p1 = self.product_model.create({
            'name': 'Unittest P1',
            'list_price': 500,
        })

        # Create a program with pricelist promo
        self.program_model.create({
            'name': 'Unittest reward product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product',
                    'product_id': p1.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'change_pricelist',
                    'pricelist_id': self.promo_pricelist.id,
                    'note_message': 'Unittest message',
                })
            ]
        })

        # Create sale order
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': p1.id,
                'product_uom_qty': 1,
                'price_unit': 40,  # price_unit will be overridden by pricelist
            })]
        })
        sale.apply_discount_programs()
        # Without manually discount, discount for lines is 0.0,
        # but price_unit is compute with 20.0 % discount (by pricelist)
        self.assertEqual(sale.order_line[0].discount, 0.)
        self.assertEqual(sale.order_line[0].price_unit, 450)
        self.assertEqual(sale.order_line[0].price_subtotal, 450)

        sale.discount_manually_percent = 5.
        sale.apply_discount_programs()
        # With manually discount, discount for lines is 5.0,
        # And with price_unit is compute with 20.0 % discount (by pricelist)
        self.assertEqual(sale.order_line[0].discount, 5.)
        self.assertEqual(sale.order_line[0].price_unit, 450)
        self.assertEqual(sale.order_line[0].price_subtotal, 427.5)

    @post_install(True)
    @at_install(False)
    def test_discount_manually_percent_with_pricelist_discount_2(self):
        # Create product with list_price (used on pricelist)
        p1 = self.product_model.create({
            'name': 'Unittest P1',
            'list_price': 500,
        })

        # Create a program with pricelist promo
        self.program_model.create({
            'name': 'Unittest reward product program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'product',
                    'product_id': p1.id,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'change_pricelist',
                    'pricelist_id': self.promo_pricelist_without_discount.id,
                    'note_message': 'Unittest message',
                })
            ]
        })

        # Create sale order
        sale = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': p1.id,
                'product_uom_qty': 1,
                'price_unit': 40,  # price_unit will be overridden by pricelist
            })]
        })
        sale.apply_discount_programs()
        # Without manually discount, discount for lines is 10.0
        self.assertEqual(sale.order_line[0].discount, 10.)
        self.assertEqual(sale.order_line[0].price_unit, 500)
        self.assertEqual(sale.order_line[0].price_subtotal, 450)

        sale.discount_manually_percent = 5.
        sale.apply_discount_programs()
        # With manually discount, discount for lines is 15.0
        self.assertEqual(sale.order_line[0].discount, 15.)
        self.assertEqual(sale.order_line[0].price_unit, 500)
        self.assertEqual(sale.order_line[0].price_subtotal, 425)

    @post_install(True)
    @at_install(False)
    def test_gift_voucher(self):
        # Set two partner
        ordering_partner = self.env.ref('base.partner_demo')
        receiving_partner = ordering_partner.copy()

        # Create gift quotation order
        gift_order = self.sale_model.create({
            'partner_id': ordering_partner.id,
            'order_line': [(0, 0, {
                'product_id': self.env.ref(
                    'specific_discount_program.gift_card').id,
                'quantity': 1,
                'price_unit': 50,
            })],
            'gift_quotation': True,
            'phototherapist_id': self.phototherapist.id,
        })

        # Confirm gift quotation
        gift_order.with_context(
            active_model='sale.order',
            active_ids=[gift_order.id],
            active_id=gift_order,
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        self.assertFalse(gift_order.generated_voucher_ids)

        # Create invoice
        gift_invoice_context = {"active_model": 'sale.order',
                                "active_ids": [gift_order.id],
                                "active_id": gift_order.id}

        payment_wiz = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'all',
        })
        payment_wiz.with_context(gift_invoice_context).create_invoices()
        gift_invoice = gift_order.invoice_ids[0]

        # Validate invoice
        gift_invoice.with_context(gift_invoice_context).invoice_validate()

        self.assertEqual(len(gift_invoice.generated_voucher_ids), 1)
        gift_voucher = gift_invoice.generated_voucher_ids[0]

        self.assertEqual(gift_voucher.voucher_amount, 50.0)
        self.assertFalse(gift_voucher.partner_id)
        self.assertFalse(gift_voucher.used)

        # Create sale order using gift voucher
        reduced_order = self.sale_model.create({
            'partner_id': receiving_partner.id,
            'program_code_ids': [(4, gift_voucher.id, False)],
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'quantity': 1,
                'price_unit': 100,
            })],
            'gift_quotation': False,
            'phototherapist_id': self.phototherapist.id,
        })

        self.assertEqual(reduced_order.state, 'draft')
        self.assertEqual(len(reduced_order.order_line), 1)

        # Apply gift voucher
        reduced_order.apply_discount_programs()
        self.assertEqual(len(reduced_order.order_line), 2)

        # Confirm sale.order
        reduced_order.with_context(
            active_model='sale.order',
            active_ids=[reduced_order.id],
            active_id=reduced_order.id,
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        # TODO : TO BE CHANGED ! THE VOUCHER PRODUCTS MUST BE HAVE TAX INCLUDED
        # Remove automatic taxes
        reduced_order.order_line.write({
            'tax_id': [(5, False, False)]
        })

        self.assertEqual(reduced_order.state, 'sale')
        self.assertEqual(reduced_order.amount_total, 50.0)

    @post_install(True)
    @at_install(False)
    def test_program_from_sale_order_validated(self):
        # Create program based on
        # another order validated between 10 and 19 days
        self.program_model.create({
            'name': 'Unittest another_order_validated program',
            'condition_ids': [
                (0, False, {
                    'type_condition': 'another_order_validated',
                    'sale_order_validated_since': 10,
                    'sale_order_validated_until': 19,
                })
            ],
            'action_ids': [
                (0, False, {
                    'type_action': 'product_discount',
                    'product_discount_selection': 'most_expensive_no_discount',
                    'discount_percent': 10,
                    'note_message': 'Unittest another_order_validated message',
                })
            ]
        })

        # Create partner
        partner = self.partner_model.create({
            'name': 'UNITTEST partner',
            'company_type': 'agency_customer',
        })

        # Create first sale order validated
        sale_validated_1 = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })]
        })
        sale_validated_1.order_line.write({
            'tax_id': [(5, False, False)]
        })
        sale_validated_1.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        # Create second sale order validated
        sale_validated_2 = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 150,
            })]
        })
        sale_validated_2.order_line.write({
            'tax_id': [(5, False, False)]
        })
        sale_validated_2.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        # Create first sale order for test
        sale_for_test_1 = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 200,
            })]
        })
        sale_for_test_1.order_line.write({
            'tax_id': [(5, False, False)]
        })
        sale_for_test_1.apply_discount_programs()
        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        # Create second sale order for test
        sale_for_test_2 = self.sale_model.create({
            'phototherapist_id': self.phototherapist.id,
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id,
                'product_uom_qty': 1,
                'price_unit': 300,
            })]
        })
        sale_for_test_2.order_line.write({
            'tax_id': [(5, False, False)]
        })
        sale_for_test_2.apply_discount_programs()
        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)

        # Define confirmation_date 20 days ago
        # ==> Program is not used
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=20)
        )

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Define confirmation_date 19 days ago
        # ==> Program used on first test order
        # ==> Program match on second validated order
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=19)
        )

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertIn(sale_validated_2,
                      sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 180.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Define confirmation_date 9 days ago
        # ==> Program is not used
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=9)
        )

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Define confirmation_date 10 days ago
        # ==> Program used on first test order
        # ==> Program match on second validated order
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=10)
        )

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertIn(sale_validated_2,
                      sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 180.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Inverse confirmation_date between 2 validated orders
        # ==> Program used on first test order
        # ==> Program match on first validated order
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=10)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertIn(sale_validated_1,
                      sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 180.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Check that the mail message
        # for program alert is missing for first test order
        domain = [
            ('model', '=', 'sale.order'),
            ('res_id', '=', sale_for_test_1.id),
            ('message_type', '=', 'email'),
            ('subject', '=', 'Program alert on %s' % sale_for_test_1.name),
        ]
        self.assertEqual(len(self.mail_mail_model.search(domain)), 0)

        # Cancel first validated order
        # ==> The first test order is now in program alert
        sale_validated_1.action_cancel()
        self.assertTrue(sale_for_test_1.program_alert)
        self.assertEqual(len(self.mail_mail_model.search(domain)), 1)

        # Reset alert on first test order
        # ==> The first test order is not anymore in program alert
        sale_for_test_1.action_reset_alert_program()
        self.assertFalse(sale_for_test_1.program_alert)

        # Re-apply discount programs on tests orders
        # ==> Program is not used now
        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Re-confirm first validated order and
        # ==> Program is not used (because the confirmation date is now)
        sale_validated_1.with_context(
            no_check_payment_rules=True
            # This context used by specific_payment_mode module
            # to ignore check on payment calculator.
            #
            # Normally, we don't need to give this context here,
            # because this module don't depend of specific_payment_mode module.
            #
            # But when travis build all units tests,
            # specific_payment_mode module is installed and
            # the check on payment calculator induce a failed test here.
        ).action_confirm()

        sale_for_test_1.apply_discount_programs()
        sale_for_test_2.apply_discount_programs()

        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        self.assertFalse(sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 300.0)

        # Define confirmation_date 10 days ago
        # AND apply discount program on second test order
        # before the first test order
        # ==> Program used on SECOND test order
        # ==> Program match on second validated order
        sale_validated_1.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=50)
        )
        sale_validated_2.confirmation_date = fields.Datetime.to_string(
            datetime.now() - relativedelta(days=10)
        )

        sale_for_test_2.apply_discount_programs()
        sale_for_test_1.apply_discount_programs()

        self.assertFalse(sale_for_test_1.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_1.program_alert)
        self.assertEqual(sale_for_test_1.amount_total, 200.0)

        self.assertIn(sale_validated_2,
                      sale_for_test_2.sale_order_used_by_program_ids)
        self.assertFalse(sale_for_test_2.program_alert)
        self.assertEqual(sale_for_test_2.amount_total, 270.0)
