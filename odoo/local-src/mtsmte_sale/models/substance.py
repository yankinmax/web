# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class ProductSubstance(models.Model):
    _name = 'product.substance'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    legal_limit_min = fields.Float(
        string='Legal limit min value',
    )
    legal_limit_max = fields.Float(
        string='Legal limit max value',
    )
    comments = fields.Char(
        string='Comments',
    )
    has_limit_min = fields.Boolean(
        string='Has limit min',
    )
    has_limit_max = fields.Boolean(
        string='Has limit max',
    )
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Substance UOM',
        required=True,
    )
    project_task_ids = fields.Many2many(
        'project.task',
        invisible=True,
    )
    sale_order_line_ids = fields.Many2many(
        'sale.order.line',
        string='Products',
        invisible=True,
    )
    detection_limit = fields.Char(
        string='Detection Limit',
    )
    quantification_limit = fields.Char(
        string='Quantification Limit',
    )
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        domain=[('customer', '=', True)],
    )
    sub_cas_number = fields.Char(
        string='CAS Number',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        index=1
    )

    @api.constrains('legal_limit_min', 'legal_limit_max')
    def _onchange_legal_limit(self):
        if ((self.has_limit_min and self.has_limit_max) and
                (float_compare(self.legal_limit_min, self.legal_limit_max,
                               False, False) > 0)):
            raise ValidationError(_('Legal limit min should be smaller than '
                                    'Legal limit max'))
