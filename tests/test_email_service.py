from odoo.tests.common import TransactionCase, tagged
from unittest.mock import patch, mock_open, MagicMock
import logging

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install')
class TestEmailService(TransactionCase):

    def setUp(self):
        super().setUp()

        # Konfiguracja SMTP w ir.config_parameter
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('mj_settings.smtp_mj_host', 'smtp.example.com')
        config.set_param('mj_settings.smtp_mj_port', '587')
        config.set_param('mj_settings.smtp_mj_user', 'user@example.com')
        config.set_param('mj_settings.smtp_mj_pwd', 'supersecret')
        config.set_param('mj_settings.smtp_mj_sender', 'user@example.com')
        config.set_param('web.base.url', 'https://myodoo.test')

    def test_send_email_basic(self):
        service = self.env['email.service']
        context_data = {'user': 'Tester'}

        dummy_html_template = "<div>Hello {{ user }}</div>"

        # Mockujemy plik CSS oraz smtplib.SMTP
        with patch("builtins.open", mock_open(read_data="body {color: red;}")), \
             patch("smtplib.SMTP") as mock_smtp:

            smtp_instance = MagicMock()
            mock_smtp.return_value = smtp_instance

            try:
                service.send_email(
                    subject="Test email",
                    template_body=dummy_html_template,
                    email_to="daniel.demedziuk@mjgroup.com",
                    context_data=context_data,
                )
                _logger.info("✅ Test wysyłki emaila zakończony sukcesem.")
            except Exception as e:
                self.fail(f"❌ Błąd przy wysyłce e-maila: {e}")

            # Sprawdzamy czy SMTP zadziałało
            smtp_instance.starttls.assert_called_once()
            smtp_instance.login.assert_called_once_with('user@example.com', 'supersecret')
            smtp_instance.sendmail.assert_called_once()
            smtp_instance.quit.assert_called_once()
