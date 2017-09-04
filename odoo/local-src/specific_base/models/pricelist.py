# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    allowed_company_ids = fields.Many2many(comodel_name='res.company',
                                           string='Allowed companies')
