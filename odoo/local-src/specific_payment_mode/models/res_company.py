# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):

    _inherit = 'res.company'

    children_company_ids = fields.Many2many(
        'res.company', 'res_company_res_company_children_rel',
        'father_company_id', 'child_company_id',
        compute='_compute_children_company_ids', store=True
    )

    @api.depends('child_ids.children_company_ids')
    def _compute_children_company_ids(self):
        for company in self:
            companies = self.env['res.company'].search(
                [('id', 'child_of', company.id)])
            company.children_company_ids = companies.ids
