# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        res['workflow_process_id'] = self.env.ref(
            'sale_automatic_workflow.automatic_validation').id
        return res

    @api.onchange('workflow_process_id')
    def _onchange_workflow_process_id(self):
        res = super(SaleOrder, self)._onchange_workflow_process_id()
        if (
                not self.workflow_process_id.validate_order
                and self.state == 'draft'
        ):
            return
        else:
            return res
