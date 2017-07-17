# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPayment(models.Model):

    _inherit = "account.payment"

    def _get_phototherapist_required(self):
        return self._context.get('journal_type', False) == 'sale'

    def _get_phototherapist(self):
        phototherapist = self.env['account.invoice'].browse(
            self._context.get('active_ids')).mapped('phototherapist_id')
        if len(phototherapist) == 1:
            return phototherapist
        else:
            return None

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist',
        default=_get_phototherapist)

    phototherapist_required = fields.Boolean(
        default=_get_phototherapist_required)
