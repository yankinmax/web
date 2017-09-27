# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResultsSentences(models.Model):
    _name = "task.results.sentences"
    _rec_name = "sentence"

    sentence = fields.Char(
        string="Sentence"
    )
    sentence_type = fields.Char(
        string="Sentence type"
    )
