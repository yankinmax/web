# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleConfig(models.TransientModel):
    _inherit = 'sale.config.settings'

    force_discount_apply = fields.Boolean(
        string="Automatically apply discount program before any other action "
               "(Print, confirm, etc..)"
    )

    @api.model
    def get_default_force_discount_apply(self, fields):
        icp = self.env['ir.config_parameter']
        return {'force_discount_apply': bool(
            icp.get_param('force_discount_apply', False)
        )}

    @api.multi
    def set_force_discount_apply(self):
        self.env['ir.config_parameter'].set_param(
            'force_discount_apply', 'True' if self.force_discount_apply else ''
        )
