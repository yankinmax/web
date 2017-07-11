# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, exceptions, _


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
