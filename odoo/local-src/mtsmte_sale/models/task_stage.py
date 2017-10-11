# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    final_stage = fields.Boolean(
        string="Final stage",
        help="Defines whether this stage is considered final in the workflow"
    )
