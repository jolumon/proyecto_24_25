from PySide6.QtWidgets import QWidget, QTableView, QHeaderView

from productos.view.ui_ventana_producto_detalle_fabricacion import Ui_Form
from auxiliares import VentanaEmergenteBorrar, VentanaEmergenteFaltaMPs, VentanaFaltanDatos
from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt, QDate, QSortFilterProxyModel


class VentanaFabricación(QWidget, Ui_Form):
    def __init__(self, ventana_detalle_of):
        super().__init__()

        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()

        self.ventana_detalle_of = ventana_detalle_of

        
        # Signals and Slots
        self.btn_salir_dof.clicked.connect(self.close)
        self.btn_imprimir_dof.clicked.connect(self.imprimir_datos_orden_fabricacion)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        
        self.ventana_detalle_of.show()
        event.accept()
        print("Saliendo del detalle de la fabricación...")
        # self.close()
        
    def imprimir_datos_orden_fabricacion(self):
        print("Imprimiendo datos...")
