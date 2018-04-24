# Copyright (C) 2018 by Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleQuoteLine(models.Model):
    _inherit = 'sale.quote.line'

    tested_sample = fields.Text(
        string='Tested Samples',
    )
