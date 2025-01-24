from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QLineEdit


def set_validar_letras(line_edit):
    # Limitar la entrada de números en el lineEdit
    regex = QRegularExpression("^[A-Za-z ]*$")  # Solo letras y espacios
    validator = QRegularExpressionValidator(regex, line_edit)
    line_edit.setValidator(validator)


def set_validar_numeros(line_edit):
    # Limitar la entrada de letras en el lineEdit
    regex = QRegularExpression("^[0-9]*([.,][0-9]+)?$")
    validator = QRegularExpressionValidator(regex, line_edit)
    line_edit.setValidator(validator)


def set_validar_telefono(line_edit):
    # Limitar la entrada a solo números y algunos caracteres permitidos para teléfonos
    # Permitir dígitos, espacios, paréntesis, + y -
    regex = QRegularExpression("^[0-9 ()+-]*$")
    validator = QRegularExpressionValidator(regex, line_edit)
    line_edit.setValidator(validator)


def set_validar_cantidad(line_edit):
    # Limitar la entrada de letras en el lineEdit
    regex = QRegularExpression("^[0-9]*$")
    validator = QRegularExpressionValidator(regex, line_edit)
    line_edit.setValidator(validator)
