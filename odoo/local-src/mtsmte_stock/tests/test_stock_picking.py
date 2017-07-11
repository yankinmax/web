# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import odoo.tests.common as common
from odoo import exceptions


class TestStockPicking(common.TransactionCase):

    def _create_picking(self):
        src_location = self.env.ref('stock.stock_location_stock')
        dest_location = self.env.ref('stock.stock_location_customers')
        return self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
        })

    def setUp(self):
        super(TestStockPicking, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.product1 = self.env.ref('product.product_product_16')
        self.product2 = self.env.ref('product.product_product_17')
        packaging_tpl = self.env['product.template'].create({'name': 'Pallet'})
        self.packaging = self.env['product.packaging'].create({
            'name': 'Pallet',
            'product_tmpl_id': packaging_tpl.id,
        })
        self.picking_a = self._create_picking()
        self.picking_a.state = 'waiting'

    def test_cancel_picking(self):
        with self.assertRaises(exceptions.UserError):
            self.picking_a.action_cancel()
