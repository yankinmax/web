# -*- coding: utf-8 -*-
from odoo.tests import common


class TestSamplesPropagation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSamplesPropagation, cls).setUpClass()
        cls.any_customer = cls.env['res.partner'].search([
            ('customer', '=', True),
        ], limit=1)
        cls.template_default = cls.env.ref(
            'website_quote.website_quote_template_default')
        cls.product_3 = cls.env.ref('product.product_product_3')
        cls.product_4 = cls.env.ref('product.product_product_4')
        cls.template_default.write({
            'quote_line': [
                (0, 0, {
                    'product_id': cls.product_3.id,
                    'name': 'Sample Text',
                    'product_uom_qty': 20.,
                    'price_unit': 123.,
                    'product_uom_id': cls.product_3.id,
                    'tested_sample': 'Sample3',
                }),
                (0, 0, {
                    'product_id': cls.product_4.id,
                    'name': 'Sample Text',
                    'product_uom_qty': 20.,
                    'price_unit': 123.,
                    'product_uom_id': cls.product_4.id,
                    'tested_sample': 'Sample4',
                }),
            ],
        })

    def test_tested_samples_propagation(self):
        order = self.env['sale.order'].create({
            'partner_id': self.any_customer.id,
            'template_id': self.template_default.id,
        })
        self.assertFalse(order.order_line)
        order.onchange_template_id()
        self.assertTrue(order.order_line)
        product_3_line = order.order_line.filtered(
            lambda ol: ol.product_id == self.product_3)
        product_4_line = order.order_line.filtered(
            lambda ol: ol.product_id == self.product_4)
        self.assertEqual(product_3_line.tested_sample, 'Sample3')
        self.assertEqual(product_4_line.tested_sample, 'Sample4')
