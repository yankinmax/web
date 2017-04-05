# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    analyze_sample = fields.Text(
        string='Samples To Analyze',
    )

    @api.multi
    def action_confirm(self):
        for order in self:
            super(SaleOrder, self).action_confirm()
            prj = self.env['project.project'].search(
                [('analytic_account_id', '=', order.project_id.id)])
            vals = {
                'analyze_sample': order.analyze_sample
            }
            prj.write(vals)
        return True
