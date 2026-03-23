from splent_framework.blueprints.base_blueprint import BaseBlueprint

mail_bp = BaseBlueprint("mail", __name__, template_folder="templates")


from .services import MailService

mail_service = MailService()

def init_feature(app):
    mail_service.init_app(app)
    app.mail_service = mail_service


def inject_context_vars(app):
    return {}