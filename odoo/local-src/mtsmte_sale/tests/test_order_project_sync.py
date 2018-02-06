# -*- coding: utf-8 -*-
from odoo.tests.common import SavepointCase


class TestOrderProjectSync(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestOrderProjectSync, cls).setUpClass()
        cls.uom = cls.env['product.uom'].create({
            'name': 'dB',
            'category_id': cls.env.ref('product.product_uom_categ_kgm').id,
            'active': True,
        })
        cls.substance = cls.env['product.substance'].create({
            'name': '13,37-Trotylline',
            'product_uom_id': cls.uom.id,
        })
        cls.products = cls.env['product.product']
        for i in range(1, 6):
            cls.products += cls.products.create({
                'name': 'Chemical %d' % i,
                'chemistry': 'chem',
                # these values are MANDATORY to make the whole thing work
                'type': 'service',
                'track_service': 'task',
                # ---
                'product_substance_line_ids': [
                    (0, 0, {
                        'product_substance_id': cls.substance.id,
                    }),
                ]
            })
        cls.consu_prod = cls.env['product.product'].create({
            'name': 'CONSUMABLE',
            'type': 'consu',
        })
        cls.customer = cls.env['res.partner'].search([
            ('customer', '=', True),
        ], limit=1)
        cls.order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'analyze_sample': '<b>Foo</b>',
            'client_order_ref': '#REF',
            'order_line': [
                (0, 0, {'product_id': cls.products[0].id}),
                (0, 0, {'product_id': cls.products[1].id}),
                (0, 0, {'product_id': cls.products[2].id}),
                (0, 0, {'product_id': cls.products[3].id}),
                (0, 0, {'product_id': cls.products[4].id}),
                (0, 0, {'product_id': cls.consu_prod.id}),
            ],
        })
        for line in cls.order.order_line:
            line.onchange_product_id()

    def test_order_project_update(self):
        self.assertEqual(self.order.state, 'draft')
        self.assertFalse(self.order.project_project_id)
        self.order.with_context(skip_task_sync=True).action_confirm()
        self.assertEqual(self.order.state, 'sale')
        # `sale_project_fixed_price_task_completed_invoicing`
        # creates a project only when an order is confirmed
        self.assertTrue(self.order.project_project_id)
        self.assertEqual(
            self.order.analyze_sample,
            self.order.project_project_id.analyze_sample)
        self.assertEqual(
            self.order.client_order_ref,
            self.order.project_project_id.client_order_ref)

    def test_order_line_is_procurement_task(self):
        for line in self.order.order_line:
            if line.product_id.type == 'consu':
                self.assertFalse(line._is_procurement_task())
            else:
                self.assertTrue(line._is_procurement_task())

    def test_order_line_task_get(self):
        self.order.with_context(
            tracking_disable=True, skip_task_sync=True).action_confirm()
        for line in self.order.order_line:
            if line._is_procurement_task():
                self.assertTrue(line.get_line_task())

    def test_order_line_task_values(self):
        line = self.order.order_line[0]
        self.assertDictEqual(line._get_task_values(), {
            'tested_sample': False
        })
        line.tested_sample = 'TESTED'
        self.assertDictEqual(line._get_task_values(), {
            'tested_sample': 'TESTED'
        })
        # product values must be reflected on task values too
        product = line.product_id
        prod_vals = {
            'test_parameters': '<h1>Parameters</h1>',
            'duration': '<h1>Duration</h1>',
            'nb_shocks': '<h1>Shocks</h1>',
            'results': '<h1>Results</h1>',
        }
        product.write(prod_vals)
        task_vals = line._get_task_values()
        for k, v in prod_vals.items():
            self.assertEqual(task_vals[k], v)

    def _get_service_line(self):
        # sorting of order lines is not granted to match our setup order.
        # Let's filter them.
        return self.order.order_line.filtered(
            lambda x: x.name != 'CONSUMABLE')[0]

    def test_order_line_task_measure_values(self):
        self.order.with_context(
            tracking_disable=True, skip_task_sync=True).action_confirm()
        line = self._get_service_line()
        task = line.get_line_task()
        values = line._get_task_measures_values(task)
        self.assertTrue(isinstance(values, list))
        self.assertTrue(isinstance(values[0], tuple))
        self.assertDictEqual(values[0][-1], {
            'product_substance_id': line.product_substance_ids[0].id,
            'task_id': task.id
        })

    def test_order_line_update_task_values(self):
        line = self._get_service_line()
        self.order.with_context(tracking_disable=True).action_confirm()
        task = line.get_line_task()
        measures = task.product_substance_measure_ids
        self.assertEqual(
            measures[0].product_substance_id,
            line.product_substance_ids[0])
        # TODO: test update of substance on the line does not update task
