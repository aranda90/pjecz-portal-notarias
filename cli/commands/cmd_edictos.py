"""
CLI Edictos
"""

from datetime import datetime

import click
import sys

from lib.exceptions import MyAnyError

from portal_notarias.app import create_app
from portal_notarias.blueprints.edictos.tasks import enviar_email_acuse_recibido as enviar_email_acuse_recibido_task
from portal_notarias.blueprints.edictos.tasks import enviar_email_republicacion as enviar_email_republicacion_task
from portal_notarias.blueprints.edictos.tasks import republicacion_edictos as republicacion_edictos_task
from portal_notarias.blueprints.edictos.models import Edicto
from portal_notarias.blueprints.edictos_acuses.models import EdictoAcuse
from portal_notarias.extensions import database

app = create_app()
app.app_context().push()
database.app = app


@click.group()
def cli():
    """Edictos"""


@click.command()
@click.argument("edicto_id", type=int)
@click.argument("nueva_fecha", type=str)
def republicacion_edictos(edicto_id: int, nueva_fecha: str):
    """Republicar un edicto en una nueva fecha"""
    try:
        # Convertir la fecha proporcionada
        nueva_fecha_dt = datetime.strptime(nueva_fecha, "%Y-%m-%d")
        # Validar si ya existe una publicacion en esa fecha
        republicacion_existente = (
            database.session.query(EdictoAcuse).filter_by(edicto_id=edicto_id, fecha=nueva_fecha_dt).first()
        )
        if republicacion_existente:
            click.echo(f"Error: Ya existe una republicación para el edicto {edicto_id} en la fecha {nueva_fecha}.")
            sys.exit(1)
        # Realizar la tarea de republicación
        mensaje = republicacion_edictos_task(edicto_id, nueva_fecha_dt)
    except ValueError:
        click.echo("Error: El formato de la fecha debe ser YYYY-MM-DD.")
        sys.exit(1)
    except MyAnyError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    # Memsaje de éxito
    click.echo(mensaje)


cli.add_command(republicacion_edictos)


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
