# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from anthem.lyrics.records import create_or_update

import anthem
from base64 import b64encode
from pkg_resources import Requirement, resource_string


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
def setup_company_report_footer(ctx):
    companies = ctx.env['res.company'].search([])
    companies.write({
        'custom_footer': True,
        'rml_footer':
            'SAS au capital de 15 000 € - Siret : 529 850 455 00062 – '
            'TVA Intracommunautaire : FR58 529 850 455 – R.C.S. NICE<br/>'
            'Siège : 196 avenue de la Californie, '
            'California Park – Château de Leliwa, 06200 NICE'
    })


@anthem.log
def setup_company_logo(ctx):
    """ Setup company logo """
    company = ctx.env.ref('base.main_company')

    # load logo on company
    req = Requirement.parse('depiltech-odoo')
    logo_content = resource_string(req, 'data/images/logo.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo


@anthem.log
def main(ctx):
    setup_admin_companies(ctx)
    remove_company_for_partners_of_coampnies(ctx)
    setup_company_report_footer(ctx)
