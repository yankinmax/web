# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    chemistry = fields.Selection(
        [('chem', 'Chemical Analysis'),
         ('test_env', 'Test Environment'),
         ('test_mec', 'Test Mécanique')],
    )
    product_substance_line_ids = fields.One2many(
        'product.substance.line',
        'product_id',
        string='Substance lines'
    )
    test_parameters = fields.Html(
        string='Test Parameters',
        translate=True,
    )
    applied_dose = fields.Html(
        string='Applied Dose',
    )
    duration = fields.Html(
        string='Duration',
    )
    nb_shocks = fields.Html(
        string='Number of Shocks',
    )
    results = fields.Html(
        string='Results',
        translate=True,
    )
    product_method_id = fields.Many2one(
        'product.method',
        string='Methods',
    )
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipment',
    )
    product_extraction_type_id = fields.Many2one(
        'product.extraction.type',
        string='Extraction Type',
    )

    legal_reference = fields.Html(
        string="Legal reference",
        translate=True,
    )

    def _get_default_category_id(self):
        """Make sure that user don't get categories he has no rights on.

        The original implementation took the product.category by ref
        "product.product_category_all" as a default value for the field
        The problem was, that it is MTS category. So when
        MTE user tries to create a product this produces an error,
        as MTE user has no permissions for MTS category
        The change was to check users company first, and only then place
        an appropriate default value
        """
        if self.env.context.get('categ_id') or self.env.context.get(
                'default_categ_id'
        ):
            return self.env.context.get('categ_id') or self.env.context.get(
                'default_categ_id'
            )
        category = self.env["product.category"].search([
            ("parent_id", "=", False),
            ("company_id", "=", self.env.user.company_id.id)
        ], limit=1)
        return category and category.type == 'normal' and category.id or False

    categ_id = fields.Many2one(
        default=lambda self: self._get_default_category_id()
    )
