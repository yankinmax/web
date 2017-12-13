# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProjectProject(models.Model):
    # TODO: shall we move this to mtsmte_project (at least part of it)?
    _inherit = 'project.project'

    client_order_ref = fields.Char(string='Customer Reference', copy=False)
    reception_date = fields.Date(string='Reception Date')
    analyze_sample = fields.Html(
        string='Samples To Analyze',
    )
    resp_one_id = fields.Many2one(
        'res.users',
        string='Responsible 1',
    )
    resp_two_id = fields.Many2one(
        'res.users',
        string='Responsible 2',
    )
    send_sample_back = fields.Boolean(
        string='Send Samples back',
    )
    conclusion = fields.Html()

    conformity = fields.Selection(
        string="Project conformity",
        selection=[
            ("conform", "Compliant"),
            ("not_conform", "Not compliant"),
            ("warning", "Warning"),
        ],
        compute="_compute_conformity",
        readonly=False,
        store=True,
    )
    sale_order_ids = fields.One2many(
        "sale.order",
        "project_project_id",
        string="Sale order ids",
    )
    expiration_date = fields.Datetime(
        string="Expiration date",
        compute="_compute_expiration",
        readonly=True,
    )
    expiration_respected = fields.Boolean(
        string="Expiration respected",
        compute="_compute_expiration",
        default=True,
        store=True,
    )
    task_quant = fields.Integer(
        string="Tasks",
        compute="_compute_task_quants",
        default=0,
        readonly=True,
    )
    finished_task_quant = fields.Integer(
        string="Completed Tasks",
        compute="_compute_task_quants",
        default=0,
        readonly=True,
    )
    ready_to_print = fields.Boolean(
        string="Project ready to print",
        compute="_compute_task_quants",
        readonly=True,
        store=True,
    )

    @api.multi
    @api.depends("task_ids", "task_ids.stage_id")
    def _compute_task_quants(self):
        for record in self:
            if record.task_ids:
                task_quant = len(record.task_ids)
                finished_task_quant = len(
                    record.task_ids.filtered("stage_id.final_stage")
                )
                ready_to_print = task_quant == finished_task_quant
                record.update({
                    'task_quant': task_quant,
                    'finished_task_quant': finished_task_quant,
                    'ready_to_print': ready_to_print,
                })

    @api.multi
    @api.depends('sale_order_ids.commitment_date',
                 'task_ids.date_deadline')
    def _compute_expiration(self):
        for record in self:
            if record.sale_order_ids:
                commitment_date = record.sale_order_ids.sorted(
                    key=lambda r: r.commitment_date,
                    reverse=True,
                )[0].commitment_date
                val = fields.Datetime.from_string(
                    commitment_date
                ).date()
                deadlines = record.task_ids.mapped("date_deadline")
                record.update({
                    'expiration_date': commitment_date,
                    'expiration_respected': all(
                        [fields.Date.from_string(x) < val for x in deadlines
                         if x]
                    )
                })

    def write(self, vals):
        for proj in self:
            if 'resp_one_id' in vals:
                self.message_subscribe_users(vals['resp_one_id'])
            if 'resp_two_id' in vals:
                self.message_subscribe_users(vals['resp_two_id'])
        return super(ProjectProject, self).write(vals)

    @api.depends("task_ids.conformity")
    def _compute_conformity(self):
        for record in self:
            conformities = record.mapped("task_ids.conformity")
            if "not_conform" in conformities:
                record.conformity = "not_conform"
            elif "warning" in conformities:
                record.conformity = "warning"
            else:
                record.conformity = "conform"
