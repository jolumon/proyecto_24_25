from PySide6.QtWidgets import QWidget, QTableView, QHeaderView, QAbstractItemView

from productos.view.ui_ventana_producto_detalle6 import Ui_Form
from productos.model.ventana_fabricaciones_prod import VentanaFabricación
from auxiliares import VentanaEmergenteBorrar, VentanaEmergenteFaltaMPs, VentanaFaltanDatos, VentanaFaltaSeleccionarFila
from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt, QDate, QSortFilterProxyModel


class VentanaDetalle(QWidget, Ui_Form):
    def __init__(self, ventana_producto):
        super().__init__()
        self.setupUi(self)

        self.ventana_producto = ventana_producto

        self.showMaximized()

# Mostrar tipos de productos en el comboBox
        self.diccionario_tipo_prod = {}

        query_tipo_prod = QSqlQuery()
        query_tipo_prod.prepare(
            """
                select
                    id_tipos ,
                    nombre_tipos
                from
                    tipos
                where
                    activo_tipos = true
                order by 
                    nombre_tipos
            """
        )
        if query_tipo_prod.exec():
            while query_tipo_prod.next():
                tipo_id = query_tipo_prod.value(0)
                nombre_tipo = query_tipo_prod.value(1)
                self.cb_tipo.addItem(nombre_tipo)
                self.diccionario_tipo_prod[nombre_tipo] = tipo_id

        # Mostrar equipos en el comboBox
        self.diccionario_equipos = {}

        query_equipos = QSqlQuery()
        query_equipos.prepare(
            f'select id_equipos, nombre_equipos from equipos where activ_equipos = true order by id_equipos')

        if query_equipos.exec():
            while query_equipos.next():
                equipo_id = query_equipos.value(0)
                nombre = query_equipos.value(1)
                self.cb_equipo_fab.addItem(nombre)
                self.diccionario_equipos[nombre] = equipo_id

        self.cb_equipo_fab.setCurrentIndex(-1)

        # Mostrar clientes en el comboBox

        self.diccionario_clientes_act = {}

        query_clientes_actualizar = QSqlQuery()
        query_clientes_actualizar.prepare(
            f'select id_clientes, nombre_clientes from clientes where activo_clientes=true order by nombre_clientes')

        if query_clientes_actualizar.exec():
            while query_clientes_actualizar.next():
                cliente_id = query_clientes_actualizar.value(0)
                nombre_cli = query_clientes_actualizar.value(1)
                self.cb_cliente.addItem(nombre_cli)
                self.diccionario_clientes_act[nombre_cli] = cliente_id

        # Signals and Slots

        self.btn_cerrar_det.clicked.connect(self.close)
        self.btn_cerrar_fab.clicked.connect(self.close)
        self.btn_borrar_det.clicked.connect(self.borrar_producto)
        self.btn_actualizar_det.clicked.connect(self.actualizar_producto)
        self.btn_confirmar_fab.clicked.connect(self.add_fab)
        self.btn_mostrar_pesada.clicked.connect(self.mostrar_pesada)
        self.btn_ver_detalle_o_fab.clicked.connect(
            self.ver_detalle_lote_fabricacion)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_producto.show()
        event.accept()

    def borrar_producto(self):
        print(f'Borrado')
        ventana_confirmacion = VentanaEmergenteBorrar()
        respuesta = ventana_confirmacion.exec()

        if respuesta:

            codigo = int(self.le_codigo_det.text())
            # print(type(codigo))
            query = QSqlQuery()
            query.prepare(
                "UPDATE cosmeticos set activo_cosmeticos= false WHERE id_cosmeticos=:codigo")
            # query.bindValue(":nombre", nombre)
            query.bindValue(":codigo", codigo)
            query.exec()

            self.ventana_producto.initial_query.exec(
                "select cos.id_cosmeticos,cos.nombre_cosmeticos , cos.fecha_cad_cosmeticos, c.nombre_clientes  from cosmeticos cos inner join clientes c on cos.cliente_id_cosmeticos =c.id_clientes  where cos.activo_cosmeticos=true order by cos.id_cosmeticos asc")
            self.ventana_producto.model.setQuery(
                self.ventana_producto.initial_query)

            self.close()
            self.ventana_producto.tabWidget.setCurrentIndex(1)
            self.ventana_producto.tv_productos.selectRow(0)

    def add_fab(self):

        if self.obtener_clave_principal_equipo() == None or self.le_cantidad_fab.text() == "":
            print("Faltan datos por introducir")
            ventana_faltan_datos = VentanaFaltanDatos()
            respuesta = ventana_faltan_datos.exec()
            return

        # # print (f'Mostrar pesada: {self.mostrar_pesada()}')

        codigo = int(self.le_codigo_det.text())
        fecha_fab = QDate.currentDate()

        fecha_caducidad = self.calcular_fecha_cad(fecha_fab, codigo)

        print(f'Fecha cad: {fecha_caducidad}')

        new_lote = self.get_last_batch()

        equipo = int(self.obtener_clave_principal_equipo())

        cantidad = int(self.le_cantidad_fab.text())

        if self.mostrar_pesada() == False:
            print("No se puede fabricar por falta de materias primas")
            ventana_falta_mp = VentanaEmergenteFaltaMPs()
            respuesta = ventana_falta_mp.exec()
            self.mostrar_pesada()

            # self.close()

        else:
            query_add_fab = QSqlQuery()
            query_add_fab.prepare(
                f"""insert into
                            ordenes (
                                fecha_fab_ordenes,
                                cosmetico_id_ordenes,
                                cantidad_ordenes ,
                                lote_ordenes,
                                fecha_cad_ordenes ,
                                equipo_id_ordenes )
                            values (
                                :fecha_fab,
                                :codigo,
                                :cantidad,
                                :new_lote,
                                :fecha_caducidad,
                                :equipo)"""
            )

            query_add_fab.bindValue(":fecha_fab", fecha_fab)
            query_add_fab.bindValue(":codigo", codigo)
            query_add_fab.bindValue(":cantidad", cantidad)
            query_add_fab.bindValue(":new_lote", new_lote)
            query_add_fab.bindValue(":fecha_caducidad", fecha_caducidad)
            query_add_fab.bindValue(":equipo", equipo)

            query_add_fab.exec()
            print('Añadida fabricación')

            id_fab_añadida = self.get_last_order()
            print(f"Fabricación añadida: {id_fab_añadida}")

            self.actualiza_stock(cantidad, codigo)

            self.ventana_producto.initial_query.exec(
                "select cos.id_cosmeticos,cos.nombre_cosmeticos , cos.fecha_cad_cosmeticos, c.nombre_clientes  from cosmeticos cos inner join clientes c on cos.cliente_id_cosmeticos =c.id_clientes  where cos.activo_cosmeticos=true order by cos.id_cosmeticos asc")

            self.ventana_producto.model.setQuery(
                self.ventana_producto.initial_query)

            self.close()
            self.ventana_producto.tabWidget.setCurrentIndex(1)
            self.ventana_producto.tv_productos.selectRow(0)

    def mostrar_pesada(self):
        if self.le_cantidad_fab.text() == "":
            print("Falta introducir la cantidad a fabricar")
            ventana_faltan_datos = VentanaFaltanDatos()
            respuesta = ventana_faltan_datos.exec()
            return

        else:
            codigo = int(self.le_codigo_det.text())
            cantidad = int(self.le_cantidad_fab.text())

            # print(f'Código despues del else: {codigo}')
            # print(f'Cantidad despues del else: {cantidad}')

            # Crear un model de tabla
            self.weight_query = QSqlQuery()
            # self.weight_query.prepare("select ls.mp_id_lotes_stock,	mp.nombre_mps,:cantidad * rcm.porcentaje_rcm / 100,ls.cantidad_lotes_stock,	ls.nombre_lotes_stock ,ls.cantidad_lotes_stock - :cantidad * rcm.porcentaje_rcm / 100 from lotes_stock ls inner join materias_primas mp on ls.mp_id_lotes_stock = mp.id_mps inner join rel_cosm_mp rcm on mp.id_mps = rcm.mp_id_rcm where rcm.cosm_id_rcm = :id_prod_fab order by mp_id_lotes_stock")
            self.weight_query.prepare("""
                                         select ls.mp_id_lotes_stock as "Código",
                                                 mp.nombre_mps as "Nombre",
                                                  :cantidad*rcm.porcentaje_rcm/100,
                                                 sum(ls.cantidad_lotes_stock)
                                            from lotes_stock ls
                                            inner join materias_primas mp on ls.mp_id_lotes_stock=mp.id_mps
                                            inner join rel_cosm_mp rcm on mp.id_mps=rcm.mp_id_rcm
                                            where rcm.cosm_id_rcm= :cosmetico
                                            group by ls.mp_id_lotes_stock, mp.nombre_mps ,rcm.porcentaje_rcm
                                      """)

            self.weight_query.bindValue(":cosmetico", codigo)
            self.weight_query.bindValue(":cantidad", cantidad)
            if self.weight_query.exec():
                # print("Dentro del if de mostrar_pesada")

                todo_true = True

                while self.weight_query.next() and todo_true:
                    # print("Dentro del while")

                    prueba_id_mp = self.weight_query.value(0)
                    prueba_nombre = self.weight_query.value(1)
                    calculado = self.weight_query.value(2)
                    cantidad_mp = self.weight_query.value(3)
                    # prueba_lote_mp = self.weight_query.value(4)
                    # prueba_restante = self.weight_query.value(5)

                    if cantidad_mp < calculado:
                        todo_true = False
                        # Si falta más de un producto no avisaría
                        print("Enviando email al departamento de compras")
            # print(todo_true)
            # No es necesario seguir iterando si ya encontramos un caso donde no se cumple la condición

            # print("Fin del while")

            self.weigth_model = QSqlQueryModel()
            self.weigth_model.setQuery(self.weight_query)

            # cabeceras_pesada = ['Código', 'Materia Prima', 'Lote',
            #                     'Stock / kg', 'Cantidad Necesaria / kg', 'Suficiente Materia Prima']
            # cabeceras_pesada = [
            #     'Código', 'Materia Prima', 'Necesario / g', 'Stock / kg', 'Lote', 'Restante / g']
            cabeceras_pesada = [
                'Código', 'Materia Prima', 'Necesario / g', 'Stock / kg']
            for i, cabecera in enumerate(cabeceras_pesada):
                self.weigth_model.setHeaderData(i, Qt.Horizontal, cabecera)

            self.tv_detalle_new_fab.setModel(self.weigth_model)
            self.tv_detalle_new_fab.setSelectionBehavior(QTableView.SelectRows)
            self.tv_detalle_new_fab.setSelectionMode(
                QTableView.SingleSelection)

            # Configurar la vista de tabla
            self.tv_detalle_new_fab.resizeRowsToContents()
            self.tv_detalle_new_fab.resizeColumnsToContents()
            self.tv_detalle_new_fab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            self.tv_detalle_new_fab.show()

        return todo_true

    def obtener_clave_principal_equipo(self):
        nombre_seleccionado = self.cb_equipo_fab.currentText()
        clave_principal = self.diccionario_equipos.get(nombre_seleccionado)

        print(f'Nombre seleccionado: {nombre_seleccionado}')
        print(f'Clave principal: {clave_principal}')

        return clave_principal

    def actualizar_producto(self):

        codigo = int(self.le_codigo_det.text())
        nombre = self.le_nombre_det.text()
        caducidad = self.le_caducidad_det.text()

        # Mostrar tipos de productos en el comboBox
        self.diccionario_tipo_prod = {}

        query_tipo_prod = QSqlQuery()
        query_tipo_prod.prepare(
            """
                select
                    id_tipos ,
                    nombre_tipos
                from
                    tipos
                where
                    activo_tipos = true
                order by 
                    nombre_tipos
            """
        )
        if query_tipo_prod.exec():
            while query_tipo_prod.next():
                tipo_id = query_tipo_prod.value(0)
                nombre_tipo = query_tipo_prod.value(1)
                self.cb_tipo.addItem(nombre_tipo)
                self.diccionario_tipo_prod[nombre_tipo] = tipo_id

        tipo_ids = self.obtener_clave_principal_tipo()

        # Mostrar clientes en el comboBox
        self.diccionario_clientes_act = {}

        query_clientes_actualizar = QSqlQuery()
        query_clientes_actualizar.prepare(
            f'select id_clientes, nombre_clientes from clientes where activo_clientes=true order by nombre_clientes')

        if query_clientes_actualizar.exec():
            while query_clientes_actualizar.next():
                cliente_id = query_clientes_actualizar.value(0)
                nombre_cli = query_clientes_actualizar.value(1)
                self.cb_cliente.addItem(nombre_cli)
                self.diccionario_clientes_act[nombre_cli] = cliente_id

        # cliente = self.cb_cliente.currentText()

        cliente_ids = int(self.obtener_clave_principal())

        query_actualizar = QSqlQuery()
        query_actualizar.prepare(
            f'update cosmeticos set nombre_cosmeticos=:nombre,fecha_cad_cosmeticos=:caducidad,tipo_id_cosmeticos=:tipo_id, cliente_id_cosmeticos=:cliente_id where id_cosmeticos = :codigo')
        query_actualizar.bindValue(":nombre", nombre)
        query_actualizar.bindValue(":caducidad", caducidad)
        query_actualizar.bindValue(":tipo_id", tipo_ids)
        query_actualizar.bindValue(":cliente_id", cliente_ids)
        query_actualizar.bindValue(":codigo", codigo)

        query_actualizar.exec()

        # print(f'Nombre:{nombre}')
        # print(f'Caducidad:{caducidad}')
        # print(f'Cliente_ids:{cliente_ids}')
        # print(f'Cliente_id:{cliente_id}')
        # print(f'Código: {codigo}')

        # print(f'{type(nombre)}-{type(caducidad)}-{type(cliente_ids)}-{type(codigo)}')

        self.ventana_producto.initial_query.exec(
            """
                select
                    c.id_cosmeticos,
                    c.nombre_cosmeticos,
                    c.fecha_cad_cosmeticos,
                    t.nombre_tipos ,
                    cli.nombre_clientes
                from
                    cosmeticos c
                inner join clientes cli on
                    c.cliente_id_cosmeticos = cli.id_clientes
                inner join tipos t on
                    c.tipo_id_cosmeticos = t.id_tipos 
                where
                    c.activo_cosmeticos = true
                order by
                    c.id_cosmeticos asc
            """
        )

        self.ventana_producto.model.setQuery(
            self.ventana_producto.initial_query)

        self.close()
        self.ventana_producto.tabWidget.setCurrentIndex(1)
        self.ventana_producto.tv_productos.selectRow(0)

        print(f'Actualizado')

    def obtener_clave_principal(self):
        nombre_seleccionado = self.cb_cliente.currentText()
        clave_principal = self.diccionario_clientes_act.get(
            nombre_seleccionado)

        print(f'Nombre seleccionado: {nombre_seleccionado}')
        print(f'Clave principal: {clave_principal}')

        return clave_principal

    def imprimir_fab(self):
        print('Impresión realizada')

    def add_datos_o_fabricacion(self, cosmetico, cantidad):

        datos_stock = []
        # codigo = int(self.le_codigo_det.text()) #No haría falta, se lo paso como parametro a la función

        stock_query = QSqlQuery()
        stock_query.prepare("""select ls.mp_id_lotes_stock as "Código",
                                      mp.nombre_mps as "Nombre",
                                      sum(ls.cantidad_lotes_stock)
                                from lotes_stock ls
                                inner join materias_primas mp on ls.mp_id_lotes_stock=mp.id_mps
                                inner join rel_cosm_mp rcm on mp.id_mps=rcm.mp_id_rcm
                                where rcm.cosm_id_rcm= :cosmetico
                                group by ls.mp_id_lotes_stock, mp.nombre_mps""")

        stock_query.bindValue(":codigo", cosmetico)

        stock_query.exec()

        while stock_query.next():
            codigo_stock = stock_query.value(0)
            nombre_stock = stock_query.value(1)
            cantidad_stock = stock_query.value(2)

            datos_stock.append(
                {'codigo_stock': codigo_stock,
                 'nombre_stock': nombre_stock,
                 'cantidad_stock': cantidad_stock})

        for mp in datos_stock:
            print(
                f"Código: {mp['codigo_stock']},Nombre:{mp['nombre_stock']},Cantidad:{mp['cantidad_stock']}")

        datos_necesario = []

        necesario_query = QSqlQuery()
        necesario_query.prepare("""select mp.id_mps,
                                          :cantidad * porcentaje_rcm / 100 as "Necesario"
                                    from rel_cosm_mp rcm
                                    inner join materias_primas mp on rcm.mp_id_rcm = mp.id_mps
                                    where rcm.cosm_id_rcm = :cosmetico
                                    order by mp.id_mps""")
        necesario_query.bindValue(":cosmetico", cosmetico)
        necesario_query.bindValue(":cantidad", cantidad)

        necesario_query.exec()

        while necesario_query.next():
            id_mps = necesario_query.value(0)
            necesario = necesario_query.value(1)

            datos_necesario.append({
                'id_mps': id_mps,
                'cantidad_mps': necesario
            })

        for mp_necesario in datos_necesario:
            print(
                f"Código: {mp_necesario['id_mps']},Cantidad:{mp_necesario['cantidad_mps']}")

# """
# ######################################################################################
# #Añadir datos a la tabla detalle_o_fabricacion

    def calcular_fecha_cad(self, fecha_fab, cosmetico):
        query_caducidad = QSqlQuery()
        query_caducidad.prepare(
            "select c.fecha_cad_cosmeticos from cosmeticos c where c.id_cosmeticos = :codigo")

        query_caducidad.bindValue(":codigo", cosmetico)

        if query_caducidad.exec():

            if query_caducidad.next():
                meses = int(query_caducidad.value(0))
                fecha_caducidad = fecha_fab.addMonths(meses)
        return fecha_caducidad

    def get_last_batch(self):
        query_lote = QSqlQuery()
        query_lote.prepare(
            "select max(lote_ordenes) from ordenes ")
        if query_lote.exec():
            if query_lote.next():  # Mueve al primer resultado
                # Obtiene el valor del primer campo
                last_lote = query_lote.value(0)
                print(f'Last lote: {last_lote}')
                # Generar el nuevo lote
                if last_lote.startswith('OF'):
                    # Obtener la parte numérica
                    number_part = int(last_lote[2:])
                    new_lote = f"OF{number_part + 1}"  # Generar el nuevo lote
                else:
                    new_lote = "OF1"  # Si no hay lotes, empezar con OF1
            else:
                new_lote = "OF1"  # Si no hay registros, iniciar con OF1
            print(f'Number_part:{number_part}')
        return new_lote

    def get_last_order(self):
        query_last_order = QSqlQuery()
        query_last_order.prepare(
            "SELECT MAX(id_ordenes) FROM ordenes")
        query_last_order.exec()
        if query_last_order.next():
            last_order_id = query_last_order.value(0)
        return last_order_id

    def actualiza_stock(self, cantidad, cosmetico):

        obtener_mps_cosmetico = QSqlQuery()
        obtener_mps_cosmetico.prepare(
            "select mp_id_rcm from rel_cosm_mp where cosm_id_rcm =:cosmetico order by mp_id_rcm")
        obtener_mps_cosmetico.bindValue(":cosmetico", cosmetico)
        if obtener_mps_cosmetico.exec():
            while obtener_mps_cosmetico.next():
                mp = int(obtener_mps_cosmetico.value(0))
                print(f"id_mp={mp}")

                query_necesario = QSqlQuery()
                query_necesario.prepare("""select :cantidad * porcentaje_rcm / 100 as "Necesario"
                                            from
                                                rel_cosm_mp rcm
                                            inner join materias_primas mp on rcm.mp_id_rcm = mp.id_mps
                                            where
                                                rcm.cosm_id_rcm = :cosmetico and mp.id_mps = :mp_id""")
                query_necesario.bindValue(":cantidad", cantidad)
                query_necesario.bindValue(":cosmetico", cosmetico)
                query_necesario.bindValue(":mp_id", mp)
                if query_necesario.exec():
                    if query_necesario.next():
                        necesario = int(query_necesario.value(0))
                        print(f"Necesario: {necesario}")

                cantidad_mp_orden = necesario
                query_lotes_mp = QSqlQuery()
                query_lotes_mp.prepare(
                    "select * from lotes_stock ls where ls.mp_id_lotes_stock =:mp order by id_lotes_stock asc")
                query_lotes_mp.bindValue(":mp", mp)

                falta = True

                if query_lotes_mp.exec():
                    while query_lotes_mp.next() and falta:
                        id_lotes = query_lotes_mp.value(0)
                        # print("Estoy en el while")
                        if query_lotes_mp.value(2) >= necesario:
                            # print("Estoy en el if query_lotes_mp.value(2) >= necesario")
                            restante = query_lotes_mp.value(2)-necesario

                            falta = False

                        else:
                            restante = 0
                            necesario = necesario-query_lotes_mp.value(2)

                        actualiza_cantidad_lote = QSqlQuery()
                        actualiza_cantidad_lote.prepare("""
                                                                UPDATE lotes_stock SET cantidad_lotes_stock=:restante where id_lotes_stock=:id_lotes_stock
                                                            """)
                        actualiza_cantidad_lote.bindValue(
                            ":restante", restante)
                        actualiza_cantidad_lote.bindValue(
                            ":id_lotes_stock", id_lotes)
                        actualiza_cantidad_lote.exec()

                        self.add_detalle_o_fab(id_lotes, mp, cantidad_mp_orden)

                # también tiene que insertar los datos en detalle_o_fabricacion

    def add_detalle_o_fab(self, lote_id_mp, mp_id, cantidad_mp):

        orden_id_fab = self.get_last_order()

        print(f"Orden Id:{orden_id_fab}")
        print(f"Lote Id:{lote_id_mp}")
        print(f"Id mp:{mp_id}")
        print(f"Cantidad:{cantidad_mp}")

        query_add_detall_fab = QSqlQuery()
        query_add_detall_fab.prepare(
            "insert into detalle_o_fabricacion (orden_id_fab,lote_id_fab,mp_id_fab,cantidad_fab) values (:id_orden,:lote_id_mp,:mp_id,:cantidad_mp)")
        query_add_detall_fab.bindValue(":id_orden", orden_id_fab)
        query_add_detall_fab.bindValue(":lote_id_mp", lote_id_mp)
        query_add_detall_fab.bindValue(":mp_id", mp_id)
        query_add_detall_fab.bindValue(":cantidad_mp", cantidad_mp)

        query_add_detall_fab.exec()

    def filter_fabricaciones(self):
        text = self.le_buscar_fabricacion.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.ventana_producto.proxy_model_fab.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.ventana_producto.proxy_model_fab.setFilterKeyColumn(3)
        # Asegurarse de que el proxy model se actualice
        self.ventana_producto.proxy_model_fab.invalidate()

    def ver_detalle_lote_fabricacion(self):
        print(f"Viendo detalle de la fabricación...")

        fila_seleccionada = self.tv_fab_historico.selectedIndexes()

        print(f"Fila seleccionada: {fila_seleccionada}")
        if fila_seleccionada:
            self.ventana_dof = VentanaFabricación(self)
            row = fila_seleccionada[0].row()
            print(f"Fila: {row}")

            id_pers_index = self.ventana_producto.proxy_model_fab.mapToSource(
                fila_seleccionada[0])
            print(f"id_pers_index:{id_pers_index}")
            id_orden = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 0))
            fecha = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 1))
            fecha_str = fecha.toString("dd/MM/yyyy")
            cantidad = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 2))
            lote = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 3))
            caducidad = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 4))
            caducidad_str = caducidad.toString("dd/MM/yyyy")
            equipo = self.ventana_producto.model_fab.data(
                self.ventana_producto.model_fab.index(id_pers_index.row(), 5))

            print(f"id_orden:{id_orden}")
            print(f"Fecha:{fecha_str}")
            print(f"CAntidad: {cantidad}")
            print(f"Lote: {lote}")
            print(f"Caducidad: {caducidad_str}")

            self.ventana_dof.le_fecha_dof.setText(fecha_str)
            self.ventana_dof.le_cosmetico_dof.setText(
                self.le_nombre_det.text())
            self.ventana_dof.le_cantidad_dof.setText(str(cantidad))
            self.ventana_dof.le_lote_dof.setText(lote)
            self.ventana_dof.le_cadudcidad_dof.setText(caducidad_str)
            self.ventana_dof.le_equipo_dof.setText(equipo)

        # Crear un modelo de tabla

            self.datos_orden_query = QSqlQuery()
            self.datos_orden_query.prepare(
                """SELECT 
                        dof.mp_id_fab ,
                        mp.nombre_mps AS nombre_materia_prima,
                        dof.cantidad_fab,
                        ls.nombre_lotes_stock,
                        u.nombre_ubicaciones
                    FROM 
                        detalle_o_fabricacion dof
                    inner JOIN 
                        lotes_stock ls ON dof.lote_id_fab = ls.id_lotes_stock
                    inner JOIN 
                        entradas e ON ls.nombre_lotes_stock = e.nombre_lotes_ent
                    inner JOIN 
                        ubicaciones u ON e.ubi_id_ent = u.id_ubicaciones
                    inner JOIN 
                        materias_primas mp ON dof.mp_id_fab = mp.id_mps
                    WHERE 
                        dof.orden_id_fab = :id_orden""")

            self.datos_orden_query.bindValue(":id_orden", id_orden)
            self.datos_orden_query.exec()

            self.model_dof = QSqlQueryModel()
            self.model_dof.setQuery(self.datos_orden_query)

        # Cabeceras
            self.model_dof.setHeaderData(0, Qt.Horizontal, str("Código"))
            self.model_dof.setHeaderData(1, Qt.Horizontal, str("Nombre"))
            self.model_dof.setHeaderData(
                2, Qt.Horizontal, str("Cantidad"))
            self.model_dof.setHeaderData(3, Qt.Horizontal, str("Lote"))
            self.model_dof.setHeaderData(4, Qt.Horizontal, str("Ubicación"))

            # Crear una vista de tabla
            self.ventana_dof.tv_dof.setModel(self.model_dof)
            self.ventana_dof.tv_dof.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_dof.tv_dof.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_dof.tv_dof.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_dof.tv_dof.resizeRowsToContents()
            self.ventana_dof.tv_dof.resizeColumnsToContents()
            self.ventana_dof.tv_dof.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            # Mostrar ventana
            # self.ventana_dof.show()

            self.hide()

        else:
            print("No hay fila seleccionada")

            ventana_falta_fila = VentanaFaltaSeleccionarFila()
            respuesta = ventana_falta_fila.exec()
            return
    def obtener_clave_principal_tipo(self):
        nombre_tipo_seleccionado = self.cb_tipo.currentText()
        clave_principal_tipo = self.diccionario_tipo_prod.get(
            nombre_tipo_seleccionado)

        print(f'Tipo seleccionado: {nombre_tipo_seleccionado}')
        print(f'Clave principal tipo: {clave_principal_tipo}')

        return clave_principal_tipo
