# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, exceptions, _


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    @api.multi
    def do_scrap(self):
        """Automatically scrap qty for the next move in the chain."""
        res = super(StockScrap, self).do_scrap()
        if not self.env.context.get('skip_scrap_move_chain'):
            for scrap in self:
                scrap._scrap_next_qty_done()
        return res

    def _scrap_next_qty_done(self):
        """Walk through moves chain and update quantities."""
        move = self._get_move_to_scrap()
        while move.move_dest_id:
            move = move.move_dest_id
            self._scrap_move_qty_done(move)

    def _get_move_to_scrap(self):
        """Get move to scrap for current scrap record."""
        return self.env['stock.move'].search([
            ('picking_id', '=', self.picking_id.id),
            ('product_id', '=', self.product_id.id),
            ('state', '=', 'done'),
            '|',
            ('restrict_lot_id', '=', False),  # correct?
            ('restrict_lot_id', '=', self.lot_id.id),
        ], limit=1)

    def _scrap_move_qty_done(self, move):
        """Update move qty.

        Steps:
        * decrease move qty by scrapped qty
        * check procurement UoM
        * decrease procurement qty by scrapped qty
        * unreser and assign again move
        """
        move.product_uom_qty -= self.scrap_qty
        if move.procurement_id:
            if move.procurement_id.product_uom != self.product_uom_id:
                raise exceptions.UserError(_(
                    'Procurement order UoM `%s` does not match scrap UoM `%s`.'
                ) % (move.procurement_id.product_uom.name,
                     self.product_uom_id.name))
            move.procurement_id.product_qty -= self.scrap_qty
        move.do_unreserve()
        move.action_assign()
