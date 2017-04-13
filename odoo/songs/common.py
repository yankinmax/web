# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement, resource_stream
from anthem.lyrics.loaders import load_csv_stream


req = Requirement.parse('depiltech-odoo')


def load_csv(ctx, path, model, delimiter=','):
    content = resource_stream(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter)


def define_settings(ctx, model, values):
    """ Define settings like being in the interface
     Example :
      - model = 'sale.config.settings'
      - values = {'default_invoice_policy': 'delivery'}
     Be careful, settings onchange are not triggered with this function.
    """
    ctx.env[model].create(values).execute()
