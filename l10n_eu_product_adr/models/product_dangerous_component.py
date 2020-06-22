# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductDangerousComponent(models.Model):
    _name = "product.dangerous.component"
    _description = "Product Dangerous Component"

    product_template_id = fields.Many2one(
        comodel_name="product.template", required=True, ondelete="cascade"
    )