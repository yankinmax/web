# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import datetime
import calendar

from odoo import api, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    @api.onchange('currency_interval_unit')
    def onchange_currency_interval_unit(self):
        """ We want to have the last day of the month when changing date
        """
        super(AccountConfigSettings, self).onchange_currency_interval_unit()
        if self.currency_interval_unit == 'monthly':
            date_now = datetime.datetime.now()
            last_day = calendar.monthrange(date_now.year, date_now.month)[1]
            date = datetime.datetime(date_now.year, date_now.month, last_day,
                                     23, 55)
            self.currency_next_execution_date = date
