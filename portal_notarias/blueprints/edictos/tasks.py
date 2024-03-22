"""
Edictos, tareas en el fondo
"""

import logging
from datetime import datetime
import os

import pytz
import sendgrid
from dotenv import load_dotenv

from lib.tasks import set_task_error, set_task_progress
from portal_notarias.app import create_app
from portal_notarias.blueprints.edictos.models import Edicto
from portal_notarias.extensions import database

load_dotenv()  # Take environment variables from .env

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
empunadura = logging.FileHandler("logs/edictos.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)

app = create_app()
app.app_context().push()
database.app = app

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")
TIMEZONE = "America/Mexico_City"


def enviar_email_acuse_recibido(edicto_id: int) -> str:
    """Enviar mensaje de acuse de recibo de un Edicto"""

    # Mensaje de termino
    return "Ya envie el mensaje de acuse de recibo"


def enviar_email_republicacion():
    """Enviar mensaje de republicacion de un Edicto"""

    # Mensaje de termino
    return "Ya envie el mensaje de republicacion"
