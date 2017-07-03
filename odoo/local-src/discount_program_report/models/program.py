# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Program(models.Model):

    _inherit = 'sale.discount.program'

    report_config_id = fields.Many2one('sale.discount.program.report.config',
                                       'Report config',
                                       compute='_get_report_config')

    is_printable = fields.Boolean('Printable', compute='_get_is_printable',
                                  store=True)

    sent_to_customer = fields.Boolean('Sent to customer', default=False,
                                      track_visibility='onchange')

    @api.depends('gift_voucher', 'voucher_code', 'partner_id')
    def _get_is_printable(self):
        for program in self:
            program.is_printable = (
                not program.gift_voucher
                and program.voucher_code
                and program.partner_id
            )

    @api.depends('is_printable')
    def _get_report_config(self):
        for program in self:
            if program.is_printable:
                company_lang = program.partner_id.company_id.partner_id.lang
                if company_lang:
                    report_config = self.env[
                        'sale.discount.program.report.config'].search(
                        [('lang_id.code', '=', company_lang)])
                else:
                    report_config = self.env[
                        'sale.discount.program.report.config'].search(
                        [('lang_id.code', '=', 'fr_FR')])
                if report_config:
                    program.report_config_id = report_config.id
                else:
                    raise UserError(_('There is no active report.config '
                                      'matching this program language.'))

    @api.multi
    def action_program_send(self):
        self.ensure_one()

        template = self.env.ref(
            'discount_program_report.email_template_discount_program')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = dict()
        ctx.update({
            'default_model': 'sale.discount.program',
            'default_res_id': self.id,
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_program_as_sent': True,
            'custom_layout':
                "discount_program_report."
                "mail_template_data_notification_email_discount_program"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def _cron_send_vouchers_to_customers(self):
        vouchers = self.search([('is_printable', '=', True),
                                ('sent_to_customer', '=', False)])
        for voucher in vouchers:
            email_act = voucher.action_program_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                voucher.with_context(email_ctx).message_post_with_template(
                    email_ctx.get('default_template_id'))
