# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.exceptions import UserError
from openerp.tests.common import TransactionCase


class TestProgram(TransactionCase):

    def setUp(self):
        super(TestProgram, self).setUp()

        self.invoice_model = self.env['account.invoice']
        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.program_model = self.env['sale.discount.program']
        self.sale_model = self.env['sale.order']
        self.sponsor_model = self.env['partner.sponsor']

        for sponsor in self.sponsor_model.search([]):
            sponsor.unlink()

        self.sponsor_pricelist = self.env.ref('scenario.pricelist_sponsorship')
        if not self.sponsor_pricelist:
            self.sponsor_pricelist = self.env['product.pricelist'].create({
                'name': 'Unittest sponsor pricelist',
            })
            self.env['ir.model.data'].create({
                'model': 'product.pricelist',
                'module': 'scenario',
                'name': 'pricelist_sponsorship',
                'res_id': self.sponsor_pricelist.id,
            })

        self.p1 = self.product_model.create({'name': 'Unittest P1'})

        self.partner1 = self.partner_model.create({
            'name': 'Sponsor partner',
            'city': 'Test city',
        })

        self.assertEqual(0, self.sponsor_model.search_count([]))

        self.sale_sponsor = self.sale_model.create({
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1
            })]
        })
        self.sale_sponsor.action_confirm()

    def test_vouchers(self):
        sponsor = self.sponsor_model.search([])
        self.assertEqual(1, len(sponsor))
        self.assertEqual(
            'Sponsor partner - Test city', sponsor[0].name
        )

        partner2 = self.partner_model.create({
            'name': 'Other partner',
            'sponsor_id': sponsor.id,
        })

        # Simulate sponsor program by setting pricelist_id to sponsor pricelist
        sale = self.sale_model.create({
            'partner_id': partner2.id,
            'pricelist_id': self.sponsor_pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1
            })]
        })
        sale.action_confirm()

        invoice_id = sale.action_invoice_create()
        invoice = self.invoice_model.browse(invoice_id)

        self.assertEqual(self.partner1, invoice.sponsor_id.partner_id)

        invoice.confirm_paid()

        # One voucher for the client
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        # One voucher for the sponsor
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

    def test_sponsor_became_invalid(self):
        sponsor = self.sponsor_model.search([])
        self.assertEqual(1, len(sponsor))

        partner2 = self.partner_model.create({
            'name': 'Other partner',
            'sponsor_id': sponsor.id,
        })

        # Simulate sponsor program by setting pricelist_id to sponsor pricelist
        sale = self.sale_model.create({
            'partner_id': partner2.id,
            'pricelist_id': self.sponsor_pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.p1.id, 'product_uom_qty': 1
            })]
        })
        sale.action_confirm()

        invoice_id = sale.action_invoice_create()
        invoice = self.invoice_model.browse(invoice_id)

        self.assertEqual(self.partner1, invoice.sponsor_id.partner_id)

        # Sponsor sale is cancelled so this partner can not be a sponsor
        # anymore
        self.sale_sponsor.action_cancel()

        invoice.confirm_paid()

        # Voucher for client
        self.assertEqual(1, self.program_model.search_count([
            ('partner_id', '=', partner2.id)
        ]))

        # No voucher on sponsor partner created.
        self.assertEqual(0, self.program_model.search_count([
            ('partner_id', '=', self.partner1.id)
        ]))

    def test_voucher_limit(self):
        icp = self.env['ir.config_parameter']
        icp.set_param('voucher_max_count', 2)

        v1 = self.program_model.create({
            'voucher_code': 'UNITTEST_V1',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
        })

        v2 = self.program_model.create({
            'voucher_code': 'UNITTEST_V2',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
        })

        v3 = self.program_model.create({
            'voucher_code': 'UNITTEST_V3',
            'voucher_amount': 100,
            'partner_id': self.partner1.id,
        })

        sale = self.sale_model.create({
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
