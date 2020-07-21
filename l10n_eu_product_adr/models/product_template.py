# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, fields, models

LABELS_SELECTION = [
    ("1", "Kl. 2"),
    ("2", "Kl. 2.1"),
    ("3", "Kl. 2.2"),
    ("4", "Kl. 3"),
    ("5", "Kl. 4.1"),
    ("6", "Kl. 4.2"),
    ("7", "Kl. 4.3"),
    ("8", "Kl. 5.1"),
    ("9", "Kl. 5.2"),
    ("10", "Kl. 8"),
    ("11", "Kl. 9"),
    ("12", "Kl. 9A"),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    un_ref = fields.Many2one("un.reference", string="UN Number")
    envir_hazardous = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Environmentally hazardous"
    )
    adr_amount = fields.Char(string="LQ - ADR amount")
    voc = fields.Char(string="VOC in%")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    veg = fields.Monetary(string="VEG in currency")
    nag = fields.Char(string="N.A.G.")
    veva_code_empty = fields.Char(string="VeVA Code: Empty packaging")
    veva_code_full = fields.Char(string="VeVA Code: Full package")
    un_report = fields.Char(string="UN Report 38.3")
    sds = fields.Char(string="SDS")
    content_package = fields.Char(string="Content Packaging")
    flash_point = fields.Char(string="Flash point(°C)")
    h_no = fields.Char(string="H-No")
    hazard_ind = fields.Char(string="Hazard identification")
    dg_unit = fields.Many2one("dangerous.uom", string="DG - Unit")
    packaging_group = fields.Selection(
        [("1", "(-)"), ("2", "I"), ("3", "II"), ("4", "III")], string="Packaging Group"
    )
    transport_category = fields.Selection(
        [("1", "0"), ("2", "1"), ("3", "2"), ("4", "3"), ("5", "4")],
        string="Transport Category",
    )
    tunnel_code = fields.Selection(
        [("1", "(-)"), ("2", "(D)"), ("3", "(E)"), ("4", "(D,E)")], string="Tunnel code"
    )
    label_first = fields.Selection(LABELS_SELECTION, string="Label 1")
    label_second = fields.Selection(LABELS_SELECTION, string="Label 2")
    label_third = fields.Selection(LABELS_SELECTION, string="Label 3")

    class_id = fields.Many2one("great.class")
    limited_amount_id = fields.Many2one("limited.amount")
    storage_class_id = fields.Many2one("storage.class")
    packaging_type_id = fields.Many2one("packaging.type")
    storage_temp_id = fields.Many2one("storage.temp")
    dangerous_selection_id = fields.Many2one("dangerous.goods")
    wgk_class_id = fields.Many2one("wgk.class")

    is_dangerous_good = fields.Boolean(help="This product belongs to a dangerous class")
    is_dangerous_waste = fields.Boolean(
        help="Waste from this product belongs to a dangerous class"
    )
    # dangerous_component_ids = fields.One2many(
    #     "product.dangerous.component",
    #     "product_template_id",
    #     string="Dangerous components",
    # )

    # @api.constrains("dangerous_component_ids")
    # def _check_dangerous_choise(self):
    #     for record in self:
    #         if record.dangerous_component_ids:
    #             raise ValidationError(
    #                 _(
    #                     "Product can not contain dangerous components and \
    #                     belong to a dangerous class at the same time. "
    #                 )
    #             )

    def get_full_class_name(self):
        class_name = "{}".format(self.un_number)
        if self.is_dangerous_waste:
            return _("WASTE ") + class_name
        else:
            return class_name
