"""
Estados, modelos
"""

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.universal_mixin import UniversalMixin
from portal_notarias.extensions import database


class Estado(database.Model, UniversalMixin):
    """Estado"""

    # Nombre de la tabla
    __tablename__ = "estados"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    clave: Mapped[str] = mapped_column(String(2), unique=True)
    nombre: Mapped[str] = mapped_column(String(256))

    # Hijos
    municipios: Mapped["Municipio"] = relationship("Municipio", back_populates="estado")

    def __repr__(self):
        """Representación"""
        return f"<Estado {self.clave}>"
