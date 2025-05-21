from odoo.tests.common import TransactionCase

class TestEmailService(TransactionCase):
    def test_send_email(self):
        service = self.env['email.service']
        html = """
            <style>p {color: red;}</style>
            <p>Hello {{ name }}</p>
        """
        context_data = {"name": "John"}
        service.send_email(
            subject="Test Email",
            template_body=html,
            email_to="john@example.com",
            context_data=context_data
        )