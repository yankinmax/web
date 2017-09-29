# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem


@anthem.log
def sale_config_settings(ctx):
    """ Setup sale.config.settings """
    model = ctx.env['sale.config.settings'].with_context({
        'tracking_disable': 1
    })
    with open(
            "./odoo/data/install/generated/sale_config_sale_note.txt"
    ) as sale_note:
        model.create({
            # Default Terms and Conditions *  # noqa
            'sale_note': sale_note.read(),
            # Tax Display: Show line subtotals without taxes (B2B)  # noqa
            'sale_show_tax': 'subtotal',
            # Sales Safety Days *  # noqa
            'security_lead': 0.0,
            # Deposit Product  # noqa
            'deposit_product_id_setting': False,
            # Sale pricelist setting: Advanced pricing based on formulas (discounts, margins, rounding)  # noqa
            'sale_pricelist_setting': 'formula',
            # Incoterms: No incoterm on reports  # noqa
            'group_display_incoterm': False,
            # Show pricelists to customers  # noqa
            'group_pricelist_item': True,
            # Date: Allow to modify the sales order dates to postpone deliveries and procurements  # noqa
            'module_sale_order_dates': 1,
            # Shipping: No shipping costs on sales orders  # noqa
            'module_delivery': False,
            # Product Variants: No variants on products  # noqa
            'group_product_variant': False,
            # Warning: All the products and the customers can be used in sales orders  # noqa
            'group_warning_sale': False,
            # Properties on SO Lines: Don't use manufacturing properties (recommended as its easier)  # noqa
            'group_mrp_properties': False,
            # Online Quotations: Print quotes or send by email  # noqa
            'module_website_quote': False,
            # Order Routing: Choose specific routes on sales order lines (advanced)  # noqa
            'group_route_so_lines': 1,
            # Company  # noqa
            'company_id': ctx.env.ref('__setup__.company_mte').id,
            # Default Invoicing: Invoice ordered quantities  # noqa
            'default_invoice_policy': 'order',
            # Sales Reports Layout: Do not personalize sales orders and invoice reports  # noqa
            'group_sale_layout': False,
            # Show pricelists On Products  # noqa
            'group_product_pricelist': False,
            # Units of Measure: Some products may be sold/purchased in different units of measure (advanced)  # noqa
            'group_uom': 1,
            # Use pricelists to adapt your price per customers  # noqa
            'group_sale_pricelist': True,
            # Discount: Allow discounts on sales order lines  # noqa
            'group_discount_per_so_line': 1,
            # Margins: Salespeople do not need to view margins when quoting  # noqa
            'module_sale_margin': False,
            # Sale Order Modification: Allow to edit sales order from the 'Sales Order' menu (not from the Quotation menu)  # noqa
            'auto_done_setting': False,
            # Sell digital products - provide downloadable content on your customer portal  # noqa
            'module_website_sale_digital': False,
            # Show total  # noqa
            'group_show_price_total': False,
            # Default Shipping Policy: Ship products when some are available, and allow back orders  # noqa
            'default_picking_policy': False,
            # Show subtotal  # noqa
            'group_show_price_subtotal': True,
            # Addresses: Display 3 fields on sales orders: customer, invoice address, delivery address  # noqa
            'group_sale_delivery_address': 1,
            # Manage subscriptions and recurring invoicing  # noqa
            'module_sale_contract': False,
            # Invoice Timesheets: Invoice all timesheets recorded (approved or not)  # noqa
            'invoiced_timesheet': 'all',

        }).execute()


@anthem.log
def main(ctx):
    sale_config_settings(ctx)
