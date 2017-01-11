# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pkg_resources import Requirement
from pkg_resources import resource_stream

import anthem
from anthem.lyrics.loaders import load_csv_stream


@anthem.log
def define_auto_generate_invoices_for_companies(ctx):
    companies = ctx.env['res.company'].search([])
    companies.write({'auto_generate_invoices': True})


@anthem.log
def configure_missing_chart_of_account(ctx, full_mode=True):
    """Configure Missing COA for companies"""

    coa_dict = {
        'scenario.company_depiltechSAS': {
            'chart_template_id': 'l10n_fr.l10n_fr_pcg_chart_template',
            'template_transfer_account_id': 'l10n_fr.pcg_58',
            'sale_tax_id': 'l10n_fr.tva_normale',
            'purchase_tax_id': 'l10n_fr.tva_acq_normale',
        },
    }
    if full_mode:
        coa_dict['scenario.company_agencyFR'] = {
            'chart_template_id': 'l10n_fr.l10n_fr_pcg_chart_template',
            'template_transfer_account_id': 'l10n_fr.pcg_58',
            'sale_tax_id': 'l10n_fr.tva_normale',
            'purchase_tax_id': 'l10n_fr.tva_acq_normale',
        }
    for company_xml_id, values in coa_dict.iteritems():
        main_company = ctx.env.ref(company_xml_id)
        coa = ctx.env.ref(values['chart_template_id'])
        template_transfer_account = ctx.env.ref(
            values['template_transfer_account_id']
        )
        sale_tax = ctx.env.ref(values['sale_tax_id'])
        purchase_tax = ctx.env.ref(values['purchase_tax_id'])
        companies = ctx.env['res.company'].search([
            ('parent_id', '=', main_company.id),
        ])
        for company in companies:
            if not company.chart_template_id:
                wizard = ctx.env['wizard.multi.charts.accounts'].create({
                    'company_id': company.id,
                    'chart_template_id': coa.id,
                    'transfer_account_id': template_transfer_account.id,
                    'code_digits': 8,
                    'sale_tax_id': sale_tax.id,
                    'purchase_tax_id': purchase_tax.id,
                    'sale_tax_rate': 15,
                    'purchase_tax_rate': 15,
                    'complete_tax_set': coa.complete_tax_set,
                    'currency_id': ctx.env.ref('base.EUR').id,
                    'bank_account_code_prefix': coa.bank_account_code_prefix,
                    'cash_account_code_prefix': coa.cash_account_code_prefix,
                })
                wizard.execute()


@anthem.log
def remove_useless_accounts(ctx):
    accounts = ctx.env['account.account'].search([
        (
            'code',
            'not in',
            [
                '40110000',
                '41110000',
                '44520100',
                '44520200',
                '44520300',
                '44562000',
                '44566000',
                '44566200',
                '44571100',
                '44571200',
                '44571300',
                '60710000',
                '70710000',
            ]
        ),
        (
            'company_id',
            'not in',
            [
                # Antibes
                ctx.env.ref('scenario.company_agencyfr_center45').id,
                # Cannes
                ctx.env.ref('scenario.company_agencyfr_center26').id,
                # Marseille
                ctx.env.ref('scenario.company_agencyfr_center55').id,
            ]
        )
    ])
    accounts.unlink()


@anthem.log
def import_account_account(ctx):
    """ Import account account
    """
    req = Requirement.parse('depiltech-odoo')
    content = resource_stream(req, 'data/install/CoA/CoA_Boulogne_50.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Nice_RdF_10.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Nice_Tra_15.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Paris3_20.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Paris16_25.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Siege_00.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')
    content = resource_stream(req, 'data/install/CoA/CoA_Toulon_40.csv')
    load_csv_stream(ctx, 'account.account', content, delimiter=',')


@anthem.log
def main(ctx):
    define_auto_generate_invoices_for_companies(ctx)
    configure_missing_chart_of_account(ctx, full_mode=False)
    remove_useless_accounts(ctx)
    import_account_account(ctx)
