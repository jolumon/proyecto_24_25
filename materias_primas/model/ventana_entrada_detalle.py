from PySide6.QtSql import QSqlQuery, QSqlTableModel, QSqlQueryModel
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QDate
from materias_primas.view.ui_materias_primas_entrada_detalle import Ui_Form
from auxiliares import VentanaEntradaNoValida, VentanaFaltanDatos, VentanaValueError
from validar_datos_entrada import set_validar_cantidad


class VentanaEntradaDetalle(QWidget, Ui_Form):
    """Clase que representa una ventana se utiliza 
    para modificar la cantidad entrada en una materia prima.

    Esta clase hereda de QWidget para crear un widget que puede ser utilizado
    como una ventana independiente. También hereda de Ui_Form para cargar
    la interfaz gráfica. 

    Args:
        QWidget (QWidget): Clase base para todos los objetos de interfaz gráfica.
        Ui_Form (object): Clase generada por PySide-Designer que define la interfaz
                          gráfica de esta ventana.
    """
    def __init__(self, ventana_detalle):
        super().__init__()
        self.setupUi(self)


        self.ventana_detalle = ventana_detalle
        
        # Limitar la entrada de datos erroneos
        set_validar_cantidad(self.le_cantidad_de)
        

    # Signal and Slots

        self.btn_salir_de.clicked.connect(self.close)
        self.btn_guardar_de.clicked.connect(self.guardar_modificacion_entrada)

        # self.showMaximized()

    def closeEvent(self, event):
        """
            Maneja el evento del cierre de la ventana.
            Cuando se cierra la ventana secundaria, se muestra la ventana padre
            Args:
                event (QCloseEvent): 
        """
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_detalle.show()
        event.accept()

    def guardar_modificacion_entrada(self):
        """
        Guarda la modificación de la cantidad y fecha caducidad de una entrada previamente seleccionada.
        """
        print(f"Estoy en guardar_modificacion_entrada")

        selected_index = self.ventana_detalle.tv_entradas_mp_det.selectedIndexes()
        # print(f'Selected index: {selected_index}')
        if selected_index:
            # Obtenemos el número de fila de la celda seleccionada
            fila = selected_index[0].row()
            print(f"Fila guardar_modi_entrada:{fila}-{type(fila)}")
            id_pers_index = self.ventana_detalle.ventana_mp.proxy_model_lote_ent.mapToSource(
                selected_index[0])

            lote = self.ventana_detalle.ventana_mp.model3.data(
                self.ventana_detalle.ventana_mp.model3.index(id_pers_index.row(), 2))
            print(f"Lote:{lote}- Tipo:{type(lote)}")  # ->Es correcto
        else:
            ventana_seleccciona = VentanaFaltaSeleccionarFila()
            ventana_seleccciona.exec()
            return

        try:

            nueva_fecha_cad = self.de_fecha_cad_de.text()
            print(
                f"Nueva fecha cad fin:{nueva_fecha_cad}-{type(nueva_fecha_cad)}")
            nueva_cantidad = int(self.le_cantidad_de.text())
            print(
                f"Nueva Cantidad: {nueva_cantidad}-Tipo:{type(nueva_cantidad)}")
            if nueva_cantidad == "":
                raise ValueError
            if nueva_fecha_cad == "":
                raise Exception
        except ValueError:
            ventana_cantidad = VentanaValueError()
            ventana_cantidad.exec()
            return
        except Exception:
            ventana_error = VentanaFaltanDatos()
            ventana_error.exec()
            return

        query_actualizar_modi = QSqlQuery()
        query_actualizar_modi.prepare(
            """
            update
                entradas
            set
                fecha_caducidad_ent = :fecha,
                cantidad_ent = :cantidad
            where
                nombre_lotes_ent =:lote
            """
        )
        query_actualizar_modi.bindValue(":fecha", nueva_fecha_cad)
        query_actualizar_modi.bindValue(":cantidad", nueva_cantidad)
        query_actualizar_modi.bindValue(":lote", lote)

        if query_actualizar_modi.exec():
            print("Entrada modificada exitosamente")
            try:

                self.modificar_lotes_stock(
                    nueva_fecha_cad, nueva_cantidad, lote)

                codigo = int(self.ventana_detalle.le_codigo_det.text())
                print(f"ventana_mp: {self.ventana_detalle.ventana_mp}")
                print(
                    f"model3: {getattr(self.ventana_detalle.ventana_mp, 'model3', 'No existe')}")

                self.ventana_detalle.ventana_mp.model3.setQuery(
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

                self.ventana_detalle.ventana_mp.proxy_model_lote_ent.setSourceModel(
                    self.ventana_detalle.ventana_mp.model3)

                self.actualizar_modelos()

                self.close()

            except Exception as e:
                print(f"Error al actualizar la vista: {e}")
        else:
            query_actualizar_modi.lastError()

    def modificar_lotes_stock(self, nueva_fecha_cad, nueva_cantidad, lote):
        """
        Actualiza la fecha de caducidad y cantidad para un lote dado.

        Args:
            nueva_fecha_cad (date): _description_
            nueva_cantidad (int): _description_
            lote (str): _description_
        """        
        query_actualizar_lotes_stock = QSqlQuery()
        query_actualizar_lotes_stock.prepare(
            """
            update
                lotes_stock 
            set
                fecha_caducidad_lotes_stock  = :fecha,
                cantidad_lotes_stock = :cantidad
            where
                lotes_stock.nombre_lotes_stock =:lote
            """
        )
        query_actualizar_lotes_stock.bindValue(":fecha", nueva_fecha_cad)
        query_actualizar_lotes_stock.bindValue(":cantidad", nueva_cantidad)
        query_actualizar_lotes_stock.bindValue(":lote", lote)

        if query_actualizar_lotes_stock.exec():
            print(f"Actualizado lotes en stock")
        else:
            query_actualizar_lotes_stock.lastError()

    def actualizar_modelos(self):
        """
        Actualiza las vistas de las tablas de las pestañas de la ventana detalle,
        tras la modificación de datos.
        """
        codigo = int(self.ventana_detalle.le_codigo_det.text())
        # print(f"ventana_mp: {self.ventana_detalle.ventana_mp}")
        # print(
        #     f"model3: {getattr(self.ventana_detalle.ventana_mp, 'model3', 'No existe')}")

        self.ventana_detalle.ventana_mp.model5.setQuery(
            f"""select
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
                    mp.id_mps , mp.nombre_mps,ls.nombre_lotes_stock """
        )

        cantidad = self.ventana_detalle.obtener_cantidad_mp(codigo)
        self.ventana_detalle.le_cantidad_det.setText(str(cantidad))

        self.ventana_detalle.ventana_mp.model.setQuery(
            f"""select
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

        self.ventana_detalle.ventana_mp.proxy_model_mp.setSourceModel(
            self.ventana_detalle.ventana_mp.model)
