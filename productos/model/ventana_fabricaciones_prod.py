from PySide6.QtWidgets import QWidget, QTableView, QHeaderView, QMessageBox
from productos.view.ui_ventana_producto_detalle_fabricacion import Ui_Form
from auxiliares import VentanaEmergenteBorrar, VentanaEmergenteFaltaMPs, VentanaFaltanDatos
from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt, QDate, QSortFilterProxyModel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class VentanaFabricación(QWidget, Ui_Form):
    def __init__(self, ventana_detalle_of):
        super().__init__()

        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()

        self.ventana_detalle_of = ventana_detalle_of

        # Signals and Slots
        self.btn_salir_dof.clicked.connect(self.close)
        self.btn_imprimir_dof.clicked.connect(
            self.imprimir_datos_orden_fabricacion)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal

        self.ventana_detalle_of.show()
        event.accept()
        print("Saliendo del detalle de la fabricación...")
        # self.close()

    def imprimir_datos_orden_fabricacion(self):
        print("Imprimiendo datos...")
        try:
            nombre_archivo = f"{self.le_lote_dof.text()}.pdf"
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            styles = getSampleStyleSheet()
            styleN = styles['Normal']
            styleH = styles['Heading1']
            aW, aH = letter
            x_position = inch

            datos = {
                "Fecha": f"{self.le_fecha_dof.text()}",
                "Cosmético": f"{self.le_cosmetico_dof.text()}",
                "Cantidad": f"{self.le_cantidad_dof.text()}",
                "Lote": f"{self.le_lote_dof.text()}",
                "Caducidad": f"{self.le_cadudcidad_dof.text()}",
                "Equipo": f"{self.le_equipo_dof.text()}",
            }

            y_position = aH - inch  # Margen superior inicial

            # Imprimir título
            titulo = Paragraph("Orden de Fabricación", styleH)
            titulo.wrapOn(c, aW - 2 * inch, aH)
            titulo.drawOn(c, x_position, y_position)
            y_position -= titulo.height + 12

            # Imprimir datos adicionales
            for clave, valor in datos.items():
                p = Paragraph(f"<b>{clave}:</b> {valor}", styleN)
                p.wrapOn(c, aW - 2 * inch, aH)
                p.drawOn(c, x_position, y_position)
                y_position -= p.height + 6

            y_position -= 12  # Espacio entre datos y tabla

            data = []

            header_row = []
            for col in range(self.ventana_detalle_of.model_dof.columnCount()):
                header_text = self.ventana_detalle_of.model_dof.headerData(
                    col, Qt.Horizontal)
                header_row.append(header_text)
            data.append(header_row)  # ***AÑADIR LA CABECERA A LOS DATOS***

            if self.ventana_detalle_of.model_dof.rowCount() > 0:
                for row in range(self.ventana_detalle_of.model_dof.rowCount()):
                    row_data = []
                    for col in range(self.ventana_detalle_of.model_dof.columnCount()):
                        index = self.ventana_detalle_of.model_dof.index(
                            row, col)
                        data_cell = self.ventana_detalle_of.model_dof.data(
                            index, Qt.DisplayRole)
                        row_data.append(
                            str(data_cell) if data_cell is not None else "")
                    data.append(row_data)

                col_widths = []
                # Manejo de tabla vacia
                for col in range(len(data[0]) if data else 0):
                    max_width = 0
                    for row_data in data:
                        try:
                            text_width = c.stringWidth(
                                str(row_data[col]), "Helvetica", 11)  # Fuente y tamaño
                        except IndexError:
                            text_width = 0
                        max_width = max(max_width, text_width)
                    # Añadir un pequeño margen
                    col_widths.append(max_width + 10)

                table = Table(data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('WORDWRAP', (0, 0), (-1, -1), 1),
                ]))

                # --- CALCULAR LA ALTURA DE LA TABLA ANTES DE DIBUJARLA ---
                table_width, table_height = table.wrapOn(c, aW - 2 * inch, aH)

                # --- DIBUJAR LA TABLA USANDO y_position Y LA ALTURA CALCULADA ---
                table.drawOn(c, x_position, y_position - table_height)
                y_position -= table_height + 24  # Actualizar y_position

            else:
                QMessageBox.warning(self, "Advertencia",
                                    "No hay datos para generar el PDF.")

            c.save()
            QMessageBox.information(
                self, "PDF Generado", f"El PDF se ha generado correctamente como '{nombre_archivo}'")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Se produjo un error al generar el PDF: {e}")
