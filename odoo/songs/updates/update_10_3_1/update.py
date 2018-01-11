# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def remove_partner_sponsor(ctx):
    """ detect and clean 'partner.sponsor' that are not linked to
        a 'res.partner' with company_type = 'agency_customer'
    """
    ctx.env['partner.sponsor'].with_context(active_test=False).search([
        ('partner_id.company_type', '!=', 'agency_customer')
    ]).unlink()


@anthem.log
def recompute_active_for_partner_sponsor(ctx):
    """ recompute active for partner_sponsor """
    partner_sponsor_all = ctx.env['res.partner'].with_context(
        active_test=False).search([])
    partner_sponsor_all._compute_already_bought()


@anthem.log
def main(ctx):
    """ Main: update 10.3.1 """
    remove_partner_sponsor(ctx)
    recompute_active_for_partner_sponsor(ctx)
