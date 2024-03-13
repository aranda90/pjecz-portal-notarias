"""
EdictosAcuses, modelos
"""

from sqlalchemy import Date, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from lib.universal_mixin import UniversalMixin

from portal_notarias.extensions import database


class EdictoAcuse(database.Model, UniversalMixin):
    """EdictoAcuse"""

    # Nombre de la tabla
    __tablename__ = "edictos_acuses"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    edicto_id = Column(Integer, ForeignKey("edictos.id"), index=True, nullable=False)
    edicto = relationship("Edicto", back_populates="edictos_acuses")

    # Columnas
    fecha = Column(Date, index=True, nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<EdictoAcuse {self.id}>"
