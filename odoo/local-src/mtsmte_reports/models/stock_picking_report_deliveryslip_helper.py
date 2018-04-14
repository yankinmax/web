# -*- coding: utf-8 -*-
# Copyright (C) 2018 by Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPickingReportDeliveryslipHelper(models.AbstractModel):
    _name = 'stock.picking.report_deliveryslip_helper'

    @staticmethod
    def _prettify_value(val):
        return '{:.3f}'.format(val)

    def _get_ordered_qty(self, pack_op, prettify=True):
        """Sum of `ordered_qty`-s on SOL-s of this `product_id` w/ no route."""
        # and having no `route_id`-s
        pack_op.ensure_one()
        self.env.cr.execute(
            """
            SELECT SUM(sol.product_uom_qty)

            FROM stock_pack_operation AS spo
            INNER JOIN stock_picking AS sp
            ON spo.picking_id = sp.id
            INNER JOIN procurement_order AS po
            ON sp.group_id = po.group_id
            INNER JOIN sale_order_line AS sol
            ON po.sale_line_id = sol.id

            WHERE spo.id in (%s)
            AND spo.product_id = sol.product_id
            AND sol.route_id IS NULL

            GROUP BY sp.group_id
            """, pack_op.ids)
        ordered_qty = self.env.cr.fetchone()[0]
        if prettify:
            return self._prettify_value(ordered_qty)
        return ordered_qty

    def _get_balance_to_deliver(self, pack_op):
        """Sum of `delivered_qty` on all pickings to Customer in current SO."""
        pack_op.ensure_one()
        self.env.cr.execute(
            """
            SELECT SUM(spo.qty_done)

            FROM stock_picking AS sp
            INNER JOIN stock_pack_operation AS spo
            ON sp.id = spo.picking_id

            WHERE sp.id IN (
                SELECT DISTINCT id FROM stock_picking WHERE group_id IN (
                    SELECT sp.group_id
                    FROM stock_picking AS sp
                    INNER JOIN stock_pack_operation AS spo
                    ON sp.id = spo.picking_id
                    WHERE spo.id IN %s))
            AND sp.location_dest_id = (
                SELECT DISTINCT res_id FROM ir_model_data
                WHERE module = 'stock'
                AND model = 'stock.location'
                AND name = 'stock_location_customers'
            )
            AND spo.product_id = %s

            GROUP BY sp.group_id
            """, (tuple(pack_op.ids), pack_op.product_id.id))
        balance = self.env.cr.fetchone()[0]
        ordered = self._get_ordered_qty(pack_op, prettify=False)
        balance_to_deliver = ordered - balance
        return self._prettify_value(balance_to_deliver)
