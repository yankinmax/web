# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields
from odoo import api

class ResLang(models.Model):

    _inherit = 'res.lang'

    tr_sequence = fields.Integer(
        string='Translation sequence',
        help='Defines the order of language to appear in translation dialog',
        default=10,
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        print(order)
        return super().search(args, offset=offset, limit=limit, order=order, count=count)
