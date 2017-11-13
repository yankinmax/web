# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('reference')
    def _onchange_reference(self):
        # If name of the invoice is null we copy the value of reference
        if not self.name and self.type in ('in_invoice', 'in_refund'):
            self.name = self.reference
