"""
CLI commands contributed by splent_feature_mail.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:mail`` group.

Usage::

    splent feature:mail hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_mail!")


cli_commands = [hello]
