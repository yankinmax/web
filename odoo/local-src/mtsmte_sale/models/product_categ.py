# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        index=1
    )
    responsible_user_id = fields.Many2one(
        comodel_name='res.users',
        compute='_compute_responsible_user_id',
    )
    manager_id = fields.Many2one(
        comodel_name='res.users',
        string='Manager',
    )
    responsible_1_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible User 1',
    )
    responsible_2_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible User 2',
    )

    @api.multi
    def _compute_responsible_user_id(self):
        for category in self:
            category.responsible_user_id = category.manager_id \
                or category.responsible_1_id \
                or category.responsible_2_id
