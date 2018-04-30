# -*- coding: utf-8 -*-
# Copyright (C) 2018 by Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestDeliveryslipHelper(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestDeliveryslipHelper, cls).setUpClass()
        cls.helper = cls.env['stock.picking.report_deliveryslip_helper']
        cls.customer = cls.env['res.partner'].search([
            ('customer', '=', True),
        ], limit=1)
        cls.products = cls.env['product.product']
        for i in range(3):
            cls.products += cls.env['product.template'].create({
                'name': 'Sample product {}'.format(i),
                'type': 'product',
            }).product_variant_ids[0]

        # Sales orders
        cls.saleorder1 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'picking_policy': 'direct',
            'order_line': [
                # Sample product 1 related SOL-s
                (0, 0, {
                    'product_id': cls.products[0].id,
                    'product_uom_qty': 10.,
                }),
                (0, 0, {
                    'product_id': cls.products[0].id,
                    'product_uom_qty': 40.,
                }),

                # Sample product 2 related SOL-s
                (0, 0, {
                    'product_id': cls.products[1].id,
                    'product_uom_qty': 20.,
                }),

                # Sample product 3 related SOL-s
                (0, 0, {
                    'product_id': cls.products[2].id,
                    'product_uom_qty': 30.,
                }),
                # this one should not affect ordered qty, since it has a route
                (0, 0, {
                    'product_id': cls.products[2].id,
                    'product_uom_qty': 50.,
                    'route_id': cls.env.ref('stock.route_warehouse0_mto').id,
                })
            ],
        })
        # For the sake of better grip of what is going on, all `qty`-s
        # on `sale.order.lines` just have been multiplied by 10.
        cls.saleorder2 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'picking_policy': 'direct',
            'order_line': [
                # Sample product 1 related SOL-s
                (0, 0, {
                    'product_id': cls.products[0].id,
                    'product_uom_qty': 100.,
                }),
                (0, 0, {
                    'product_id': cls.products[0].id,
                    'product_uom_qty': 400.,
                }),

                # Sample product 2 related SOL-s
                (0, 0, {
                    'product_id': cls.products[1].id,
                    'product_uom_qty': 200.,
                }),

                # Sample product 3 related SOL-s
                (0, 0, {
                    'product_id': cls.products[2].id,
                    'product_uom_qty': 300.,
                }),
                # this one should not affect ordered qty, since it has a route
                (0, 0, {
                    'product_id': cls.products[2].id,
                    'product_uom_qty': 500.,
                    'route_id': cls.env.ref('stock.route_warehouse0_mto').id,
                })
            ],
        })
        # it's here to distinct related pack ops later
        cls.fake_picking_type = cls.env['stock.picking.type'].create({
            'name': 'Fake procurements picking type',
            'sequence_id': cls.env.ref('stock.seq_picking_internal').id,
            'code': 'internal',
        })

    def _prepare_pack_operation_ids(self, saleorder):
        fake_procurement = self.env['stock.picking'].create({
            'picking_type_id': self.fake_picking_type.id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.env.ref(
                'stock.stock_location_suppliers').id,  # yolo, whatever
            'move_lines': [
                (0, 0, {
                    'name': 'who cares?',
                    'product_id': self.products[1].id,
                    'product_uom_qty': 20.,
                    'product_uom': self.env.ref('product.product_uom_unit').id,
                }),
            ],
        })

        saleorder.action_confirm()

        # point a fake procurement picking to a given SO
        fake_procurement.group_id = saleorder.procurement_group_id
        fake_procurement.action_confirm()

        pickings = saleorder.picking_ids
        pickings.force_assign()
        packops = pickings.mapped('pack_operation_product_ids')

        # `stock.pack.operation`-s of a real SO outgoing picking
        self.pack_out_1 = packops.filtered(
            lambda x: x.product_id == self.products[0]
            and x.picking_id.picking_type_id.id != self.fake_picking_type.id)
        self.pack_out_2 = packops.filtered(
            lambda x: x.product_id == self.products[1]
            and x.picking_id.picking_type_id.id != self.fake_picking_type.id)
        self.pack_out_3 = packops.filtered(
            lambda x: x.product_id == self.products[2]
            and x.picking_id.picking_type_id.id != self.fake_picking_type.id)

        # `stock.pack.operation` of a fake procurement
        self.pack_in = packops.filtered(
            lambda x: x.product_id == self.products[1]
            and x.picking_id.picking_type_id.id == self.fake_picking_type.id)

    def test_ordered_qty_calc_so1(self):
        """Healthcheck of `_get_ordered_qty`"""
        # This product has two order lines inside `self.saleorder1`,
        # one w/ 10.0 of it ordered, and another w/ 40.0,
        # so we're expecting 10.0 + 40.0 = 50.0 unit(s).
        self._prepare_pack_operation_ids(self.saleorder1)
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_1), '50.0')
        # This product is holding a single SOL
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_2), '20.0')
        # This product has two SOL-s, but only one
        # of them should affect the result
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_3), '30.0')
        # Finally, this is a fake procurement's `stock.pack.operation`
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_in), '20.0')

    def test_ordered_qty_calc_so2(self):
        """Same as above, but w/ a different sales order."""
        self._prepare_pack_operation_ids(self.saleorder2)
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_1), '500.0')
        # This product is holding a single SOL
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_2), '200.0')
        # This product has two SOL-s, but only one
        # of them should affect the result
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_out_3), '300.0')
        # Finally, this is a fake procurement's `stock.pack.operation`
        self.assertEqual(
            self.helper._get_ordered_qty(self.pack_in), '200.0')

    def test_ordered_qty_prettify(self):
        # prepare pack operation with 50 (10+40) ordered elements
        self._prepare_pack_operation_ids(self.saleorder1)
        # by default prettify=True so we expect receive string value
        value = self.helper._get_ordered_qty(self.pack_out_1)
        self.assertIsInstance(value, str)
        self.assertEqual(value, '50.0')
        # when prettify=False we expect receive float value
        value = self.helper._get_ordered_qty(self.pack_out_1, prettify=False)
        self.assertIsInstance(value, float)
        self.assertEqual(value, 50.0)

    def test_balance_to_deliver_calc(self):
        self.saleorder1.action_confirm()
        pickings = self.saleorder1.picking_ids
        pickings.force_assign()
        self._prepare_pack_operation_ids(self.saleorder1)

        # Happenings on pickings to `Customers` location
        # also affects another picking, tied to the same SO as well,
        # (the latter shouldn't affect balance to deliver value)
        for picking in pickings:
            for operation_product in picking.pack_operation_product_ids:
                if operation_product == self.pack_out_1:
                    operation_product.write({'qty_done': 2})
                if operation_product == self.pack_out_2:
                    operation_product.write({'qty_done': 4})
                if operation_product == self.pack_out_3:
                    operation_product.write({'qty_done': 6})
        wiz_act = pickings.do_new_transfer()
        wiz = self.env[wiz_act['res_model']].browse(wiz_act['res_id'])
        wiz.process()

        # for pack_out_1 ordered = 50 done = 2 expected 48 (50-2)
        self.assertEqual(
            self.helper._get_balance_to_deliver(self.pack_out_1), '48.0')
        # for pack_out_2 ordered = 20 done = 4 expected 16 (20-4)
        self.assertEqual(
            self.helper._get_balance_to_deliver(self.pack_out_2), '16.0')
        # for pack_out_3 ordered = 30 done = 6 expected 24 (30-6)
        self.assertEqual(
            self.helper._get_balance_to_deliver(self.pack_out_3), '24.0')
