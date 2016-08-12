# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import uuid

from datetime import datetime, timedelta

from openerp import models, fields, api, _


DUPLICATE_FIELDS_KEY = ['company_type', 'company_id',
                        'name', 'email']


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_family_situation_selection(self):
        return [('single', _('Single')),
                ('couple', _('Couple')),
                ('divorced', _('Divorced')),
                ('widower', _('Widower')),
                ]

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist')
    birthday = fields.Date()
    # canal = fields.Selection(selection='_get_partner_canal_selection',
    #                          string='How do you know us ?')
    info_meeting_date = fields.Date()
    positive_flash_test = fields.Selection(
        selection=[('y', 'Yes'), ('n', 'No')],
        default='n',
        )
    # socio_professional_category = fields.Selection(
    #     selection='_get_socio_pro_categ_selection',
    #     string='Socio-Professional Category'
    #     )
    family_situation = fields.Selection(
        selection='_get_family_situation_selection'
        )
    children_nb = fields.Integer()  # or Selection ???
    # why_no_buy = fields.Selection(
    #     selection='_get_why_no_buy_selection'
    #     )
    # maximum_budget = fields.Selection(
    #     selection='_get_maximum_budget_selection'
    #     )
    beauty_institute_attented = fields.Selection(
        selection=[('y', 'Yes'), ('n', 'No')],
        )
    comment1 = fields.Text(string='Anecdote/Vacations')
    comment2 = fields.Text(string='Cosmetic habits / Brand used')
    comment3 = fields.Text(string='Other')
    sponsor_ids = fields.Many2many('res.partner',
                                   'partner_sponsorship',
                                   'partner_id',
                                   'sponsor_id',
                                   string="Sponsors"
                                   )
    survey_done = fields.Boolean(default=False)

    @api.multi
    def take_me_to_diagnostic_survey(self):
        self.ensure_one()
        survey_response_obj = self.env['survey.user_input']
        # generate invitation link for this partner
        # (do not send email to customer)
        token = uuid.uuid4().__str__()
        # create response with token
        now = datetime.now()
        diagnostic_survey = self.env.ref(
            'specific_base_scen.diagnostic_survey')
        survey_response_obj.create({
            'survey_id': diagnostic_survey.id,
            'deadline': fields.Datetime.to_string(now + timedelta(days=1)),
            'date_create': fields.Datetime.to_string(now),
            'type': 'link',
            'state': 'new',
            'token': token,
            'partner_id': self.id,
            'email': self.email}
            )
        # get link to the survey
        url = '%s/%s' % (diagnostic_survey.public_url, token)

        self.survey_done = True
        # open survey
        return {
            'type': 'ir.actions.act_url',
            'name': "Start Survey",
            'target': 'self',
            'url': url,
        }

    _sql_constraints = [
        ('customer_unique',
         'unique(%s)' % ','.join(DUPLICATE_FIELDS_KEY),
         'It seems that there already a customer existing with same '
         'name and email adress. Please use the search function to find it.'
         )
    ]
