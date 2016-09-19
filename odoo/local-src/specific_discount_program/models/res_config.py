# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleConfig(models.TransientModel):
    _inherit = 'sale.config.settings'

    voucher_percent = fields.Integer(
        string="Pourcentage pour calcul du montant d'un bon d'achat",
    )

    voucher_max_amount = fields.Integer(
        string="Montant max. d'un bon d'achat",
    )

    voucher_max_count = fields.Integer(
        string="Nombre de bons d'achats autorisé par commande.",
    )

    voucher_default_validity = fields.Integer(
        string="Validité (en mois) par défaut des bons d'achats",
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
