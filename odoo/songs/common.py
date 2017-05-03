# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement, resource_stream
from anthem.lyrics.loaders import load_csv_stream

import os


req = Requirement.parse('depiltech-odoo')


def load_csv(ctx, path, model, delimiter=','):
    content = resource_stream(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter)


def load_users_csv(ctx, path, delimiter=','):
    # make sure we don't send any email
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, path, model, delimiter=delimiter)


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
    Model = ctx.env[model].with_context(load_ctx)
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


def define_settings(ctx, model, values):
    """ Define settings like being in the interface
     Example :
      - model = 'sale.config.settings'
      - values = {'default_invoice_policy': 'delivery'}
     Be careful, settings onchange are not triggered with this function.
    """
    ctx.env[model].create(values).execute()
