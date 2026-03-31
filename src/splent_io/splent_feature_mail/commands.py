"""
CLI commands contributed by splent_feature_mail.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:mail`` group.

Usage::

    splent feature:mail test --to user@example.com
    splent feature:mail config
"""

import click
from flask import current_app


@click.command("test")
@click.option(
    "--to",
    required=True,
    metavar="EMAIL",
    help="Recipient email address for the test message.",
)
def mail_test(to):
    """Send a test email to verify SMTP configuration."""
    svc = current_app.extensions.get("splent_mail_service")
    if not svc:
        click.secho("  MailService not registered.", fg="red")
        raise SystemExit(1)

    click.echo(f"  Sending test email to {to}...")
    try:
        svc.send_email(
            subject="SPLENT Mail Test",
            recipients=[to],
            body="This is a test email sent by `splent feature:mail test`.",
        )
        click.secho(f"  ✅ Test email sent to {to}.", fg="green")
    except Exception as e:
        click.secho(f"  ❌ Failed to send: {e}", fg="red")
        raise SystemExit(1)


@click.command("config")
def mail_config():
    """Show current SMTP configuration (passwords masked)."""
    cfg = current_app.config
    keys = [
        "MAIL_SERVER",
        "MAIL_PORT",
        "MAIL_USE_TLS",
        "MAIL_USE_SSL",
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
        "MAIL_DEFAULT_SENDER",
    ]
    click.echo()
    click.secho("  SMTP Configuration", bold=True)
    click.secho(f"  {'─' * 40}", fg="bright_black")
    for key in keys:
        value = cfg.get(key, "—")
        if "PASSWORD" in key and value:
            value = "****"
        click.echo(f"  {key:<25} {value}")
    click.echo()


cli_commands = [mail_test, mail_config]
