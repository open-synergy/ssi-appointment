# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AppointmentSchedule(models.Model):
    _name = "appointment_schedule"
    _inherit = [
        "appointment_schedule",
    ]

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )
    auto_create_task = fields.Boolean(
        string="Auto Create Task",
    )
    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
    )

    def action_create_task(self):
        for record in self.sudo():
            record._create_task()

    def action_delete_task(self):
        for record in self.sudo():
            record._delete_task()

    def _delete_task(self):
        self.ensure_one()
        task = self.task_id

        if not task:
            return True

        self.write({"task_id": False})
        task.unlink()

    def _create_task(self):
        self.ensure_one()
        Task = self.env["project.task"]
        if not self.auto_create_task:
            return True

        task = Task.create(self._prepare_create_task())
        self.write({"task_id": task.id})

    def _get_task_timebox(self):
        self.ensure_one()
        Timebox = self.env["task.timebox"]
        criteria = [
            ("date_start", "<=", self.date),
            ("date_end", ">=", self.date),
            ("state", "!=", "done"),
        ]
        timeboxes = Timebox.search(criteria)

        if len(timeboxes) == 0:
            error_message = _(
                """
            Context: Create task from appointment schedule
            Database ID: %s
            Problem: No timebox
            Solution: Create timebox
            """
                % (self.id)
            )
            raise ValidationError(error_message)

        return [(6, 0, timeboxes.ids)]

    def _prepare_create_task(self):
        self.ensure_one()
        return {
            "name": self.name,
            "project_id": self.project_id.id,
            "type_id": self.type_id.task_type_id.id,
            "user_id": self.appointee_id.id,
            "timebox_ids": self._get_task_timebox(),
            "stage_id": self.type_id.task_stage_id
            and self.type_id.task_stage_id.id
            or False,
            "work_estimation": self.type_id.task_type_id.work_estimation,
        }
