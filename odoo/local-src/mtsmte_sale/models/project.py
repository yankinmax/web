# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    analyze_sample = fields.Text(
        string='Samples To Analyze',
    )
