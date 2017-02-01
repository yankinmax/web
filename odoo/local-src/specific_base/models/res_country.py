# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    is_active_b2c = fields.Boolean(
        string='Activate on B2C site',
        help='Is country activated on B2C site?'
    )

    is_active_b2b = fields.Boolean(
        string='Activate on B2B site',
        help='Is country activated on B2B site?'
    )
