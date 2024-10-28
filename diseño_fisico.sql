CREATE TABLE tipos (
		id_tipos serial NOT NULL,
		nombre_tipos varchar(10),
		activo_tipos bool default true,
		CONSTRAINT pk_tipos PRIMARY KEY (id_tipos)
);

INSERT
	INTO
	tipos(nombre_tipos)
values
	('Emulsión'),
	('Gel'),
	('Polvo'),
	('Solución');



create table salas (
		id_salas serial not null,
		nombre_salas varchar(20),
		activo_salas bool default true,
		constraint pk_salas primary key (id_salas)
	);

INSERT into salas (nombre_salas)
VALUES
	('Pesada'),
	('Fabricación 1'),
	('Fabricación 2'),
	('Envasado 1'),
	('Envasado 2'),
	('Acondicionamiento');

CREATE table equipos (
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

INSERT into equipos (
		nombre_equipos,
		fecha_adquisicion_equipos,
		capacidad_equipos,
		sala_id_equipos
	)
VALUES
	('P016', '2024-10-26', 200, 2),
	('P017', '2024-10-26', 500, 2),
	('P019', '2024-10-26', 200, 1),
	('P020', '2024-10-26', 400, 1);

CREATE table clientes (
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

INSERT into clientes (
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

CREATE table materias_primas (
		id_mps serial NOT NULL,
		nombre_mps varchar(50) NULL,
		/*cantidad_mps float NULL DEFAULT 0.0,*/
		activo_mps bool DEFAULT true,
		CONSTRAINT pk PRIMARY KEY (id_mps)
	);

INSERT into materias_primas (nombre_mps)
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

CREATE table proveedores (
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

INSERT into proveedores (nombre_proveedores)
VALUES
	('Lipotec'),
	('Seppic'),
	('Veracetics'),
	('Escuder'),
	('Provital'),
	('Interfat'),
	('Coralis'),
	('DKSH'),
	('Quimidroga'),
	('M2C2 Lab'),
	('Saffic');

CREATE table rel_mps_proveedores (
		mp_id_rmp int4 NOT NULL,
		proveedor_id_rmp int4 NOT NULL,
		CONSTRAINT pk_rel_mps_proveedores PRIMARY KEY (mp_id_rmp, proveedor_id_rmp),
		CONSTRAINT fk1_rel_mps_proveedores FOREIGN KEY (mp_id_rmp) REFERENCES materias_primas (id_mps),
		CONSTRAINT fk2_mrel_mps_proveedores FOREIGN KEY (proveedor_id_rmp) REFERENCES proveedores (id_proveedores)
	);

insert into rel_mps_proveedores (mp_id_rmp, proveedor_id_rmp)
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

CREATE table cosmeticos (
		id_cosmeticos serial NOT NULL,
		nombre_cosmeticos varchar(45) NOT NULL,
		fecha_cad_cosmeticos int default 36,
		tipo_id_cosmeticos int not null,
		cliente_id_cosmeticos int not null,
		activo_cosmeticos bool default true,
		CONSTRAINT pk_cosmeticos PRIMARY KEY (id_cosmeticos),
		CONSTRAINT fk1_cosmeticos FOREIGN KEY (tipo_id_cosmeticos) REFERENCES tipos (id_tipos),
		CONSTRAINT fk2_cosmeticos FOREIGN KEY (cliente_id_cosmeticos) REFERENCES clientes (id_clientes)
	
	);

insert
	into
	cosmeticos (
		nombre_cosmeticos,
		cliente_id_cosmeticos,
		tipo_id_cosmeticos
	)
values
	('Crema día',
1,
1),
	('Crema noche',
1,
1),
	('Contorno ojos',
1,
2),
	('Gel aloe',
2,
2),
	('Tónico',
2,
3);

CREATE table rel_cosm_mp (
		cosm_id_rcm int NOT NULL,
		mp_id_rcm int NOT NULL,
		porcentaje_rcm decimal(10, 2),
		CONSTRAINT pk_rel_cosm_mp PRIMARY KEY (cosm_id_rcm, mp_id_rcm),
		CONSTRAINT fk1_rel_cosm_mp FOREIGN KEY (cosm_id_rcm) REFERENCES cosmeticos (id_cosmeticos),
		CONSTRAINT fk2_rel_cosm_mp FOREIGN KEY (mp_id_rcm) REFERENCES materias_primas (id_mps)
	);

INSERT into rel_cosm_mp VALUES
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

CREATE table ubicaciones (
		id_ubicaciones serial NOT NULL,
		nombre_ubicaciones varchar(20),
		activo_ubicaciones bool default true,
		CONSTRAINT pk_ubicaciones PRIMARY KEY (id_ubicaciones)
	);

INSERT into ubicaciones (nombre_ubicaciones)
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
	('0102A03');
	/*
	('0102B01'),
	('0102B02'),
	('0102B03'),
	('0102C01'),
	('0102C02'),
	('0102C03'),
	('0102D01'),
	('0102D02'),
	('0102D03');
*/

CREATE table entradas_lotes (
		id_ent_el serial not null,
		mp_id_el int not null,
		proveedor_id_el int not null,
		fecha_el date,
		fecha_cad_el date,
		cantidad_el int,
		nombre_lotes varchar(10),
		cantidad_lotes_el decimal(10, 2),
		ubicacion_id_el int,
		CONSTRAINT pk_el PRIMARY KEY (id_ent_el),
		CONSTRAINT fk1_el FOREIGN KEY (mp_id_el,proveedor_id_el) REFERENCES rel_mps_proveedores(mp_id_rmp,proveedor_id_rmp),
		CONSTRAINT fk2_el FOREIGN KEY (ubicacion_id_el) REFERENCES ubicaciones (id_ubicaciones)
	);

INSERT into entradas_lotes (
		mp_id_el,
		proveedor_id_el,
		fecha_el,
		fecha_cad_el,
		nombre_lotes,
		cantidad_el,
		cantidad_lotes_el,
		ubicacion_id_el
		
	)
VALUES
	(1, 10, '2028-11-26', '2028-11-26', 'MF0001', 1000000,1000000,1),
	(2, 1, '2028-11-26', '2028-11-26', 'MF0001', 20000,20000,2),
	(3, 2, '2028-11-26', '2028-11-26', 'MF0002', 25000,25000,3),
	(4, 3, '2028-11-26', '2028-11-26', 'MF0003', 2000,2000,4),
	(5, 4, '2028-11-26', '2028-11-26', 'MF0004', 5000,5000,5),
	(6, 4, '2028-11-26', '2028-11-26', 'MF0005', 5000,5000,6),
	(7, 6, '2028-11-26', '2028-11-26', 'MF0006', 5000,5000,7),
	(8, 7, '2028-11-26', '2028-11-26', 'MF0007', 25000,25000,8),
	(9, 8, '2028-11-26', '2028-11-26', 'MF0008', 1000,1000,9),
	(10, 9, '2028-11-26', '2028-11-26', 'MF009', 200000,200000,10),
	(11, 4, '2028-11-26', '2028-11-26', 'MF0010', 5000,5000,11),
	(12, 4, '2028-11-26', '2028-11-26', 'MF0011', 250000,25000,12),
	(13, 9, '2028-11-26', '2028-11-26', 'MF0012', 5000,5000,13),
	(14, 4, '2028-11-26', '2028-11-26', 'MF0013', 10000,10000,14),
	(15, 8, '2028-11-26', '2028-11-26', 'MF0014', 200000,20000,15);



CREATE table ordenes (
		id_ordenes serial NOT NULL,
		cosmetico_id_ordenes int NOT NULL,
		fecha_fab_ordenes date NOT NULL,
		lote_ordenes varchar(10) NOT NULL,
		cantidad_ordenes int NOT NULL,
		fecha_cad_ordenes date NOT NULL,
		equipo_id_ordenes int NOT NULL,
		indicaciones_ordenes varchar(1000) NULL,
		CONSTRAINT ch CHECK ((fecha_fab_ordenes < fecha_cad_ordenes)),
		CONSTRAINT pk_ofab PRIMARY KEY (id_ordenes),
		CONSTRAINT fk_ofab1 FOREIGN KEY (cosmetico_id_ordenes) REFERENCES cosmeticos (id_cosmeticos),
		CONSTRAINT fk_ofab2 FOREIGN KEY (equipo_id_ordenes) REFERENCES equipos (id_equipos)
	);

INSERT into ordenes (
		cosmetico_id_ordenes,
		fecha_fab_ordenes,
		lote_ordenes,
		cantidad_ordenes,
		fecha_cad_ordenes,
		equipo_id_ordenes
	)
VALUES
	(1, '2024-10-25', 'MF0015',50,'2027-12-24', 3),
	(1, '2024-11-26', 'MF0016',250, '2027-12-25', 4);

