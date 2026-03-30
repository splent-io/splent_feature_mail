"""
Mail feature configuration.

Injects SMTP settings into Flask app.config from environment variables.
In development, splent_feature_mailhog overrides these to point to the
local Mailhog container.
"""

import os


def inject_config(app):
    app.config.update({
        "MAIL_SERVER": os.getenv("MAIL_SERVER", "smtp.example.com"),
        "MAIL_PORT": int(os.getenv("MAIL_PORT", "587")),
        "MAIL_USE_TLS": os.getenv("MAIL_USE_TLS", "True").lower() == "true",
        "MAIL_USE_SSL": os.getenv("MAIL_USE_SSL", "False").lower() == "true",
        "MAIL_USERNAME": os.getenv("MAIL_USERNAME", ""),
        "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD", ""),
        "MAIL_DEFAULT_SENDER": os.getenv(
            "MAIL_DEFAULT_SENDER",
            os.getenv("MAIL_USERNAME", "noreply@example.com"),
        ),
    })
