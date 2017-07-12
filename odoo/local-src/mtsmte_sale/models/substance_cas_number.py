# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _


class SubstanceCasNumber(models.Model):
    _name = 'substance.cas.number'

    name = fields.Char(
        required=True,
    )
    substance_id = fields.Many2one(
        'product.substance',
        string='Product',
    )
    substance_mesure_id = fields.Many2one(
        'product.substance.mesure',
        string='Product',
    )
    _sql_constraints = [
        ('name_uniq', 'unique (name)', _('The name must be unique')),
    ]
