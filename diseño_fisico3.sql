--Creación de la tabla tipos de cosméticos y inserción de los datos
CREATE TABLE
    tipos (
        id_tipos serial NOT NULL,
        nombre_tipos varchar(10),
        activo_tipos bool default true,
        CONSTRAINT pk_tipos PRIMARY KEY (id_tipos)
    );

INSERT INTO
    tipos (nombre_tipos)
values
    ('Emulsión'),
    ('Gel'),
    ('Polvo'),
    ('Solución');
-- Creación de la tabla salas donde se encuentran los equipos.
create table
    salas (
        id_salas serial not null,
        nombre_salas varchar(20),
        activo_salas bool default true,
        constraint pk_salas primary key (id_salas)
    );

INSERT into
    salas (nombre_salas)
VALUES
    ('Pesada'),
    ('Fabricación 1'),
    ('Fabricación 2'),
    ('Envasado 1'),
    ('Envasado 2'),
    ('Acondicionamiento');
--Creación de la tabla equipos donde se realizan las detalle_o_fabricaciones
CREATE table
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

INSERT into
    equipos (
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
--Creación de la tabla clientes propietarios de los cosméticos que se fabrican en el laboratorio.
CREATE table
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

INSERT into
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
--Creación de las la tabla materias primas con las que se hacen los cosméticos.
CREATE table
    materias_primas (
        id_mps serial NOT NULL,
        nombre_mps varchar(50) NULL,
        /*cantidad_mps decimal(10, 2),*/
        activo_mps bool DEFAULT true,
        CONSTRAINT pk PRIMARY KEY (id_mps)
    );

INSERT into
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
--Creación de la tabla proveedores que son los que suministran las materias primas.
CREATE table
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

INSERT into
    proveedores (nombre_proveedores)
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
--Creación de la tabla rel_mps_proveedores que se obtiene de una relación muchos a muchos entre las tablas materias primas y proveedores.
CREATE table
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
    (16,9),
    (3, 11),
    (4, 4),
    (2, 9),
    (10, 4),
    (4, 8);
--Creación de la tabla cosmeticos, son los productos que se fabrican en el laboratorio.
CREATE table
    cosmeticos (
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

insert into
    cosmeticos (
        nombre_cosmeticos,
        cliente_id_cosmeticos,
        tipo_id_cosmeticos
    )
values
    ('Crema día', 1, 1),
    ('Crema noche', 1, 1),
    ('Contorno ojos', 1, 2),
    ('Gel aloe', 2, 2),
    ('Tónico', 2, 3);
--Creación de la tabla rel_cosm_mp que se obtiene de uan relación muchos a muchos entre cosméticos y materias primas e indica la composición del cosmético.
CREATE table
    rel_cosm_mp (
        cosm_id_rcm int NOT NULL,
        mp_id_rcm int NOT NULL,
        porcentaje_rcm decimal(10, 2),
        CONSTRAINT pk_rel_cosm_mp PRIMARY KEY (cosm_id_rcm, mp_id_rcm),
        CONSTRAINT fk1_rel_cosm_mp FOREIGN KEY (cosm_id_rcm) REFERENCES cosmeticos (id_cosmeticos),
        CONSTRAINT fk2_rel_cosm_mp FOREIGN KEY (mp_id_rcm) REFERENCES materias_primas (id_mps)
    );

INSERT into
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
--Creación de la tabla ubicaciones, en cada ubicación se almacena una materia prima. ******SE PODRÍA CAMBIAR PARA NO TENER TANTAS UBICACIONES*******
CREATE table
    ubicaciones (
        id_ubicaciones serial NOT NULL,
        nombre_ubicaciones varchar(20),
        libre_ubicaciones bool DEFAULT true,
        activo_ubicaciones bool default true,
        CONSTRAINT pk_ubicaciones PRIMARY KEY (id_ubicaciones)
    );

INSERT into
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
-- Creación de la tabla lotes_stock. Representa el inventario de materias primas con lotes y cantidades.
create table
    lotes_stock (
        id_lotes_stock serial not null,
        nombre_lotes_stock varchar(10) unique,
        cantidad_lotes_stock DECIMAL(10, 2),
        fecha_caducidad_lotes_stock date,
        mp_id_lotes_stock int,
        constraint pk_id_lotes_stock primary key (id_lotes_stock),
        constraint fk_mp_id_lotes_stock foreign key (mp_id_lotes_stock) references materias_primas (id_mps)
    );

CREATE TABLE
    entradas (
        id_ent serial NOT NULL,
        mp_id_ent int not null,
        proveedor_id_ent int not null,
        fecha_ent date,
        nombre_lotes_ent varchar(10) unique,
        fecha_caducidad_ent date not null,
        cantidad_ent decimal(10, 2),
        ubi_id_ent int unique,
        CONSTRAINT pk_entradas PRIMARY KEY (id_ent),
        constraint fk1_entradas foreign KEY (mp_id_ent, proveedor_id_ent) references rel_mps_proveedores (mp_id_rmp, proveedor_id_rmp),
        CONSTRAINT fk2_entradas FOREIGN KEY (ubi_id_ent) REFERENCES ubicaciones (id_ubicaciones)
    );

--Funcion para generar de forma automatica los lotes de entrada de las materias primas
CREATE OR REPLACE FUNCTION generar_lote_entradas()
RETURNS TRIGGER AS $$
BEGIN
NEW.nombre_lotes_ent := 'BT' || NEW.id_ent;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--Trigger que ejecuta la funcion generar_lote_entradas() despues de realizar una entrada de materia prima para generar el lote de entrada. 
create trigger after_insert_entrada
before
insert
on
entradas
for each row
execute function generar_lote_entradas();
--Fución que cambia el estado de la ubicación que se utiliza para almacenar una materia prima después de su correspondiente entrada.
CREATE OR REPLACE FUNCTION estado_ubicacion()
RETURNS TRIGGER AS $$
BEGIN
UPDATE ubicaciones
SET libre_ubicaciones = false
WHERE id_ubicaciones = NEW.ubi_id_ent;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- Trigger que  ejecuta la función after_insert_entrada2() para cambiar el estado de la ubicación que acaba de ser ocupada por una materia prima.
create trigger after_insert_entrada2
after
insert
on
entradas
for each row
execute function estado_ubicacion();
 -- Creación de la tabla ordenes. Cada inserción representa una fabricación de un cosmético en la que se indica cantidad a fabricar. Se el asigna un lote y una fecha de caducidad "en función de la caducidad del cosmetico, esto todavía no lo hace".
CREATE table
    ordenes (
        id_ordenes serial NOT NULL,
        fecha_fab_ordenes date NOT NULL,
        cosmetico_id_ordenes int not null,
        lote_ordenes varchar(10) NOT NULL,
        cantidad_ordenes int NOT NULL,
        fecha_cad_ordenes date NOT NULL,
        equipo_id_ordenes int NOT NULL,
        indicaciones_ordenes varchar(1000) NULL,
        CONSTRAINT ch CHECK ((fecha_fab_ordenes < fecha_cad_ordenes)),
        CONSTRAINT pk_ofab PRIMARY KEY (id_ordenes),
        CONSTRAINT fk1_ofab FOREIGN KEY (cosmetico_id_ordenes) REFERENCES cosmeticos (id_cosmeticos),
        CONSTRAINT fk2_ofab FOREIGN KEY (equipo_id_ordenes) REFERENCES equipos (id_equipos)
    );

--Genera de forma automatica el lote y la fecha de caducidad de la orden
CREATE OR REPLACE FUNCTION generar_fecha_caducidad_orden()
RETURNS TRIGGER AS $$
BEGIN
NEW.lote_ordenes := 'OF' || NEW.id_ordenes;
NEW.fecha_cad_ordenes := NEW.fecha_fab_ordenes+INTERVAL '3 years';
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

create trigger genera_fecha_cad_orden
before
insert
on
ordenes
for each row
execute function generar_fecha_caducidad_orden();


 
insert into
    ordenes (
        fecha_fab_ordenes,
        cosmetico_id_ordenes,
        cantidad_ordenes,
        equipo_id_ordenes
    )
values
    ('2024-11-03', 1, 200, 4),
    ('2024-10-25', 2, 100, 3);


-- Función para insertar automaticamente los datos en la tabla lotes_stock()
create or replace
function insertar_en_lotes_stock()
returns trigger as $$
begin
insert
into
lotes_stock (nombre_lotes_stock,
cantidad_lotes_stock,
fecha_caducidad_lotes_stock,
mp_id_lotes_stock)
values (NEW.nombre_lotes_ent,
NEW.cantidad_ent,
NEW.fecha_caducidad_ent,
NEW.mp_id_ent);

return new;
end;

$$ language plpgsql;

create trigger after_insert_entradas
after
insert
	on
	entradas
for each row
execute function insertar_en_lotes_stock();
 
insert
	into
	entradas (
        fecha_ent,
	mp_id_ent,
	proveedor_id_ent,
	cantidad_ent,
	fecha_caducidad_ent,
	ubi_id_ent
    )
values
    ('2024-11-02',
1,
10,
1000000,
'2028-11-02',
1),
    ('2024-11-02',
2,
1,
5000,
'2028-11-02',
2),
    ('2024-11-02',
3,
2,
5000,
'2028-11-02',
3),
    ('2024-11-02',
4,
3,
5000,
'2028-11-02',
4),
    ('2024-11-02',
5,
4,
5000,
'2028-11-02',
5),
    ('2024-11-02',
6,
4,
5000,
'2028-11-02',
6),
    ('2024-11-02',
7,
6,
5000,
'2028-11-02',
7),
    ('2024-11-02',
8,
7,
5000,
'2028-11-02',
8),
    ('2024-11-02',
9,
8,
5000,
'2028-11-02',
9),
    ('2024-11-02',
10,
9,
5000,
'2028-11-02',
10),
    ('2024-11-02',
11,
4,
5000,
'2028-11-02',
11),
    ('2024-11-02',
12,
4,
5000,
'2028-11-02',
12),
    ('2024-11-02',
13,
9,
5000,
'2028-11-02',
13),
('2024-11-02',
14,
4,
5000,
'2028-11-02',
14),
('2024-11-02',
15,
8,
5000,
'2028-11-02',
15),
('2024-11-02',
16,
9,
15000,
'2028-11-02',
16);
    
 --Creación de la tabla fabricación. Representa los datos de las materias primas empleadas en una orden de fabricación  
create table detalle_o_fabricacion(

        orden_id_fab int not null,
        lote_id_fab int not null,
        mp_id_fab int not null,
        cantidad_fab decimal(10,2) not null,
        constraint pk_fab primary key (orden_id_fab,
lote_id_fab),
        constraint fk1_fab foreign key(orden_id_fab) references ordenes(id_ordenes),
        constraint fk2_fab foreign key(lote_id_fab) references lotes_stock(id_lotes_stock),
        constraint fk3_fab foreign key(mp_id_fab) references materias_primas(id_mps) 
    );

-- La inserción de datos se debe hacer de forma automatica y también se debe descontar de la tabla lotes_stock las cantidades empleadas.
--Hay que ve si es más fácil hacerlo mediante código o con funciones y trigger en la base de datos. Creo que lo segundo
  /*
   -- Función para insertar datos en detalle_o_fabricacion y descontar cantidades
CREATE OR REPLACE FUNCTION insertar_detalle_o_fabricacion_y_descontar()
RETURNS TRIGGER AS $$
DECLARE
    cosmetico_actual INTEGER;
    materias_primas RECORD;
    lote_disponible RECORD;
    cantidad_necesaria DECIMAL(10,2);
    cantidad_restante DECIMAL(10,2);
BEGIN
    -- Obtener el cosmético de la orden
    SELECT cosmetico_id_ordenes INTO cosmetico_actual 
    FROM ordenes 
    WHERE id_ordenes = NEW.orden_id_fab;

    -- Iterar sobre las materias primas del cosmético
    FOR materias_primas IN 
        SELECT mp_id_rcm, porcentaje_rcm 
        FROM rel_cosm_mp 
        WHERE cosm_id_rcm = cosmetico_actual
    LOOP
        -- Calcular la cantidad necesaria de la materia prima
        cantidad_necesaria := (NEW.cantidad_fab * materias_primas.porcentaje_rcm) / 100;

        -- Buscar lotes disponibles de la materia prima
        FOR lote_disponible IN 
            SELECT id_lotes_stock, cantidad_lotes_stock 
            FROM lotes_stock 
            WHERE mp_id_lotes_stock = materias_primas.mp_id_rcm 
            AND cantidad_lotes_stock > 0 
            ORDER BY fecha_caducidad_lotes_stock
        LOOP
            -- Determinar cuánto se puede tomar de este lote
            IF lote_disponible.cantidad_lotes_stock >= cantidad_necesaria THEN
                -- Insertar en detalle_o_fabricacion
                INSERT INTO detalle_o_fabricacion (
                    orden_id_fab, 
                    lote_id_fab, 
                    mp_id_fab, 
                    cantidad_fab
                ) VALUES (
                    NEW.orden_id_fab,
                    lote_disponible.id_lotes_stock,
                    materias_primas.mp_id_rcm,
                    cantidad_necesaria
                );

                -- Descontar de lotes_stock
                UPDATE lotes_stock
                SET cantidad_lotes_stock = cantidad_lotes_stock - cantidad_necesaria
                WHERE id_lotes_stock = lote_disponible.id_lotes_stock;

                EXIT;  -- Salir del bucle de lotes
            ELSE
                -- Insertar parcialmente
                INSERT INTO detalle_o_fabricacion (
                    orden_id_fab, 
                    lote_id_fab, 
                    mp_id_fab, 
                    cantidad_fab
                ) VALUES (
                    NEW.orden_id_fab,
                    lote_disponible.id_lotes_stock,
                    materias_primas.mp_id_rcm,
                    lote_disponible.cantidad_lotes_stock
                );

                -- Actualizar cantidad necesaria
                cantidad_necesaria := cantidad_necesaria - lote_disponible.cantidad_lotes_stock;

                -- Poner a cero el lote
                UPDATE lotes_stock
                SET cantidad_lotes_stock = 0
                WHERE id_lotes_stock = lote_disponible.id_lotes_stock;
            END IF;
        END LOOP;

        -- Verificar si se pudo obtener toda la cantidad necesaria
        IF cantidad_necesaria > 0 THEN
            RAISE EXCEPTION 'No hay suficiente cantidad de materia prima %', materias_primas.mp_id_rcm;
        END IF;
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para ejecutar la función
CREATE TRIGGER after_insert_detalle_o_fabricacion
AFTER INSERT ON ordenes
FOR EACH ROW
EXECUTE FUNCTION insertar_detalle_o_fabricacion_y_descontar();
   */
   
  /*
CREATE OR REPLACE FUNCTION insertar_detalle_o_fabricacion(p_orden_id INT, p_cosmetico_id INT)
RETURNS VOID AS $$
DECLARE
    v_cantidad_necesaria NUMERIC;
    v_cantidad_stock NUMERIC;
BEGIN
    -- Calcular la cantidad necesaria
    SELECT 
        o.cantidad_ordenes * rcm.porcentaje_rcm / 100,
        ls.cantidad_lotes_stock
    INTO v_cantidad_necesaria, v_cantidad_stock
    FROM ordenes o
        INNER JOIN cosmeticos c ON o.cosmetico_id_ordenes = c.id_cosmeticos
        INNER JOIN rel_cosm_mp rcm ON c.id_cosmeticos = rcm.cosm_id_rcm
        INNER JOIN materias_primas mp ON rcm.mp_id_rcm = mp.id_mps
        INNER JOIN lotes_stock ls ON mp.id_mps = ls.mp_id_lotes_stock
    WHERE o.id_ordenes = p_orden_id
        AND c.id_cosmeticos = p_cosmetico_id
    LIMIT 1;

    -- Verificar si hay suficientes existencias
    IF v_cantidad_stock >= v_cantidad_necesaria THEN
        INSERT INTO detalle_o_fabricacion (
            orden_id_fab,
            lote_id_fab,
            mp_id_fab,
            cantidad_fab
        )
        SELECT DISTINCT
            o.id_ordenes,
            ls.id_lotes_stock,
            ls.mp_id_lotes_stock,
            v_cantidad_necesaria
        FROM ordenes o
            INNER JOIN cosmeticos c ON o.cosmetico_id_ordenes = c.id_cosmeticos
            INNER JOIN rel_cosm_mp rcm ON c.id_cosmeticos = rcm.cosm_id_rcm
            INNER JOIN materias_primas mp ON rcm.mp_id_rcm = mp.id_mps
            INNER JOIN lotes_stock ls ON mp.id_mps = ls.mp_id_lotes_stock
        WHERE o.id_ordenes = p_orden_id
            AND c.id_cosmeticos = p_cosmetico_id
            AND ls.cantidad_lotes_stock >= v_cantidad_necesaria
        LIMIT 1;
    ELSE
        RAISE EXCEPTION 'No hay suficientes existencias en stock para fabricar esta orden.';
    END IF;
END;
$$ LANGUAGE plpgsql;


*/ 