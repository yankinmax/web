# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProgramCondition(models.Model):
    _inherit = 'sale.discount.program.condition'

    type_condition = fields.Selection(
        selection_add=[('customer_sponsor', 'Sponsorship')]
    )

    @api.multi
    def _check_customer_sponsor(self, sale):
        """ Check if the sale order customer has a sponsor and if it's his
        first sale.order
        """
        return sale.partner_id.sponsor_id \
            and not sale.partner_id.already_bought
