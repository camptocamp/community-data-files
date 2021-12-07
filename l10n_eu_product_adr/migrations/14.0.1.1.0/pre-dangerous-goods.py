# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

_logger = logging.getLogger(__name__)

try:
    from openupgradelib import openupgrade
except (ImportError, IOError) as err:
    _logger.debug(err)


PREVIOUS_MODULE_NAME = "l10n_eu_product_adr"
NEW_MODULE_NAME = "l10n_eu_product_adr_dangerous_goods"


QUERY_GET_NAMES = """
    SELECT array_agg(name)
    FROM ir_model_data
    WHERE module = %s
    AND model in %s;
"""

FIELD_NAMES_TO_MOVE = {
    "product.product": [
        "limited_quantity",
        "limited_amount_id",
        "content_package",
        "nag",
        "veva_code_empty",
        "veva_code_full",
        "un_report",
        "storage_class_id",
        "packaging_type_id",
        "storage_temp_id",
        "flash_point",
        "wgk_class_id",
        "h_no",
    ],
}
ACCESS_NAMES_TO_MOVE = [
    "access_storage_class",
    "access_packaging_type",
    "access_storage_temp",
    "access_wgk_class",
    "access_limited_amount",
]
MODELS_TO_MOVE = (
    "storage.class",
    "packaging.type",
    "storage.temp",
    "wgk.class",
    "limited.amount",
)


def move_fields_to_new_module(cr):
    for model, field_names in FIELD_NAMES_TO_MOVE.items():
        openupgrade.update_module_moved_fields(
            cr, model, field_names, PREVIOUS_MODULE_NAME, NEW_MODULE_NAME
        )


def move_records_to_new_module(cr):
    cr.execute(QUERY_GET_NAMES, (PREVIOUS_MODULE_NAME, MODELS_TO_MOVE))
    xmlid_names = cr.fetchall()
    xmlids = [
        (f"{PREVIOUS_MODULE_NAME}.{name}", f"{NEW_MODULE_NAME}.{name}")
        for name in xmlid_names + ACCESS_NAMES_TO_MOVE
    ]
    openupgrade.rename_xmlids(cr, xmlids)


def migrate(cr, version):
    """Move fields and records not present in the new implementation to
    `l10n_eu_product_adr_dangerous_goods`."""
    move_fields_to_new_module(cr)
    move_records_to_new_module(cr)
