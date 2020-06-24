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
            # Amount of 7 lines is to satisfy requirements for first page
            # as this amount is fiting A4 page
            "first_page_lines": lines[:7],
            "next_page_lines": lines[7:],
        }
        return docargs

    def _prepare_dangerous_lines(self, pickings):
        # TODO report needs fixing as for now it cannot prepare any values for
        # the report
        pass
        # vals = []
        # pickings.ensure_one()
        # for move_line in pickings.move_line_ids:
        #     if move_line.product_id.dangerous_component_ids:
        #         vals += self._get_dangerous_class_line_vals(move_line)
        # return vals

    def _get_dangerous_class_line_vals(self, move):
        vals = []
        for component in move.product_id.dangerous_component_ids:
            product = component.component_product_id
            vals.append(
                {
                    "name": product.name,
                    "class": product.get_full_class_name(),
                    "gross_weight": move.move_id.weight,
                }
            )
        return vals
