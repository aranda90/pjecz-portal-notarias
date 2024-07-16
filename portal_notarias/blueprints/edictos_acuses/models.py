"""
EdictosAcuses, modelos
"""

from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.universal_mixin import UniversalMixin
from portal_notarias.extensions import database


class EdictoAcuse(database.Model, UniversalMixin):
    """EdictoAcuse"""

    # Nombre de la tabla
    __tablename__ = "edictos_acuses"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    edicto_id: Mapped[int] = mapped_column(ForeignKey("edictos.id"))
    edicto: Mapped["Edicto"] = relationship(back_populates="edictos_acuses")

    # Columnas
    fecha: Mapped[date] = mapped_column(index=True)

    def __repr__(self):
        """Representación"""
        return f"<EdictoAcuse {self.id}>"
