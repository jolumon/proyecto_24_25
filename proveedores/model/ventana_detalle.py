import sys
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView
from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt
from proveedores.view.ui_proveedor_detalle import Ui_Form
from auxiliares import VentanaEmergenteBorrar, VentanaEmergenteVacio
from validar_datos_entrada import set_validar_cantidad, set_validar_telefono, set_validar_numeros


class VentanaDetalle(QWidget, Ui_Form):
    """
         Clase que representa la ventana de detalle un proveedor.
    Hereda de QMainWindow para proporcionar una ventana y de
    Ui_MainWindow para cargar la interfaz gráfica.

     Args:
        QWidget (QWidget): Clase base para todas las ventanas de la aplicación
        Ui_Form (Ui_Form): Clase generada que define la interfaz gráfica de la ventana.
    """
    
    
    def __init__(self, ventana_proveedor):
        super().__init__()

        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.ventana_proveedor = ventana_proveedor

        set_validar_telefono(self.le_telefono)
        set_validar_telefono(self.le_movil)
        set_validar_numeros(self.le_codigo_postal)

        self.showMaximized()

    # Signals and Slots

        self.btn_cerrar.clicked.connect(self.close)
        self.btn_borrar.clicked.connect(self.borrar_proveedor)
        self.btn_actualizar.clicked.connect(self.actualizar_proveedor)

    def closeEvent(self, event):
        """
        Maneja el evento del cierre de la ventana.
        Cuando se cierra la ventana detalle de proveedor, se muestra la ventana de proveedores
        Args:
            event (QCloseEvent): El evento de cierre que contiene información sobre el 
            cierre de la ventana.
        """ 
        self.ventana_proveedor.show()
        event.accept()

    def borrar_proveedor(self):
        """
        Borrar proveedor.
        """

        ventana_confirmacion = VentanaEmergenteBorrar()
        respuesta = ventana_confirmacion.exec()

        if respuesta:

            codigo = int(self.le_codigo.text())
            print(f'Código:{codigo}')
            print(type(codigo))
            query = QSqlQuery()
            query.prepare(
                "update proveedores set activo_proveedores =false where id_proveedores =:codigo")
            query.bindValue(":codigo", codigo)
            query.exec()

            self.limpiar_datos()
            self.ventana_proveedor.initial_query.exec(
                "select * from proveedores where activo_provedores=true order by id_proveedores")
            self.ventana_proveedor.model.setQuery(
                self.ventana_proveedor.initial_query)

            self.ventana_proveedor.tv_proveedores.selectRow(0)
            # self.ventana_proveedor.model.select()
            self.close()

            self.ventana_proveedor.initial_query.exec(
                "select * from proveedores where activo_proveedores=true order by id_proveedores")
            self.ventana_proveedor.model.setQuery(
                self.ventana_proveedor.initial_query)

            self.ventana_proveedor.tv_proveedores.selectRow(0)

    def limpiar_datos(self):
        """
        Limpiar datos de la ventana.
        """
        self.le_codigo.setText("")
        self.le_nombre.setText("")
        self.le_direccion.setText("")
        self.le_codigo_postal.setText("")
        self.le_poblacion.setText("")
        self.le_provincia.setText("")
        self.le_telefono.setText("")
        self.le_contacto.setText("")
        self.le_movil.setText("")
        self.le_email.setText("")

    def actualizar_proveedor(self):
        """
        Actualizar proveedor.
        """

        codigo = int(
            self.le_codigo.text())  # Lo paso a entero para que coincida con el tipo de datos de la bd
        # codigo = self.model.index(fila, 0).data()->Aquí no conozco fila, tendría que hacerla global

        nombre = self.le_nombre.text()
        if nombre.strip() == "":
            ventana_nombre_error = VentanaEmergenteVacio()
            respuesta = ventana_nombre_error.exec()
            return
        direccion = self.le_direccion.text()
        codigo_postal = self.le_codigo_postal.text()
        poblacion = self.le_poblacion.text()
        provincia = self.le_provincia.text()
        telefono = self.le_telefono.text()
        contacto = self.le_contacto.text()
        movil = self.le_movil.text()
        email = self.le_email.text()
        print(type(codigo))
        print(f'{codigo},{nombre},{direccion},{codigo_postal},{poblacion},{provincia},{telefono},{email},{contacto}')

        query = QSqlQuery()
        # query.prepare(
        #     "UPDATE clientes SET nombre_clientes=:nombre,direccion_clientes=:direccion,codigo_postal=:codigo_postal,"
        #     "poblacion=:poblacion,provincia=:provincia, telefono=:telefono,email=:email,contacto=:contacto"
        #     "WHERE id_clientes=:codigo")
        query.prepare(
            f'UPDATE proveedores SET nombre_proveedores=:nombre,direccion_proveedores=:direccion,cp_proveedores=:codigo_postal,poblacion_proveedores=:poblacion,provincia_proveedores=:provincia, telefono_proveedores=:telefono,contacto_proveedores=:contacto,movil_proveedores=:movil,email_proveedores=:email WHERE id_proveedores=:codigo')

        query.bindValue(":codigo", codigo)
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

        self.close()

        self.ventana_proveedor.initial_query.exec(
            "select * from proveedores where activo_proveedores=true order by id_proveedores")
        self.ventana_proveedor.model.setQuery(
            self.ventana_proveedor.initial_query)

        self.ventana_proveedor.tv_proveedores.selectRow(0)
