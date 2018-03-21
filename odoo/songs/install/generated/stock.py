# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem
from ...common import load_csv


@anthem.log
def load_ir_sequence(ctx):
    """ Import ir.sequence from csv """
    model = ctx.env['ir.sequence'].with_context({'tracking_disable': 1})  # noqa
    load_csv(ctx, 'data/install/generated/ir.sequence.csv', model)


@anthem.log
def stock_config_settings_MT(ctx):
    """ Setup stock.config.settings for Metallo-Tests S.A. """
    model = ctx.env['stock.config.settings'].with_context(
        {'tracking_disable': 1})
    model.create({
        # Landed Costs: No landed costs  # noqa
        'module_stock_landed_costs': False,
        # Inventory Valuation: Periodic inventory valuation (recommended)  # noqa
        'group_stock_inventory_valuation': False,
        # Minimum Stock Rules: Set lead times in calendar days (easy)  # noqa
        'module_stock_calendar': False,
        # Barcode scanner support  # noqa
        'module_stock_barcode': False,
        # Picking Waves: Manage pickings one at a time  # noqa
        'module_stock_picking_wave': False,
        # Company  # noqa
        'company_id': ctx.env.ref('__setup__.company_mte').id,
        # Packages: Do not manage packaging  # noqa
        'group_stock_tracking_lot': False,
        # Product Variants: No variants on products  # noqa
        'group_product_variant': False,
        # Warning: All the partners can be used in pickings  # noqa
        'group_warning_stock': False,
        # Temando integration  # noqa
        'module_delivery_temando': False,
        # Lots and Serial Numbers: Do not track individual product items  # noqa
        'group_stock_production_lot': False,
        # Manage several warehouses  # noqa
        'group_stock_multi_warehouses': False,
        # Product Owners: All products in your warehouse belong to your company  # noqa
        'group_stock_tracking_owner': False,
        # Minimum days to trigger a propagation of date change in pushed/pull flows.  # noqa
        'propagation_minimum_delta': 1,
        # USPS integration  # noqa
        'module_delivery_usps': False,
        # Dropshipping: Suppliers always deliver to your warehouse(s)  # noqa
        'module_stock_dropshipping': False,
        # Quality  # noqa
        'module_quality': False,
        # Procurements: Reserve products immediately after the sale order confirmation  # noqa
        'module_procurement_jit': 1,
        # Packaging Methods: Do not manage packaging  # noqa
        'group_stock_packaging': False,
        # Fedex integration  # noqa
        'module_delivery_fedex': False,
        # Decimal precision on weight  # noqa
        'decimal_precision': 0,
        # Units of Measure: Some products may be sold/purchased in different units of measure (advanced)  # noqa
        'group_uom': 1,
        # Warehouses and Locations usage level: Manage only 1 Warehouse, composed by several stock locations  # noqa
        'warehouse_and_location_usage_level': 1,
        # UPS integration  # noqa
        'module_delivery_ups': False,
        # Expiration Dates: Do not use Expiration Date on serial numbers  # noqa
        'module_product_expiry': False,
        # Manage several stock locations  # noqa
        'group_stock_multi_locations': True,
        # Routes: Advanced routing of products using rules  # noqa
        'group_stock_adv_location': 1,
        # DHL integration  # noqa
        'module_delivery_dhl': False,

    }).execute()


@anthem.log
def stock_config_settings_MTS(ctx):
    """ Setup stock.config.settings for MTS Materiaux Technologies Surfaces SA
    """
    model = ctx.env['stock.config.settings'].with_context(
        {'tracking_disable': 1})
    model.create({
        # Landed Costs: No landed costs  # noqa
        'module_stock_landed_costs': False,
        # Inventory Valuation: Periodic inventory valuation (recommended)  # noqa
        'group_stock_inventory_valuation': False,
        # Minimum Stock Rules: Set lead times in calendar days (easy)  # noqa
        'module_stock_calendar': False,
        # Barcode scanner support  # noqa
        'module_stock_barcode': False,
        # Picking Waves: Manage pickings one at a time  # noqa
        'module_stock_picking_wave': False,
        # Company  # noqa
        'company_id': ctx.env.ref('base.main_company').id,
        # Packages: Do not manage packaging  # noqa
        'group_stock_tracking_lot': False,
        # Product Variants: No variants on products  # noqa
        'group_product_variant': False,
        # Warning: All the partners can be used in pickings  # noqa
        'group_warning_stock': False,
        # Temando integration  # noqa
        'module_delivery_temando': False,
        # Lots and Serial Numbers: Do not track individual product items  # noqa
        'group_stock_production_lot': 1,
        # Manage several warehouses  # noqa
        'group_stock_multi_warehouses': False,
        # Product Owners: All products in your warehouse belong to your company  # noqa
        'group_stock_tracking_owner': False,
        # Minimum days to trigger a propagation of date change in pushed/pull flows.  # noqa
        'propagation_minimum_delta': 0,
        # USPS integration  # noqa
        'module_delivery_usps': False,
        # Dropshipping: Suppliers always deliver to your warehouse(s)  # noqa
        'module_stock_dropshipping': False,
        # Quality  # noqa
        'module_quality': False,
        # Procurements: Reserve products immediately after the sale order confirmation  # noqa
        'module_procurement_jit': 1,
        # Packaging Methods: Do not manage packaging  # noqa
        'group_stock_packaging': False,
        # Fedex integration  # noqa
        'module_delivery_fedex': False,
        # Decimal precision on weight  # noqa
        'decimal_precision': 0,
        # Units of Measure: Some products may be sold/purchased in different units of measure (advanced)  # noqa
        'group_uom': 1,
        # Warehouses and Locations usage level: Manage only 1 Warehouse, composed by several stock locations  # noqa
        'warehouse_and_location_usage_level': 1,
        # UPS integration  # noqa
        'module_delivery_ups': False,
        # Expiration Dates: Do not use Expiration Date on serial numbers  # noqa
        'module_product_expiry': False,
        # Manage several stock locations  # noqa
        'group_stock_multi_locations': True,
        # Routes: Advanced routing of products using rules  # noqa
        'group_stock_adv_location': 1,
        # DHL integration  # noqa
        'module_delivery_dhl': False,

    }).execute()


@anthem.log
def stock_config_settings(ctx):
    stock_config_settings_MT(ctx)
    stock_config_settings_MTS(ctx)


@anthem.log
def add_xmlid_to_existing_stock_location(ctx):
    # this works if `base_dj` is installed
    model = ctx.env['stock.location'].with_context(
        dj_xmlid_fields_map={'stock.location': []},
        dj_multicompany=True,
    )
    for item in model.search([]):
        item._dj_export_xmlid()


@anthem.log
def load_stock_location(ctx):
    """ Import stock.location from csv """
    model = ctx.env['stock.location'].with_context({'tracking_disable': 1})  # noqa
    header_exclude = ['location_id/id', ]
    load_csv(ctx, 'data/install/generated/stock.location.csv', model, header_exclude=header_exclude)  # noqa
    if header_exclude:
        load_csv(ctx, 'data/install/generated/stock.location.csv', model, header=['id', ] + header_exclude)  # noqa


@anthem.log
def add_xmlid_to_existing_ir_sequence(ctx):
    # this works if `base_dj` is installed
    model = ctx.env['ir.sequence'].with_context(
        dj_xmlid_fields_map={'ir.sequence': []},
        dj_multicompany=True,
    )
    for item in model.search([]):
        item._dj_export_xmlid()


@anthem.log
def load_stock_picking_type(ctx):
    """ Import stock.picking.type from csv """
    model = ctx.env['stock.picking.type'].with_context({'tracking_disable': 1})  # noqa
    header_exclude = ['return_picking_type_id/id', ]
    load_csv(ctx, 'data/install/generated/stock.picking.type.csv', model, header_exclude=header_exclude)  # noqa
    if header_exclude:
        load_csv(ctx, 'data/install/generated/stock.picking.type.csv', model, header=['id', ] + header_exclude)  # noqa


@anthem.log
def load_stock_location_route(ctx):
    """ Import stock.location.route from csv """
    model = ctx.env['stock.location.route'].with_context({'tracking_disable': 1})  # noqa
    load_csv(ctx, 'data/install/generated/stock.location.route.csv', model)


@anthem.log
def load_res_partner(ctx):
    """ Import res.partner from csv """
    model = ctx.env['res.partner'].with_context({'tracking_disable': 1})  # noqa
    header_exclude = ['parent_id/id']
    load_csv(ctx, 'data/install/generated/res.partner.csv', model, header_exclude=header_exclude)  # noqa
    if header_exclude:
        load_csv(ctx, 'data/install/generated/res.partner.csv', model, header=['id', ] + header_exclude)  # noqa


@anthem.log
def load_procurement_rule(ctx):
    """ Import procurement.rule from csv """
    model = ctx.env['procurement.rule'].with_context({'tracking_disable': 1})  # noqa
    load_csv(ctx, 'data/install/generated/procurement.rule.csv', model)


@anthem.log
def main(ctx):
    load_ir_sequence(ctx)
    stock_config_settings(ctx)
    add_xmlid_to_existing_stock_location(ctx)
    load_stock_location(ctx)
    add_xmlid_to_existing_ir_sequence(ctx)
    load_stock_picking_type(ctx)
    load_stock_location_route(ctx)
    load_res_partner(ctx)
    load_procurement_rule(ctx)
