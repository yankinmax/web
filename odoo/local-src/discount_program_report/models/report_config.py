# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleDiscountProgramReportConfig(models.Model):

    _name = 'sale.discount.program.report.config'

    lang_id = fields.Many2one('res.lang', 'Language', required=True)

    program_type = fields.Selection([('voucher', 'Voucher'),
                                     ('sponsorship', 'Sponsorship')],
                                    'Program type', required=True)

    top_image = fields.Binary('Top image')
    left_image = fields.Binary('Left image')
    right_image = fields.Binary('Right image')
    bottom_image = fields.Binary('Bottom image')

    ribbon_text = fields.Char('Ribbon text')

    general_terms_conditions_title = fields.Html('General terms and conditions title')
    general_terms_conditions_left = fields.Html('General terms and conditions left column')
    general_terms_conditions_right = fields.Html(
        'General terms and conditions right column')

    discount_program_ids = fields.One2many('sale.discount.program',
                                           'report_config_id',)

    _sql_constraints = [
        ('program_type_lang_id_unique',
         'unique(program_type,lang_id)',
         'Error, you cannot have multiple entries having the same Program '
         'type and Language'),
    ]
