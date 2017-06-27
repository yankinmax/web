# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class SaleDiscountProgramReportConfig(models.Model):

    _name = 'sale.discount.program.report.config'

    name = fields.Char('Name')
    lang_id = fields.Many2one('res.lang', 'Language', required=True)

    active = fields.Boolean('Active')

    top_image = fields.Binary('Top image',
                              help='This image will be displayed with a width '
                                   'of 1083px at the top of the report')

    amount_zone_height = fields.Integer('Amount zone height (in px)',
                                       help='This is the height of the amount '
                                            'zone in the top picture.'
                                            'Be aware that a 20px padding is'
                                            'applied both on top and bottom.')
    amount_zone_width = fields.Integer('Amount zone width (in px)',
                                       help='This is the width of the amount '
                                            'zone in the top picture ')
    amount_position_top = fields.Integer('Amount zone position top (in px)',
                                         help='This is the position in pixels '
                                              'from the top of the image '
                                              'where the amount zone is '
                                              'displayed.')
    amount_position_left = fields.Integer('Amount zone position left (in px)',
                                          help='This is the position in pixels'
                                               ' from the left of the image '
                                               'where the amount zone is '
                                               'displayed.'
                                          )

    amount_container_style = fields.Char(
        compute='_compute_amount_container_style')

    date_format = fields.Char('Date format', help='Uses Unicode LDML (Locale '
                                                  'Data Markup Language) Date '
                                                  'Format')

    ribbon_text = fields.Char('Ribbon text')

    general_terms_conditions_title = fields.Html(
        'General terms and conditions title')
    general_terms_conditions_left = fields.Html(
        'General terms and conditions left column')
    general_terms_conditions_right = fields.Html(
        'General terms and conditions right column')

    @api.multi
    def name_get(self):
        return [(record.id, "%s (%s)" % (record.name, record.lang_id.name))
                for record in self]

    @api.constrains('lang_id', 'active')
    def _check_unique_active_lang(self):
        if self.active and self.search([('lang_id', '=', self.lang_id.id),
                                        ('id', '!=', self.id)]):
            raise models.ValidationError(_(
                'You cannot have two active models for the same language'))

    @api.multi
    def copy(self, default=None):
        default['active'] = False
        return super(SaleDiscountProgramReportConfig, self).copy(default)

    @api.multi
    def _compute_amount_container_style(self):
        for conf in self:
            conf.amount_container_style = ('position: absolute; top: %spx; '
                                           'left: %spx; height: %spx; width: '
                                           '%spx; padding-top: 20px; '
                                           'font-size: 2em; font-weight: '
                                           'bold; text-align: center;') % (
                conf.amount_position_top, conf.amount_position_left,
                conf.amount_zone_height, conf.amount_zone_width)
