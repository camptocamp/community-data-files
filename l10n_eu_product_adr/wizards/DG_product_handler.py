# Copyright 2020 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models
from itertools import groupby

from ..models.product_template import TRANSPORT_CATEGORY


class DGProductCounter(models.TransientModel):
    _name = "dangerous.goods.handler"
    _description = "Wizard to count and prepare data fro dangerous goods report"

    picking_ids = fields.Many2many("stock.picking", string="Pickings")
    # pallet_ids = fields.Many2many('stock.picking', string='Pickings')

    def prepare_DG_data(self):

        vals = {
            "dg_lines": [],
            "total_section": {},
        }
        for pick in self.picking_ids:
            if pick.state == 'done':
                moves = pick.move_lines.filtered(lambda l: l.state == 'done')
            else:
                moves = pick.move_lines

            for move_line in moves:
                if move_line.product_id.is_dangerous:
                    vals["dg_lines"] += self._get_DG_move_line_vals(move_line)

        # for pallet in self.pallet_ids

        vals["dg_lines"] = self._merge_products_data(vals["dg_lines"])
        vals["total_section"] = self._compute_total_points(vals["dg_lines"])
        return vals

    def _compute_total_points(self, vals):
        import pdb
        # pdb.set_trace()

        index = {'1': 0.0, '2': 0.0, '3': 0.0, '4': 0.0, '5': 0.0}
        total_vals = {
            'total_units': index.copy(),
            'factor': index.copy(),
            'mass_points': index.copy(),
            'total_points': 0.0,
        }
        self._init_total_vals(total_vals)

        for k in index.keys():
            total_vals['total_units'][k] = self._sum_values(vals, 'dangerous_amount', k)
            total_vals['mass_points'][k] = total_vals['total_units'][k] * total_vals['factor'][k]

        self._is_limit_exceeded(total_vals)
        return total_vals

    def _sum_values(self, vals, field, index):
        return sum([
            item[field] for item in vals if item['column_index'] == index
        ])

    def _is_limit_exceeded(self, vals):
        vals['warn'] = False
        vals['total_points'] = sum(vals['mass_points'].values())
        if vals['total_points'] > 1000.0:
            vals['warn'] = True

    def _init_total_vals(self, vals):
        vals['factor']['1'] = 0.0
        vals['factor']['2'] = 50.0
        vals['factor']['3'] = 3.0
        vals['factor']['4'] = 1.0
        vals['factor']['5'] = 0.0


    def _merge_products_data(self, vals):
        # merge lines for same product
        # unit measurement on stock is not concidered
        new_vals = []
        grouped_lines = groupby(sorted(vals, key=lambda l: l.get('product_id')), key=lambda l: l.get('product_id'))

        for k, v in grouped_lines:
            lines = list(v)
            new_vals.append(lines[0])
            new_vals[-1]['qty_amount'] = sum([l.get('qty_amount') for l in lines])
            new_vals[-1]['product_weight'] = sum([l.get('product_weight') for l in lines])
            new_vals[-1]['dangerous_amount'] = sum([l.get('dangerous_amount') for l in lines])
            new_vals[-1]['class'] += ', {}, {}, {}, {}'.format(
                new_vals[-1]['qty_amount'],
                new_vals[-1]['packaging_type'].name,
                new_vals[-1]['dangerous_amount'],
                new_vals[-1]['dg_unit'],
            )

        return new_vals

    def _get_DG_move_line_vals(self, move):
        product = move.product_id
        if move.state == 'done':
            qty = move.quantity_done
        else:
            qty = move.product_uom_qty
        return [
            {
                "product": product,
                "product_id": product.id,
                "dg_unit": product.dg_unit.name,
                "class": product.product_tmpl_id.get_full_class_name(),
                "packaging_type": product.packaging_type_id,
                "qty_amount": qty,
                "product_weight": product.content_package,
                "column_index": str(product.transport_category),
                "dangerous_amount": qty * product.content_package,
            }
        ]

    def _get_DG_pallet_vals(self, pallet):
        return []
