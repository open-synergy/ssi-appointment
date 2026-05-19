# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Appointment - Work Log Integration",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": (
        "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia,"
        " Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_appointment",
        "ssi_work_log_mixin",
    ],
    "data": [
        "views/appointment_type_views.xml",
    ],
    "demo": [],
    "images": [],
}
