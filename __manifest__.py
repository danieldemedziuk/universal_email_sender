{
    "name": "Universal Email Sender",
    "version": "17.0.0.0.1",
    "category": "Tools",
    "summary": "Universal email sending service with external SMTP and templating",
    "author": "DSquare Net",
    "license": 'LGPL-3',
    "sequence": 50,
    "description": """
Universal email sender template
==================================
Module for Odoo with mail templates.
""",
    "depends": [
        "base", 
        "mj_settings", 
        "web",
    ],
    "data": [
        "data/email_template_data.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "universal_email_sender/static/src/scss/email_styles.scss"
        ]
    },
    "external_dependencies": {
        "python": ['premailer', 'cssutils'],
    },
    "auto_install": False,
    "application": True,
    "installable": True,
}