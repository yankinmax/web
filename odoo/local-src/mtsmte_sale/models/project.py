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
    resp_one_id = fields.Many2one(
        'res.users',
        string='Responsible 1',
    )
    resp_two_id = fields.Many2one(
        'res.users',
        string='Responsible 2',
    )
    send_sample_back = fields.Boolean(
        string='Send Samples back',
    )
    conclusion = fields.Html(
    )

    def write(self, vals):
        for proj in self:
            if 'resp_one_id' in vals:
                self.message_subscribe_users(vals['resp_one_id'])
            if 'resp_two_id' in vals:
                self.message_subscribe_users(vals['resp_two_id'])
        return super(ProjectProject, self).write(vals)
