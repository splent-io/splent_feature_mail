from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_mail.services import MailService

mail_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.settings.settings_schema import register_settings

    register_service(app, "MailService", MailService)
    # Admin-editable sender address (declared once; the framework renders the
    # panel and persists the value). Blank falls back to the MAIL_FROM config.
    register_settings(
        "mail",
        "Email",
        [
            {
                "key": "mail_from",
                "type": "text",
                "default": "",
                "label": "Sender (From)",
                "help": "From address for outgoing email; blank uses MAIL_FROM.",
            }
        ],
        icon="mail",
    )


def inject_context_vars(app):
    return {}
