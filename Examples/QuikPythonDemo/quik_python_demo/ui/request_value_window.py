"""
Окно для запроса значений - порт FormRequestValue.cs на Python Qt6
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'quik_python'))

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, 
    QDialogButtonBox
)



class RequestValueWindow(QDialog):
    """
    Диалоговое окно для запроса значений от пользователя
    """

    def __init__(self, title: str = "Запрос значения", label_text: str = "Введите значение:", parent=None):
        super().__init__(parent)
        self.requested_value = ""
        self.init_ui(title, label_text)

    def init_ui(self, title: str, label_text: str):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 120)
        
        # Основной layout
        layout = QVBoxLayout(self)
        
        # Метка
        self.label = QLabel(label_text)
        layout.addWidget(self.label)
        
        # Поле ввода
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Фокус на поле ввода
        self.line_edit.setFocus()

    def get_value(self) -> str:
        """Получить введенное значение"""
        return self.line_edit.text()

    def set_value(self, value: str):
        """Установить значение в поле ввода"""
        self.line_edit.setText(value)

    @staticmethod
    def get_text(parent=None, title: str = "Запрос значения", 
                 label_text: str = "Введите значение:", 
                 default_value: str = "") -> tuple:
        """
        Статический метод для быстрого получения текста от пользователя
        
        Returns:
            tuple: (text, ok) где text - введенный текст, ok - True если нажата OK
        """
        dialog = RequestValueWindow(title, label_text, parent)
        dialog.set_value(default_value)
        
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            return dialog.get_value(), True
        else:
            return "", False
