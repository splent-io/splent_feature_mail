from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_mail.services import MailService

mail_bp = create_blueprint(__name__)


def init_feature(app):
    register_service(app, "MailService", MailService)


def inject_context_vars(app):
    return {}
