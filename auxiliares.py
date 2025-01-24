from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QTableView, QAbstractItemView,QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem


class VentanaEmergenteBorrar(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("¿Está seguro de la eliminación?"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaEmergenteVacio(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Se debe introducir un nombre"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaEmergenteFechaIncorrecta(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("La fecha de caducidad debe ser mayor que la fecha de entrada"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaEmergenteFaltaMPs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("Falta algún componente de la composición"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaMPExistente(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Ya existe esta materia prima"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaFaltanDatos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Faltan datos por introducir"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaFaltaSeleccionarFila(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Falta seleccionar alguna fila"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaEntradaNoValida(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("Debes introducir el tipo dato correcto."))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaValueError(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("Debes introducir un número."))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaUbicacionNoDisponible(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atención")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("No hay ubicaciones libres. Contacta con el administrador"))

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)


class VentanaFaltas(QDialog):
    def __init__(self, faltas):
        super().__init__()
        self.setWindowTitle("ATENCIÓN")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(
            QLabel("Las siguientes materias primas no estan diponibles"))

        # Crear un QTableView
        self.tv_faltas = QTableView()
        self.layout.addWidget(self.tv_faltas)

        # Crear un modelo y llenar con datos
        self.modelo_faltas = QStandardItemModel()
        self.modelo_faltas.setHorizontalHeaderLabels(
            ["Materia Prima", "Cantidad Faltante /g"])  # Encabezados de las columnas

        for materia, cantidad in faltas:
            items = [QStandardItem(materia), QStandardItem(str(cantidad))]
            self.modelo_faltas.appendRow(items)

        self.tv_faltas.setModel(self.modelo_faltas)

        self.tv_faltas.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
        # Seleccionar filas completas
        self.tv_faltas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_faltas.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Seleccionar filas completas

        # Configurar la vista de tabla
        self.tv_faltas.resizeRowsToContents()
        self.tv_faltas.resizeColumnsToContents()
        # Amplia el tamaño de la tabla a toda la pantalla
        self.tv_faltas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_faltas.selectRow(0)

        self.botones = QDialogButtonBox(
            QDialogButtonBox.Ok)

        self.botones.accepted.connect(self.accept)
        # self.botones.rejected.connect(self.reject)

        self.layout.addWidget(self.botones)
