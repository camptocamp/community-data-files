# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class DangerousDeliveryADR(models.AbstractModel):
    _name = (
        'report.l10n_eu_adr_report.report_delivery_dangerous'
    )

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking']
        data = data if data is not None else {}
        picks = docs.browse(docids)
        lines = self._prepare_dangerous_lines(picks)
        docargs = {
            'doc_ids': docs.ids,
            'doc_model': 'stock.picking',
            'docs': picks,
            'data': data.get('form', False),
            # Amount of 7 lines is to satisfy requirements for first page
            # as this amount is fiting A4 page
            'first_page_lines': lines[:7],
            'next_page_lines': lines[7:],
        }
        return docargs

    def _prepare_dangerous_lines(self, pickings):
        vals = []
        for pick in pickings:
            for move_line in pick.move_line_ids:
                product = move_line.product_id
                if product.dangerous_component_ids:
                    for component in product.dangerous_component_ids:
                        vals.append(
                            {
                                'name': component.component_product_id.name,
                                'class': component.dangerous_class.name,
                                'un':
                                component.dangerous_class.class_type.division,
                                'weight': component.weight
                                * move_line.qty_done,
                                'volume': component.volume
                                * move_line.qty_done,
                                'gross_weight': move_line.move_id.weight,
                            }
                        )
                elif product.dangerous_class:
                    vals.append(
                        {
                            'name': product.name,
                            'class': product.dangerous_class.name,
                            'un': product.dangerous_class.class_type.division,
                            'weight': move_line.qty_done,
                            'volume': move_line.qty_done,
                            'gross_weight': move_line.move_id.weight,
                        }
                    )
                if (
                    product.is_dangerous_waste
                    or component.component_product_id.is_dangerous_waste
                ):
                    vals[-1]['class'] = 'WASTE ' + vals[-1]['class']
        return vals
