# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem
from ...common import load_csv


@anthem.log
def load_account_followup_followup(ctx):
    """ Import account_followup.followup from csv """
    model = ctx.env['account_followup.followup'].with_context({'tracking_disable':1})  # noqa
    load_csv(ctx, 'data/install/generated/account_followup.followup.csv', model)  # noqa


@anthem.log
def load_account_followup_followup_line(ctx):
    """ Import account_followup.followup.line from csv """
    model = ctx.env['account_followup.followup.line'].with_context({'tracking_disable':1})  # noqa
    load_csv(ctx, 'data/install/generated/account_followup.followup.line.csv', model)  # noqa


@anthem.log
def main(ctx):
    load_account_followup_followup(ctx)
    load_account_followup_followup_line(ctx)
