from typing import Optional
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableView
from PySide6.QtSql import QSqlTableModel, QSqlQuery, QSqlQueryModel
from PySide6.QtCore import Qt, QSortFilterProxyModel, QDate
from materias_primas.view.ui_materias_primas3 import Ui_Form
from materias_primas.model.ventana_detalle_mp import VentanaDetalle
from auxiliares import VentanaEmergenteBorrar, VentanaMPExistente


class VentanaMateriasPrimas(QWidget, Ui_Form):
    def __init__(self, ventana_principal):
        super().__init__()
        self.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.showMaximized()
        self.ventana_principal = ventana_principal

        # Crear un model de tabla

        self.initial_query = QSqlQuery()
        self.initial_query.exec(
            "SELECT id_mps,nombre_mps FROM materias_primas where activo_mps=true order by id_mps asc")
        self.model = QSqlQueryModel()
        self.model.setQuery(self.initial_query)

       # Cabeceras de la tabla
        cabeceras = ['Codigo', 'Nombre']
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


    #     #Nueva pestaña de materias primas

    #     # Crear un model de tabla

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
                    e.fecha_ent desc"""

        )
        self.model_ent = QSqlQueryModel()
        self.model_ent.setQuery(self.entradas_query)

       # Cabeceras de la tabla
        cabeceras = ['Codigo', 'Nombre', 'Lote',
                     'Fecha entrada', 'Cantidad / kg', 'Proveedor']
        for i, cabecera in enumerate(cabeceras):
            self.model_ent.setHeaderData(i, Qt.Horizontal, cabecera)

        # Crear un filtro para la búsqueda
        self.proxy_model_mp_ent = QSortFilterProxyModel()
        self.proxy_model_mp_ent.setSourceModel(self.model_ent)

        # Crear un cuadro de texto para la búsqueda

        self.le_buscar_mp.setPlaceholderText("Buscar por nombre...")
        self.le_buscar_mp.textChanged.connect(self.filter)

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
##########################################################################################
        # Signal and Slots para pestaña Nueva
        self.btn_guardar_nueva_mp.clicked.connect(self.guardar_nueva_mp)
        self.btn_cancelar_nueva_mp.clicked.connect(self.cambia_pestaña)

        # Signal and Slots para pestaña Listado
        self.btn_ver_detalle_mp.clicked.connect(self.ver_detalle_producto2)
        self.btn_cerrar_listado_mp.clicked.connect(self.close)

    def filter(self):
        text = self.le_buscar_mp.text()
        # Usar setFilterFixedString en lugar de setFilterRegExp
        self.proxy_model_mp.setFilterFixedString(text)
        # Filtrar por la columna "nombre_persona"
        self.proxy_model_mp.setFilterKeyColumn(1)
        self.proxy_model_mp.invalidate()  # Asegurarse de que el proxy model se actualice

    # def ver_detalle_producto(self):

    #     self.ventana_detalle = VentanaDetalle(self)
    #     selected_index = self.tv_mat_primas.currentIndex()
    #     print(f'Selected index: {selected_index}')
    #     if selected_index.isValid():
    #         # Obtenemos el número de fila de la celda seleccionada
    #         # print('Entra en el if del selected_index')
    #         fila = selected_index.row()
    #         print(f'Fila: {fila}')

    #         codigo = self.model.index(fila, 0).data()
    #         nombre = self.model.index(fila, 1).data()
    #         cantidad = self.model.index(fila, 2).data()
    #         # proveedor = self.model.index(fila, 3).data()

    #         # establecemos los campos con los valores seleccionados
    #         self.ventana_detalle.le_codigo_det.setText(str(codigo))
    #         self.ventana_detalle.le_nombre_det.setText(nombre)
    #         self.ventana_detalle.le_cantidad_det.setText(str(cantidad))
    #         # self.ventana_detalle.le_proveedor_det.setText(str(proveedor))

    #         self.ventana_detalle.le_codigo_entrada.setText(str(codigo))
    #         self.ventana_detalle.le_nombre_entrada.setText(nombre)
    #         # self.ventana_detalle.le_cantidad_entrada.setText(str(cantidad))
    #         # self.ventana_detalle.le_proveedor_entrada.setText(str(proveedor))
    #         self.ventana_detalle.le_f_entrada.setText(str(QDate.currentDate().toString('dd-MM-yyyy')))

    #         self.query_productos = QSqlQuery()
    #         self.query_productos.prepare(
    #             "SELECT productos.id_prod,productos.nombre_prod, productos.linea_prod FROM productos INNER JOIN clientes on productos.cliente_prod=clientes.id_cli WHERE id_cli=:codigo ORDER BY productos.nombre_prod")
    #         self.query_productos.bindValue(':codigo', codigo)
    #         self.query_productos.exec()

    #         # Se crea el modelo para mostrar los datos de las entradas del producto seleccionado
    #         self.model3 = QSqlQueryModel()
    #         self.model3.setQuery(
    #             f'select e.fecha_ent_ent , e.lote_ent ,e.fecha_cad_ent ,e.cantidad_ent ,e.precio_ent ,p.nombre_prov from materias_primas mp inner join entradas e on mp.id_mp = e.id_mp_ent inner join proveedores p on p.id_prov = e.id_prov_ent where mp.id_mp = {codigo}')

    #         self.model3.setHeaderData(0, Qt.Horizontal, str("Fecha Entrada"))
    #         self.model3.setHeaderData(1, Qt.Horizontal, str("Lote"))
    #         self.model3.setHeaderData(2, Qt.Horizontal, str("Fecha Caducidad"))
    #         self.model3.setHeaderData(3, Qt.Horizontal, str("Cantidad / kg"))
    #         self.model3.setHeaderData(4, Qt.Horizontal, str("Precio"))
    #         self.model3.setHeaderData(5, Qt.Horizontal, str("Proveedor"))

    #         # Crear una vista de tabla
    #         self.ventana_detalle.tv_entradas_mp_det.setModel(self.model3)
    #         self.ventana_detalle.tv_entradas_mp_det.setEditTriggers(
    #             QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
    #         self.ventana_detalle.tv_entradas_mp_det.setSelectionMode(
    #             QAbstractItemView.SingleSelection)  # Seleccionar filas completas
    #         self.ventana_detalle.tv_entradas_mp_det.setSelectionBehavior(
    #             QAbstractItemView.SelectRows)  # Seleccionar filas completas

    #         # Configurar la vista de tabla
    #         self.ventana_detalle.tv_entradas_mp_det.resizeRowsToContents()
    #         self.ventana_detalle.tv_entradas_mp_det.resizeColumnsToContents()
    #         self.ventana_detalle.tv_entradas_mp_det.horizontalHeader(
    #         ).setSectionResizeMode(QHeaderView.Stretch)

    #         # Se crea el modelo para mostrar los proveedores de la materia prima
    #         self.model4 = QSqlQueryModel()
    #         self.model4.setQuery(
    #             f'select p.id_prov ,p.nombre_prov  from materias_primas mp inner join matprimas_proveedores mp2 on mp.id_mp =mp2.id_mp_mpprov inner join proveedores p on mp2.id_prov_mpprov = p.id_prov  where mp.id_mp={codigo}')

    #         self.model4.setHeaderData(0, Qt.Horizontal, str("Código"))
    #         self.model4.setHeaderData(1, Qt.Horizontal, str("Nombre"))

    #         # Crear una vista de tabla
    #         self.ventana_detalle.tv_provs_detalle_mp.setModel(self.model4)
    #         self.ventana_detalle.tv_provs_detalle_mp.setEditTriggers(
    #             QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
    #         self.ventana_detalle.tv_provs_detalle_mp.setSelectionMode(
    #             QAbstractItemView.SingleSelection)  # Seleccionar filas completas
    #         self.ventana_detalle.tv_provs_detalle_mp.setSelectionBehavior(
    #             QAbstractItemView.SelectRows)  # Seleccionar filas completas

    #         # Configurar la vista de tabla
    #         self.ventana_detalle.tv_provs_detalle_mp.resizeRowsToContents()
    #         self.ventana_detalle.tv_entradas_mp_det.resizeColumnsToContents()
    #         self.ventana_detalle.tv_provs_detalle_mp.horizontalHeader(
    #         ).setSectionResizeMode(QHeaderView.Stretch)

    #         self.ventana_detalle.show()

    #         self.hide()
    #         # Se puede quitar el else-->Habrá que hacerlo
    #     else:
    #         print('No entra en if del selected_index')

    #     print(f'Dentro de ver_detalle_producto')

    def ver_detalle_producto2(self):

        self.ventana_detalle = VentanaDetalle(self)
        selected_index = self.tv_mat_primas.selectedIndexes()
        print(f'Selected index: {selected_index}')
        if selected_index:
            # Obtenemos el número de fila de la celda seleccionada
            # print('Entra en el if del selected_index')
            fila = selected_index[0].row()
            print(f'Fila: {fila}')

            id_pers_index = self.proxy_model_mp.mapToSource(selected_index[0])

            codigo = self.model.data(self.model.index(id_pers_index.row(), 0))

            nombre = self.model.data(self.model.index(id_pers_index.row(), 1))
            cantidad = self.model.data(
                self.model.index(id_pers_index.row(), 2))
            # proveedor = self.model.index(fila, 3).data()

            # establecemos los campos con los valores seleccionados
            self.ventana_detalle.le_codigo_det.setText(str(codigo))
            self.ventana_detalle.le_nombre_det.setText(nombre)
            self.ventana_detalle.le_cantidad_det.setText(str(cantidad))
            # self.ventana_detalle.le_proveedor_det.setText(str(proveedor))

            self.ventana_detalle.le_codigo_entrada.setText(str(codigo))
            self.ventana_detalle.le_nombre_entrada.setText(nombre)
            # self.ventana_detalle.le_cantidad_entrada.setText(str(cantidad))
            # self.ventana_detalle.le_proveedor_entrada.setText(str(proveedor))
            self.ventana_detalle.le_f_entrada.setText(
                str(QDate.currentDate().toString('dd-MM-yyyy')))

            self.query_productos = QSqlQuery()
            self.query_productos.prepare(
                # "SELECT productos.id_prod,productos.nombre_prod, productos.linea_prod FROM productos INNER JOIN clientes on productos.cliente_prod=clientes.id_cli WHERE id_cli=:codigo ORDER BY productos.nombre_prod")
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
                # f'select e.fecha_ent_ent , e.lote_ent ,e.fecha_cad_ent ,e.cantidad_ent ,e.precio_ent ,p.nombre_prov from materias_primas mp inner join entradas e on mp.id_mp = e.id_mp_ent inner join proveedores p on p.id_prov = e.id_prov_ent where mp.id_mp = {codigo}')
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
            self.model3.setHeaderData(4, Qt.Horizontal, str("Cantidad / kg"))
            self.model3.setHeaderData(5, Qt.Horizontal, str("Proveedor"))
            # self.model3.setHeaderData(5, Qt.Horizontal, str("Proveedor"))

            # Crear una vista de tabla
            self.ventana_detalle.tv_entradas_mp_det.setModel(self.model3)
            self.ventana_detalle.tv_entradas_mp_det.setEditTriggers(
                QAbstractItemView.NoEditTriggers)  # Deshabilitar edición
            self.ventana_detalle.tv_entradas_mp_det.setSelectionMode(
                QAbstractItemView.SingleSelection)  # Seleccionar filas completas
            self.ventana_detalle.tv_entradas_mp_det.setSelectionBehavior(
                QAbstractItemView.SelectRows)  # Seleccionar filas completas

            # Configurar la vista de tabla
            self.ventana_detalle.tv_entradas_mp_det.resizeRowsToContents()
            self.ventana_detalle.tv_entradas_mp_det.resizeColumnsToContents()
            self.ventana_detalle.tv_entradas_mp_det.horizontalHeader(
            ).setSectionResizeMode(QHeaderView.Stretch)

            # Se crea el modelo para mostrar los proveedores de la materia prima
            self.model4 = QSqlQueryModel()
            self.model4.setQuery(
                # f'select p.id_prov ,p.nombre_prov  from materias_primas mp inner join matprimas_proveedores mp2 on mp.id_mp =mp2.id_mp_mpprov inner join proveedores p on mp2.id_prov_mpprov = p.id_prov  where mp.id_mp={codigo}')
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
            
            self.model5=QSqlQueryModel()
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
            self.model5.setHeaderData(3, Qt.Horizontal, str("Cantidad / Kg"))
            

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
            # Se puede quitar el else-->Habrá que hacerlo
        else:
            print('No entra en if del selected_index')

        print(f'Dentro de ver_detalle_producto')

    def obtener_clave_principal_proveedor(self):
        nombre_seleccionado = self.cb_proveedor_nueva.currentText()
        clave_principal = self.diccionario_proveedores.get(nombre_seleccionado)

        # print(f'Nombre seleccionado: {nombre_seleccionado}')
        # print(f'Clave principal: {clave_principal}')

        return clave_principal

    def cambia_pestaña(self):
        self.tabWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        # Cuando se cierra la ventana secundaria, se muestra la ventana principal
        self.ventana_principal.show()
        event.accept()

    def mp_existe(self, nombre):
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

        # Recuperar datos de los lineEdit y comboBox
        nombre = self.le_nombre_nueva.text()
        # cantidad = self.ventana_nueva_materia_prima.le_cantidad.text()
        proveedor = int(self.obtener_clave_principal_proveedor())

        if self.mp_existe(nombre):

            print('Ya existe la materia prima')
            # Pop up indicando que ya existe la materia prima
            ventana_mp_existente = VentanaMPExistente()
            respuesta = ventana_mp_existente.exec()
            self.cambia_pestaña()

            return

        # Crear y preparacion de la sentencia sql para insertar materia prima
        query = QSqlQuery()
        query.prepare(
            f'insert into materias_primas (nombre_mps) values (:nombre)')

        query.bindValue(":nombre", nombre)
        query.exec()
        ######################################################################
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
            print("Error al ejecutar la consulta:", query_ultimo_id_mps.lastError().text())
                
        
        
        
        ####################################################################
        # Crear y preparacion de la sentencia sql para insertar en matprimas_proveedores
        query_insertar_rel_mps_pro = QSqlQuery()
        query_insertar_rel_mps_pro.prepare(
            f'insert into rel_mps_proveedores (mp_id_rmp,proveedor_id_rmp) values (:ultimo_id_mps,:proveedor) ')

        query_insertar_rel_mps_pro.bindValue(":ultimo_id_mps", ultimo_id_mps)
        query_insertar_rel_mps_pro.bindValue(":proveedor", proveedor)

        query_insertar_rel_mps_pro.exec()

        self.tabWidget.setCurrentIndex(0)

        self.initial_query.exec(
            "SELECT id_mps,nombre_mps FROM materias_primas where activo_mps=true order by id_mps asc")
        self.model.setQuery(self.initial_query)
        self.tv_mat_primas.selectRow(0)
        # self.close()

        # self.model.select()

        self.le_nombre_nueva.setText('')
        self.cb_proveedor_nueva.setCurrentIndex(-1)
