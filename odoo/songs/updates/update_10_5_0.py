# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import anthem
from anthem.lyrics.modules import uninstall


@anthem.log
def uninstall_module(ctx):
    """Uninstall module 'base_dj'"""
    uninstall(ctx, ['base_dj'])


@anthem.log
def main(ctx):
    """Applying update 10.5.0"""
    uninstall_module(ctx)
