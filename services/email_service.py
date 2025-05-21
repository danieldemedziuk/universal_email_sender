import base64
import cssutils
from premailer import transform
from jinja2 import Template
from odoo import models, api
from odoo.exceptions import UserError

class EmailService(models.AbstractModel):
    _name = 'email.service'
    _description = 'Usługa wysyłania wiadomości e-mail'

    @api.model
    def send_email(self, subject, template_body, email_to, email_from=None, attachments=None, context_data=None):
        if not email_from:
            email_from = self.env.user.email or self.env.user.company_id.email
        if not email_from:
            raise UserError("Brakuje adresu e-mail nadawcy.")

        # Renderowanie Jinja2
        if context_data is None:
            context_data = {}
        jinja_template = Template(template_body)
        rendered_body = jinja_template.render(**context_data)

        # Inlining CSS
        cssutils.log.setLevel("FATAL")
        final_html = transform(rendered_body)

        mail_values = {
            'subject': subject,
            'body_html': final_html,
            'email_to': email_to,
            'email_from': email_from,
            'auto_delete': False,
        }

        if attachments:
            mail_values['attachment_ids'] = []
            for name, content in attachments.items():
                attachment = self.env['ir.attachment'].create({
                    'name': name,
                    'type': 'binary',
                    'datas': base64.b64encode(content).decode(),
                    'mimetype': 'application/octet-stream',
                })
                mail_values['attachment_ids'].append((4, attachment.id))

        mail = self.env['mail.mail'].create(mail_values)
        mail.send()