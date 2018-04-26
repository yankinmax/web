# -*- coding: utf-8 -*-
# Copyright (C) 2018 by Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    # override
    def _create_service_task(self):
        res_task = super(ProcurementOrder, self)._create_service_task()
        # grab a responsible from product
        # if no one is in charge for it, grab a responsible from category
        # NOTE: we don't want neither `manager`s nor `responsible_1`s assigned
        # to tasks, so we pick `responsible_2_id` explicitly
        responsible_user = self.product_id.responsible_2_id \
            or self.product_id.categ_id.responsible_2_id
        if responsible_user:
            res_task.write({
                'user_id': responsible_user.id,
            })
        return res_task
