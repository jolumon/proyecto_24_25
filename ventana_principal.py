import sys

from clientes.model.ventana_clientes import VentanaCliente
from materias_primas.model.ventana_mp import VentanaMateriasPrimas
from proveedores.model.ventana_proveedores import VentanaProveedor
from productos.model.ventana_productos import VentanaProducto
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QCloseEvent, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt
from PySide6 import QtCore
from ui_ventana_principal5 import Ui_MainWindow
from conexion_v3 import Conexion


class VentanaPrincipal(QMainWindow, Ui_MainWindow):
    """Clase que representa la Ventana de bienvenida del proyecto
        Muestra 4 botones que al pulsar sobre cualquiera de ellos
        mostrará el módulo en cuestión en una nueva ventana"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Principal: labERP")
        self.showMaximized()


        # Carga la imagen
        original_pixmap = QPixmap(
            "/home/jolumon/Documentos/proyecto_24_25/lab-1009190_1920.jpg")

        # Ajusta el tamaño de la imagen
        scaled_pixmap = original_pixmap.scaled(
            875, 659, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Crea un nuevo QPixmap con el mismo tamaño que la imagen escalada
        result_pixmap = QPixmap(scaled_pixmap.size())

        # Rellena con color transparente
        result_pixmap.fill(QColor(0, 0, 0, 0))

        # Dibuja la imagen y el texto en el nuevo QPixmap
        painter = QPainter(result_pixmap)
        painter.setOpacity(0.4)  # Ajusta la opacidad:1 opaco,0 transparente
        painter.drawPixmap(0, 0, scaled_pixmap)

        # Establece la fuente y el color del texto
        painter.setOpacity(1.0)
        painter.setPen(QColor(0, 0, 0, 255))  # Color del texto
        painter.setFont(self.label.font())  # Usa la fuente del QLabel
        painter.drawText(scaled_pixmap.rect(), QtCore.Qt.AlignCenter,
                         "Bienvenido a labERP")  # Dibuja el texto centrado
        painter.end()

        # Establece el QPixmap resultante en el QLabel
        self.label.setPixmap(result_pixmap)

        # Conexión a la base de datos
        self.conexion = Conexion()
        self.conexion.conectar()

        # Signals and Slots

        self.btn_clientes.clicked.connect(self.ventana_clientes)
        self.btn_materias_primas.clicked.connect(self.ventana_materias_primas)
        self.btn_productos.clicked.connect(self.ventana_productos)
        self.btn_proveedores.clicked.connect(self.ventana_proveedores)

    def ventana_clientes(self):
        """
        Crea una ventana del tipo VentanaCliente y la muestra. Oculta la ventana principal.
        """
        self.ventana_cliente = VentanaCliente(self)
        self.ventana_cliente.show()
        self.hide()

    def ventana_materias_primas(self):
        """
        Crea una ventana del tipo VentanaMateriasPrimas y la muestra. Oculta la ventana principal.
        """
        self.ventana_materia_prima = VentanaMateriasPrimas(self)
        self.ventana_materia_prima.show()
        self.hide()

    def ventana_productos(self):
        """
        Crea una ventana del tipo VentanaProducto y la muestra. Oculta la ventana principal.
        """
        self.ventana_producto = VentanaProducto(self)
        self.ventana_producto.show()
        self.hide()

    def ventana_proveedores(self):
        """
        Crea una ventana del tipo VentanaProveedor y la muestra. Oculta la ventana principal.
        """
        self.ventana_proveedor = VentanaProveedor(self)
        self.ventana_proveedor.show()
        self.hide()

    def closeEvent(self, event):
        """
        Maneja el evento del cierre de la ventana.
        Cuando se cierra la ventana secundaria, se muestra la ventana padre
        Args:
            event (QCloseEvent): 
        """       
        event.accept()
        self.conexion.desconectar()


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
