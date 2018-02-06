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
            'name': 'TNT',
            'product_uom_id': cls.uom.id,
        })
        cls.products = cls.env['product.product']
        for i in range(1, 3):
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
                (0, 0, {'product_id': cls.products[0].id, 'name': 'A'}),
                (0, 0, {'product_id': cls.consu_prod.id, 'name': 'Z'}),
            ],
        })
        cls.service_line = [
            x for x in cls.order.order_line if x.name == 'A'][0]
        for line in cls.order.order_line:
            line.onchange_product_id()

    def test_order_project_update(self):
        self.assertEqual(self.order.state, 'draft')
        self.assertFalse(self.order.project_project_id)
        self.order.with_context(
            tracking_disable=True, skip_task_sync=True).action_confirm()
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

    def _get_task(self, line):
        return self.env['project.task'].search(
            [('sale_line_id', '=', line.id)], limit=1)

    def test_task_line_values(self):
        self.order.with_context(tracking_disable=True).action_confirm()
        line = self.service_line
        task = self._get_task(line)

        self.assertDictEqual(task._get_values_from_so_line(), {
            'tested_sample': False
        })
        line.tested_sample = 'TESTED'
        self.assertDictEqual(task._get_values_from_so_line(), {
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
        task_vals = task._get_values_from_so_line()
        for k, v in prod_vals.items():
            self.assertEqual(task_vals[k], v)

    def test_task_line_measure_values(self):
        self.order.with_context(tracking_disable=True).action_confirm()
        line = self.service_line
        task = self._get_task(line)
        values = task._get_task_measures_from_so_line()
        self.assertTrue(isinstance(values, list))
        self.assertTrue(isinstance(values[0], tuple))
        self.assertDictEqual(values[0][-1], {
            'product_substance_id': line.product_substance_ids[0].id,
            'task_id': task.id
        })

    def test_order_line_update_task_values(self):
        self.order.with_context(tracking_disable=True).action_confirm()
        line = self.service_line
        task = self._get_task(line)
        measures = task.product_substance_measure_ids
        self.assertEqual(
            measures[0].product_substance_id,
            line.product_substance_ids[0])

    def _get_wiz(self):
        return self.env['wiz.so.sync.task'].with_context(
            active_id=self.order.id).create({})

    def test_force_sync_via_wizard(self):
        line = self.service_line
        line.tested_sample = 'TESTED'
        self.order.with_context(tracking_disable=True).action_confirm()
        task = self._get_task(line)
        self.assertEqual(task.tested_sample, 'TESTED')
        line.tested_sample = 'FOO'
        # no change on the task
        self.assertEqual(task.tested_sample, 'TESTED')
        wiz = self._get_wiz()
        self.assertEqual(len(wiz.so_line_ids), 1)
        self.assertEqual(wiz.so_line_ids[0], line)
        self.assertEqual(len(wiz._get_tasks()), 1)
        self.assertEqual(wiz._get_tasks()[0], task)
        wiz.action_sync()
        self.assertEqual(task.tested_sample, 'FOO')
