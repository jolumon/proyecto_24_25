CREATE TABLE
	tipos (
		id_tipos serial NOT NULL,
		nombre_tipos varchar(10),
		activo_tipos bool default true,
		CONSTRAINT pk_tipos PRIMARY KEY (id_tipos)
	);

INSERT INTO
	tipos (nombre_tipos)
VALUES
	('Emulsión'),
	('Gel'),
	('Polvo'),
	('Solución');

CREATE TABLE
	ubicaciones (
		id_ubicaciones serial NOT NULL,
		nombre_ubicaciones varchar(20),
		lotes_id_ubicaciones int not null,
		activo_ubicaciones bool default true,
		CONSTRAINT pk_ubicaciones PRIMARY KEY (id_ubicaciones)
	);

INSERT INTO
	ubicaciones (nombre_ubicaciones)
VALUES
	('0101A01'),
	('0101A02'),
	('0101A03'),
	('0101B01'),
	('0101B02'),
	('0101B03'),
	('0101C01'),
	('0101C02'),
	('0101C03'),
	('0101D01'),
	('0101D02'),
	('0101D03'),
	('0102A01'),
	('0102A02'),
	('0102A03'),
	('0102B01'),
	('0102B02'),
	('0102B03'),
	('0102C01'),
	('0102C02'),
	('0102C03'),
	('0102D01'),
	('0102D02'),
	('0102D03');

CREATE TABLE
	salas (
		id_salas serial NOT NULL,
		nombre_salas varchar(20),
		activo_salas bool default true,
		CONSTRAINT pk_salas PRIMARY KEY (id_salas)
	)
INSERT INTO
	salas (nombre_salas)
VALUES
	('Pesada'),
	('Fabricación 1'),
	('Fabricación 2'),
	('Envasado 1'),
	('Envasado 2'),
	('Acondicionamiento');

CREATE TABLE
	equipos (
		id_equipos serial NOT NULL,
		nombre_equipos varchar(10),
		fecha_adquisicion_equipos date NOT NULL,
		capacidad_equipos int4 NOT NULL,
		revision_equipos int4 DEFAULT 12,
		sala_id_equipos int,
		activ_equipos bool default true,
		CONSTRAINT pk_equipos PRIMARY KEY (id_equipos),
		CONSTRAINT fk_equipos_sala FOREIGN KEY (sala_id_equipos) REFERENCES salas (id_salas)
	);

INSERT INTO
	equipos (
		nombre_equipos,
		fecha_adquisicion_equipos,
		capacidad_equipos,
		sala_id_equipos
	)
VALUES
	('P016', '26/10/2024', 200, 2),
	('P017', '26/10/2024', 500, 2),
	('P019', '26/10/2024', 200, 1),
	('P020', '26/10/2024', 400, 1);

CREATE TABLE
	clientes (
		id_clientes serial NOT NULL,
		nombre_clientes varchar(100) NOT NULL,
		direccion_clientes varchar(100) NULL,
		codigo_postal_clientes varchar(5) NULL,
		poblacion_clientes varchar(100) NULL,
		provincia_clientes varchar(10) NULL,
		telefono_clientes varchar(100) NULL,
		email_clientes varchar(30) NULL,
		contacto_clientes varchar(60) NULL,
		activo_clientes bool DEFAULT true,
		CONSTRAINT pk_clientes PRIMARY KEY (id_clientes)
	);

INSERT INTO
	clientes (
		nombre_clientes,
		direccion_clientes,
		codigo_postal_clientes,
		poblacion_clientes,
		provincia_clientes,
		telefono_clientes,
		email_clientes,
		contacto_clientes,
		activo_clientes
	)
VALUES
	(
		'Cosmetics ChemDev',
		'C/ Manhatan 1',
		'96456',
		'New York',
		'New York',
		'123456789',
		'info@chemdev.com',
		'David Perales Gómez',
		true
	),
	(
		'Laboratorios m2c',
		'Ramón Muntaner',
		'46950',
		'Xirivella',
		'Valencia',
		'987456321',
		'info@laboratoriosm2c.com',
		'Juan Zafra Marín',
		true
	),
	(
		'Desarrollos qúimicos S.L.',
		'C/ Iglesia 12',
		'46950',
		'Masamagrell',
		'Valencia',
		'1234567',
		'info@desaquim.com',
		'Macarena del Carmen',
		true
	),
	(
		'Laboratorios Deluxe Maris',
		'C/China',
		'45679',
		'El pueblo 4',
		'El pueblo',
		'987456321',
		'info@labdml.com ',
		'Pepe Papi Papito',
		true
	);

CREATE TABLE
	materias_primas (
		id_mps serial NOT NULL,
		nombre_mps varchar(50) NULL,
		cantidad_mps float NULL DEFAULT 0.0,
		activo_mps bool DEFAULT true,
		CONSTRAINT pk PRIMARY KEY (id_mps)
	);

INSERT INTO
	materias_primas (nombre_mps)
VALUES
	('Agua'),
	('Ultrez 10'),
	('Montanov 68'),
	('Aloe 200x'),
	('Agua hamamelis'),
	('Agua Rosas'),
	('Rosa mosqueta aceite'),
	('Goma xantana'),
	('Sodio hialuronato'),
	('TEA'),
	('Sodio benzoato'),
	('Potasio sorbato'),
	('glicerina'),
	('Cítrico acido'),
	('Euxyl PE9010'),
	('Propilenglicol');

CREATE TABLE
	proveedores (
		id_proveedores serial NOT NULL,
		nombre_proveedores varchar(50) NULL,
		direccion_proveedores varchar(60) NULL,
		cp_proveedores varchar(5) NULL,
		poblacion_proveedores varchar(50) NULL,
		provincia_proveedores varchar(30) NULL,
		telefono_proveedores varchar(9) NULL,
		contacto_proveedores varchar(50) NULL,
		movil_proveedores varchar(9) NULL,
		email_proveedores varchar(30) NULL,
		activo_proveedores bool DEFAULT true,
		CONSTRAINT pk_proveedores PRIMARY KEY (id_proveedores)
	);

INSERT INTO
	proveedores (nombre_proveedores)
VALUES
	('Lipotec'),
	('Seppic'),
	('Veracetics',),
	('Escuder'),
	('Provital'),
	('Interfat'),
	('Coralis'),
	('DKSH'),
	('Quimidroga'),
	('M2C2 Lab'),
	('Saffic');

CREATE TABLE
	rel_mps_proveedores (
		mp_id_rmp int4 NOT NULL,
		proveedor_id_rmp int4 NOT NULL,
		CONSTRAINT pk_rel_mps_proveedores PRIMARY KEY (mp_id_rmp, proveedor_id_rmp),
		CONSTRAINT fk1_rel_mps_proveedores FOREIGN KEY (mp_id_rmp) REFERENCES materias_primas (id_mps),
		CONSTRAINT fk2_mrel_mps_proveedores FOREIGN KEY (proveedor_id_rmp) REFERENCES proveedores (id_proveedores)
	);

insert into
	rel_mps_proveedores (mp_id_rmp, proveedor_id_rmp)
values
	(1, 10),
	(2, 1),
	(3, 2),
	(4, 3),
	(5, 4),
	(6, 4),
	(7, 6),
	(8, 7),
	(9, 8),
	(10, 9),
	(11, 4),
	(12, 4),
	(13, 9),
	(14, 4),
	(15, 8),
	(3, 11),
	(4, 4),
	(2, 9),
	(10, 4),
	(4, 8);

CREATE TABLE
	cosmeticos (
		id_cosmeticos serial NOT NULL,
		nombre_cosmeticos varchar(45) NOT NULL,
		fecha_cad_cosmeticos int default 36,
		tipo_id_cosmeticos int not null,
		cliente_id_cosmeticos int not null
	);

INSERT INTO
	cosmeticos (
		nombre_cosmeticos,
		cliente_id_cosmeticos,
		tipo_id_cosmeticos
	)
VALUES
	('Crema día', 1, 1),
	('Crema noche', 1, 1),
	('Contorno ojos', 1, 2),
	('Gel aloe', 2, 2),
	('Tónico' 2, 3);

CREATE TABLE
	rel_cosm_mp (
		cosm_id_rcm int NOT NULL,
		mp_id_rcm int NOT NULL,
		porcentaje_rcm decimal(10, 2),
		CONSTRAINT pk_rel_cosm_mp PRIMARY KEY (cosm_id_rcm, proveedor_id_rmp),
		CONSTRAINT fk1_rrel_cosm_mp FOREIGN KEY (cosm_id_rcm) REFERENCES cosmeticos (id_cosmeticos),
		CONSTRAINT fk2_rel_cosm_mp FOREIGN KEY (mp_id_rcm) REFERENCES materias_primas (id_mps)
	);

INSERT INTO
	rel_cosm_mp
VALUES
	(1, 1, 87.05),
	(1, 2, 0.3),
	(1, 3, 5),
	(1, 13, 3),
	(1, 7, 3),
	(1, 11, 0.15),
	(1, 12, 0.05),
	(1, 15, 0.8),
	(1, 10, 0.15),
	(2, 1, 83.55),
	(2, 2, 0.3),
	(2, 3, 5),
	(2, 13, 5),
	(2, 7, 5),
	(2, 11, 0.15),
	(2, 12, 0.05),
	(2, 15, 0.8),
	(2, 10, 0.15),
	(3, 1, 59.05),
	(3, 2, 0.5),
	(3, 10, 0.4),
	(3, 16, 40),
	(3, 4, 0.05),
	(4, 1, 97.45),
	(4, 4, 0.05),
	(4, 2, 0.8),
	(4, 10, 0.8),
	(4, 15, 0.9),
	(5, 13, 4.45),
	(5, 5, 5),
	(5, 6, 90),
	(5, 11, 0.3),
	(5, 12, 0.15),
	(5, 14, 0.1);

CREATE TABLE
	entradas_lotes (
		id_ent_el serial not null,
		mp_id_el int not null,
		proveedor_id_el int not null,
		fecha_el date,
		fecha_cad_el,
		cantidad_el,
		id_lotes serial not null,
		nombre_lotes,
		cantidad_lotes_el,
		ubicacion_id_el
	);

/*
CREATE TABLE
lotes (
id_lotes int not null,
nombre_lotes varchar(6),
cantidad_lotes decimal(10, 2) not null default 100000,
entrada_id_lotes int not null,
ubicacion_id_lotes int not null,
CONSTRAINT pk_lotes PRIMARY KEY (id_lotes),
CONSTRAINT fk1_lotes FOREIGN KEY (entrada_id_lotes) REFERENCES entradas (id_entradas),
CONSTRAINT fk2_lotes FOREIGN KEY (ubicacion_id_lotes) REFERENCES ubicaciones (id_ubicaciones)
);

INSERT INTO
lotes (nombre_lotes, entrada_id_lotes)
values
('MF0001', 2, 100),
('MF0002', 2, 100),
('MF0003', 2, 100),
('MF0004', 2, 100),
('MF0005', 2, 100),
('MF0006', 2, 100),
('MF0007', 2, 100),
('MF0008', 2, 100),
('MF0009', 2, 100),
('MF0010', 2, 100),
('MF0011', 2, 100),
('MF0012', 2, 100),
('MF0013', 2, 100),
('MF0014', 2, 100),
('MF0015', 2, 100),
('MF0016', 2, 100),
('MF0017', 2, 100),
('MF0018', 2, 100),;

CREATE TABLE
entradas (
id_entradas serial not null,
mp_id_lotes int not null,
proveedor_id_lotes int not null,
fecha_entradas date,
lote_id_entradas int not null,
fecha_cad_entradas date,
cantidad_entradas int,
CONSTRAINT fec_cad_entradas CHECK (fecha_cad_ent > 12),
CONSTRAINT pk_entradas PRIMARY KEY (id_entradas),
CONSTRAINT fk1_entradas FOREIGN KEY (lote_id_entradas) REFERENCES lotes (id_lotes)
);

INSERT INTO
entradas (
id_mp_entradas,
id_prov_entradas,
lote_id_entradas,
fecha_entradas,
fecha_cad_entradas,
cantidad_entradas,
precio_entradas
)
VALUES
(),
(),
(),
(),
(),
(),
(),
(),
(),
();
 */
CREATE TABLE
	ordenes_fab (
		id_ofab serial NOT NULL,
		id_prod_ofab int NOT NULL,
		fecha_ofab date NOT NULL,
		lote_ofab varchar(10) NOT NULL,
		/*No haría falta, se podría identificar con la pk*/
		fecha_cad_ofab date NULL,
		equipo_ofab int4 NULL,
		cantidad_ofab int4 NULL,
		indicaciones_ofab varchar(1000) NULL,
		CONSTRAINT ch CHECK ((fecha_ofab < fecha_cad_ofab)),
		CONSTRAINT pk_ofab PRIMARY KEY (id_ofab, id_prod_ofab),
		CONSTRAINT fk_ofab1 FOREIGN KEY (id_prod_ofab) REFERENCES productos (id_prod),
		CONSTRAINT fk_ofab2 FOREIGN KEY (equipo_ofab) REFERENCES equipos (id_eq)
	);

INSERT INTO
	ordenes_fab (
		id_prod_ofab,
		fecha_ofab,
		lote_ofab,
		fecha_cad_ofab,
		equipo_ofab,
		cantidad_ofab,
		indicaciones_ofab
	)
VALUES
	(
		1,
		'2023-06-06',
		'20230001',
		'2025-06-06',
		2,
		75,
		'Todo junto a la bartola'
	),
	(
		1,
		'2023-06-08',
		'20230002',
		'2025-06-08',
		5,
		1600,
		'Una fase detras de otra. Subir a 75ºC, 
	 emulsionar.Enfriar y por debajo de 40ºC añadir fase termolabil'
	),
	(
		1,
		'2023-06-04',
		'20230003',
		'2025-06-03',
		5,
		800,
		'Todo a la vez'
	),
	(
		2,
		'2023-11-11',
		'1465sdfd',
		'2026-03-02',
		4,
		300,
		NULL
	),
	(
		2,
		'2023-11-17',
		'abc',
		'2024-01-01',
		4,
		300,
		NULL
	);