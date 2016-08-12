# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist')

    @api.model
    def create(self, values):
        if not values.get('validity_date', False):
            values['validity_date'] = fields.Date.to_string(
                datetime.now() + timedelta(days=90))

        return super(SaleOrder, self).create(values)
