# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# TODO: Fix this class
# TODO: Probably linked with 'account_tax_exigible' TODO
from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _create_payment_entry(self, amount):
        return super(AccountPayment, self.with_context(
            copy_partner_on_move=self.partner_id,
            copy_ref_on_move=self.communication
        ))._create_payment_entry(amount)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def create(self, vals):
        new_vals = vals.copy()
        ctx = self.env.context or {}
        if ctx.get('copy_partner_on_move') and not new_vals.get('partner_id'):
            new_vals['partner_id'] = ctx['copy_partner_on_move'].id
        if ctx.get('copy_ref_on_move') and not vals.get('ref'):
            new_vals['ref'] = ctx['copy_ref_on_move']
        return super(AccountMoveLine, self).create(new_vals)
