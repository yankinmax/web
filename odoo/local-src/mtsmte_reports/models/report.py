# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.exceptions import UserError

import logging


_logger = logging.getLogger(__name__)


class Report(models.Model):
    _inherit = 'report'

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):
        if report_name == 'mtsmte_reports.report_invoice_with_payment_slip':
            return self._get_pdf_for_invoice_with_payment_slip(
                docids, html=html, data=data,
            )
        else:
            return super(Report, self).get_pdf(docids, report_name, html, data)

    def _get_pdf_for_invoice_with_payment_slip(
            self, docids, html=None, data=None):
        """Generate PDF for invoice + payslip and merge them."""
        invoice = self.env['account.invoice'].browse(docids)
        pdf_to_print = []
        invoice_pdf = super(Report, self).get_pdf(
            docids, 'account.report_invoice', html=html, data=data)
        pdf_to_print.append(invoice_pdf)
        # Check with the bvr report is generatable.
        # If yes, add the report to the list of reports to print
        try:
            invoice._check_bvr_generatable()
            payment_slip_pdf = super(Report, self).get_pdf(
                docids,
                'l10n_ch_payment_slip.one_slip_per_page_from_invoice',
            )
            pdf_to_print.append(payment_slip_pdf)
        except UserError, e:
            # Do nothing, because in this case,
            # we just display the classic invoice report
            _logger.info(
                'Impossible to generate BVR report: %s',
                e.name
            )
        # `merge_pdf_in_memory` comes from `l10n_ch_payment_slip`
        return self.merge_pdf_in_memory(pdf_to_print)
