# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests.common import TransactionCase


class TestProductSubstanceMeasure(TransactionCase):

    def setUp(self):
        super(TestProductSubstanceMeasure, self).setUp()

        self.product = self.env.ref('product.service_delivery')
        self.substance = self.env['product.substance'].create({
            'name': 'substance',
            'product_ids': self.product,
            'product_uom_id': self.product.uom_id.id,
        })
        self.task = self.env.ref('project.project_task_data_0')

        self.measure = self.env['product.substance.measure'].create({
            'product_substance_id': self.substance.id,
            'task_id': self.task.id,
        })

    def _test_case_measure(self, has_limit_min, has_limit_max, legal_limit_min,
                           legal_limit_max, bdl, measure):
        self.substance.write({
            'has_limit_min': has_limit_min,
            'has_limit_max': has_limit_max,
            'legal_limit_min': legal_limit_min,
            'legal_limit_max': legal_limit_max,
        })
        self.measure.write({
            'measure': measure,
            'bdl': bdl
        })
        self.measure._compute_conformity()
        return self.measure.conformity

    def test__compute_conformity(self):
        self.assertEqual(
            self._test_case_measure(True, True, 1, 10, False, 5),
            "conform"
        )
        self.assertEqual(
            self._test_case_measure(True, False, 1, 10, False, 5),
            "conform"
        )
        self.assertEqual(
            self._test_case_measure(True, True, 1, 10, True, 15),
            "conform"
        )
        self.assertEqual(
            self._test_case_measure(False, False, 1, 10, False, 5),
            "conform"
        )
        self.assertEqual(
            self._test_case_measure(False, False, 1, 10, False, 15),
            "warning"
        )
        self.assertEqual(
            self._test_case_measure(True, True, 1, 10, False, 0),
            "not_conform"
        )
        self.assertEqual(
            self._test_case_measure(True, True, 1, 10, False, 12),
            "not_conform"
        )
        self.assertEqual(
            self._test_case_measure(True, False, 1, 10, False, 0),
            "not_conform"
        )
        self.assertEqual(
            self._test_case_measure(False, True, 1, 10, False, 12),
            "not_conform"
        )
