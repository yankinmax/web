# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
import StringIO
import pyPdf


class Report(models.Model):

    _inherit = 'report'

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):

        if report_name == 'discount_program_report.report_sale_order_voucher':
            sale_order_pdf = super(Report, self).get_pdf(
                docids, 'sale.report_saleorder', html, data)
            sale_order = self.env['sale.order'].browse(docids)
            voucher_pdfs = []
            for voucher in sale_order.generated_voucher_ids:
                if voucher.is_printable and voucher.type == 'voucher':
                    voucher_pdf = super(Report, self).get_pdf(
                        [voucher.id],
                        'discount_program_report.report_discountprogram',
                        html, data)
                    if voucher_pdf:
                        voucher_pdfs.append(voucher_pdf)
            return self.merge_pdf_in_memory([sale_order_pdf] + voucher_pdfs)

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
