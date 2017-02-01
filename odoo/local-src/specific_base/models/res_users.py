# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    qualitelis_responsable_region_id = fields.Integer(
        string='Qualitelis, region id',
        help='For network animators, '
             'region id in Qualitelis for the responsible of the user'
    )
