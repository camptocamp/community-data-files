# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # To be set manually for the moment. Could eventually be computed after,
    # depending on the dangerous class and the product's weight/captain'sage…
    limited_quantity = fields.Boolean()

    # package-related fields
    content_package = fields.Float(string="Content Packaging")
    nag = fields.Char(string="N.A.G.")
    veva_code_empty = fields.Char(string="VeVA Code: Empty packaging")
    veva_code_full = fields.Char(string="VeVA Code: Full package")
    un_report = fields.Char(string="UN Report 38.3")

    # storage-related fields
    storage_class_id = fields.Many2one("storage.class")
    packaging_type_id = fields.Many2one("packaging.type")
    storage_temp_id = fields.Many2one("storage.temp")
    flash_point = fields.Char(string="Flash point(°C)")
    wgk_class_id = fields.Many2one("wgk.class")
    h_no = fields.Char(string="H-No")  # Ho, NoooOOooooO!
