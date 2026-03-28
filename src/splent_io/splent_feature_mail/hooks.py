from splent_framework.hooks.template_hooks import register_template_hook
from flask import url_for


def mail_scripts():
    return '<script src="' + url_for('mail.assets', subfolder='dist', filename='mail.bundle.js') + '"></script>'


register_template_hook("layout.scripts", mail_scripts)
