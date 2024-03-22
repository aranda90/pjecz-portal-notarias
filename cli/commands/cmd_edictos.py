"""
CLI Edictos
"""

import click


@click.group()
def cli():
    """Edictos"""


@click.command()
def enviar_email_acuse_recibido():
    """Enviar mensaje de acuse de recibo de un Edicto"""

    # Mensaje de termino
    click.echo("Ya envie el mensaje de acuse de recibo")


@click.command()
def enviar_email_republicacion():
    """Enviar mensaje de republicacion de un Edicto"""

    # Mensaje de termino
    click.echo("Ya envie el mensaje de republicacion")


cli.add_command(enviar_email_acuse_recibido)
cli.add_command(enviar_email_republicacion)
