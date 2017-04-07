# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductSubstanceMesure(models.Model):
    _name = 'product.substance.mesure'

    product_substance_id = fields.Many2one(
        'product.substance',
        string='Substance',
    )
    task_id = fields.Many2one(
        'project.task',
        string='Task',
    )
    measure = fields.Float(
        'Measure',
    )
    conformity = fields.Boolean(
        string='Conformity',
    )
