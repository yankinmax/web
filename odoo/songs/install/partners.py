# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import deferred_import, deferred_compute_parents


@anthem.log
def import_partners(ctx):
    model = ctx.env['res.partner'].with_context({'tracking_disable': 1})
    deferred_import(ctx, model, 'data/install/res.partner.csv')


@anthem.log
def import_partners_contacts(ctx):
    model = ctx.env['res.partner'].with_context({'tracking_disable': 1})
    deferred_import(ctx, model, 'data/install/res.partner.contact.csv')


@anthem.log
def partner_compute_parents(ctx):
    """Compute parent_left, parent_right"""
    deferred_compute_parents(ctx, 'res.partner')


@anthem.log
def main(ctx):
    """ Configuring partners """
    # import_partners, import_partners_contacts, partner_compute_parents
    # are not needed here as we delegate imports to `importer.sh`
