# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDiscountProgramReport(TransactionCase):

    def setUp(self):
        super(TestDiscountProgramReport, self).setUp()

        self.customer = self.env['res.partner'].create({
            'name': 'Test customer',
            'email': 'test@test.com',
        })

        self.env['base.language.install'].create(
            {'lang': 'fr_FR'}).lang_install()

        company = self.env.ref('base.main_company')
        company.partner_id.lang = 'fr_FR'

        self.voucher = self.env['sale.discount.program'].create({
            'partner_id': self.customer.id,
            'voucher_amount': 100.0,
            'voucher_code': 'ABCDEFGHIJK',
            'note_message_for_action': 'Blablabla',
            'type': 'sponsorship_voucher'
        })

    def test_cron_send_email(self):
        self.assertFalse(self.voucher.sent_to_customer)

        cron = self.env.ref(
            'discount_program_report.discount_program_send_mails')
        cron.method_direct_trigger()

        self.assertTrue(self.voucher.sent_to_customer)
