# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ventana_producto_detalle7TXPKyo.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDateEdit,
    QFormLayout, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(1110, 758)
        Form.setStyleSheet(u"QPushButton{\n"
"\n"
"	\n"
"	background-color: rgb(6, 191, 249);\n"
"\n"
"}")
        self.horizontalLayout_6 = QHBoxLayout(Form)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_detalle = QWidget()
        self.tab_detalle.setObjectName(u"tab_detalle")
        self.verticalLayout_3 = QVBoxLayout(self.tab_detalle)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_codigo_det = QLabel(self.tab_detalle)
        self.lbl_codigo_det.setObjectName(u"lbl_codigo_det")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_codigo_det)

        self.le_codigo_det = QLineEdit(self.tab_detalle)
        self.le_codigo_det.setObjectName(u"le_codigo_det")
        self.le_codigo_det.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_codigo_det)

        self.lbl_nombre_det = QLabel(self.tab_detalle)
        self.lbl_nombre_det.setObjectName(u"lbl_nombre_det")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_nombre_det)

        self.le_nombre_det = QLineEdit(self.tab_detalle)
        self.le_nombre_det.setObjectName(u"le_nombre_det")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_nombre_det)

        self.lbl_caducidad_det = QLabel(self.tab_detalle)
        self.lbl_caducidad_det.setObjectName(u"lbl_caducidad_det")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lbl_caducidad_det)

        self.le_caducidad_det = QLineEdit(self.tab_detalle)
        self.le_caducidad_det.setObjectName(u"le_caducidad_det")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_caducidad_det)

        self.lbl_cliente_det = QLabel(self.tab_detalle)
        self.lbl_cliente_det.setObjectName(u"lbl_cliente_det")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lbl_cliente_det)

        self.cb_cliente = QComboBox(self.tab_detalle)
        self.cb_cliente.setObjectName(u"cb_cliente")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cb_cliente)

        self.lbl_tipo_det = QLabel(self.tab_detalle)
        self.lbl_tipo_det.setObjectName(u"lbl_tipo_det")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lbl_tipo_det)

        self.cb_tipo = QComboBox(self.tab_detalle)
        self.cb_tipo.setObjectName(u"cb_tipo")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cb_tipo)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btn_actualizar_det = QPushButton(self.tab_detalle)
        self.btn_actualizar_det.setObjectName(u"btn_actualizar_det")

        self.horizontalLayout_2.addWidget(self.btn_actualizar_det)

        self.btn_borrar_det = QPushButton(self.tab_detalle)
        self.btn_borrar_det.setObjectName(u"btn_borrar_det")
        self.btn_borrar_det.setStyleSheet(u"background-color: rgb(254, 20, 20);")

        self.horizontalLayout_2.addWidget(self.btn_borrar_det)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.tabWidget_2 = QTabWidget(self.tab_detalle)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.tv_composicion_prod = QTableView(self.tab_2)
        self.tv_composicion_prod.setObjectName(u"tv_composicion_prod")
        self.tv_composicion_prod.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.tv_composicion_prod)

        self.frame = QFrame(self.tab_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.btn_add_component = QPushButton(self.frame)
        self.btn_add_component.setObjectName(u"btn_add_component")

        self.verticalLayout_2.addWidget(self.btn_add_component)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.btn_modificar_comp = QPushButton(self.frame)
        self.btn_modificar_comp.setObjectName(u"btn_modificar_comp")

        self.verticalLayout_2.addWidget(self.btn_modificar_comp)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_7.addWidget(self.frame)

        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.le_buscar_fabricacion = QLineEdit(self.tab)
        self.le_buscar_fabricacion.setObjectName(u"le_buscar_fabricacion")
        self.le_buscar_fabricacion.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.le_buscar_fabricacion)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.btn_ver_detalle_o_fab = QPushButton(self.tab)
        self.btn_ver_detalle_o_fab.setObjectName(u"btn_ver_detalle_o_fab")

        self.horizontalLayout_5.addWidget(self.btn_ver_detalle_o_fab)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.tv_fab_historico = QTableView(self.tab)
        self.tv_fab_historico.setObjectName(u"tv_fab_historico")
        self.tv_fab_historico.setFrameShape(QFrame.Shape.StyledPanel)
        self.tv_fab_historico.setSortingEnabled(True)

        self.verticalLayout_6.addWidget(self.tv_fab_historico)

        self.tabWidget_2.addTab(self.tab, "")

        self.verticalLayout_3.addWidget(self.tabWidget_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_cerrar_det = QPushButton(self.tab_detalle)
        self.btn_cerrar_det.setObjectName(u"btn_cerrar_det")
        self.btn_cerrar_det.setStyleSheet(u"background-color: rgb(22, 183, 40);")

        self.horizontalLayout.addWidget(self.btn_cerrar_det)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab_detalle, "")
        self.tab_fabricacion = QWidget()
        self.tab_fabricacion.setObjectName(u"tab_fabricacion")
        self.verticalLayout_4 = QVBoxLayout(self.tab_fabricacion)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lbl_fecha_fab = QLabel(self.tab_fabricacion)
        self.lbl_fecha_fab.setObjectName(u"lbl_fecha_fab")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lbl_fecha_fab)

        self.de_fecha_fab = QDateEdit(self.tab_fabricacion)
        self.de_fecha_fab.setObjectName(u"de_fecha_fab")
        self.de_fecha_fab.setEnabled(False)
        font = QFont()
        font.setHintingPreference(QFont.PreferVerticalHinting)
        self.de_fecha_fab.setFont(font)
        self.de_fecha_fab.setReadOnly(True)
        self.de_fecha_fab.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.de_fecha_fab.setCalendarPopup(False)
        self.de_fecha_fab.setDate(QDate(2024, 1, 1))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.de_fecha_fab)

        self.lbl_produto_fab = QLabel(self.tab_fabricacion)
        self.lbl_produto_fab.setObjectName(u"lbl_produto_fab")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lbl_produto_fab)

        self.le_producto_fab = QLineEdit(self.tab_fabricacion)
        self.le_producto_fab.setObjectName(u"le_producto_fab")
        self.le_producto_fab.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.le_producto_fab)

        self.lbl_cantidad_fab = QLabel(self.tab_fabricacion)
        self.lbl_cantidad_fab.setObjectName(u"lbl_cantidad_fab")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.lbl_cantidad_fab)

        self.le_cantidad_fab = QLineEdit(self.tab_fabricacion)
        self.le_cantidad_fab.setObjectName(u"le_cantidad_fab")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.le_cantidad_fab)

        self.lbl_equipo_fab = QLabel(self.tab_fabricacion)
        self.lbl_equipo_fab.setObjectName(u"lbl_equipo_fab")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.lbl_equipo_fab)

        self.cb_equipo_fab = QComboBox(self.tab_fabricacion)
        self.cb_equipo_fab.setObjectName(u"cb_equipo_fab")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.cb_equipo_fab)


        self.verticalLayout_4.addLayout(self.formLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.btn_mostrar_pesada = QPushButton(self.tab_fabricacion)
        self.btn_mostrar_pesada.setObjectName(u"btn_mostrar_pesada")

        self.horizontalLayout_3.addWidget(self.btn_mostrar_pesada)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.groupBox_2 = QGroupBox(self.tab_fabricacion)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tv_detalle_new_fab = QTableView(self.groupBox_2)
        self.tv_detalle_new_fab.setObjectName(u"tv_detalle_new_fab")
        self.tv_detalle_new_fab.setFrameShape(QFrame.Shape.StyledPanel)

        self.verticalLayout_5.addWidget(self.tv_detalle_new_fab)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.btn_confirmar_fab = QPushButton(self.tab_fabricacion)
        self.btn_confirmar_fab.setObjectName(u"btn_confirmar_fab")
        self.btn_confirmar_fab.setStyleSheet(u"background-color: rgb(245, 194, 17);")

        self.horizontalLayout_4.addWidget(self.btn_confirmar_fab)

        self.btn_cerrar_fab = QPushButton(self.tab_fabricacion)
        self.btn_cerrar_fab.setObjectName(u"btn_cerrar_fab")
        self.btn_cerrar_fab.setStyleSheet(u"background-color: rgb(22, 183, 40);")

        self.horizontalLayout_4.addWidget(self.btn_cerrar_fab)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab_fabricacion, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Detalle Producto", None))
        self.lbl_codigo_det.setText(QCoreApplication.translate("Form", u"C\u00f3digo", None))
        self.lbl_nombre_det.setText(QCoreApplication.translate("Form", u"Nombre", None))
        self.lbl_caducidad_det.setText(QCoreApplication.translate("Form", u"Caducidad", None))
        self.lbl_cliente_det.setText(QCoreApplication.translate("Form", u"Cliente", None))
        self.lbl_tipo_det.setText(QCoreApplication.translate("Form", u"Tipo", None))
        self.btn_actualizar_det.setText(QCoreApplication.translate("Form", u"Actualizar", None))
        self.btn_borrar_det.setText(QCoreApplication.translate("Form", u"Borrar", None))
        self.btn_add_component.setText(QCoreApplication.translate("Form", u"A\u00f1adir", None))
        self.btn_modificar_comp.setText(QCoreApplication.translate("Form", u"Modificar", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Guardar", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Composici\u00f3n", None))
        self.le_buscar_fabricacion.setPlaceholderText(QCoreApplication.translate("Form", u"Busca por lote de fabricaci\u00f3n", None))
        self.btn_ver_detalle_o_fab.setText(QCoreApplication.translate("Form", u"Ver", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("Form", u"Fabricaciones", None))
        self.btn_cerrar_det.setText(QCoreApplication.translate("Form", u"Salir", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_detalle), QCoreApplication.translate("Form", u"Detalle", None))
        self.lbl_fecha_fab.setText(QCoreApplication.translate("Form", u"Fecha", None))
        self.de_fecha_fab.setDisplayFormat(QCoreApplication.translate("Form", u"dd/MM/yyyy", None))
        self.lbl_produto_fab.setText(QCoreApplication.translate("Form", u"Producto", None))
        self.lbl_cantidad_fab.setText(QCoreApplication.translate("Form", u"Cantidad", None))
        self.lbl_equipo_fab.setText(QCoreApplication.translate("Form", u"Equipo", None))
        self.btn_mostrar_pesada.setText(QCoreApplication.translate("Form", u"Calcular", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Pesada", None))
        self.btn_confirmar_fab.setText(QCoreApplication.translate("Form", u"Confirmar", None))
        self.btn_cerrar_fab.setText(QCoreApplication.translate("Form", u"Salir", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fabricacion), QCoreApplication.translate("Form", u"Nueva fabricaci\u00f3n", None))
    # retranslateUi

