# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..install.generated.stock import load_ir_sequence, load_res_partner


@anthem.log
def main(ctx):
    load_ir_sequence(ctx)
    load_res_partner(ctx)
