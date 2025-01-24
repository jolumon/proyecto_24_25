import sys
from PySide6.QtSql import QSqlTableModel, QSqlQuery, QSqlQueryModel
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableView, QApplication
from proveedores.view.ui_ventana_proveedores2 import Ui_Form
from proveedores.model.ventana_detalle import VentanaDetalle
from PySide6.QtCore import Qt, QSortFilterProxyModel
from auxiliares import VentanaEmergenteVacio
from validar_datos_entrada import set_validar_cantidad, set_validar_telefono, set_validar_numeros


class VentanaProveedor(QWidget, Ui_Form):
    """
        Clase que representa la ventana de proveedores.
    Hereda de QMainWindow para proporcionar una ventana y de
    Ui_MainWindow para cargar la interfaz gráfica.

     Args:
        QWidget (QWidget): Clase base para todas las ventanas de la aplicación
        Ui_Form (Ui_Form): Clase generada que define la interfaz gráfica de la ventana.
    """

    def __init__(self, ventana_principal):
        super().__init__()
        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()
        self.ventana_principal = ventana_principal

        set_validar_telefono(self.le_telefono)
        set_validar_telefono(self.le_movil)
        set_validar_numeros(self.le_codigo_postal)

        # Crear un model de tabla

        self.initial_query = QSqlQuery()
        self.initial_query.exec(
            "select * from proveedores where activo_proveedores=true order by id_proveedores")
        self.model = QSqlQueryModel()
        self.model.setQuery(self.initial_query)

        self.model.setHeaderData(0, Qt.Horizontal, str("Código"))
        self.model.setHeaderData(1, Qt.Horizontal, str("Nombre"))
        self.model.setHeaderData(2, Qt.Horizontal, str("Dirección"))
        self.model.setHeaderData(3, Qt.Horizontal, str("Código postal"))
        self.model.setHeaderData(4, Qt.Horizontal, str("Población"))
        self.model.setHeaderData(5, Qt.Horizontal, str("Provincia"))
        self.model.setHeaderData(6, Qt.Horizontal, str("Teléfono"))
        self.model.setHeaderData(7, Qt.Horizontal, str("Contacto"))
        self.model.setHeaderData(8, Qt.Horizontal, str("Móvil"))
        self.model.setHeaderData(9, Qt.Horizontal, str("Email"))
        self.model.setHeaderData(10, Qt.Horizontal, str("Activo"))

        # Crear un filtro para la búsqueda
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        # Crear un cuadro de texto para la búsqueda

        self.le_buscar.setPlaceholderText("Buscar por nombre...")
        self.le_buscar.textChanged.connect(self.filter)

        # Crear una tabla para mostrar los datos

        self.tv_proveedores.setModel(self.proxy_model)
        self.tv_proveedores.setSelectionBehavior(QTableView.SelectRows)
        self.tv_proveedores.setSelectionMode(QTableView.SingleSelection)
        self.tv_proveedores.setColumnHidden(10, True)

        self.tv_proveedores.show()

        # Crear la vista de tabla y establecer el modelo
        # self.tv_proveedores.setModel(self.model)
        self.tv_proveedores.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        # Seleccionar filas completas
        self.tv_proveedores.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_proveedores.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Seleccionar filas completas

        # Configurar la vista de tabla
        self.tv_proveedores.resizeRowsToContents()
        self.tv_proveedores.resizeColumnsToContents()
        # Amplia el tamaño de la tabla a toda la pantalla
        self.tv_proveedores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_proveedores.selectRow(0)

        # Señales pestaña listado proveedores
        self.btn_cerrar_listado_proveedores.clicked.connect(self.close)
        self.btn_ver_listado_proveedor.clicked.connect(
            self.ver_detalle_proveedor2)

        # Señales pestana nuevo proveedor

        self.btn_guardar_nuevo_proveedor.clicked.connect(self.guardar_nuevo)
        self.btn_cancelar_nuevo_proveedor.clicked.connect(self.cambia_pestaña)

    def cambia_pestaña(self):
        """
        Cambiar de pestaña a la pestaña de listado de proveedores
        """
        self.tabWidget.setCurrentIndex(1)

    def closeEvent(self, event):
        """
        Maneja el evento del cierre de la ventana.
        Cuando se cierra la ventana proveedores, se muestra la ventana principal
        Args:
            event (QCloseEvent): El evento de cierre que contiene información sobre el 
            cierre de la ventana.

        """

        self.ventana_principal.show()
        event.accept()

    def filter(self):
        """
        Filtrar la tabla de proveedores según el texto ingresado en el campo de búsqueda
        """
        text = self.le_buscar.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model.setFilterFixedString(text)
        # Filtrar por la columna proveedor
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.invalidate()  # Asegurarse de que el proxy model se actualice

    def guardar_nuevo(self):
        """
        Guardar un nuevo proveedor en la base de datos
        """
        # Recuperar datos de los lineEdit
        nombre = self.le_nombre.text()

        if len(nombre) > 0:
            direccion = self.le_direccion.text()
            codigo_postal = self.le_codigo_postal.text()
            poblacion = self.le_poblacion.text()
            provincia = self.le_poblacion.text()
            telefono = self.le_telefono.text()
            contacto = self.le_contacto.text()
            movil = self.le_movil.text()
            email = self.le_email.text()

            # Crear y preparacion de la sentencia sql
            query = QSqlQuery()
            query.prepare(
                f'insert into proveedores (nombre_proveedores,direccion_proveedores,cp_proveedores,poblacion_proveedores,provincia_proveedores,telefono_proveedores,contacto_proveedores, movil_proveedores, email_proveedores) values (:nombre, :direccion, :codigo_postal, :poblacion, :provincia, :telefono, :contacto, :movil,:email)')

            query.bindValue(":nombre", nombre)
            query.bindValue(":direccion", direccion)
            query.bindValue(":codigo_postal", codigo_postal)
            query.bindValue(":poblacion", poblacion)
            query.bindValue(":provincia", provincia)
            query.bindValue(":telefono", telefono)
            query.bindValue(":contacto", contacto)
            query.bindValue(":movil", movil)
            query.bindValue(":email", email)

            query.exec()

            # Borrar datos introducidos
            self.le_nombre.setText("")
            self.le_direccion.setText("")
            self.le_codigo_postal.setText("")
            self.le_poblacion.setText("")
            self.le_provincia.setText("")
            self.le_telefono.setText("")
            self.le_email.setText("")
            self.lbl_contacto.setText("")

            # self.close()

            self.tabWidget.setCurrentIndex(1)

            self.initial_query.exec(
                "select * from proveedores where activo_proveedores=true order by id_proveedores")
            self.model.setQuery(self.initial_query)

            self.tv_proveedores.selectRow(0)

        else:
            ventana_confirmacion = VentanaEmergenteVacio()
            respuesta = ventana_confirmacion.exec()

    def ver_detalle_proveedor2(self):
        """"
        Funcion para ver el detalle de un proveedor
        """

        # Se crea la ventana de detalle del cliente
        self.ventana_detalle = VentanaDetalle(self)
        selected_index = self.tv_proveedores.selectedIndexes()
        print(f'Selected index: {selected_index}')
        if selected_index:
            # Obtenemos el número de fila de la celda seleccionada
            # print('Entra en el if del selected_index')
            row = selected_index[0].row()
            id_pers_index = self.proxy_model.mapToSource(selected_index[0])

            codigo = self.model.data(self.model.index(id_pers_index.row(), 0))
            nombre = self.model.data(self.model.index(id_pers_index.row(), 1))
            direccion = self.model.data(
                self.model.index(id_pers_index.row(), 2))
            codigo_postal = self.model.data(
                self.model.index(id_pers_index.row(), 3))
            poblacion = self.model.data(
                self.model.index(id_pers_index.row(), 4))
            provincia = self.model.data(
                self.model.index(id_pers_index.row(), 5))
            telefono = self.model.data(
                self.model.index(id_pers_index.row(), 6))
            contacto = self.model.data(
                self.model.index(id_pers_index.row(), 7))
            contacto = self.model.data(
                self.model.index(id_pers_index.row(), 7))
            movil = self.model.data(self.model.index(id_pers_index.row(), 8))
            email = self.model.data(self.model.index(id_pers_index.row(), 9))

            # establecemos los campos con los valores seleccionados
            self.ventana_detalle.le_codigo.setText(str(codigo))
            self.ventana_detalle.le_nombre.setText(nombre)
            self.ventana_detalle.le_direccion.setText(direccion)
            self.ventana_detalle.le_codigo_postal.setText(codigo_postal)
            self.ventana_detalle.le_poblacion.setText(poblacion)
            self.ventana_detalle.le_provincia.setText(provincia)
            self.ventana_detalle.le_telefono.setText(telefono)
            self.ventana_detalle.le_contacto.setText(contacto)
            self.ventana_detalle.le_movil.setText(movil)
            self.ventana_detalle.le_email.setText(email)

            self.query_materias_primas = QSqlQuery()
            self.query_materias_primas.prepare("""
                SELECT
                    mp.id_mps,
                    mp.nombre_mps,
                    COALESCE(SUM(ls.cantidad_lotes_stock), 0) AS total_cantidad,
                    CASE 
                        WHEN mp.activo_mps THEN 'Verdadero' 
                        ELSE 'Falso' 
                    END AS estado_activo
                FROM
                    lotes_stock ls
                RIGHT JOIN materias_primas mp ON
                    ls.mp_id_lotes_stock = mp.id_mps
                INNER JOIN rel_mps_proveedores rmp ON
                    mp.id_mps = rmp.mp_id_rmp 
                WHERE
                    rmp.proveedor_id_rmp = :codigo
                GROUP BY
                    mp.id_mps,
                    mp.nombre_mps,
                    mp.activo_mps"""
                                               )
            # "select mp.id_mp ,mp.nombre_mp, mp.cantidad_mp from materias_primas mp inner join matprimas_proveedores mp2 on mp.id_mp=mp2.id_mp_mpprov where mp.activo_mp =true  and mp2.id_prov_mpprov =:codigo")
            self.query_materias_primas.bindValue(':codigo', codigo)
            self.query_materias_primas.exec()

            self.model2 = QSqlQueryModel()
            self.model2.setQuery(self.query_materias_primas)

            self.model2.setHeaderData(0, Qt.Horizontal, str("Código"))
            self.model2.setHeaderData(1, Qt.Horizontal, str("Materia prima"))
            self.model2.setHeaderData(2, Qt.Horizontal, str("Cantidad / g"))
            self.model2.setHeaderData(3, Qt.Horizontal, str("Activo"))

            # Crear una vista de tabla
            self.ventana_detalle.tv_materias_primas.setModel(self.model2)
            self.ventana_detalle.tv_materias_primas.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_materias_primas.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_materias_primas.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_materias_primas.resizeRowsToContents()
            self.ventana_detalle.tv_materias_primas.resizeColumnsToContents()
            self.ventana_detalle.tv_materias_primas.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            self.ventana_detalle.show()
            # self.ventana_detalle.show()

            self.hide()
