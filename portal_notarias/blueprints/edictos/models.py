"""
Edictos, modelos
"""

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from lib.universal_mixin import UniversalMixin

from portal_notarias.extensions import database


class Edicto(database.Model, UniversalMixin):
    """Edicto"""

    # Nombre de la tabla
    __tablename__ = "edictos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = database.Column(database.Integer, database.ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = database.relationship("Autoridad", back_populates="edictos")

    # Columnas
    fecha = Column(Date)
    descripcion = Column(String(256), nullable=False)
    expediente = Column(String(16), nullable=False, default="", server_default="")
    numero_publicacion = Column(String(16), nullable=False, default="", server_default="")
    archivo = Column(String(256), nullable=False, default="", server_default="")
    url = Column(String(512), nullable=False, default="", server_default="")

    # Columnas nuevas
    acuse_num = Column(Integer, nullable=False, default=0)
    edicto_id_original = Column(Integer, nullable=False, default=0)

    # Hijos
    edictos_acuses = relationship("EdictoAcuse", back_populates="edicto")

    @property
    def descargar_url(self):
        """URL para descargar el archivo desde el sitio web"""
        if self.id:
            return f"https://www.pjecz.gob.mx/consultas/edictos/descargar/?id={self.id}"
        return ""

    def __repr__(self):
        """Representación"""
        return f"<Edicto {self.descripcion}>"
