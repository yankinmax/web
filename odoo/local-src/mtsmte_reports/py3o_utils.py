# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.report_py3o.models.py3o_report import py3o_report_extender
from genshi.core import Markup
from lxml import html

LINE_BREAK_TAGS = (
    'p', 'div',
)


def format_py3o_val(value):
    """Format html value to keep minimal formatting as line breaks."""
    placeholder = '##LINE-BREAK##'
    for tag in LINE_BREAK_TAGS:
        open_tag = '<%s>' % tag
        close_tag = '</%s>' % tag
        value = value.replace(
            open_tag, placeholder + open_tag
        ).replace(close_tag, close_tag + placeholder)
    doc = html.fromstring(value)
    # drop all html tags and then keep line breaks w/ the placeholder
    odt_value = '\n'.join([
        x.strip() for x in doc.text_content().splitlines() if x.strip()])
    return Markup(odt_value.replace(placeholder, '\n<text:line-break />'))


@py3o_report_extender()
def add_formatters(report_xml, localcontext):
    localcontext['format_py3o_val'] = format_py3o_val
