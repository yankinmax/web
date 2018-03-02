# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.addons.stock.tests.common import TestStockCommon


class TestStockScraping(TestStockCommon):

    def setUp(self):
        super(TestStockScraping, self).setUp()
        self._prepare_move_chain()

    def _prepare_move_chain(self):
        """Create a small chain of moves.

        2 pickings: IN/OUT
        1 move each: move IN -> move_dest_id -> move OUT
        """
        self.picking_in = self.PickingObj.create({
            'partner_id': self.partner_delta_id,
            'picking_type_id': self.picking_type_in,
            'location_id': self.supplier_location,
            'location_dest_id': self.stock_location,
        })
        self.moveA_in = self.MoveObj.create({
            'name': self.productA.name,
            'product_id': self.productA.id,
            'product_uom_qty': 100.0,
            'product_uom': self.productA.uom_id.id,
            'picking_id': self.picking_in.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.stock_location,
        })
        self.picking_out = self.PickingObj.create({
            'partner_id': self.partner_agrolite_id,
            'picking_type_id': self.picking_type_out,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location,
        })
        self.moveA_out = self.MoveObj.create({
            'name': self.productA.name,
            'product_id': self.productA.id,
            'product_uom_qty': 100.0,
            'product_uom': self.productA.uom_id.id,
            'picking_id': self.picking_out.id,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location,
        })
        # link moves
        self.moveA_in.move_dest_id = self.moveA_out
        # create a lot
        self.lotA = self._create_lot(name='LotA', product_id=self.productA.id)
        # confirm both pickings
        self.picking_in.action_confirm()
        self.picking_out.action_confirm()

    def _get_pack_op(self, picking, prod):
        return self.StockPackObj.search([
          ('picking_id', '=', picking.id),
          ('product_id', '=', prod.id),
        ], limit=1)

    def _create_lot(self, **kw):
        return self.env['stock.production.lot'].create(kw)

    def _validate_picking(self, picking):
        # simulate click on `validate` + create back order if needed
        action = picking.do_new_transfer()
        if action:
            self.env[action['res_model']].browse(action['res_id']).process()

    def _prepare_picking(self, picking, prod, lot, qty_done):
        pack_op = self._get_pack_op(picking, prod)
        # pack A partial
        action = pack_op.action_split_lots()
        pack_op.update({
            'qty_done': qty_done,
            'pack_lot_ids': [(0, 0, {'lot_id': lot.id, 'qty': qty_done})]
        })
        pack_op.with_context(**action['context']).save()
        self._validate_picking(picking)
        self.assertEqual(picking.move_lines.mapped('state'), ['done'])

    def test_scrap_NO_adjustment(self):
        picking = self.picking_in
        self._prepare_picking(picking, self.productA, self.lotA, 90.0)
        self.env['stock.scrap'].with_context(
            skip_scrap_move_chain=True).create({
                'picking_id': picking.id,
                'lot_id': self.lotA.id,
                'product_id': self.productA.id,
                'scrap_qty': 10.0,
                'product_uom_id': self.productA.uom_id.id,
                'location_id': picking.location_dest_id.id,
            })
        # check IN
        scrapped_move = self.picking_in.move_lines.filtered(
            lambda x: x != self.moveA_in)[0]
        self.assertEqual(self.moveA_in.product_uom_qty, 90.0)
        self.assertEqual(self.moveA_in.state, 'done')
        self.assertEqual(scrapped_move.product_uom_qty, 10.0)
        self.assertEqual(scrapped_move.state, 'done')
        # check OUT
        # quantities are the same
        self.assertEqual(
            self.picking_out.pack_operation_ids[0].product_qty, 90.0)
        scrapped_move = self.picking_out.move_lines.filtered(
            lambda x: x != self.moveA_out)[0]
        self.assertEqual(self.moveA_out.product_uom_qty, 90.0)
        self.assertEqual(self.moveA_out.state, 'assigned')
        self.assertEqual(scrapped_move.product_uom_qty, 10.0)
        self.assertEqual(scrapped_move.state, 'waiting')

    def test_scrap_adjustment(self):
        picking = self.picking_in
        picking.do_prepare_partial()
        self._prepare_picking(picking, self.productA, self.lotA, 90.0)
        self.env['stock.scrap'].create({
            'picking_id': picking.id,
            'lot_id': self.lotA.id,
            'product_id': self.productA.id,
            'scrap_qty': 10,
            'product_uom_id': self.productA.uom_id.id,
            'location_id': picking.location_dest_id.id,
        })
        # check IN
        scrapped_move = self.picking_in.move_lines.filtered(
            lambda x: x != self.moveA_in)[0]
        self.assertEqual(self.moveA_in.product_uom_qty, 90.0)
        self.assertEqual(self.moveA_in.state, 'done')
        self.assertEqual(scrapped_move.product_uom_qty, 10.0)
        self.assertEqual(scrapped_move.state, 'done')
        # check OUT
        # here is the main difference: on the next move
        # we get the original qty - scrapped qty
        self.assertEqual(
            self.picking_out.pack_operation_ids[0].product_qty, 80.0)
        scrapped_move = self.picking_out.move_lines.filtered(
            lambda x: x != self.moveA_out)[0]
        self.assertEqual(self.moveA_out.product_uom_qty, 80.0)
        self.assertEqual(self.moveA_out.state, 'assigned')
        self.assertEqual(scrapped_move.product_uom_qty, 10.0)
        self.assertEqual(scrapped_move.state, 'waiting')
