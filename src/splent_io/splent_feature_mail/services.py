"""Email sending service (SMTP, stdlib only).

A utility service with no DB model. Registered under the generic
``MailService`` name so any feature can send transactional email without
caring about the transport. Built on stdlib ``smtplib`` +
``email.message.EmailMessage`` — no third-party dependency.

SMTP transport is read from the product's config/.env (MAIL_HOST, MAIL_PORT,
MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD) — see config.py. The From address
is read from the admin-editable SettingsService first (key ``mail_from``, so it
can be changed at runtime from the admin panel), falling back to MAIL_FROM.

Defaults target MailHog in development (localhost:1025, no TLS/auth).
"""

import smtplib
from email.message import EmailMessage

from flask import current_app

from splent_framework.services.service_locator import service_proxy

# Keep SMTP I/O from hanging a request if the server is slow/unreachable.
SMTP_TIMEOUT = 10


class MailService:
    """Send transactional email over SMTP."""

    def _setting(self, key, default=None):
        """Read an admin-editable setting, tolerating an absent SettingsService."""
        try:
            return service_proxy("SettingsService").get(key, default)
        except Exception:
            return default

    def from_address(self):
        """The From address: admin setting first, then MAIL_FROM config."""
        configured = self._setting("mail_from", None)
        if configured:
            return configured
        return current_app.config["MAIL_FROM"]

    def send(self, to, subject, body, reply_to=None):
        """Send a plain-text email. Returns True on success, False on failure.

        Raises nothing for transport errors: it logs and returns False so the
        caller decides how to react (retry, flash, ignore).

        Args:
            to: recipient address (or list of addresses).
            subject: subject line.
            body: plain-text message body.
            reply_to: optional Reply-To address.
        """
        recipients = [to] if isinstance(to, str) else list(to)

        msg = EmailMessage()
        msg["From"] = self.from_address()
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)

        cfg = current_app.config
        host = cfg["MAIL_HOST"]
        port = cfg["MAIL_PORT"]
        use_tls = cfg["MAIL_USE_TLS"]
        username = cfg.get("MAIL_USERNAME") or ""
        password = cfg.get("MAIL_PASSWORD") or ""

        try:
            with smtplib.SMTP(host, port, timeout=SMTP_TIMEOUT) as smtp:
                if use_tls:
                    smtp.starttls()
                if username:
                    smtp.login(username, password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            current_app.logger.warning(
                "MailService failed to send to %s via %s:%s — %s",
                recipients,
                host,
                port,
                e,
            )
            return False


def sender():
    """Convenience accessor for the registered MailService instance."""
    return service_proxy("MailService")
