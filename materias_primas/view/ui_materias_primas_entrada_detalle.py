# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'materias_primas_entrada_detallecfbvBP.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QDateTimeEdit, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(595, 112)
        Form.setStyleSheet(u"QPushButton{background-color: rgb(6, 191, 249);}\n"
"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_fecha_cad_de = QLabel(Form)
        self.lbl_fecha_cad_de.setObjectName(u"lbl_fecha_cad_de")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_fecha_cad_de)

        self.lbl_cantidad_de = QLabel(Form)
        self.lbl_cantidad_de.setObjectName(u"lbl_cantidad_de")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_cantidad_de)

        self.le_cantidad_de = QLineEdit(Form)
        self.le_cantidad_de.setObjectName(u"le_cantidad_de")
        self.le_cantidad_de.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.le_cantidad_de.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_cantidad_de)

        self.de_fecha_cad_de = QDateEdit(Form)
        self.de_fecha_cad_de.setObjectName(u"de_fecha_cad_de")
        self.de_fecha_cad_de.setInputMethodHints(Qt.InputMethodHint.ImhDate)
        self.de_fecha_cad_de.setCurrentSection(QDateTimeEdit.Section.DaySection)
        self.de_fecha_cad_de.setCalendarPopup(True)
        self.de_fecha_cad_de.setDate(QDate(2025, 1, 1))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.de_fecha_cad_de)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_salir_de = QPushButton(Form)
        self.btn_salir_de.setObjectName(u"btn_salir_de")

        self.horizontalLayout.addWidget(self.btn_salir_de)

        self.btn_guardar_de = QPushButton(Form)
        self.btn_guardar_de.setObjectName(u"btn_guardar_de")

        self.horizontalLayout.addWidget(self.btn_guardar_de)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Materias Primas", None))
        self.lbl_fecha_cad_de.setText(QCoreApplication.translate("Form", u"Fecha caducidad", None))
        self.lbl_cantidad_de.setText(QCoreApplication.translate("Form", u"Cantidad", None))
        self.de_fecha_cad_de.setDisplayFormat(QCoreApplication.translate("Form", u"d/M/yyyy", None))
        self.btn_salir_de.setText(QCoreApplication.translate("Form", u"Salir", None))
        self.btn_guardar_de.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

