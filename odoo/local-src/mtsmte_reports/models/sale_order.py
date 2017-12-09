# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()
        if self.state == 'sale':
            template_id = self.env.ref(
                'mtsmte_reports.email_template_edi_sale_specific'
            )
        else:
            template_id = self.env.ref(
                'mtsmte_reports.quotation_confirmation_mail_specific'
            )
        ctx = res.get('context', {})
        ctx['default_template_id'] = template_id.id
        res['context'] = ctx
        return res
