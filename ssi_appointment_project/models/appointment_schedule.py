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
    host_id_task_id = fields.Many2one(
        comodel_name="project.task", string="Task Host", required=False
    )
    co_appointee_ids_task_id = fields.Many2many(
        comodel_name="project.task",
        string="Co-Appointees Task",
        relation="rel_co_appointees_2_project_task",
        column1="co_appointee_ids",
        column2="task_id",
        required=False,
    )

    def action_create_task(self):
        for record in self.sudo():
            record._create_task()
            record._create_host()
            record._create_co_appointee()

    def action_delete_task(self):
        for record in self.sudo():
            record._delete_task()
            record._delete_host()
            record._delete_co_appointee()

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

    def _create_host(self):
        self.ensure_one()
        Host = self.env["project.task"]
        if not self.auto_create_task:
            return True
        host = Host.create(
            {
                "host_id_task_id": self.host_id_task_id.id,
                "type_id": self.type_id.host_id_task_type_id.id,
            }
        )
        self.write({"host_id_task_id": host.id})

    def _delete_host(self):
        self.ensure_one()
        host = self.host_id_task_id

        if not host:
            return True

        self.write({"host_id_task_id": False})
        host.unlink()

    def _create_co_appointee(self):
        self.ensure_one()
        Co_appointee = self.env["project.task"]
        if not self.auto_create_task:
            return True
        co_appointee = Co_appointee.create(
            {
                "co_appointee_ids_task_id": self.co_appointee_ids_task_id.id,
                "type_id": self.type_id.co_appointee_task_type_id.id,
            }
        )
        self.write({"co_appointee_ids_task_id": co_appointee.id})

    def _delete_co_appointee(self):
        self.ensure_one()
        host = self.co_appointee_ids_task_id

        if not host:
            return True

        self.write({"co_appointee_ids_task_id": False})
        host.unlink()
