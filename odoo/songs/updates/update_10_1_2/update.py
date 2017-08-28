# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def clean_groups(ctx):
    """ Clean useless groups """

    bad_siege_group = ctx.env.ref('specific_base.group_siege_depiltech',
                                  raise_if_not_found=False)
    if bad_siege_group:
        bad_siege_group.unlink()

    bad_admin_group = ctx.env.ref('specific_base.group_admin_depiltech',
                                  raise_if_not_found=False)
    if bad_admin_group:
        bad_admin_group.unlink()


@anthem.log
def main(ctx):
    """ Main: update 10.1.2 """
    clean_groups(ctx)
