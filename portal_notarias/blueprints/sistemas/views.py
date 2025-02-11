"""
Sistemas
"""

from datetime import datetime, timezone

from flask import Blueprint, redirect, render_template, send_from_directory
from flask_login import current_user

from portal_notarias.blueprints.edictos.models import Edicto
from portal_notarias.extensions import database
from sqlalchemy import func

ROLES_EDICTOS_NOTARIAS = ["ADMINISTRADOR", "NOTARIA"]
MODULO = "SISTEMAS"

sistemas = Blueprint("sistemas", __name__, template_folder="templates")


@sistemas.route("/")
def start():
    """Pagina Inicial"""
    # Si el usuario está autenticado mostrar la página de inicio
    if current_user.is_authenticated:
        # Obtener los roles del usuario
        obtener_roles = set(current_user.get_roles())

        # Calcular fecha actual
        fecha_actual = datetime.now(timezone.utc).date()

        print(fecha_actual)
        # Consultar las cantidades de EDICTOS publicados en la fecha actual
        consulta = (
            database.session.query(
                Edicto.fecha,
                Edicto.descripcion,
                func.count(Edicto.id).label("cantidad"),
            )
            .filter(func.date(Edicto.fecha) == fecha_actual)  # compara fechas
            .filter(Edicto.estatus == "A")
            .filter(Edicto.autoridad_id == current_user.autoridad.id)
            .group_by(Edicto.fecha, Edicto.descripcion)
            .order_by(Edicto.descripcion)
            .all()
        )

        # Crear un listado de tuplas con el nombre del área y la cantidad de procedimientos
        cantidad_edictos_por_fecha = [(fecha, descripcion, cantidad) for fecha, descripcion, cantidad in consulta]
        return render_template(
            "sistemas/start.jinja2",
            mostrar_notaria=obtener_roles.intersection(ROLES_EDICTOS_NOTARIAS),
            cantidad_edictos_por_fecha=cantidad_edictos_por_fecha,
            titulo="Publicaciones de Edictos a la fecha actual",
        )

    # No está autenticado, debe de iniciar sesión
    return redirect("/login")


@sistemas.route("/favicon.ico")
def favicon():
    """Favicon"""
    return send_from_directory("static/img", "favicon.ico", mimetype="image/vnd.microsoft.icon")


@sistemas.app_errorhandler(400)
def bad_request(error):
    """Solicitud errónea"""
    return render_template("sistemas/403.jinja2", error=error), 403


@sistemas.app_errorhandler(403)
def forbidden(error):
    """Acceso no autorizado"""
    return render_template("sistemas/403.jinja2"), 403


@sistemas.app_errorhandler(404)
def page_not_found(error):
    """Error página no encontrada"""
    return render_template("sistemas/404.jinja2"), 404


@sistemas.app_errorhandler(500)
def internal_server_error(error):
    """Error del servidor"""
    return render_template("sistemas/500.jinja2"), 500
