# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def _get_company_type_selection(self):
        return [('not_real', _('Not real')),
                ('branch', _('Branch')),
                ('franchised', _('Franchised')),
                ('Closed', _('Closed')),
                ]

    @api.model
    def _get_royalties_freq_selection(self):
        return [('monthly', _('Monthly')),
                ('bimonthly', _('Bimonthly')),
                ('quarterly', _('Quarterly')),
                ]

    @api.model
    def _get_sms_abo_selection(self):
        return [(str(i), str(i))for i in range(100, 1600, 100)]

    @api.model
    def _get_royalties_pub_selection(self):
        return [('none', _('None')),
                ('100', '100'),
                ('200', '200'),
                ('300', '300'),
                ]

    @api.model
    def _get_payments_mode_selection(self):
        return [('check', _('Check')),
                ('levy', _('Levy')),
                ('transfer', _('Transfer')),
                ]
    #############################################
    # fields for centers (franchised, succ., ...)
    #############################################
    active = fields.Boolean(default=True)
    opening = fields.Boolean(default=True, help="Opening in progress")
    active_campaigns = fields.Boolean(default=False,
                                      help="SEM active")
    form = fields.Char(help="Juridical form")
    company_name = fields.Char(help="Juridical name of the company")
    franchised_mobile = fields.Char()
    franchised_email = fields.Char()
    longitude = fields.Float()
    latitude = fields.Float()
    description = fields.Text()
    description_active = fields.Boolean(default=False)
    come_by_transport = fields.Text(string='How to come by transport')
    come_by_car = fields.Text(string='How to come by car')
    sms_abo = fields.Selection(selection='_get_sms_abo_selection',
                               default='500')
    info_phoning = fields.Text(string='Phoning infos',
                               help="Used by teleop user to inform a customer")
    date_start_contract = fields.Date()
    date_end_contract = fields.Date()
    royalties_pub = fields.Selection(
        selection='_get_royalties_pub_selection',
        default='100')
    royalties_percentage = fields.Integer(help="Royalties percentage")
    royalties_min = fields.Integer(help="Minimum royalties")
    payments_mode = fields.Selection(
        selection='_get_payments_mode_selection',
        default='check')
    url_virtual_visit = fields.Char()
    nb_desk = fields.Integer(help="Desks number")
    nb_room = fields.Integer(help="Rooms number")
    tz = fields.Selection(related="partner_id.tz")
    date_opening = fields.Date()
    display_teleop = fields.Boolean(default=True)
    center_manager_name = fields.Char()
    franchised_name = fields.Char()
    capital_stock = fields.Integer()
    coach_id = fields.Many2one(comodel_name='res.users')
    # coach_id :: add domain on a specific group
    url_customer_reviews = fields.Char()
    # rcs, siret(siren+nic) --> install l10n_fr_siret modules
    company_type = fields.Selection(selection='_get_company_type_selection',
                                    string="Type")
    royalties_freq = fields.Selection(
        selection='_get_royalties_freq_selection',
        default='monthly')
