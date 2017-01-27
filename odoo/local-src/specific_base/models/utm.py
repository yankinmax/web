# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, _


class UtmSource(models.Model):
    _inherit = 'utm.source'

    _sql_constraints = [
        ('uniq_slug',
         'unique(slug)',
         _('Slug should be unique')),
    ]

    slug = fields.Char(
        string='Slug',
        help='Unique id for source',
        size=128,
    )


class UtmMedium(models.Model):
    _inherit = 'utm.medium'

    _sql_constraints = [
        ('uniq_slug',
         'unique(slug)',
         _('Slug should be unique')),
    ]

    slug = fields.Char(
        string='Slug',
        help='Unique id for medium',
        size=128,
    )

    name = fields.Char(
        translate=True,
    )


class UtmCampaign(models.Model):
    _inherit = 'utm.campaign'

    _sql_constraints = [
        ('uniq_slug',
         'unique(slug)',
         _('Slug should be unique')),
    ]

    slug = fields.Char(
        string='Slug',
        help='Unique id for campaign',
        size=128,
    )
