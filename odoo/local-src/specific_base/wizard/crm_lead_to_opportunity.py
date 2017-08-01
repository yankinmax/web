# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class CrmLead2opportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    partner_phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist',
    )
    partner_title_id = fields.Many2one(
        comodel_name='res.partner.title',
        string='Title',
    )
    partner_lastname = fields.Char(
        string='Last name',
    )
    partner_firstname = fields.Char(
        string='First name',
    )
    partner_birthday = fields.Date(
        string='Birthday'
    )

    partner_street = fields.Char(
        string='Street',
    )
    partner_street2 = fields.Char(
        string='Street2',
    )
    partner_zip = fields.Char(
        string='ZIP',
    )
    partner_city = fields.Char(
        string='City',
    )
    partner_state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
    )
    partner_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
    )

    partner_function = fields.Char(
        string='Function',
    )
    partner_phone = fields.Char(
        string='Phone',
    )
    partner_mobile = fields.Char(
        string='Mobile',
    )
    partner_email = fields.Char(
        string='Email',
    )

    @api.model
    def default_get(self, fields):
        result = super(CrmLead2opportunityPartner, self).default_get(fields)
        if self._context.get('active_id'):
            lead = self.env['crm.lead'].browse(self._context['active_id'])

            if lead.phototherapist_id:
                result['partner_phototherapist_id'] = lead.phototherapist_id.id
            if lead.title:
                result['partner_title_id'] = lead.title.id
            if lead.contact_name:
                partner_temp = self.env['res.partner'].new({
                    'name': lead.contact_name,
                })
                partner_temp._inverse_name()
                result['partner_lastname'] = partner_temp.lastname
                result['partner_firstname'] = partner_temp.firstname

            if lead.street:
                result['partner_street'] = lead.street
            if lead.street2:
                result['partner_street2'] = lead.street2
            if lead.zip:
                result['partner_zip'] = lead.zip
            if lead.city:
                result['partner_city'] = lead.city
            if lead.state_id:
                result['partner_state_id'] = lead.state_id.id
            if lead.country_id:
                result['partner_country_id'] = lead.country_id.id

            if lead.function:
                result['partner_function'] = lead.function
            if lead.phone:
                result['partner_phone'] = lead.phone
            if lead.mobile:
                result['partner_mobile'] = lead.mobile
            if lead.email_from:
                result['partner_email'] = lead.email_from

            result['name'] = 'convert'
            result['action'] = 'create'

        return result

    @api.multi
    def action_apply(self):
        result = super(CrmLead2opportunityPartner, self).action_apply()
        lead = self.env['crm.lead'].browse(self.env.context['active_id'])
        partner = lead.partner_id
        partner.write({
            'company_type': 'agency_customer',
            'phototherapist_id': self.partner_phototherapist_id.id,
            'title': self.partner_title_id.id,
            'lastname': self.partner_lastname,
            'firstname': self.partner_firstname,
            'birthday': self.partner_birthday,
            'street': self.partner_street,
            'street2': self.partner_street2,
            'zip': self.partner_zip,
            'city': self.partner_city,
            'state_id': self.partner_state_id.id,
            'country_id': self.partner_country_id.id,
            'function': self.partner_function,
            'phone': self.partner_phone,
            'mobile': self.partner_mobile,
            'email': self.partner_email,
        })
        return result
