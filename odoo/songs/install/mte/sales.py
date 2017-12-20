# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem

from ...common import set_sale_conditions


@anthem.log
def set_sale_conditions_MTE(ctx):
    """ Set sale description """
    company_mte = ctx.env.ref('__setup__.company_mte')
    conditions = [
        # lang, filepath
        ('de_DE', 'data/install/mte/mte_sale_conditions_de.html'),
        ('en_US', 'data/install/mte/mte_sale_conditions_en.html'),
        ('fr_FR', 'data/install/mte/mte_sale_conditions_fr.html'),
    ]
    set_sale_conditions(ctx, company_mte, conditions)


@anthem.log
def main(ctx):
    """ Configuring Sales settings MTE """
    set_sale_conditions_MTE(ctx)
