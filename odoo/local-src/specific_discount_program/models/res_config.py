# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models


class SaleConfig(models.TransientModel):
    _inherit = 'sale.config.settings'

    voucher_percent = fields.Integer(
        string="Percent used to compute voucher amount",
    )

    voucher_max_amount = fields.Integer(
        string="Maximum amount for a voucher",
    )

    voucher_max_count = fields.Integer(
        string="Number of vouchers allowed by sale order",
    )

    voucher_default_validity = fields.Integer(
        string="Default validity (by months) for a voucher",
    )

    discount_manually_percent_max = fields.Float(
        string="Maximum percent of discount for a sale order",
        digits=dp.get_precision('Discount'),
    )

    discount_manually_percent_note_message = fields.Char(
        string="Description of percent of discount",
    )

    @api.model
    def get_default_voucher_percent(self, fields):
        icp = self.env['ir.config_parameter']
        return {'voucher_percent': int(icp.get_param('voucher_percent', '0'))}

    @api.multi
    def set_voucher_percent(self):
        self.env['ir.config_parameter'].set_param(
            'voucher_percent', str(self.voucher_percent)
        )

    @api.model
    def get_default_voucher_max_amount(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'voucher_max_amount': int(icp.get_param('voucher_max_amount', '0'))
        }

    @api.multi
    def set_voucher_max_amount(self):
        self.env['ir.config_parameter'].set_param(
            'voucher_max_amount', str(self.voucher_max_amount)
        )

    @api.model
    def get_default_voucher_max_count(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'voucher_max_count': int(
                icp.get_param('voucher_max_count', '0')
            )
        }

    @api.multi
    def set_voucher_max_count(self):
        self.env['ir.config_parameter'].set_param(
            'voucher_max_count', str(self.voucher_max_count)
        )

    @api.model
    def get_default_voucher_default_validity(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'voucher_default_validity': int(
                icp.get_param('voucher_default_validity', '0')
            )
        }

    @api.multi
    def set_voucher_default_validity(self):
        self.env['ir.config_parameter'].set_param(
            'voucher_default_validity', str(self.voucher_default_validity)
        )

    @api.model
    def get_default_discount_manually_percent_max(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'discount_manually_percent_max':
                float(icp.get_param('discount_manually_percent_max', 10.))
        }

    @api.multi
    def set_discount_manually_percent_max(self):
        self.env['ir.config_parameter'].set_param(
            'discount_manually_percent_max',
            str(self.discount_manually_percent_max)
        )

    @api.model
    def get_default_discount_manually_percent_note_message(self, fields):
        icp = self.env['ir.config_parameter']
        return {
            'discount_manually_percent_note_message':
                icp.get_param('discount_manually_percent_note_message', '')
        }

    @api.multi
    def set_discount_manually_percent_note_message(self):
        self.env['ir.config_parameter'].set_param(
            'discount_manually_percent_note_message',
            self.discount_manually_percent_note_message
        )
