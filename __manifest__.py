{
    "name": "Universal email sender",
    "version": "17.0.0.0.1",
    "category": "Tools",
    "summary": "Centralny moduł do wysyłania wiadomości e-mail",
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
        "mail",
    ],
    "data": [
        "data/email_template_data.xml"
    ],
    "external_dependencies": {
        "python": ['premailer', 'cssutils'],
    },
    "auto_install": False,
    "application": True,
    "installable": True,
}