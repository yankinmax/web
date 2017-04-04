# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    import html2text
except ImportError:
    _logger.warning('could not import html2text')
    html2text = None


class ProjectTask(models.Model):
    _inherit = 'project.task'

    description_text = fields.Text(
        string='Description as text',
        compute='_compute_description_text',
    )

    @api.depends('description')
    def _compute_description_text(self):
        if html2text is None:
            return
        for task in self:
            converter = html2text.HTML2Text()
            task.description_text = converter.handle(task.description or '')
