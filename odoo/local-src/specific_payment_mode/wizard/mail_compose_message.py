# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        condition = (
            self._context.get('default_model') == 'sale.order' and
            self._context.get('default_res_id') and
            self._context.get('mark_so_as_sent')
        )
        if condition:
            order = self.env['sale.order'].browse(
                [self._context['default_res_id']]
            )
            to_be_sent = (
                order.state == 'waiting_calculator' and
                order.partner_company_type == 'agency_customer'
            )
            if to_be_sent:
                order.state = 'sent'
        return super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit
        )
