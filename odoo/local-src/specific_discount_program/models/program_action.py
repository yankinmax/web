# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class DiscountProgramAction(models.Model):
    _inherit = 'sale.discount.program.action'

    note_message = fields.Char(
        required=True,
        string='Discount description',
    )

    @api.multi
    def apply(self, sale):
        self.ensure_one()
        super(DiscountProgramAction, self).apply(sale)
        if sale.note and sale.note != '':
            sale.note += '\n'
        sale.note += self.note_message
