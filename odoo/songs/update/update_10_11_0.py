# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from anthem.lyrics.modules import update_translations


@anthem.log
def post(ctx):
    """ Applying 10.11.0, reapply mtsmte_reports module translations """
    update_translations(ctx, ['mtsmte_reports'])
