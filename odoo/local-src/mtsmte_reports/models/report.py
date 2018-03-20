# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.exceptions import UserError

import logging
import StringIO
import pyPdf


_logger = logging.getLogger(__name__)


class Report(models.Model):
    _inherit = 'report'

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):

        if report_name == 'mtsmte_reports.report_invoice_with_payment_slip':
            invoice = self.env['account.invoice'].browse(docids)
            pdf_to_print = []
            invoice_pdf = super(Report, self).get_pdf(
                docids, 'account.report_invoice', html, data)
            pdf_to_print.append(invoice_pdf)
            # Check with the bvr report is generatable.
            # If yes, add the report to the list of reports to print
            try:
                invoice._check_bvr_generatable()
                payment_slip_pdf = super(Report, self).get_pdf(
                    docids,
                    'l10n_ch_payment_slip.one_slip_per_page_from_invoice',
                    html,
                    data
                )
                pdf_to_print.append(payment_slip_pdf)
            except UserError, e:
                # Do nothing, because in this case,
                # we just display the classic invoice report
                _logger.info(
                    'Impossible to generate BVR report: %s',
                    e.name
                )
            return self.merge_pdf_in_memory(pdf_to_print)
        else:
            return super(Report, self).get_pdf(docids, report_name, html, data)

    def merge_pdf_in_memory(self, docs):
        streams = []
        writer = pyPdf.PdfFileWriter()
        for doc in docs:
            current_buff = StringIO.StringIO()
            streams.append(current_buff)
            current_buff.write(doc)
            current_buff.seek(0)
            reader = pyPdf.PdfFileReader(current_buff)
            for page in xrange(reader.getNumPages()):
                writer.addPage(reader.getPage(page))
        buff = StringIO.StringIO()
        try:
            # The writer close the reader file here
            writer.write(buff)
            return buff.getvalue()
        except IOError:
            raise
        finally:
            buff.close()
            for stream in streams:
                stream.close()
