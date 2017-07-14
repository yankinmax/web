# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    name = fields.Char(
        required=True,
    )
    product_ids = fields.One2many(
        'product.template',
        'equipment_id',
        string='Product',
    )
    _sql_constraints = [
        ('name_uniq', 'unique (name)', _('The name must be unique')),
    ]
