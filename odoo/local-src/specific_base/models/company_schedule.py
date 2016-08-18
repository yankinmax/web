# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompanySchedule(models.Model):
    _name = 'res.company.schedule'
    _desc = "Manage open hours for a company"
    _rec_name = 'company_id'

    company_id = fields.Many2one(comodel_name='res.company')
    # monday
    is_open_am_0 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_0 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_0 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_0 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_0 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_0 = fields.Float(string="Closing at")  # widget="float_time"
    # tuesday
    is_open_am_1 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_1 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_1 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_1 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_1 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_1 = fields.Float(string="Closing at")  # widget="float_time"
    # wednesday
    is_open_am_2 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_2 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_2 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_2 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_2 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_2 = fields.Float(string="Closing at")  # widget="float_time"
    # thursday
    is_open_am_3 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_3 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_3 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_3 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_3 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_3 = fields.Float(string="Closing at")  # widget="float_time"
    # friday
    is_open_am_4 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_4 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_4 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_4 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_4 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_4 = fields.Float(string="Closing at")  # widget="float_time"
    # saturday
    is_open_am_5 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_5 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_5 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_5 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_5 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_5 = fields.Float(string="Closing at")  # widget="float_time"
    # sunday
    is_open_am_6 = fields.Boolean(string='Is open AM ?', default=True)
    time_begin_am_6 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_am_6 = fields.Float(string="Closing at")  # widget="float_time"
    is_open_pm_6 = fields.Boolean(string='Is open PM ?', default=True)
    time_begin_pm_6 = fields.Float(string="Opening at")  # widget="float_time"
    time_end_pm_6 = fields.Float(string="Closing at")  # widget="float_time"
