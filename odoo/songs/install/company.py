# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from anthem.lyrics.records import create_or_update

import anthem


@anthem.log
def setup_admin_companies(ctx):
    companies = ctx.env['res.company'].search([])
    admin = ctx.env['res.users'].search([('login', '=', 'admin')])
    admin.company_ids = companies.ids


@anthem.log
def remove_company_for_partners_of_coampnies(ctx):
    companies = ctx.env['res.company'].search([])
    for company in companies:
        partner = company.partner_id
        if partner:
            partner.company_id = False


@anthem.log
def main(ctx):
    setup_admin_companies(ctx)
    remove_company_for_partners_of_coampnies(ctx)
