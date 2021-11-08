# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# Copyright 2021 Opener B.V. <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dangerous = fields.Boolean(help="This product belongs to a dangerous class")
    adr_goods_id = fields.Many2one("adr.goods", "Dangerous Goods")
    adr_class_id = fields.Many2one(
        "adr.class", related="adr_goods_id.class_id", readonly=True
    )
    adr_classification_code = fields.Char(
        related="adr_goods_id.classification_code", readonly=True
    )
    adr_label_ids = fields.Many2many(
        "adr.label", related="adr_goods_id.label_ids", readonly=True
    )
    adr_limited_quantity = fields.Boolean(
        "Limited Qty",
        compute="_compute_adr_limited_quantity",
        # store=True
    )
    adr_packing_instruction_ids = fields.Many2many(
        "adr.packing.instruction",
        related="adr_goods_id.packing_instruction_ids",
        readonly=True,
    )
    adr_transport_category = fields.Selection(
        related="adr_goods_id.transport_category", readonly=True
    )
    adr_tunnel_restriction_code = fields.Selection(
        related="adr_goods_id.tunnel_restriction_code", readonly=True
    )

    @api.onchange("is_dangerous")
    def onchange_is_dangerous(self):
        """Remove the dangerous goods attribute from the product

        (when is_dangerous is deselected)
        """
        if not self.is_dangerous and self.adr_goods_id:
            self.adr_goods_id = False

    @api.depends(
        "adr_goods_id.limited_quantity_uom", "adr_goods_id.limited_quantity", "uom_id"
    )
    def _compute_adr_limited_quantity(self):
        for record in self:
            p_uom = record.uom_id
            adr_uom = record.adr_goods_id.limited_quantity_uom
            if record.is_dangerous and p_uom and adr_uom:
                adr_qty = record.adr_goods_id.limited_quantity
                # TODO not safe with different categories
                qty = p_uom._compute_quantity(
                    adr_qty, record.adr_goods_id.limited_quantity, adr_uom
                )
                record.adr_limited_quantity = record.weight > qty
            else:
                record.adr_limited_quantity = False
