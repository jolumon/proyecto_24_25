from PySide6.QtSql import QSqlQuery, QSqlTableModel, QSqlQueryModel
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QMessageBox
from materias_primas.view.ui_materias_primas_detalle3 import Ui_Form
from PySide6.QtCore import Qt
from auxiliares import VentanaEmergenteBorrar, VentanaFaltanDatos


class VentanaDetalle(QWidget, Ui_Form):
    def __init__(self, ventana_mp):
        super().__init__()
        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()

        self.ventana_mp = ventana_mp

        # Mostrar proveedores en el comboBox de la pestaña entrada
        self.diccionario_proveedores_entrada = {}

        selected_index = self.ventana_mp.tv_mat_primas.currentIndex()
        print(f'Selected index: {selected_index}')
        if selected_index.isValid():
            # Obtenemos el número de fila de la celda seleccionada
            # print('Entra en el if del selected_index')
            fila = selected_index.row()
            print(f'Fila: {fila}')

            codigo = self.ventana_mp.model.index(fila, 0).data()

        query_proveedores_entrada = QSqlQuery()
        query_proveedores_entrada.prepare(
            # f'select p.id_prov ,p.nombre_prov  from materias_primas mp inner join matprimas_proveedores mp2 on mp.id_mp =mp2.id_mp_mpprov inner join proveedores p on mp2.id_prov_mpprov = p.id_prov  where mp.id_mp={codigo}')
            """
            select
                p.id_proveedores ,
                p.nombre_proveedores 
            from
                materias_primas mp
            inner join rel_mps_proveedores rmp on
                mp.id_mps = rmp.mp_id_rmp 
            inner join proveedores p on
                rmp.proveedor_id_rmp = p.id_proveedores 
            where
                mp.id_mps = :codigo
            
            """

        )
        query_proveedores_entrada.bindValue(':codigo', codigo)

        if query_proveedores_entrada.exec():
            while query_proveedores_entrada.next():
                proveedor_id = query_proveedores_entrada.value(0)
                nombre = query_proveedores_entrada.value(1)
                self.cb_proveedor_entrada.addItem(nombre)
                self.diccionario_proveedores_entrada[nombre] = proveedor_id

        self.cb_proveedor_entrada.setCurrentIndex(-1)

        # Signals and Slots pestaña detalle

        self.btn_cerrar_det.clicked.connect(self.close)
        self.btn_borrar_det.clicked.connect(self.borrar_mp)
        self.btn_actualizar_det.clicked.connect(self.actualizar_det)

        # Signals and Slots pestaña entrada

        self.btn_cerrar_entrada.clicked.connect(self.cierra_pest_entrada)
        self.btn_guardar_entrada.clicked.connect(self.guardar_entrada)

    def cierra_pest_entrada(self):
        print(f'Dentro de cierra_pestaña_entrada')
        self.tabWidget.setCurrentIndex(0)

    def obtener_clave_principal(self):
        nombre_seleccionado = self.cb_proveedor_entrada.currentText()
        clave_principal = self.diccionario_proveedores_entrada.get(
            nombre_seleccionado)

        return clave_principal

    def guardar_entrada(self):
        """ Guarda el registro de una nueva entrada en la base de datos """

        if self.le_codigo_entrada.text() == "" or self.obtener_clave_principal() == "" or self.de_f_caducidad.text() == "" or self.le_cantidad_entrada.text() == "":
            ventana_faltan_datos = VentanaFaltanDatos()
            respuesta = ventana_faltan_datos.exec()
            return

        id_materia_prima = int(self.le_codigo_entrada.text())
        print(f"id_materia_prima:{id_materia_prima}")
        print(f"tipo_id_mp: {type(id_materia_prima)}")

        # Hay que hacer un comboBox para que se pueda elegir el proveedor. Antes al ser solo un proveedor venia impuesto y no hacia falta seleccionarlo porque se ponia por defecto .

        id_proveedor = int(self.obtener_clave_principal())
        print(f'id_proveedor: {id_proveedor}')
        print(f"tipo_id_prov: {type(id_proveedor)}")
        fecha_entrada = str(self.le_f_entrada.text())
        fecha_entrada_fin=f"'{fecha_entrada}'"
        print(f"fecha_entrada:{fecha_entrada_fin}")
        print(f"tipo_fecha_entrada:{type(fecha_entrada_fin)}")
        fecha_caducidad = str(self.de_f_caducidad.text())
        fecha_caducidad_fin = f"'{fecha_caducidad}'"
        print(f"fecha_caducidad:{fecha_caducidad_fin}")
        print(f"tipo_fecha_caducidad:{type(fecha_caducidad_fin)}")
        # lote = self.le_lote_entrada.text() # Se gener
        if self.le_cantidad_entrada.text() == "":
            self.le_cantidad_entrada.setText('0')
            # Lanzar ventana error: faltan datos
        cantidad = float(self.le_cantidad_entrada.text())
        print(f"cantidad: {cantidad}")
        print(f"tipo_cantidad: {type(cantidad)}")
        # precio = self.le_precio_entrada.text()

        query_insertar_nueva_entrada = QSqlQuery()
        query_insertar_nueva_entrada.prepare(
            #
            """insert into entradas (
                mp_id_ent,
                proveedor_id_ent,
                fecha_ent,   
                fecha_caducidad_ent,        
                cantidad_ent
                )
            values (
                
                :id_materia_prima,
                :id_proveedor,
                :fecha_entrada,
                :fecha_caducidad,
                :cantidad)
        """)
        query_insertar_nueva_entrada.bindValue(
            ':id_materia_prima', id_materia_prima)
        query_insertar_nueva_entrada.bindValue(
            ':id_proveedor', id_proveedor)
        query_insertar_nueva_entrada.bindValue(
            ':fecha_entrada', fecha_entrada_fin)
        query_insertar_nueva_entrada.bindValue(
            ':fecha_caducidad', fecha_caducidad_fin)
        # query_insertar_nueva_entrada.bindValue(':lote', lote)
        query_insertar_nueva_entrada.bindValue(':cantidad', cantidad)
        # query_insertar_nueva_entrada.bindValue(':precio', precio)

        query_insertar_nueva_entrada.exec()
        print('Guardado')

        # Si muestro la pestaña 1 para que se vean lso datos de la entrada introducida,
        # no sé cómo actualizar la vista de la tableView
        # self.tabWidget.setCurrentIndex(0)
        self.close()

    def borrar_mp(self):

        ventana_confirmacion = VentanaEmergenteBorrar()
        respuesta = ventana_confirmacion.exec()

        if respuesta:

            codigo = int(self.le_codigo_det.text())
            # print(type(codigo))

            query_busqueda = QSqlQuery()
            # query_busqueda.prepare(
            #     "select * from matprimas_proveedores where id_mp_mpprov=:codigo")
            query_busqueda.prepare(
                "select * from rel_mps_proveedores where mp_id_rmp=:codigo")
            query_busqueda.bindValue(":codigo", codigo)
            query_busqueda.exec()

            if query_busqueda:
                query_actualizar = QSqlQuery()
                query_actualizar.prepare(
                    "update materias_primas set activo_mps=false where id_mps=:codigo")
                query_actualizar.bindValue(":codigo", codigo)
                query_actualizar.exec()
            # else:
            #     query = QSqlQuery()
            #     query.prepare(
            #         "DELETE FROM materias_primas WHERE id_mps=:codigo")
            #     # query.bindValue(":nombre", nombre)
            #     query.bindValue(":codigo", codigo)
            #     query.exec()

            self.ventana_mp.initial_query.exec(
                "SELECT id_mps,nombre_mps FROM materias_primas where activo_mps=true order by id_mps asc")
            self.ventana_mp.model.setQuery(self.ventana_mp.initial_query)
            self.ventana_mp.tv_mat_primas.selectRow(0)
            self.close()

            # self.ventana_mp.model.select()

            # self.close()
        # self.tabWidget.setCurrentIndex(0)
        # self.tableView.selectRow(0)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_mp.show()
        event.accept()

    def actualizar_det(self):
        codigo = int(
            self.le_codigo_det.text())  # Lo paso a entero para que coincida con el tipo de datos de la bd
        # codigo = self.model.index(fila, 0).data()->Aquí no conozco fila, tendría que hacerla global
        nombre = self.le_nombre_det.text()
        # cantidad = self.le_cantidad_det.text()
        # proveedor = int(self.le_proveedor_det.text())

        # print(type(codigo))
        # print(f'{codigo},{nombre},{cantidad}')

        query = QSqlQuery()

        query.prepare(
            f'UPDATE materias_primas SET nombre_mps=:nombre WHERE id_mps=:codigo')
        # query.prepare(
        #     f'UPDATE materias_primas SET nombre_mp=:nombre,cantidad_mp=:cantidad, proveedor_mp=:proveedor WHERE id_mp=:codigo')

        query.bindValue(":codigo", codigo)
        query.bindValue(":nombre", nombre)
        # query.bindValue(":cantidad", cantidad)
        # query.bindValue(":proveedor", proveedor)

        query.exec()

        self.ventana_mp.initial_query.exec(
            "SELECT id_mps,nombre_mps FROM materias_primas where activo_mps=true order by id_mps  asc")
        self.ventana_mp.model.setQuery(self.ventana_mp.initial_query)
        self.ventana_mp.tv_mat_primas.selectRow(0)
        self.close()
    
    def obtener_cantidad_mp(self,codigo_mp):
        
        query_cantidad_mp=QSqlQuery()
        query_cantidad_mp.prepare(
        """
            select
	            sum(ls.cantidad_lotes_stock)
            from
                lotes_stock ls
            where
                ls.mp_id_lotes_stock = :codigo 
        
        """
            
            
        )
        query_cantidad_mp.bindValue(":codigo", codigo_mp)
        
        if query_cantidad_mp.exec():
            while query_cantidad_mp.next():
                cantidad_mp=query_cantidad_mp.value(0)
                print(f"Cantidad_funcion:{cantidad_mp}")
                return cantidad_mp
