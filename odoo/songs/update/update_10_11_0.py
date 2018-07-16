# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem
from anthem.lyrics.modules import update_translations


@anthem.log
def post(ctx):
    """ Applying update 10.10.2 """
    update_translations(ctx, ['mtsmte_reports'])
