# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def update_project_task_type(ctx):
    """ Deactivate project task installed by default and keep
        the ones installed by specific_module """
    task_types = ctx.env['project.task.type'].search([])
    for task_type in task_types:
        if 'mtsmte_project' not in task_type.get_external_id().values()[0]:
            task_type.write({'active': False,
                             'case_default': False})


@anthem.log
def main(ctx):
    """ Configuring Project """
    update_project_task_type(ctx)
