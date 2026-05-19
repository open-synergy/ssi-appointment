# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestAppointmentSchedule(YamlTransactionCase):
    def test_appointment_schedule(self):
        self.run_yaml_scenario("test_data_appointment_schedule.yaml")

    def test_onchange_appointee_clears_type_fields(self):
        """Changing appointee_id should clear type_id via onchange."""
        time_slot = self.env["appointment_time_slot"].create(
            {
                "name": "09:00 - 10:00",
                "code": "OCT0900",
                "time_start": 9.0,
                "time_end": 10.0,
            }
        )
        appt_type = self.env["appointment_type"].create(
            {
                "name": "Onchange Test Type",
                "code": "OCT",
            }
        )
        user = self.env.ref("base.user_admin")
        form = Form(self.env["appointment_schedule"])
        form.title = "Onchange Test"
        form.appointee_id = user
        form.time_slot_id = time_slot
        form.type_id = appt_type
        # Setting same appointee triggers onchange → type_id cleared
        form.appointee_id = user
        self.assertFalse(form.type_id._origin)

    def test_timeslot_constraint(self):
        """Two schedules with same date/appointee/time_slot should raise."""
        from odoo.exceptions import ValidationError

        time_slot = self.env["appointment_time_slot"].create(
            {
                "name": "11:00 - 12:00",
                "code": "CON1100",
                "time_start": 11.0,
                "time_end": 12.0,
            }
        )
        user = self.env.ref("base.user_admin")
        schedule_vals = {
            "title": "Test Schedule",
            "appointee_id": user.id,
            "time_slot_id": time_slot.id,
            "date": fields.Date.today(),
            "appointment_method": "online",
        }
        self.env["appointment_schedule"].create(schedule_vals)
        with self.assertRaises(ValidationError):
            self.env["appointment_schedule"].create(schedule_vals)
