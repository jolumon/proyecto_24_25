from productos.view.ui_ventana_productos import Ui_Form
from productos.model.ventana_detalle_prod import VentanaDetalle
from PySide6.QtCore import Qt, QSortFilterProxyModel, QDate
from PySide6.QtSql import QSqlTableModel, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlRelation
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableView
from auxiliares import VentanaFaltanDatos, VentanaValueError


class VentanaProducto(QWidget, Ui_Form):
    def __init__(self, ventana_principal):
        super().__init__()

        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()
        self.ventana_principal = ventana_principal

        # Crear un modelo de tabla

        self.initial_query = QSqlQuery()
        self.initial_query.exec(
            
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
        self.model = QSqlQueryModel()
        self.model.setQuery(self.initial_query)

       # Cabeceras
        self.model.setHeaderData(0, Qt.Horizontal, str("Código"))
        self.model.setHeaderData(1, Qt.Horizontal, str("Nombre"))
        self.model.setHeaderData(
            2, Qt.Horizontal, str("Fecha caducidad / meses"))
        self.model.setHeaderData(
            3, Qt.Horizontal, str("Tipo"))
        self.model.setHeaderData(4, Qt.Horizontal, str("Cliente"))

        # Crear un filtro para la búsqueda
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        # Crear un cuadro de texto para la búsqueda

        self.le_buscar_prod.setPlaceholderText("Buscar por nombre...")
        self.le_buscar_prod.textChanged.connect(self.filter)

        # Crear una tabla para mostrar los datos
        self.tv_productos.setModel(self.proxy_model)

        self.tv_productos.setSelectionBehavior(QTableView.SelectRows)
        self.tv_productos.setSelectionMode(QTableView.SingleSelection)

        self.tv_productos.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        # Seleccionar filas completas
        self.tv_productos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_productos.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Seleccionar filas completas

        # Configurar la vista de tabla
        self.tv_productos.resizeRowsToContents()
        self.tv_productos.resizeColumnsToContents()
        # Amplia el tamaño de la tabla a toda la pantalla
        self.tv_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tv_productos.selectRow(0)
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
                self.cb_tipo_prod.addItem(nombre_tipo)
                self.diccionario_tipo_prod[nombre_tipo] = tipo_id

        self.cb_tipo_prod.setCurrentIndex(-1)

    # Mostrar clientes en el comboBox
        self.diccionario_clientes = {}

        query_clientes = QSqlQuery()
        query_clientes.prepare(
            f'select id_clientes, nombre_clientes from clientes where activo_clientes=true order by id_clientes')

        if query_clientes.exec():
            while query_clientes.next():
                cliente_id = query_clientes.value(0)
                nombre = query_clientes.value(1)
                self.cb_cliente_prod.addItem(nombre)
                self.diccionario_clientes[nombre] = cliente_id

        self.cb_cliente_prod.setCurrentIndex(-1)

        # Signal and Slots pestaña listado productos
        self.btn_cerrar_listado.clicked.connect(self.close)
        self.btn_ver_prod_listado.clicked.connect(self.ver_detalle_producto)

        # Signals and slots pestaña nuevo

        self.btn_cancelar_nuevo.clicked.connect(self.cambia_pestaña)
        self.btn_guardar_nuevo.clicked.connect(self.guardar_nuevo)

    def cambia_pestaña(self):
        self.tabWidget.setCurrentIndex(1)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_principal.show()
        event.accept()

    def filter(self):
        text = self.le_buscar_prod.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.invalidate()  # Asegurarse de que el proxy model se actualice

    def ver_detalle_producto(self):
        # Se crea la ventana de detalle del producto
        self.ventana_detalle = VentanaDetalle(self)
        selected_index = self.tv_productos.selectedIndexes()

        # print(f'Selected index: {selected_index}')
        if selected_index:

            row = selected_index[0].row()
            id_pers_index = self.proxy_model.mapToSource(selected_index[0])

            codigo = self.model.data(self.model.index(id_pers_index.row(), 0))
            nombre = self.model.data(self.model.index(id_pers_index.row(), 1))
            fecha_cad = self.model.data(
                self.model.index(id_pers_index.row(), 2))
            tipo = self.model.data(
                self.model.index(id_pers_index.row(), 3))
            print(f"Tipo:{tipo}")
            cliente = self.model.data(
                self.model.index(id_pers_index.row(), 4))

            # Este cliente es correcto
            # print(f'Cliente antes proxy-model:{cliente}')

            # establecemos los campos con los valores seleccionados
            self.ventana_detalle.le_codigo_det.setText(str(codigo))
            self.ventana_detalle.le_nombre_det.setText(nombre)
            self.ventana_detalle.le_caducidad_det.setText(str(fecha_cad))
            self.ventana_detalle.cb_tipo.setCurrentText(tipo)
            self.ventana_detalle.cb_cliente.setCurrentText(cliente)

            self.query_composicion = QSqlQuery()
            self.query_composicion.prepare(
                "select mp.nombre_mps , rcm.porcentaje_rcm from materias_primas mp inner join rel_cosm_mp rcm on mp.id_mps = rcm.mp_id_rcm  inner join cosmeticos cos on rcm.cosm_id_rcm = cos.id_cosmeticos where rcm.cosm_id_rcm = :codigo order by rcm.porcentaje_rcm desc")

            self.query_composicion.bindValue(':codigo', codigo)
            self.query_composicion.exec()

            # self.model2 = QSqlRelationalTableModel()

            self.model2 = QSqlQueryModel()
            self.model2.setQuery(self.query_composicion)

            self.model2.setHeaderData(0, Qt.Horizontal, str("Materia Prima"))
            self.model2.setHeaderData(1, Qt.Horizontal, str("Porcentaje"))
            # self.model2.setHeaderData(2, Qt.Horizontal, str("Linea"))

            # Crear una vista de tabla
            self.ventana_detalle.tv_composicion_prod.setModel(self.model2)
            self.ventana_detalle.tv_composicion_prod.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_composicion_prod.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_composicion_prod.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_composicion_prod.resizeRowsToContents()
            self.ventana_detalle.tv_composicion_prod.resizeColumnsToContents()
            self.ventana_detalle.tv_composicion_prod.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

        # Ver las fabricaciones del producto en la pestaña Nueva Fabricación

            # self.ventana_detalle.le_codigo_fab.setText(str(codigo))
            self.ventana_detalle.le_producto_fab.setText(nombre)
            fecha_entrada = QDate.currentDate()
            self.ventana_detalle.de_fecha_fab.setDate(
                fecha_entrada)

            self.query_fabricaciones = QSqlQuery()
            # self.query_fabricaciones.prepare(
            #     "select f.fecha_fab ,f.lote_fab ,f.cantidad_fab  ,f.fecha_cad_fab,e.nombre_eq  from productos p inner join fabricaciones f on p.id_prod = f.id_prod_fab inner join equipos e on f.equipo_fab = e.id_eq where p.id_prod = :codigo order by f.fecha_fab desc")
            self.query_fabricaciones.prepare(
                """select
                    o.id_ordenes,o.fecha_fab_ordenes  , o.cantidad_ordenes ,o.lote_ordenes,o.fecha_cad_ordenes, e.nombre_equipos
                from
                    ordenes o
                inner join cosmeticos c on
                    o.cosmetico_id_ordenes = c.id_cosmeticos
                inner join equipos e on o.equipo_id_ordenes = e.id_equipos 
                where c.id_cosmeticos=:codigo""")
            self.query_fabricaciones.bindValue(':codigo', codigo)
            self.query_fabricaciones.exec()
#                select f.fecha_fab ,f.lote_fab ,f.cantidad_fab  ,f.fecha_cad_fab,e.nombre_eq  from productos p inner join fabricaciones f on p.id_prod = f.id_prod_fab inner join equipos e on f.equipo_fab = e.id_eq where p.id_prod = 1 order by f.fecha_fab desc
            # self.model2 = QSqlRelationalTableModel()

            self.model_fab = QSqlQueryModel()
            self.model_fab.setQuery(self.query_fabricaciones)
            self.model_fab.setHeaderData(0, Qt.Horizontal, str("Código"))

            self.model_fab.setHeaderData(
                1, Qt.Horizontal, str("Fecha fabricación"))
            # self.model_fab.setHeaderData(2, Qt.Horizontal, str("Cosmético"))
            self.model_fab.setHeaderData(2, Qt.Horizontal, str("Cantidad"))
            self.model_fab.setHeaderData(3, Qt.Horizontal, str("Lote"))
            self.model_fab.setHeaderData(4, Qt.Horizontal, str("Caducidad"))
            self.model_fab.setHeaderData(5, Qt.Horizontal, str("Equipo"))

            # Crear un filtro para la búsqueda
            self.proxy_model_fab = QSortFilterProxyModel()
            self.proxy_model_fab.setSourceModel(self.model_fab)

            # Crear un cuadro de texto para la búsqueda

            self.ventana_detalle.le_buscar_fabricacion.setPlaceholderText(
                "Buscar por lote fabricación...")
            self.ventana_detalle.le_buscar_fabricacion.textChanged.connect(
                self.ventana_detalle.filter_fabricaciones)
# Crear una vista de tabla
            self.ventana_detalle.tv_fab_historico.setModel(
                self.proxy_model_fab)

            self.ventana_detalle.tv_fab_historico.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_fab_historico.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_fab_historico.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_fab_historico.resizeRowsToContents()
            self.ventana_detalle.tv_fab_historico.resizeColumnsToContents()
            self.ventana_detalle.tv_fab_historico.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            self.ventana_detalle.show()

            self.hide()

    def obtener_clave_principal(self):
        nombre_seleccionado = self.cb_cliente_prod.currentText()
        clave_principal = self.diccionario_clientes.get(nombre_seleccionado)

        print(f'Nombre seleccionado: {nombre_seleccionado}')
        print(f'Clave principal: {clave_principal}')

        return clave_principal

    def obtener_clave_principal_tipo(self):
        nombre_tipo_seleccionado = self.cb_tipo_prod.currentText()
        clave_principal_tipo = self.diccionario_tipo_prod.get(
            nombre_tipo_seleccionado)

        print(f'Tipo seleccionado: {nombre_tipo_seleccionado}')
        print(f'Clave principal tipo: {clave_principal_tipo}')

        return clave_principal_tipo

    def guardar_nuevo(self):
        # Recuperar datos de los lineEdit
        try:
            nombre = self.le_nombre_prod.text()
            if nombre == "":
                raise Exception
            fecha_cad = int(self.le_caducidad_prod.text())
            tipo = int(self.obtener_clave_principal_tipo())
            cliente_id = int(self.obtener_clave_principal())
        except ValueError as eV:
            print(f"Exception:{eV}")
            ventana_error = VentanaValueError()
            ventana_error.exec()
            return
        except Exception as e:
            print(f"Exception:{e}")
            ventana_faltan_datos = VentanaFaltanDatos()
            ventana_faltan_datos.exec()
            return

        # Crear y preparacion de la sentencia sql
        query = QSqlQuery()
        query.prepare(
            f'insert into cosmeticos (nombre_cosmeticos,fecha_cad_cosmeticos,tipo_id_cosmeticos,cliente_id_cosmeticos) values (:nombre, :caducidad,:tipo,:cliente_id)')

        query.bindValue(":nombre", nombre)
        query.bindValue(":caducidad", fecha_cad)
        query.bindValue(":tipo", tipo)
        query.bindValue(":cliente_id", cliente_id)

        query.exec()

        # Limpiar datos introducidos
        self.le_nombre_prod.setText("")
        self.le_caducidad_prod.setText("")
        self.cb_tipo_prod.setCurrentIndex(-1)
        self.cb_cliente_prod.setCurrentIndex(-1)
        # Cambiar a la pestaña de listado productos
        self.tabWidget.setCurrentIndex(1)

        self.initial_query.exec(
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
        self.model.setQuery(self.initial_query)
