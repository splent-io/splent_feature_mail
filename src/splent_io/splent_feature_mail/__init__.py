from splent_framework.blueprints.base_blueprint import BaseBlueprint

mail_bp = BaseBlueprint(
    "mail", __name__, template_folder="templates"
)


def init_feature(app):
    from splent_io.splent_feature_mail.services import MailService
    mail_service = MailService()
    mail_service.init_app(app)
    app.extensions["splent_mail_service"] = mail_service


def inject_context_vars(app):
    return {}
