# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmOpportunityToCustomer(models.TransientModel):
    _name = 'crm.opportunity.to.customer'

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        readonly=True,
    )

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist',
        required=True,
    )
    title_id = fields.Many2one(
        comodel_name='res.partner.title',
        string='Title',
        required=True,
    )
    lastname = fields.Char(
        string='Last name',
        required=True,
    )
    firstname = fields.Char(
        string='First name',
        required=True,
    )
    birthday = fields.Date(
        string='Birthday',
        required=True,
    )

    street = fields.Char(
        string='Street',
        required=True,
    )
    street2 = fields.Char(
        string='Street2',
    )
    zip = fields.Char(
        string='ZIP',
        required=True,
    )
    city = fields.Char(
        string='City',
        required=True,
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
    )

    function = fields.Char(
        string='Function',
    )
    phone = fields.Char(
        string='Phone',
    )
    mobile = fields.Char(
        string='Mobile',
        required=True,
    )
    email = fields.Char(
        string='Email',
        required=True,
    )

    can_edit_user = fields.Boolean(
        readonly=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        required=True,
    )

    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Sales Team',
        required=True,
    )

    campaign_id = fields.Many2one(
        comodel_name='utm.campaign',
        string='Campaign',
    )
    source_id = fields.Many2one(
        comodel_name='utm.source',
        string='Source',
    )
    medium_id = fields.Many2one(
        comodel_name='utm.medium',
        string='Medium',
    )

    can_edit_marketing_values = fields.Boolean(
        readonly=True,
    )

    @api.model
    def get_new_stage(self):
        new_stage = self.env['crm.stage'].search(
            [('used_when_convert_to_customer', '=', True)],
            limit=1,
        )
        if not new_stage:
            raise ValidationError(_(
                'Configuration error on lead stages '
                '(not stage defined to convert lead to customer).'
            ))
        return new_stage

    @api.model
    def default_get(self, fields):
        result = {}

        # To check if lead stages is correctly defined
        self.get_new_stage()

        if self._context.get('active_id'):
            lead = self.env['crm.lead'].browse(self._context['active_id'])
            result['lead_id'] = lead.id

            if lead.contact_name:
                partner_temp = self.env['res.partner'].new({
                    'name': lead.contact_name,
                })
                partner_temp._inverse_name()
                result.update({
                    'lastname': partner_temp.lastname,
                    'firstname': partner_temp.firstname,
                })

            result.update({
                'phototherapist_id': lead.phototherapist_id.id,
                'title_id': lead.title.id,

                'street': lead.street,
                'street2': lead.street2,
                'zip': lead.zip,
                'city': lead.city,
                'state_id': lead.state_id.id,
                'country_id': lead.country_id.id,

                'function': lead.function,
                'phone': lead.phone,
                'mobile': lead.mobile,
                'email': lead.email_from,

                'can_edit_user': lead.can_edit_user_value(),
                'user_id': lead.user_id.id,
                'team_id': lead.team_id.id,

                'can_edit_marketing_values': (
                    lead.can_edit_marketing_values_value()
                ),
                'campaign_id': lead.campaign_id.id,
                'medium_id': lead.medium_id.id,
                'source_id': lead.source_id.id,
            })

        return result

    def get_values_to_create_customer(self):
        return {
            'company_type': 'agency_customer',

            'lastname': self.lastname,
            'firstname': self.firstname,

            'birthday': self.birthday,

            'phototherapist_id': self.phototherapist_id.id,
            'title': self.title_id.id,

            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'state_id': self.state_id.id,
            'country_id': self.country_id.id,

            'function': self.function,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,

            'user_id': self.user_id.id,
            'team_id': self.team_id.id,

            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
        }

    @api.multi
    def convert(self):
        self.ensure_one()
        customer = self.env['res.partner'].create(
            self.get_values_to_create_customer()
        )
        self.lead_id.write({
            'partner_id': customer.id,
            'stage_id': self.get_new_stage().id,
        })
        action = {
            'name': 'Partner',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': customer.id,
        }
        return action
