# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Appointment - Integration With Project",
    "version": "14.0.1.4.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_appointment",
        "ssi_project_template",
        "ssi_task_timebox",
        "ssi_task_work_log",
    ],
    "data": [
        "views/appointment_type_views.xml",
        "views/appointment_schedule_views.xml",
    ],
    "demo": [],
}
