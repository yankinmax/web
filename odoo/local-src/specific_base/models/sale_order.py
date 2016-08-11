# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist')
