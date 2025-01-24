from typing import Optional
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableView
from PySide6.QtSql import QSqlTableModel, QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt, QSortFilterProxyModel, QDate
from materias_primas.view.ui_materias_primas3 import Ui_Form
from materias_primas.model.ventana_detalle_mp import VentanaDetalle
from auxiliares import VentanaEmergenteBorrar, VentanaMPExistente, VentanaFaltanDatos
from validar_datos_entrada import set_validar_letras


class VentanaMateriasPrimas(QWidget, Ui_Form):
    """ 
    Clase que representa la ventana de materias primas.
    Hereda de QMainWindow para proporcionar una ventana y de
    Ui_MainWindow para cargar la interfaz gráfica.
    """

    def __init__(self, ventana_principal):
        super().__init__()
        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()
        self.ventana_principal = ventana_principal

        # #Limitar la entrada de números en el lineEdit de nueva materia prima

        set_validar_letras(self.le_nombre_nueva)

        # Crear un model de tabla

        self.initial_query = QSqlQuery()
        self.initial_query.exec(
            # "SELECT id_mps,nombre_mps FROM materias_primas where activo_mps=true order by id_mps asc")
            """
                select
                    mp.id_mps,
                    mp.nombre_mps,
                    COALESCE(sum(ls.cantidad_lotes_stock),0)
                from
                    materias_primas mp
                left join lotes_stock ls on
                    mp.id_mps =ls.mp_id_lotes_stock
                where mp.activo_mps =true
                group by mp.id_mps,mp.nombre_mps
                order by mp.id_mps
            """
        )
        self.model = QSqlQueryModel()
        self.model.setQuery(self.initial_query)

       # Cabeceras de la tabla
        cabeceras = ['Codigo', 'Nombre', 'Cantidad / g']
        for i, cabecera in enumerate(cabeceras):
            self.model.setHeaderData(i, Qt.Horizontal, cabecera)

        # Crear un filtro para la búsqueda
        self.proxy_model_mp = QSortFilterProxyModel()
        self.proxy_model_mp.setSourceModel(self.model)

        # Crear un cuadro de texto para la búsqueda

        self.le_buscar_mp.setPlaceholderText("Buscar por nombre...")
        self.le_buscar_mp.textChanged.connect(self.filter)

        # Crear una tabla para mostrar los datos

        self.tv_mat_primas.setModel(self.proxy_model_mp)
        self.tv_mat_primas.setSelectionBehavior(QTableView.SelectRows)
        self.tv_mat_primas.setSelectionMode(QTableView.SingleSelection)

        # Crear la vista de tabla y establecer el modelo
        # self.tv_mat_primas.setModel(self.model)
        self.tv_mat_primas.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        self.tv_mat_primas.setSelectionMode(
            QAbstractItemView.SingleSelection)  # Seleccionar filas completas
        self.tv_mat_primas.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Seleccionar filas completas
        self.tv_mat_primas.selectRow(0)
        # Configurar la vista de tabla
        self.tv_mat_primas.resizeColumnsToContents()
        self.tv_mat_primas.resizeRowsToContents()
        self.tv_mat_primas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Mostrar proveedores en el comboBox
        self.diccionario_proveedores = {}

        query_proveedores = QSqlQuery()
        query_proveedores.prepare(
            "select id_proveedores ,nombre_proveedores from proveedores where activo_proveedores=true order by nombre_proveedores")

        if query_proveedores.exec():
            while query_proveedores.next():
                proveedor_id = query_proveedores.value(0)
                nombre = query_proveedores.value(1)
                self.cb_proveedor_nueva.addItem(nombre)
                self.diccionario_proveedores[nombre] = proveedor_id

        self.cb_proveedor_nueva.setCurrentIndex(-1)

        # Pestaña entradas de la ventana materias primas

        # Crear un model de tabla

        self.entradas_query = QSqlQuery()
        self.entradas_query.exec(
            """ select
                    e.id_ent ,
                    mp.nombre_mps,
                    e.nombre_lotes_ent ,
                    e.fecha_ent ,
                    e.cantidad_ent ,
                    p.nombre_proveedores
                from
                    entradas e
                inner join rel_mps_proveedores rmp on
                    e.mp_id_ent = rmp.mp_id_rmp
                    and e.proveedor_id_ent = rmp.proveedor_id_rmp
                inner join materias_primas mp on
                    rmp.mp_id_rmp = mp.id_mps
                inner join proveedores p on
                    p.id_proveedores = rmp.proveedor_id_rmp 
                order by
                    e.id_ent desc"""

        )
        self.model_ent = QSqlQueryModel()
        self.model_ent.setQuery(self.entradas_query)

       # Cabeceras de la tabla
        cabeceras = ['Codigo', 'Nombre', 'Lote',
                     'Fecha entrada', 'Cantidad / g', 'Proveedor']
        for i, cabecera in enumerate(cabeceras):
            self.model_ent.setHeaderData(i, Qt.Horizontal, cabecera)

        # Crear un filtro para la búsqueda
        self.proxy_model_mp_ent = QSortFilterProxyModel()
        self.proxy_model_mp_ent.setSourceModel(self.model_ent)

        # Crear un cuadro de texto para la búsqueda

        self.le_buscar_entrada_mp.setPlaceholderText("Buscar por nombre...")
        self.le_buscar_entrada_mp.textChanged.connect(self.filter_ent_mp)

        # Crear una tabla para mostrar los datos

        self.tv_entradas_list.setModel(self.proxy_model_mp_ent)
        self.tv_entradas_list.setSelectionBehavior(QTableView.SelectRows)
        self.tv_entradas_list.setSelectionMode(QTableView.SingleSelection)

        # Crear la vista de tabla y establecer el modelo
        # self.tv_mat_primas.setModel(self.model)
        self.tv_entradas_list.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        self.tv_entradas_list.setSelectionMode(
            QAbstractItemView.SingleSelection)  # Seleccionar filas completas
        self.tv_entradas_list.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Seleccionar filas completas
        self.tv_entradas_list.selectRow(0)
        # Configurar la vista de tabla
        self.tv_entradas_list.resizeColumnsToContents()
        self.tv_entradas_list.resizeRowsToContents()
        self.tv_entradas_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Fin nueva pestaña materias primas

        # Signal and Slots para pestaña Nueva
        self.btn_guardar_nueva_mp.clicked.connect(self.guardar_nueva_mp)
        self.btn_cancelar_nueva_mp.clicked.connect(self.cambia_pestaña)

        # Signal and Slots para pestaña Listado
        self.btn_ver_detalle_mp.clicked.connect(self.ver_detalle_producto2)
        self.btn_cerrar_listado_mp.clicked.connect(self.close)

    def filter(self):
        """Filtra la busqueda de materias primas por nombre
        """
        text = self.le_buscar_mp.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model_mp.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.proxy_model_mp.setFilterKeyColumn(1)
        self.proxy_model_mp.invalidate()  # Asegurarse de que el proxy model se actualice

    def filter_ent_mp(self):
        """Filtar la busqueda en la pestaña entradas por materias primas
        """
        text = self.le_buscar_entrada_mp.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model_mp_ent.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.proxy_model_mp_ent.setFilterKeyColumn(1)
        # Asegurarse de que el proxy model se actualice
        self.proxy_model_mp_ent.invalidate()

    def filter_ent_lote(self):
        """
        Filtrar la busqueda por lote
        """
        text = self.ventana_detalle.le_buscar_entrada.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model_lote_ent.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.proxy_model_lote_ent.setFilterKeyColumn(2)
        # Asegurarse de que el proxy model se actualice
        self.proxy_model_lote_ent.invalidate()

    def ver_detalle_producto2(self):
        """ 
        Muestra el detalle de un producto seleccionado en la tabla.
        """

        self.ventana_detalle = VentanaDetalle(self)
        selected_index = self.tv_mat_primas.selectedIndexes()
        # print(f'Selected index: {selected_index}')
        if selected_index:
            # Obtenemos el número de fila de la celda seleccionada
            fila = selected_index[0].row()
            # print(f'Fila: {fila}')

            id_pers_index = self.proxy_model_mp.mapToSource(selected_index[0])

            codigo = self.model.data(self.model.index(id_pers_index.row(), 0))

            nombre = self.model.data(self.model.index(id_pers_index.row(), 1))
            cantidad = self.ventana_detalle.obtener_cantidad_mp(codigo)

            # establecemos los campos con los valores seleccionados
            self.ventana_detalle.le_codigo_det.setText(str(codigo))
            self.ventana_detalle.le_nombre_det.setText(nombre)
            self.ventana_detalle.le_cantidad_det.setText(str(cantidad))
            # self.ventana_detalle.le_proveedor_det.setText(str(proveedor))

            self.ventana_detalle.le_codigo_entrada.setText(str(codigo))
            self.ventana_detalle.le_nombre_entrada.setText(nombre)
            self.ventana_detalle.le_f_entrada.setText(
                str(QDate.currentDate().toString('dd/MM/yyyy')))

            self.query_productos = QSqlQuery()
            self.query_productos.prepare(
                """ 
                select
                        cos.id_cosmeticos ,
                        cos.nombre_cosmeticos ,
                        cos.fecha_cad_cosmeticos ,
                        cos.tipo_id_cosmeticos ,
                        c.nombre_clientes 
                    from
                        cosmeticos cos
                    inner join clientes c on
                        cos.cliente_id_cosmeticos = c.id_clientes 
                    where
                        c.id_clientes =:codigo 
                    order by
                        cos.nombre_cosmeticos 
                    """
            )
            self.query_productos.bindValue(':codigo', codigo)
            self.query_productos.exec()

            # Se crea el modelo para mostrar los datos de las entradas del producto seleccionado
            self.model3 = QSqlQueryModel()
            self.model3.setQuery(
                f"""select
                    e.fecha_ent ,
                    mp.nombre_mps ,
                    e.nombre_lotes_ent ,
                    e.fecha_caducidad_ent ,
                    e.cantidad_ent ,
                    p.nombre_proveedores 
                from
                    materias_primas mp
                inner join entradas e on
                    mp.id_mps = e.mp_id_ent 
                inner join proveedores p on
                    p.id_proveedores = e.proveedor_id_ent 
                where
                    mp.id_mps= {codigo}"""
            )

            self.model3.setHeaderData(0, Qt.Horizontal, str("Fecha Entrada"))
            self.model3.setHeaderData(1, Qt.Horizontal, str("Materia Prima"))
            self.model3.setHeaderData(2, Qt.Horizontal, str("Lote"))
            self.model3.setHeaderData(3, Qt.Horizontal, str("Fecha Caducidad"))
            self.model3.setHeaderData(4, Qt.Horizontal, str("Cantidad / g"))
            self.model3.setHeaderData(5, Qt.Horizontal, str("Proveedor"))

            # Crear un filtro para la búsqueda
            self.proxy_model_lote_ent = QSortFilterProxyModel()
            self.proxy_model_lote_ent.setSourceModel(self.model3)

            # Crear un cuadro de texto para la búsqueda

            self.ventana_detalle.le_buscar_entrada.setPlaceholderText(
                "Buscar por lote...")
            self.ventana_detalle.le_buscar_entrada.textChanged.connect(
                self.filter_ent_lote)

            # Crear una vista de tabla
            self.ventana_detalle.tv_entradas_mp_det.setModel(
                self.proxy_model_lote_ent)
            # self.ventana_detalle.tv_entradas_mp_det.setEditTriggers(
            #     QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            # self.ventana_detalle.tv_entradas_mp_det.setSelectionMode(
            #     QAbstractItemView.SingleSelection)  # Seleccionar un único elemento
            # self.ventana_detalle.tv_entradas_mp_det.setSelectionBehavior(
            #     QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_entradas_mp_det.resizeRowsToContents()
            self.ventana_detalle.tv_entradas_mp_det.resizeColumnsToContents()
            self.ventana_detalle.tv_entradas_mp_det.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            # Se crea el modelo para mostrar los proveedores de la materia prima
            self.model4 = QSqlQueryModel()
            self.model4.setQuery(
                f"""
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
                        mp.id_mps = {codigo}
                """
            )

            self.model4.setHeaderData(0, Qt.Horizontal, str("Código"))
            self.model4.setHeaderData(1, Qt.Horizontal, str("Nombre"))

            # Crear una vista de tabla
            self.ventana_detalle.tv_provs_detalle_mp.setModel(self.model4)
            self.ventana_detalle.tv_provs_detalle_mp.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_provs_detalle_mp.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_provs_detalle_mp.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_provs_detalle_mp.resizeRowsToContents()
            self.ventana_detalle.tv_entradas_mp_det.resizeColumnsToContents()
            self.ventana_detalle.tv_provs_detalle_mp.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            # Modelo para listar los lotes de materia prima seleccionada

            self.model5 = QSqlQueryModel()
            self.model5.setQuery(
                f""" 
                select
                    mp.id_mps ,
                    mp.nombre_mps,
                    ls.nombre_lotes_stock ,
                    sum(ls.cantidad_lotes_stock)
                from
                    materias_primas mp
                inner join lotes_stock ls on
                    mp.id_mps = ls.mp_id_lotes_stock
                where
                    mp.id_mps = {codigo}
                group by
                    mp.id_mps , mp.nombre_mps,ls.nombre_lotes_stock 
                """)

            self.model5.setHeaderData(0, Qt.Horizontal, str("Código"))
            self.model5.setHeaderData(1, Qt.Horizontal, str("Nombre"))
            self.model5.setHeaderData(2, Qt.Horizontal, str("Lote"))
            self.model5.setHeaderData(3, Qt.Horizontal, str("Cantidad / g"))

            # Crear una vista de tabla
            self.ventana_detalle.tv_lotes_det.setModel(self.model5)
            self.ventana_detalle.tv_lotes_det.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_lotes_det.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_lotes_det.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_lotes_det.resizeRowsToContents()
            self.ventana_detalle.tv_lotes_det.resizeColumnsToContents()
            self.ventana_detalle.tv_lotes_det.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            self.ventana_detalle.show()

            self.hide()

    def obtener_clave_principal_proveedor(self):
        """ Obtiene la clave principal del proveedor seleccionado en el combobox

        Returns:
            int: La clave principal del proveedor
        """

        nombre_seleccionado = self.cb_proveedor_nueva.currentText()
        clave_principal = self.diccionario_proveedores.get(
            nombre_seleccionado)

        return clave_principal

    def cambia_pestaña(self):
        """
        Resetea los datos de la materia prima y el combobox y marca la fila 0 de la tabla.
        """
        self.le_nombre_nueva.setText("")
        self.cb_proveedor_nueva.setCurrentIndex(-1)
        self.tabWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        """
        Maneja el evento del cierre de la ventana.
        Cuando se cierra la ventana secundaria, se muestra la ventana padre
        Args:
            event (QCloseEvent): 
        """
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_principal.show()
        event.accept()

    def mp_existe(self, nombre):
        """ Indica la existencia de una materia prima

        Args:
            nombre (str): Recibe un nombre tipo string

        Returns:
            boolean: Devuelve True si la materia prima existe y False si no existe
        """
        query = QSqlQuery()
        query.prepare(
            "SELECT COUNT(*) FROM materias_primas WHERE nombre_mps = :nombre")
        query.bindValue(":nombre", nombre)

        if not query.exec():
            print("Error al ejecutar la consulta:", query.lastError().text())
            return False

        if query.next():
            count = query.value(0)
            return count > 0
        else:
            print("Error: No se obtuvieron resultados de la consulta.")
            return False

    def guardar_nueva_mp(self):
        """
        Guarda una nueva materia prima en la base de datos.
        """

        try:
            nombre = self.le_nombre_nueva.text()
            nombre_formateado = nombre[0].upper()+nombre[1:].lower()
            # Recuperar datos de los lineEdit y comboBox
            if nombre_formateado.strip() == "":
                raise Exception
                print("Algo mal está pasando")
            proveedor = int(self.obtener_clave_principal_proveedor())
        except:
            ventana_faltan_datos = VentanaFaltanDatos()
            ventana_faltan_datos.exec()
            return

        if self.mp_existe(nombre):

            print('Ya existe la materia prima')
            # Pop up indicando que ya existe la materia prima
            ventana_mp_existente = VentanaMPExistente()
            respuesta = ventana_mp_existente.exec()
            # self.cambia_pestaña()

            return

        if nombre_formateado.strip() != "":

            # Crear y preparacion de la sentencia sql para insertar materia prima
            query = QSqlQuery()
            query.prepare(
                f'insert into materias_primas (nombre_mps) values (:nombre)')

            query.bindValue(":nombre", nombre_formateado)
            query.exec()
            # Crear y preparacion de la sentencia sql para insertar materia prima en rel_mps_proveedores automaticamente
            query_ultimo_id_mps = QSqlQuery()
            query_ultimo_id_mps.prepare(
                """
                select max(id_mps) from materias_primas
                """
            )
    # Crear la consulta

            if query_ultimo_id_mps.exec_():
                # Avanzar al primer resultado
                if query_ultimo_id_mps.next():
                    # Obtener el valor de la primera columna (que es el resultado de MAX(id_mps))
                    ultimo_id_mps = query_ultimo_id_mps.value(0)
                    print("El último id_mps es:", ultimo_id_mps)
                else:
                    print("No se encontraron resultados.")
            else:
                print("Error al ejecutar la consulta:",
                      query_ultimo_id_mps.lastError().text())

            # Crear y preparacion de la sentencia sql para insertar en matprimas_proveedores
            query_insertar_rel_mps_pro = QSqlQuery()
            query_insertar_rel_mps_pro.prepare(
                f'insert into rel_mps_proveedores (mp_id_rmp,proveedor_id_rmp) values (:ultimo_id_mps,:proveedor) ')

            query_insertar_rel_mps_pro.bindValue(
                ":ultimo_id_mps", ultimo_id_mps)
            query_insertar_rel_mps_pro.bindValue(":proveedor", proveedor)

            query_insertar_rel_mps_pro.exec()

            self.tabWidget.setCurrentIndex(0)

            self.initial_query.exec(
                """
                    select
                        mp.id_mps,
                        mp.nombre_mps,
                        COALESCE(sum(ls.cantidad_lotes_stock),0)
                    from
                        materias_primas mp
                    left join lotes_stock ls on
                        mp.id_mps =ls.mp_id_lotes_stock
                    where mp.activo_mps =true
                    group by mp.id_mps,mp.nombre_mps
                    order by mp.id_mps
                """
            )
            self.model.setQuery(self.initial_query)
            self.tv_mat_primas.selectRow(0)

            self.le_nombre_nueva.setText('')
            self.cb_proveedor_nueva.setCurrentIndex(-1)
