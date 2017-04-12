# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

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
