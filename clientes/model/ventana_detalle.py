import sys
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView
from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt
from clientes.view.ui_cliente_detalle import Ui_Form
from auxiliares import VentanaEmergenteBorrar


class VentanaDetalle(QWidget, Ui_Form):
    """
    Clase que representa la ventana para mostrar los detalles de un cliente.

    Args:
        QWidget (_type_): _description_
        Ui_Form (_type_): _description_
    """
    def __init__(self, ventana_cliente):
        super().__init__()

        self.setupUi(self)

        # self.setWindowModality(Qt.ApplicationModal)
        self.ventana_cliente = ventana_cliente

        self.showMaximized()

    # Signals and Slots

        self.btn_cerrar.clicked.connect(self.close)
        self.btn_borrar.clicked.connect(self.borrar_cliente)
        self.btn_actualizar.clicked.connect(self.actualizar_cliente)

    def closeEvent(self, event):
        """
        Maneja el evento del cierre de la ventana.
        Cuando se cierra la ventana detalle, se muestra la ventana clientes

        Args:
            event (QCloseEvent): El evento de cierre que contiene información sobre el 
            cierre de la ventana.
        """
        
        self.ventana_cliente.show()
        event.accept()

    def borrar_cliente(self):
        """
        Borra un cliente.
        """

        ventana_confirmacion = VentanaEmergenteBorrar()
        respuesta = ventana_confirmacion.exec()

        if respuesta:

            codigo = int(self.le_codigo.text())
            print(f'Código:{codigo}')
            print(type(codigo))
            query = QSqlQuery()
            query.prepare(
                "UPDATE clientes SET activo_clientes= false WHERE id_clientes=:codigo")
            query.bindValue(":codigo", codigo)
            query.exec()

            self.limpiar_datos()
            
            self.ventana_cliente.initial_query.exec("select * from clientes where activo_clientes=true order by id_clientes")
            self.ventana_cliente.model.setQuery(self.ventana_cliente.initial_query)
            self.ventana_cliente.tv_clientes.selectRow(0)
            self.close()

    def limpiar_datos(self):
        """
        Limpia los datos de la ventana.
        """
        self.le_codigo.setText("")
        self.le_nombre.setText("")
        self.le_direccion.setText("")
        self.le_codigo_postal.setText("")
        self.le_poblacion.setText("")
        self.le_provincia.setText("")
        self.le_telefono.setText("")
        self.le_email.setText("")
        self.le_contacto.setText("")

    def actualizar_cliente(self):
        """
        Actualiza un cliente.
        """

        codigo = int(
            self.le_codigo.text())  # Lo paso a entero para que coincida con el tipo de datos de la bd
        # codigo = self.model.index(fila, 0).data()->Aquí no conozco fila, tendría que hacerla global
        nombre = self.le_nombre.text()
        direccion = self.le_direccion.text()
        codigo_postal = self.le_codigo_postal.text()
        poblacion = self.le_poblacion.text()
        provincia = self.le_provincia.text()
        telefono = self.le_telefono.text()
        email = self.le_email.text()
        contacto = self.le_contacto.text()
        print(type(codigo))
        print(f'{codigo},{nombre},{direccion},{codigo_postal},{poblacion},{provincia},{telefono},{email},{contacto}')

        query = QSqlQuery()
        query.prepare(
            f'UPDATE clientes SET nombre_clientes=:nombre,direccion_clientes=:direccion,codigo_postal_clientes=:codigo_postal,poblacion_clientes=:poblacion,provincia_clientes=:provincia, telefono_clientes=:telefono,email_clientes=:email,contacto_clientes=:contacto WHERE id_clientes=:codigo')

        query.bindValue(":codigo", codigo)
        query.bindValue(":nombre", nombre)
        query.bindValue(":direccion", direccion)
        query.bindValue(":codigo_postal", codigo_postal)
        query.bindValue(":poblacion", poblacion)
        query.bindValue(":provincia", provincia)
        query.bindValue(":telefono", telefono)
        query.bindValue(":email", email)
        query.bindValue(":contacto", contacto)

        query.exec()
        print(f'{codigo},{nombre},{direccion},{codigo_postal},{poblacion},{provincia},{telefono},{email},{contacto}')


        self.close()
        
        self.ventana_cliente.initial_query.exec("select * from clientes where activo_clientes=true order by id_clientes")
        self.ventana_cliente.model.setQuery(self.ventana_cliente.initial_query)
        
        # self.ventana_cliente.model.select()
        self.ventana_cliente.tv_clientes.selectRow(0)
        
        
