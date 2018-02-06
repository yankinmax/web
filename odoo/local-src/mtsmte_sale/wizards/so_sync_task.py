# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions, _


class SOSyncTask(models.TransientModel):
    _name = 'wiz.so.sync.task'

    so_line_ids = fields.Many2many(
        'sale.order.line',
        string="Lines to sync",
        default=lambda self: self._default_so_lines(),
    )

    def _default_so_lines(self):
        order = self._get_order()
        return [(6, 0, [
            x.id for x in order.order_line if x._is_service_task()])]

    def _get_order(self):
        order_id = self.env.context.get('active_id')
        return self.env['sale.order'].browse(order_id)

    @api.multi
    def action_sync(self):
        self.ensure_one()
        order = self._get_order()
        if not order.state == 'sale':
            raise exceptions.UserError(_('Order must be confirmed!'))
        self._get_tasks().with_context(so_sync_wizard=True).sync_with_so_line()
        return {'type': 'ir.actions.act_window_close'}

    def _get_tasks(self):
        return self.env['project.task'].search([
            ('sale_line_id', 'in', self.so_line_ids.ids)
        ])
