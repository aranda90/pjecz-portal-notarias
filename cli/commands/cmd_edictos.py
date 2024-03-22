"""
CLI Edictos
"""

import click
import sys

from lib.exceptions import MyAnyError

from portal_notarias.blueprints.edictos.tasks import enviar_email_acuse_recibido as enviar_email_acuse_recibido_task
from portal_notarias.blueprints.edictos.tasks import enviar_email_republicacion as enviar_email_republicacion_task


@click.group()
def cli():
    """Edictos"""


@click.command()
@click.argument("edicto_id", type=int)
def enviar_email_acuse_recibido(edicto_id: int):
    """Enviar mensaje de acuse de recibo de un Edicto"""

    # Ejecutar tarea
    try:
        mensaje = enviar_email_acuse_recibido_task(edicto_id)
    except MyAnyError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)

    # Mensaje de termino
    click.echo(mensaje)


@click.command()
@click.argument("edicto_id", type=int)
def enviar_email_republicacion(edicto_id: int):
    """Enviar mensaje de republicacion de un Edicto"""

    # Ejecutar tarea
    try:
        mensaje = enviar_email_republicacion_task(edicto_id)
    except MyAnyError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)

    # Mensaje de termino
    click.echo(mensaje)


cli.add_command(enviar_email_acuse_recibido)
cli.add_command(enviar_email_republicacion)
