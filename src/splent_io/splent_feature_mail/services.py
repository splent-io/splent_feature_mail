"""
MailService — send emails via Flask-Mail.

Usage from other features::

    from flask import current_app

    mail_service = current_app.extensions["splent_mail_service"]
    mail_service.send_email(
        subject="Welcome",
        recipients=["user@example.com"],
        body="Hello!",
    )
"""

import logging

from flask_mail import Mail, Message

logger = logging.getLogger(__name__)


class MailService:
    def __init__(self):
        self._app = None

    def init_app(self, app):
        """Store the app reference. Mail is initialized lazily on first send
        so that refinement features (like mailhog) can override SMTP config
        after mail's init_feature runs.
        """
        self._app = app

    @property
    def mail(self):
        """Lazy-init Flask-Mail on first access to pick up final config."""
        if not hasattr(self, "_mail") or self._mail is None:
            self._mail = Mail(self._app)
            logger.info(
                "Flask-Mail initialized (server=%s, port=%s)",
                self._app.config.get("MAIL_SERVER"),
                self._app.config.get("MAIL_PORT"),
            )
        return self._mail

    def send_email(self, subject, recipients, body=None, html=None, sender=None):
        """Send an email."""
        if not self._app:
            raise RuntimeError("MailService not initialized. Call init_app() first.")

        default_sender = self._app.config.get("MAIL_DEFAULT_SENDER", "noreply@example.com")

        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html,
            sender=sender or default_sender,
        )

        with self._app.app_context():
            self.mail.send(msg)

        from splent_io.splent_feature_mail.signals import email_sent
        email_sent.send(self._app, subject=subject, recipients=recipients)

        logger.info("Email sent: '%s' to %s", subject, recipients)
