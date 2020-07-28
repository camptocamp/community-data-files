# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class DangerousDeliveryADR(models.AbstractModel):
    _name = "report.l10n_eu_adr_report.report_delivery_dangerous"
    _description = "Dangerous Delivery Report ADR"

    def _get_report_values(self, docids, data=None):
        docs = self.env["stock.picking"]
        data = data or {}
        docs = self.env["stock.picking"].browse(docids)
        lines = self._prepare_dangerous_lines(docs)
        docargs = {
            "doc_ids": docs.ids,
            "doc_model": "stock.picking",
            "docs": docs,
            "data": data.get("form", False),
            "page_lines": lines,
        }
        return docargs

    def _prepare_dangerous_lines(self, pickings):
        vals = []
        pickings.ensure_one()
        for move_line in pickings.move_line_ids:
            if move_line.product_id.is_dangerous:
                vals += self._get_dangerous_class_line_vals(move_line)
        return vals

    def _get_dangerous_class_line_vals(self, move):
        product = move.product_id
        return [
            {
                "name": product.name,
                "class": product.product_tmpl_id.get_full_class_name(),
                # quantity_done
                "move_amount": move.move_id.product_uom_qty,
                "product_weight": product.content_package,
            }
        ]
