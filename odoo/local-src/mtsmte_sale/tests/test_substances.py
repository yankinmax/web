# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests.common import TransactionCase


class TestProductSubstance(TransactionCase):

    def setUp(self):
        super(TestProductSubstance, self).setUp()

        self.product = self.env.ref('product.service_delivery')
        vals = {
            'name': 'substance',
            'product_ids': self.product,
            'product_uom_id': self.product.uom_id.id,
        }
        self.substance = self.env['product.substance'].create(vals)
