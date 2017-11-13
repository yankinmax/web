# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, exceptions, _
import logging
logger = logging.getLogger('[mts-stock-scrap]')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_cancel(self):
        waiting = self.filtered(lambda rec: rec.state == 'waiting')
        if waiting:
            raise exceptions.UserError(
                _("You can't cancel an operation waiting on another one "
                  "(%s)") % (', '.join(waiting.mapped('name')),)
            )
        return super(StockPicking, self).action_cancel()


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    @api.multi
    def do_scrap(self):
        """Automatically scrape qty for the next picking in the chain."""
        res = super(StockScrap, self).do_scrap()
        for scrap in self:
            next_picking = self._get_next_picking(scrap.picking_id)
            if next_picking:
                next_picking.do_unreserve()
                next_picking.action_assign()
            else:
                logger.warn('Cannot find next picking for '
                            'scrap: {} picking: {}'.format(
                                scrap.id, scrap.picking_id.name))
        return res

    def _get_next_picking(self, prev_picking):
        """Retrieve next picking in the route flow.

        Match by:
            * location = the next location for given picking
            * product = the same of the given picking
            * procurement group = the same of the given picking
        """
        return self.env['stock.picking'].search([
            ('location_id', '=', prev_picking.location_dest_id.id),
            ('product_id', '=', prev_picking.product_id.id),
            ('group_id', '=', prev_picking.group_id.id),
        ], limit=1)
