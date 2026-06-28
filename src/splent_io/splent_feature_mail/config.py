"""mail feature configuration.

Injects SMTP/email environment variables into Flask app.config so the
MailService can send mail through any SMTP server. Defaults target MailHog
(host=localhost, port=1025, no TLS/auth) so development works out of the box;
set real values in the product's .env for production.

To regenerate from source code: splent feature:inject-config splent_feature_mail
"""

import os


def inject_config(app):
    # setdefault: respect anything the product/.env already set; only fill gaps.
    app.config.setdefault("MAIL_HOST", os.getenv("MAIL_HOST", "localhost"))
    app.config.setdefault("MAIL_PORT", int(os.getenv("MAIL_PORT", "1025")))
    app.config.setdefault("MAIL_USE_TLS", os.getenv("MAIL_USE_TLS", "0") == "1")
    app.config.setdefault("MAIL_USERNAME", os.getenv("MAIL_USERNAME", ""))
    app.config.setdefault("MAIL_PASSWORD", os.getenv("MAIL_PASSWORD", ""))
    app.config.setdefault("MAIL_FROM", os.getenv("MAIL_FROM", "no-reply@localhost"))
