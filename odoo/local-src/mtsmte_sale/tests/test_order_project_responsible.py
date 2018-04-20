# -*- coding: utf-8 -*-
# Copyright (C) 2018 by Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestOrderProjectResponsible(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestOrderProjectResponsible, cls).setUpClass()

        # responsible users
        model_users = cls.env['res.users'].with_context({
            'no_reset_password': True,
            'tracking_disable': True,
        })
        cls.product_responsibles = model_users
        cls.category_responsibles = model_users
        for i in range(3):
            # Responsible #0 is a manager
            cls.product_responsibles |= model_users.create({
                'name': 'Product responsible {}'.format(i),
                'login': 'product-responsible{}'.format(i),
                'email': 'productresponsible{}@example.com'.format(i),
            })
            cls.category_responsibles |= model_users.create({
                'name': 'Category responsible {}'.format(i),
                'login': 'category-responsible{}'.format(i),
                'email': 'categoryresponsible{}@example.com'.format(i),
            })

        sample_product_service = cls.env.ref('product.service_order_01')
        sample_product_service.track_service = 'task'

        cls.products = cls.env['product.product']
        # This one has no manager, so the resulting responsible
        cls.products |= sample_product_service.copy({
            'manager_id': False,
            'responsible_1_id': cls.product_responsibles[1].id,
            'responsible_2_id': cls.product_responsibles[2].id,
        })
        # `responsible_2_id` isn't set, inherits from category
        cls.products |= sample_product_service.copy({
            'manager_id': cls.product_responsibles[0].id,
            'responsible_1_id': cls.product_responsibles[1].id,
            'responsible_2_id': False,
        })
        # this one has no directly assigned responsibles -
        # will use those set on categories
        cls.products |= sample_product_service.copy({
            'manager_id': False,
            'responsible_1_id': False,
            'responsible_2_id': False,
        })
        cls.category_services = cls.env.ref('product.product_category_3')
        cls.category_services.write({
            'manager_id': cls.category_responsibles[0].id,
            'responsible_1_id': cls.category_responsibles[1].id,
            'responsible_2_id': cls.category_responsibles[2].id,
        })

        # Sample customer
        cls.any_customer = cls.env['res.partner'].search([
            ('customer', '=', True),
        ], limit=1)

    def test_sale_order_responsible(self):
        order = self.env['sale.order'].create({
            'partner_id': self.any_customer.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.products[0].id,
                }),
                (0, 0, {
                    'product_id': self.products[1].id,
                }),
                (0, 0, {
                    'product_id': self.products[2].id,
                }),
            ],
        })
        order.action_confirm()
        project = order.project_project_id
        self.assertTrue(project)

        # project responsible is supposed to be somewhat random by spec,
        # shouldn't be tested that hard.
        # ...in fact, this should be equal to `self.product_responsibles[1]`,
        # since first order line we're checking sells `self.product_service_1`,
        # which has no `manager`, but has directly assigned `responsible_1_id`
        # instead, and that is `self.product_responsibles[1]`.
        self.assertIn(
            project.user_id,
            (self.product_responsibles | self.category_responsibles))
        task_service_1 = project.task_ids.filtered(
            lambda t: t.sale_line_id.product_id == self.products[0])
        task_service_2 = project.task_ids.filtered(
            lambda t: t.sale_line_id.product_id == self.products[1])
        task_service_3 = project.task_ids.filtered(
            lambda t: t.sale_line_id.product_id == self.products[2])
        self.assertEqual(task_service_1.user_id, self.product_responsibles[2])
        self.assertEqual(task_service_2.user_id, self.category_responsibles[2])
        self.assertEqual(task_service_3.user_id, self.category_responsibles[2])
