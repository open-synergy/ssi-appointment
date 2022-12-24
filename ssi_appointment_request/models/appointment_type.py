# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AppointmentType(models.Model):
    _name = "appointment_type"
    _inherit = [
        "appointment_type",
    ]

    request_date_offset = fields.Integer(
        string="Appointment Request Date Offset",
        default=1,
    )
