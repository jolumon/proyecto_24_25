from typing import List, Optional

from sqlalchemy import Boolean, CheckConstraint, Column, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Table, UniqueConstraint, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


class Clientes(Base):
    __tablename__ = 'clientes'
    __table_args__ = (
        PrimaryKeyConstraint('id_clientes', name='pk_clientes'),
    )

    id_clientes = mapped_column(Integer)
    nombre_clientes = mapped_column(String(100), nullable=False)
    direccion_clientes = mapped_column(String(100))
    codigo_postal_clientes = mapped_column(String(5))
    poblacion_clientes = mapped_column(String(100))
    provincia_clientes = mapped_column(String(100))
    telefono_clientes = mapped_column(String(100))
    email_clientes = mapped_column(String(30))
    contacto_clientes = mapped_column(String(60))
    activo_clientes = mapped_column(Boolean, server_default=text('true'))

    cosmeticos: Mapped[List['Cosmeticos']] = relationship('Cosmeticos', uselist=True, back_populates='clientes')


class MateriasPrimas(Base):
    __tablename__ = 'materias_primas'
    __table_args__ = (
        PrimaryKeyConstraint('id_mps', name='pk'),
    )

    id_mps = mapped_column(Integer)
    nombre_mps = mapped_column(String(50))
    activo_mps = mapped_column(Boolean, server_default=text('true'))

    proveedores: Mapped['Proveedores'] = relationship('Proveedores', secondary='rel_mps_proveedores', back_populates='materias_primas')
    lotes_stock: Mapped[List['LotesStock']] = relationship('LotesStock', uselist=True, back_populates='materias_primas')
    rel_cosm_mp: Mapped[List['RelCosmMp']] = relationship('RelCosmMp', uselist=True, back_populates='materias_primas')
    detalle_o_fabricacion: Mapped[List['DetalleOFabricacion']] = relationship('DetalleOFabricacion', uselist=True, back_populates='materias_primas')


class Proveedores(Base):
    __tablename__ = 'proveedores'
    __table_args__ = (
        PrimaryKeyConstraint('id_proveedores', name='pk_proveedores'),
    )

    id_proveedores = mapped_column(Integer)
    nombre_proveedores = mapped_column(String(50))
    direccion_proveedores = mapped_column(String(60))
    cp_proveedores = mapped_column(String(5))
    poblacion_proveedores = mapped_column(String(50))
    provincia_proveedores = mapped_column(String(30))
    telefono_proveedores = mapped_column(String(9))
    contacto_proveedores = mapped_column(String(50))
    movil_proveedores = mapped_column(String(9))
    email_proveedores = mapped_column(String(30))
    activo_proveedores = mapped_column(Boolean, server_default=text('true'))

    materias_primas: Mapped['MateriasPrimas'] = relationship('MateriasPrimas', secondary='rel_mps_proveedores', back_populates='proveedores')


class Salas(Base):
    __tablename__ = 'salas'
    __table_args__ = (
        PrimaryKeyConstraint('id_salas', name='pk_salas'),
    )

    id_salas = mapped_column(Integer)
    nombre_salas = mapped_column(String(20))
    activo_salas = mapped_column(Boolean, server_default=text('true'))

    equipos: Mapped[List['Equipos']] = relationship('Equipos', uselist=True, back_populates='salas')


class Tipos(Base):
    __tablename__ = 'tipos'
    __table_args__ = (
        PrimaryKeyConstraint('id_tipos', name='pk_tipos'),
    )

    id_tipos = mapped_column(Integer)
    nombre_tipos = mapped_column(String(10))
    activo_tipos = mapped_column(Boolean, server_default=text('true'))

    cosmeticos: Mapped[List['Cosmeticos']] = relationship('Cosmeticos', uselist=True, back_populates='tipos')


class Ubicaciones(Base):
    __tablename__ = 'ubicaciones'
    __table_args__ = (
        PrimaryKeyConstraint('id_ubicaciones', name='pk_ubicaciones'),
    )

    id_ubicaciones = mapped_column(Integer)
    nombre_ubicaciones = mapped_column(String(20))
    libre_ubicaciones = mapped_column(Boolean, server_default=text('true'))
    activo_ubicaciones = mapped_column(Boolean, server_default=text('true'))

    entradas: Mapped['Entradas'] = relationship('Entradas', uselist=False, back_populates='ubicaciones')


class Cosmeticos(Base):
    __tablename__ = 'cosmeticos'
    __table_args__ = (
        ForeignKeyConstraint(['cliente_id_cosmeticos'], ['clientes.id_clientes'], name='fk2_cosmeticos'),
        ForeignKeyConstraint(['tipo_id_cosmeticos'], ['tipos.id_tipos'], name='fk1_cosmeticos'),
        PrimaryKeyConstraint('id_cosmeticos', name='pk_cosmeticos')
    )

    id_cosmeticos = mapped_column(Integer)
    nombre_cosmeticos = mapped_column(String(45), nullable=False)
    tipo_id_cosmeticos = mapped_column(Integer, nullable=False)
    cliente_id_cosmeticos = mapped_column(Integer, nullable=False)
    fecha_cad_cosmeticos = mapped_column(Integer, server_default=text('36'))
    activo_cosmeticos = mapped_column(Boolean, server_default=text('true'))

    clientes: Mapped['Clientes'] = relationship('Clientes', back_populates='cosmeticos')
    tipos: Mapped['Tipos'] = relationship('Tipos', back_populates='cosmeticos')
    ordenes: Mapped[List['Ordenes']] = relationship('Ordenes', uselist=True, back_populates='cosmeticos')
    rel_cosm_mp: Mapped[List['RelCosmMp']] = relationship('RelCosmMp', uselist=True, back_populates='cosmeticos')


class Equipos(Base):
    __tablename__ = 'equipos'
    __table_args__ = (
        ForeignKeyConstraint(['sala_id_equipos'], ['salas.id_salas'], name='fk_equipos_sala'),
        PrimaryKeyConstraint('id_equipos', name='pk_equipos')
    )

    id_equipos = mapped_column(Integer)
    fecha_adquisicion_equipos = mapped_column(Date, nullable=False)
    capacidad_equipos = mapped_column(Integer, nullable=False)
    nombre_equipos = mapped_column(String(10))
    revision_equipos = mapped_column(Integer, server_default=text('12'))
    sala_id_equipos = mapped_column(Integer)
    activ_equipos = mapped_column(Boolean, server_default=text('true'))

    salas: Mapped[Optional['Salas']] = relationship('Salas', back_populates='equipos')
    ordenes: Mapped[List['Ordenes']] = relationship('Ordenes', uselist=True, back_populates='equipos')


class LotesStock(Base):
    __tablename__ = 'lotes_stock'
    __table_args__ = (
        ForeignKeyConstraint(['mp_id_lotes_stock'], ['materias_primas.id_mps'], name='fk_mp_id_lotes_stock'),
        PrimaryKeyConstraint('id_lotes_stock', name='pk_id_lotes_stock'),
        UniqueConstraint('nombre_lotes_stock', name='lotes_stock_nombre_lotes_stock_key')
    )

    id_lotes_stock = mapped_column(Integer)
    nombre_lotes_stock = mapped_column(String(10))
    cantidad_lotes_stock = mapped_column(Numeric(10, 2))
    fecha_caducidad_lotes_stock = mapped_column(Date)
    mp_id_lotes_stock = mapped_column(Integer)

    materias_primas: Mapped[Optional['MateriasPrimas']] = relationship('MateriasPrimas', back_populates='lotes_stock')
    detalle_o_fabricacion: Mapped[List['DetalleOFabricacion']] = relationship('DetalleOFabricacion', uselist=True, back_populates='lotes_stock')


t_rel_mps_proveedores = Table(
    'rel_mps_proveedores', metadata,
    Column('mp_id_rmp', Integer, nullable=False),
    Column('proveedor_id_rmp', Integer, nullable=False),
    ForeignKeyConstraint(['mp_id_rmp'], ['materias_primas.id_mps'], name='fk1_rel_mps_proveedores'),
    ForeignKeyConstraint(['proveedor_id_rmp'], ['proveedores.id_proveedores'], name='fk2_mrel_mps_proveedores'),
    PrimaryKeyConstraint('mp_id_rmp', 'proveedor_id_rmp', name='pk_rel_mps_proveedores')
)


class Entradas(Base):
    __tablename__ = 'entradas'
    __table_args__ = (
        ForeignKeyConstraint(['mp_id_ent', 'proveedor_id_ent'], ['rel_mps_proveedores.mp_id_rmp', 'rel_mps_proveedores.proveedor_id_rmp'], name='fk1_entradas'),
        ForeignKeyConstraint(['ubi_id_ent'], ['ubicaciones.id_ubicaciones'], name='fk2_entradas'),
        PrimaryKeyConstraint('id_ent', name='pk_entradas'),
        UniqueConstraint('nombre_lotes_ent', name='entradas_nombre_lotes_ent_key'),
        UniqueConstraint('ubi_id_ent', name='entradas_ubi_id_ent_key')
    )

    id_ent = mapped_column(Integer)
    mp_id_ent = mapped_column(Integer, nullable=False)
    proveedor_id_ent = mapped_column(Integer, nullable=False)
    fecha_caducidad_ent = mapped_column(Date, nullable=False)
    fecha_ent = mapped_column(Date)
    nombre_lotes_ent = mapped_column(String(10))
    cantidad_ent = mapped_column(Numeric(10, 2))
    ubi_id_ent = mapped_column(Integer)

    ubicaciones: Mapped[Optional['Ubicaciones']] = relationship('Ubicaciones', back_populates='entradas')


class Ordenes(Base):
    __tablename__ = 'ordenes'
    __table_args__ = (
        CheckConstraint('fecha_fab_ordenes < fecha_cad_ordenes', name='ch'),
        ForeignKeyConstraint(['cosmetico_id_ordenes'], ['cosmeticos.id_cosmeticos'], name='fk1_ofab'),
        ForeignKeyConstraint(['equipo_id_ordenes'], ['equipos.id_equipos'], name='fk2_ofab'),
        PrimaryKeyConstraint('id_ordenes', name='pk_ofab')
    )

    id_ordenes = mapped_column(Integer)
    fecha_fab_ordenes = mapped_column(Date, nullable=False)
    cosmetico_id_ordenes = mapped_column(Integer, nullable=False)
    lote_ordenes = mapped_column(String(10), nullable=False)
    cantidad_ordenes = mapped_column(Integer, nullable=False)
    fecha_cad_ordenes = mapped_column(Date, nullable=False)
    equipo_id_ordenes = mapped_column(Integer, nullable=False)
    indicaciones_ordenes = mapped_column(String(1000))

    cosmeticos: Mapped['Cosmeticos'] = relationship('Cosmeticos', back_populates='ordenes')
    equipos: Mapped['Equipos'] = relationship('Equipos', back_populates='ordenes')
    detalle_o_fabricacion: Mapped[List['DetalleOFabricacion']] = relationship('DetalleOFabricacion', uselist=True, back_populates='ordenes')


class RelCosmMp(Base):
    __tablename__ = 'rel_cosm_mp'
    __table_args__ = (
        ForeignKeyConstraint(['cosm_id_rcm'], ['cosmeticos.id_cosmeticos'], name='fk1_rel_cosm_mp'),
        ForeignKeyConstraint(['mp_id_rcm'], ['materias_primas.id_mps'], name='fk2_rel_cosm_mp'),
        PrimaryKeyConstraint('cosm_id_rcm', 'mp_id_rcm', name='pk_rel_cosm_mp')
    )

    cosm_id_rcm = mapped_column(Integer, nullable=False)
    mp_id_rcm = mapped_column(Integer, nullable=False)
    porcentaje_rcm = mapped_column(Numeric(10, 2))

    cosmeticos: Mapped['Cosmeticos'] = relationship('Cosmeticos', back_populates='rel_cosm_mp')
    materias_primas: Mapped['MateriasPrimas'] = relationship('MateriasPrimas', back_populates='rel_cosm_mp')


class DetalleOFabricacion(Base):
    __tablename__ = 'detalle_o_fabricacion'
    __table_args__ = (
        ForeignKeyConstraint(['lote_id_fab'], ['lotes_stock.id_lotes_stock'], name='fk2_fab'),
        ForeignKeyConstraint(['mp_id_fab'], ['materias_primas.id_mps'], name='fk3_fab'),
        ForeignKeyConstraint(['orden_id_fab'], ['ordenes.id_ordenes'], name='fk1_fab'),
        PrimaryKeyConstraint('orden_id_fab', 'lote_id_fab', name='pk_fab')
    )

    orden_id_fab = mapped_column(Integer, nullable=False)
    lote_id_fab = mapped_column(Integer, nullable=False)
    mp_id_fab = mapped_column(Integer, nullable=False)
    cantidad_fab = mapped_column(Numeric(10, 2), nullable=False)

    lotes_stock: Mapped['LotesStock'] = relationship('LotesStock', back_populates='detalle_o_fabricacion')
    materias_primas: Mapped['MateriasPrimas'] = relationship('MateriasPrimas', back_populates='detalle_o_fabricacion')
    ordenes: Mapped['Ordenes'] = relationship('Ordenes', back_populates='detalle_o_fabricacion')
