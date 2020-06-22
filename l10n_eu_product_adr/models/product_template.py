# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    un_number = fields.Char(string="UN Number", size=4)
    is_dangerous_good = fields.Boolean(help="This product belongs to a dangerous class")
    is_dangerous_waste = fields.Boolean(
        help="Waste from this product belongs to a dangerous class"
    )
    dangerous_component_ids = fields.One2many(
        "product.dangerous.component",
        "product_template_id",
        string="Dangerous components",
    )

    _sql_constraints = [
        ("un_number_unique", "unique(un_number)", "This UN code already exist")
    ]

    @api.constrains("dangerous_component_ids")
    def _check_dangerous_choise(self):
        for record in self:
            if record.dangerous_component_ids:
                raise ValidationError(
                    _(
                        "Product can not contain dangerous components and \
                        belong to a dangerous class at the same time. "
                    )
                )

    def get_full_class_name(self):
        class_name = "{}".format(self.un_number)
        if self.is_dangerous_waste:
            return _("WASTE ") + class_name
        else:
            return class_name