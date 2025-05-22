from odoo import models, api
import jinja2
import cssutils
from premailer import transform
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64
import logging
import os

_logger = logging.getLogger(__name__)

class EmailService(models.AbstractModel):
    _name = 'email.service'
    _description = 'Universal Email Sending Service'

    def _get_smtp_config(self):
        host = self.env['ir.config_parameter'].sudo().get_param('mj_settings.smtp_mj_host', default=False)
        port = self.env['ir.config_parameter'].sudo().get_param('mj_settings.smtp_mj_port', default=0)
        user = self.env['ir.config_parameter'].sudo().get_param('mj_settings.smtp_mj_user', default=False)
        pwd = self.env['ir.config_parameter'].sudo().get_param('mj_settings.smtp_mj_pwd', default=False)
        sender = self.env['ir.config_parameter'].sudo().get_param('mj_settings.smtp_mj_sender', default=False)
        
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': pwd
        }

    def _render_template(self, template_str, context):
        template = jinja2.Template(template_str)
        html = template.render(**context)

        css_path = os.path.join(os.path.dirname(__file__), '../static/src/scss/email_styles.scss')
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()

        style_tag = f"<style>{css}</style>"
        html_with_style = f"{style_tag}\n{html}"
        return transform(html_with_style)

    def send_email(self, subject, template_body, email_to, context_data=None, attachments=None, link_record=None):
        smtp = self._get_smtp_config()
        context_data = context_data or {}
        
        if link_record:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            context_data['odoo_link'] = f"{base_url}/web#id={link_record.id}&model={link_record._name}&view_type=form"

        html_body = self._render_template(template_body, context_data)

        msg = MIMEMultipart()
        msg['From'] = smtp['user']
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        for attach in (attachments or []):
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(base64.b64decode(attach['data']))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attach["filename"]}"')
            msg.attach(part)

        try:
            server = smtplib.SMTP(smtp['host'], smtp['port'])
            server.starttls()
            server.login(smtp['user'], smtp['password'])
            server.sendmail(smtp['user'], email_to, msg.as_string())
            server.quit()
        except Exception as e:
            _logger.exception("Email sending failed: %s", e)
            raise
