# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement, resource_stream

from anthem.lyrics.records import add_xmlid
from anthem.lyrics.loaders import load_csv_stream


req = Requirement.parse('mtsmte-odoo')


def load_file_content(path):
    return resource_stream(req, path)


def load_chart_of_accounts(ctx, company_xmlid, filepath):
    """ Import Chart of Accounts """
    company = ctx.env.ref(company_xmlid)
    suffix = company_xmlid.replace('.', '_')

    def account_xmlid(base):
        """ Generate an xmlid including the company xmlid

        For instance, the xmlid for the account 1100 for company
        'base.main_company' will be:
        __setup__.l10n_ch_coa_original_1100_base_main_company
        """
        return '_'.join([base, suffix])

    if not ctx.env.ref(account_xmlid('__setup__.l10n_ch_coa_original_1100'),
                       raise_if_not_found=False):
        # First install: the default l10n_ch chart has been
        # automatically installed, we'll clean the accounts
        # but the mandatory ones (used by taxes, properties, ...)

        # We don't have xmlids on the accounts because they have
        # been generated from the templates. We create a XMLID
        # from the account's code as defined in the default template.
        # So we'll have a consistent way to link the usual accounts
        company_accounts = ctx.env['account.account'].search(
            [('company_id', '=', company.id)]
        )
        for account in company_accounts:
            base_xmlid = '__setup__.l10n_ch_coa_original_%s' % account.code
            add_xmlid(ctx, account, account_xmlid(base_xmlid))

        # We want to keep those accounts because they are required
        # by the system (taxes and so on).
        # As we have added XMLIDs on them, we can safely change their
        # code (and other fields) in 'account.account.csv'.
        # All the other accounts will be removed and imported
        # from 'account.account.csv'
        required_account_codes = ('1100', '1170', '1171', '2000', '2200',
                                  '3200', '4200', '3806', '4906', '1090',
                                  '1001', '1021', '999999')
        required_accounts = ctx.env['account.account'].browse()
        for code in required_account_codes:
            required_accounts |= ctx.env.ref(
                account_xmlid('__setup__.l10n_ch_coa_original_%s' % code)
            )

        other_accounts = ctx.env['account.account'].search(
            [('id', 'not in', required_accounts.ids),
             ('company_id', '=', company.id)]
        )
        other_accounts.unlink()

    # Import the custom chart of account.
    # To modify a required account (1100, 2000, ...), XMLID in the
    # following form should be used in the file:
    # __setup__.l10n_ch_coa_original_xxxx
    with ctx.log('Import Accounts for company %s' % company.name):
        csv_content = resource_stream(req, filepath)
        load_csv_stream(ctx, 'account.account', csv_content)


def load_users_csv(ctx, content, delimiter=','):
    # make sure we don't send any email
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv_stream(ctx, model, content, delimiter=delimiter)
