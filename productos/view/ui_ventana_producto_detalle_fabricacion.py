# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ventana_producto_detalle_fabricacionbpSXFt.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

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
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_fecha_dof = QLabel(Form)
        self.lbl_fecha_dof.setObjectName(u"lbl_fecha_dof")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_fecha_dof)

        self.lbl_cosmtico_dof = QLabel(Form)
        self.lbl_cosmtico_dof.setObjectName(u"lbl_cosmtico_dof")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_cosmtico_dof)

        self.lbl_lote_dof = QLabel(Form)
        self.lbl_lote_dof.setObjectName(u"lbl_lote_dof")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lbl_lote_dof)

        self.lbl_caducidad_dof = QLabel(Form)
        self.lbl_caducidad_dof.setObjectName(u"lbl_caducidad_dof")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lbl_caducidad_dof)

        self.lbl_equipo_dof = QLabel(Form)
        self.lbl_equipo_dof.setObjectName(u"lbl_equipo_dof")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lbl_equipo_dof)

        self.le_fecha_dof = QLineEdit(Form)
        self.le_fecha_dof.setObjectName(u"le_fecha_dof")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_fecha_dof)

        self.le_cosmetico_dof = QLineEdit(Form)
        self.le_cosmetico_dof.setObjectName(u"le_cosmetico_dof")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_cosmetico_dof)

        self.le_lote_dof = QLineEdit(Form)
        self.le_lote_dof.setObjectName(u"le_lote_dof")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.le_lote_dof)

        self.le_cadudcidad_dof = QLineEdit(Form)
        self.le_cadudcidad_dof.setObjectName(u"le_cadudcidad_dof")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.le_cadudcidad_dof)

        self.le_equipo_dof = QLineEdit(Form)
        self.le_equipo_dof.setObjectName(u"le_equipo_dof")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.le_equipo_dof)

        self.lbl_cantidad_dof = QLabel(Form)
        self.lbl_cantidad_dof.setObjectName(u"lbl_cantidad_dof")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lbl_cantidad_dof)

        self.le_cantidad_dof = QLineEdit(Form)
        self.le_cantidad_dof.setObjectName(u"le_cantidad_dof")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_cantidad_dof)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tv_dof = QTableView(Form)
        self.tv_dof.setObjectName(u"tv_dof")
        self.tv_dof.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.tv_dof)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_imprimir_dof = QPushButton(Form)
        self.btn_imprimir_dof.setObjectName(u"btn_imprimir_dof")

        self.horizontalLayout_2.addWidget(self.btn_imprimir_dof)

        self.btn_salir_dof = QPushButton(Form)
        self.btn_salir_dof.setObjectName(u"btn_salir_dof")
        self.btn_salir_dof.setStyleSheet(u"background-color: rgb(22, 183, 40);")

        self.horizontalLayout_2.addWidget(self.btn_salir_dof)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 8)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Detalle Orden de Fabricaci\u00f3n", None))
        self.lbl_fecha_dof.setText(QCoreApplication.translate("Form", u"Fecha", None))
        self.lbl_cosmtico_dof.setText(QCoreApplication.translate("Form", u"Cosm\u00e9tico", None))
        self.lbl_lote_dof.setText(QCoreApplication.translate("Form", u"Lote", None))
        self.lbl_caducidad_dof.setText(QCoreApplication.translate("Form", u"Caducidad", None))
        self.lbl_equipo_dof.setText(QCoreApplication.translate("Form", u"Equipo", None))
        self.lbl_cantidad_dof.setText(QCoreApplication.translate("Form", u"Cantidad", None))
        self.btn_imprimir_dof.setText(QCoreApplication.translate("Form", u"Imprmir", None))
        self.btn_salir_dof.setText(QCoreApplication.translate("Form", u"Salir", None))
    # retranslateUi

