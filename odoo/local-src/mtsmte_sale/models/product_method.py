# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _


class ProductMethod(models.Model):
    _name = 'product.method'

    name = fields.Char(
        required=True,
        translate=True,
    )
    product_ids = fields.One2many(
        'product.template',
        'product_method_id',
        string='Product',
    )
    task_id = fields.One2many(
        'project.task',
        'product_method_id',
        string='Task',
    )
    _sql_constraints = [
        ('name_uniq', 'unique (name)', _('The name must be unique')),
    ]
