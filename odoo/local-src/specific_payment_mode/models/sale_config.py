# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleConfig(models.TransientModel):
    _inherit = 'sale.config.settings'

    max_month_number = fields.Integer(
        string='Max month number used in sale order payment calculator',
    )

    @api.model
    def get_default_max_month_number(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'max_month_number': int(icp.get_param('max_month_number', '0'))
        }

    @api.multi
    def set_max_month_number(self):
        self.env['ir.config_parameter'].set_param(
            'max_month_number',
            str(self.max_month_number)
        )
