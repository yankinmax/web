# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..install.project import update_task_stage


@anthem.log
def main(ctx):
    update_task_stage(ctx)
