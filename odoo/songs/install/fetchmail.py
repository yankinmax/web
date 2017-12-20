# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def update_incoming_mail_servers(ctx):
    """create crm.lead when a new email arrives."""
    mail_servers = ctx.env["fetchmail.server"].search([])
    lead_model = ctx.env.ref("crm.model_crm_lead")
    mail_servers.write({
        "object_id": lead_model.id,
    })


@anthem.log
def main(ctx):
    update_incoming_mail_servers(ctx)
