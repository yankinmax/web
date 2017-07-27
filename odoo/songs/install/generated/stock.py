# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem
from ...common import (
    load_csv,
    deferred_import,
    deferred_compute_parents
)


@anthem.log
def add_xmlid_to_existing_sequences(ctx):
    # this works if `base_dj` is installed
    model = ctx.env['ir.sequence'].with_context(
        dj_export=1,
        dj_xmlid_fields_map={'ir.sequence': ['prefix', ]},
        dj_multicompany=True
    )
    for item in model.search([]):
        item._dj_export_xmlid()


@anthem.log
def add_xmlid_to_existing_locations(ctx):
    # this works if `base_dj` is installed
    model = ctx.env['stock.location'].with_context(
        dj_export=1,
        dj_xmlid_fields_map={'stock.location': ['name', ]},
        dj_multicompany=True
    )
    for item in model.search([]):
        item._dj_export_xmlid()


@anthem.log
def load_stock_location(ctx):
    add_xmlid_to_existing_locations(ctx)
    deferred_import(
        ctx,
        'stock.location',
        'data/install/generated/stock.location.csv',
        defer_parent_computation=True)


@anthem.log
def location_compute_parents(ctx):
    """Compute parent_left, parent_right"""
    deferred_compute_parents(ctx, 'stock.location')


@anthem.log
def load_stock_picking_type(ctx):
    """ Import stock.picking.type from csv """
    model = ctx.env['stock.picking.type'].with_context({'tracking_disable':1})  # noqa
    header_exclude = ['return_picking_type_id/id']
    load_csv(ctx, 'data/install/generated/stock.picking.type.csv', model, header_exclude=header_exclude)  # noqa
    if header_exclude:
        load_csv(ctx, 'data/install/generated/stock.picking.type.csv', model, header=['id', ] + header_exclude)  # noqa


@anthem.log
def load_stock_location_route(ctx):
    """ Import stock.location.route from csv """
    model = ctx.env['stock.location.route'].with_context({'tracking_disable':1})  # noqa
    load_csv(ctx, 'data/install/generated/stock.location.route.csv', model)


@anthem.log
def load_procurement_rule(ctx):
    """ Import procurement.rule from csv """
    model = ctx.env['procurement.rule'].with_context({'tracking_disable':1})  # noqa
    load_csv(ctx, 'data/install/generated/procurement.rule.csv', model)


@anthem.log
def main(ctx):
    add_xmlid_to_existing_sequences(ctx)
    load_stock_location(ctx)
    load_stock_picking_type(ctx)
    load_stock_location_route(ctx)
    load_procurement_rule(ctx)
