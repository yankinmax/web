# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class Program(models.Model):

    _inherit = 'sale.discount.program'

    report_config_id = fields.Many2one('sale.discount.program.report.config',
                                       'discount_program_ids',)
    #                                    compute='_get_report_config',

    #
    # @api.depends('partner_id.lang_id')
    # def _get_report_config(self):
    #     for program in self:
    #         program.report_config_id = self.env[
    #             'sale.discount.program.report.config'].search(
    #             [('lang_id', '=', self.env.ref('base.lang_fr').id),
    #              ('program_type', '=', 'voucher')]).id

    @api.multi
    def action_program_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('discount_program_report',
                                                             'email_template_discount_program')[
                1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail',
                                                                 'email_compose_message_wizard_form')[
                1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'sale.discount.program',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            # 'mark_so_as_sent': True,
            'custom_layout': "discount_program_report.mail_template_data_notification_email_discount_program"
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
