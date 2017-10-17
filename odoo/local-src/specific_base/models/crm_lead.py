# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import pytz
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _order = "priority desc,datetime_action,id desc"

    lead_planning_url = fields.Char(
        string='Lead planning url',
        compute='_compute_lead_planning_url',
    )

    @api.model
    def _compute_lead_planning_url(self):
        try:
            url = self.env['ir.config_parameter'].get_param(
                'lead_planning_url'
            )
            for lead in self:
                if url and lead.id:
                    lead.lead_planning_url = url % lead.id
        except Exception:
            raise UserError(
                _('Error on configuration of lead planning url')
            )

    opening_date = fields.Date(
        string='Opening date',
        help='Estimated date of opening of the future center',
    )

    opening_location = fields.Char(
        string='Opening location',
        help='Opening location of the future center',
        size=255,
    )

    opening_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Opening country',
        help='Opening country of the future center',

    )

    personal_contribution = fields.Char(
        string='Personal contribution',
        help='Amount of personal contribution '
             'in currency of the future franchise',
        size=255,
    )

    graduate_education = fields.Char(
        string='Graduate education',
        help='Training and diplomas',
        size=255,
    )

    has_franchisee = fields.Boolean(
        string='Already owning a franchise',
        help='Has candidate ever been responsible of a franchise?',
    )

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        ondelete='restrict',
        string='Phototherapist',
    )

    can_edit_user = fields.Boolean(
        compute='_compute_can_edit_user',
        default=lambda self: self.can_edit_user_value(),
    )

    @api.model
    def can_edit_user_value(self):
        return self.env.user.has_group(
            'specific_security.group_can_edit_lead_vendor'
        )

    @api.depends()
    def _compute_can_edit_user(self):
        can_edit_user = self.can_edit_user_value()
        for line in self:
            line.can_edit_user = can_edit_user

    can_edit_marketing_values = fields.Boolean(
        compute='_compute_can_edit_marketing_values',
        default=lambda self: self.can_edit_marketing_values_value(),
    )

    @api.model
    def can_edit_marketing_values_value(self):
        return self.env.user.has_group(
            'specific_security.group_can_edit_marketing_values'
        )

    @api.depends()
    def _compute_can_edit_marketing_values(self):
        can_edit_marketing_values = self.can_edit_marketing_values_value()
        for line in self:
            line.can_edit_marketing_values = can_edit_marketing_values

    datetime_action = fields.Datetime(
        string='Next Activity Date',
        index=True,
    )

    @api.onchange('datetime_action')
    def onchange_datetime_action(self):
        self.date_action = self.datetime_action

    @api.model
    def get_datetime_action_in_timestamp(self, date_action, action_hour):
        if action_hour:
            tz_name = self.env.context.get('tz') or self.env.user.tz
            context_tz = pytz.timezone(tz_name)

            timestamp = (
                fields.Datetime.from_string(date_action) +
                timedelta(hours=action_hour)
            )
            tz_timestamp = context_tz.localize(timestamp)
            utc_timestamp = tz_timestamp.astimezone(pytz.utc)

            datetime_action = fields.Datetime.to_string(utc_timestamp)
        else:
            datetime_action = date_action
        return datetime_action

    @api.onchange('next_activity_id')
    def _onchange_next_activity_id(self):
        result = super(CrmLead, self)._onchange_next_activity_id()

        self.datetime_action = self.get_datetime_action_in_timestamp(
            self.date_action,
            self.next_activity_id.action_hour
        )

        return result

    @api.model
    def create(self, values):
        if values.get('datetime_action'):
            values['date_action'] = values['datetime_action']
        return super(CrmLead, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('datetime_action'):
            values['date_action'] = values['datetime_action']
        return super(CrmLead, self).write(values)

    @api.multi
    def convert_to_opportunity(self):
        self.ensure_one()
        wizard = self.env['crm.lead2opportunity.partner'].with_context(
            active_id=self.id,
            active_ids=self.ids,
        ).create({
            'name': 'convert',
            'action': 'nothing',
        })
        return wizard.action_apply()


class CrmLeadTag(models.Model):
    _inherit = 'crm.lead.tag'

    _sql_constraints = [
        ('uniq_slug',
         'unique(slug)',
         _('Slug should be unique')),
    ]

    slug = fields.Char(
        string='Slug',
        help='Unique id for lead tag',
        size=128,
    )

    name = fields.Char(
        translate=True,
    )


class CrmLostReason(models.Model):
    _inherit = 'crm.lost.reason'

    name = fields.Char(
        translate=True,
    )
