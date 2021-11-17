# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# Copyright 2021 Opener B.V. <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dangerous = fields.Boolean(help="This product belongs to a dangerous class")
    adr_goods_id = fields.Many2one("adr.goods", "Dangerous Goods")
    adr_class_id = fields.Many2one(
        "adr.class",
        related="adr_goods_id.class_id",
    )
    adr_classification_code = fields.Char(
        related="adr_goods_id.classification_code",
    )
    adr_label_ids = fields.Many2many(
        "adr.label",
        related="adr_goods_id.label_ids",
    )
    adr_limited_quantity = fields.Char(
        related="adr_goods_id.limited_quantity",
    )
    adr_packing_instruction_ids = fields.Many2many(
        "adr.packing.instruction",
        related="adr_goods_id.packing_instruction_ids",
    )
    adr_transport_category = fields.Selection(
        related="adr_goods_id.transport_category",
    )
    adr_tunnel_restriction_code = fields.Selection(
        related="adr_goods_id.tunnel_restriction_code",
    )

    @api.onchange("is_dangerous")
    def onchange_is_dangerous(self):
        """Remove the dangerous goods attribute from the product

        (when is_dangerous is deselected)
        """
        if not self.is_dangerous and self.adr_goods_id:
            self.adr_goods_id = False
