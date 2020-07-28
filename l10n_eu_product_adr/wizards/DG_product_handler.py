# Copyright 2020 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class DGProductCounter(models.TransientModel):
    _name = "dangerous.goods.handler"
    _description = "Wizard to count and prepare data fro dangerous goods report"

    picking_ids = fields.Many2many("stock.picking", string="Pickings")
    # pallet_ids = fields.Many2many('stock.picking', string='Pickings')

    def prepare_DG_data(self):

        vals = {
            "dg_lines": [],
            "total": {},
        }

        for pick in self.picking_ids:
            for move_line in pick.move_line_ids:
                if move_line.product_id.is_dangerous:
                    vals["dg_lines"] += self._get_dangerous_class_line_vals(move_line)

        # for pallet in self.pallet_ids

        vals["dg_lines"] = self._merge_products_data(vals["dg_lines"])
        vals["total"] = self._compute_total_points(vals["dg_lines"])

        return vals

    def _compute_total_points(self, vals):

        return []

    def _merge_products_data(self, vals):
        # merge lines for same unit and product

        return vals

    def _get_DG_move_line_vals(self, move):
        product = move.product_id
        return [
            {
                "name": product,
                "class": product.product_tmpl_id.get_full_class_name(),
                "unit": product.dg_unit,
                # quantity_done
                "move_amount": move.move_id.product_uom_qty,
                "product_weight": product.content_package,
            }
        ]

    def _get_DG_pallet_vals(self, pallet):
        return []
