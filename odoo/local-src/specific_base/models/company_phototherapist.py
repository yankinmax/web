# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResCompanyPhototherapist(models.Model):
    _name = 'res.company.phototherapist'
    _desc = "Manage phototherapist of a company"

    company_id = fields.Many2one(comodel_name='res.company', required=True,
                                 string='Company')
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    date_deleted = fields.Date()

    @api.onchange('active')
    def onchange_active(self):
        if not self.active:
            self.date_deleted = fields.Date.today()
