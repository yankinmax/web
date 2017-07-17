# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        condition = (
            self._context.get('default_model') == 'sale.discount.program'
            and self._context.get('default_res_id')
            and self._context.get('mark_program_as_sent')
        )
        if condition:
            program = self.env['sale.discount.program'].browse(
                self._context['default_res_id'])
            if not program.sent_to_customer:
                program.sent_to_customer = True
        return super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit)
