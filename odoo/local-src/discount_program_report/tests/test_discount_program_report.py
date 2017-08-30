# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDiscountProgramReport(TransactionCase):

    def setUp(self):
        super(TestDiscountProgramReport, self).setUp()

        self.env['base.language.install'].create(
            {'lang': 'fr_FR'}).lang_install()

        company = self.env.ref('base.main_company')
        company.partner_id.lang = 'fr_FR'

        self.customer = self.env['res.partner'].create({
            'name': 'Test customer',
            'email': 'test@test.com',
            'lang': 'fr_FR',
        })

        report_config_voucher_fr = self.env.ref(
            'discount_program_report.voucher_config_template_fr')

        report_config_sponsorship_fr = report_config_voucher_fr.copy({
            'type': 'sponsorship_voucher'
        })

        report_config_sponsorship_fr.active = True

        program = self.env['sale.discount.program']

        self.discount = program.create({
            'program_name': 'Test discount program',
            'type': 'discount_program',
        })

        self.promo_code = program.create({
            'promo_code': 'Test promo code',
            'type': 'promo_code'
        })

        self.voucher = program.with_context(program_voucher=True).create({
            'partner_id': self.customer.id,
            'voucher_amount': 100.0,
            'note_message_for_action': 'Blablabla',
            'type': 'voucher'
        })

        self.sponsorship_voucher = program.with_context(
            program_voucher=True).create({
                'partner_id': self.customer.id,
                'voucher_amount': 100.0,
                'note_message_for_action': 'Blablabla',
                'type': 'sponsorship_voucher'
            })

        self.gift_voucher = program.with_context(program_voucher=True).create({
            'voucher_amount': 100.0,
            'note_message_for_action': 'Blablabla',
            'type': 'gift_voucher'
        })

    def test_cron_send_email(self):
        self.assertFalse(self.discount.sent_to_customer)
        self.assertFalse(self.promo_code.sent_to_customer)
        self.assertFalse(self.voucher.sent_to_customer)
        self.assertFalse(self.sponsorship_voucher.sent_to_customer)
        self.assertFalse(self.gift_voucher.sent_to_customer)

        self.assertFalse(self.discount.is_printable)
        self.assertFalse(self.promo_code.is_printable)
        self.assertTrue(self.voucher.is_printable)
        self.assertTrue(self.sponsorship_voucher.is_printable)
        self.assertFalse(self.gift_voucher.is_printable)

        self.env['sale.discount.program']._cron_send_vouchers_to_customers()

        self.assertFalse(self.discount.sent_to_customer)
        self.assertFalse(self.promo_code.sent_to_customer)
        self.assertTrue(self.voucher.sent_to_customer)
        self.assertTrue(self.sponsorship_voucher.sent_to_customer)
        self.assertFalse(self.gift_voucher.sent_to_customer)
