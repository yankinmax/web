# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleConfig(models.TransientModel):
    _inherit = 'sale.config.settings'

    lead_planning_url = fields.Char(
        string='Lead planning url',
        help='Lead planning url with %s inside which be replaced by lead id'
    )

    @api.model
    def get_default_lead_planning_url(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'lead_planning_url': icp.get_param('lead_planning_url')
        }

    @api.multi
    def set_lead_planning_url(self):
        self.env['ir.config_parameter'].set_param(
            'lead_planning_url',
            self.lead_planning_url
        )

    partner_planning_url = fields.Char(
        string='Partner planning url',
        help='Partner planning url with %s inside '
             'which be replaced by partner id'
    )

    @api.model
    def get_default_partner_planning_url(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'partner_planning_url': icp.get_param('partner_planning_url')
        }

    @api.multi
    def set_partner_planning_url(self):
        self.env['ir.config_parameter'].set_param(
            'partner_planning_url',
            self.partner_planning_url
        )
