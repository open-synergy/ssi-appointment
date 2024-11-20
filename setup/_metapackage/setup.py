import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-appointment",
    description="Meta package for open-synergy-ssi-appointment Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_appointment',
        'odoo14-addon-ssi_appointment_project',
        'odoo14-addon-ssi_appointment_request',
        'odoo14-addon-ssi_appointment_request_work_log',
        'odoo14-addon-ssi_appointment_schedule_state_change_constrain',
        'odoo14-addon-ssi_appointment_work_log',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
