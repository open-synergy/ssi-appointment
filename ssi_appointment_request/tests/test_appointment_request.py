# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestAppointmentRequest(YamlTransactionCase):
    def test_appointment_request(self):
        self.run_yaml_scenario("test_data_appointment_request.yaml")

    def test_onchange_appointment_request(self):
        """Test onchange methods on appointment_request."""
        appt_type = self.env["appointment_type"].create(
            {
                "name": "Onchange Request Type",
                "code": "ORT",
                "request_date_offset": 3,
            }
        )
        company = self.env["res.partner"].create(
            {
                "name": "Test Company OC",
                "is_company": True,
            }
        )
        contact = self.env["res.partner"].create(
            {
                "name": "Test Contact OC",
                "is_company": False,
                "parent_id": company.id,
            }
        )
        form = Form(self.env["appointment_request"])
        form.title = "Onchange Test Request"
        form.partner_id = contact
        form.type_id = appt_type
        form.date = fields.Date.today()
        # date_offset should be set by onchange_date_offset
        self.assertEqual(form.date_offset, 3)
        # Setting another type resets date_offset
        another_type = self.env["appointment_type"].create(
            {
                "name": "Another Request Type",
                "code": "ART",
                "request_date_offset": 5,
            }
        )
        form.type_id = another_type
        self.assertEqual(form.date_offset, 5)
        # appointee_id should be cleared when type_id changes
        self.assertFalse(form.appointee_id._origin)
