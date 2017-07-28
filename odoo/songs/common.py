# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement, resource_stream

from anthem.lyrics.records import add_xmlid, switch_company
from anthem.lyrics.loaders import load_csv_stream

import os

req = Requirement.parse('mtsmte-odoo')


def load_file_content(path):
    return resource_stream(req, path)


def load_csv(ctx, path, model, delimiter=',',
             header=None, header_exclude=None):
    content = resource_stream(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter,
                    header=header, header_exclude=header_exclude)


def load_users_csv(ctx, path, delimiter=','):
    # make sure we don't send any email
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, path, model, delimiter=delimiter)


def load_warehouses(ctx, company, path):
    # in multicompany moded we must force the company
    # otherwise the sequences that stock module generates automatically
    # will have the wrong company assigned.
    with switch_company(ctx, company) as ctx:
        load_csv(ctx, path, 'stock.warehouse')
        # NOTE: dirty hack here.
        # We are forced to load the CSV twice because
        # if you are modifying the existing base warehouse (stock.warehouse0)
        # and you've changed the `code` (short name)
        # the changes are not reflected on existing sequences
        # until you load warehouse data again.
        # We usually don't have that many WHs so... it's fine :)
        load_csv(ctx, path, 'stock.warehouse')


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


def get_files(default_file):
    """ Check if there is a DATA_DIR in environment else open default_file.

    DATA_DIR is passed by importer.sh when importing splitted file in parallel

    Returns a generator of file to import as DATA_DIR can contain a split of
    csv file
    """
    try:
        dir_path = os.environ['DATA_DIR']
    except KeyError:
        yield resource_stream(req, default_file)
    else:
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            yield open(file_path)


def deferred_import(ctx, model, csv_path,
                    defer_parent_computation=True,
                    delimiter=','):
    """Use me to load heavy files.

    Usage::

        @anthem.log
        def setup_locations(ctx):
            deferred_import(
                ctx,
                'stock.location',
                'data/install/stock.location.csv',
                defer_parent_computation=True)

    Then in `migration.yml`::

        - importer.sh songs.install.inventory::setup_locations /opt/odoo/data/install/stock.location.csv
        # if defer_parent_computation=True
        - anthem songs.install.inventory::location_compute_parents

    """ # noqa
    load_ctx = ctx.env.context.copy()
    if defer_parent_computation:
        load_ctx.update({'defer_parent_store_computation': 'manually'})
    if isinstance(model, basestring):
        model = ctx.env[model]
    Model = model.with_context(load_ctx)
    for content in get_files(csv_path):
        load_csv_stream(ctx, Model, content, delimiter=delimiter)


def deferred_compute_parents(ctx, model):
    """Use me for heavy files after calling `deferred_import`.

    Usage::

        @anthem.log
        def location_compute_parents(ctx):
            deferred_compute_parents(ctx, 'stock.location')

    """
    ctx.env[model]._parent_store_compute()
