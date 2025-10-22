"""
Label class - параметры метки графика
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .base import BaseDataStructure


class LabelAlignment(Enum):
    """Расположение картинки относительно точки"""
    LEFT = "LEFT"

    RIGHT = "RIGHT"

    TOP = "TOP"

    BOTTOM = "BOTTOM"


@dataclass
class Label(BaseDataStructure):
    """
    Формат таблицы с параметрами метки (получаемая при помощи GetLabelParams)
    
    Наименование параметров метки в возвращаемой таблице указаны в нижнем регистре,
    и все значения имеют тип STRING.
    
    Используется для работы с метками на графиках в QUIK.
    """
    
    # Значение параметра на оси Y, к которому будет привязана метка
    yvalue: Optional[str] = None
    
    # Дата в формате «ГГГГММДД», к которой привязана метка
    date: Optional[str] = None
    
    # Время в формате «ЧЧММСС», к которому будет привязана метка
    time: Optional[str] = None
    
    # Подпись метки (если подпись не требуется, то пустая строка)
    # Хотя бы один из параметров text или image_path должен быть задан
    text: Optional[str] = None
    
    # Путь к картинке, которая будет отображаться в качестве метки
    # Используются картинки формата *.bmp, *.jpeg
    # Хотя бы один из параметров text или image_path должен быть задан
    image_path: Optional[str] = None
    
    # Расположение картинки относительно точки
    # Возможные значения: LEFT, RIGHT, TOP, BOTTOM (по умолчанию LEFT)
    alignment: Optional[str] = None
    
    # Текст всплывающей подсказки
    hint: Optional[str] = None
    
    # Красная компонента цвета в формате RGB [0;255]
    r: Optional[str] = None
    
    # Зеленая компонента цвета в формате RGB [0;255]
    g: Optional[str] = None
    
    # Синяя компонента цвета в формате RGB [0;255]
    b: Optional[str] = None
    
    # Прозрачность метки (картинки) в процентах [0;100]
    transparency: Optional[str] = None
    
    # Прозрачность фона картинки (0 - отключена, 1 - включена)
    transparent_background: Optional[str] = None
    
    # Название шрифта (по умолчанию "Arial")
    font_face_name: Optional[str] = None
    
    # Размер шрифта (по умолчанию 12)
    font_height: Optional[str] = None

    def __post_init__(self):
        """Инициализация значений по умолчанию"""
        # Установка значений по умолчанию
        if self.alignment is None:
            self.alignment = "LEFT"
        if self.r is None:
            self.r = "0"
        if self.g is None:
            self.g = "0"
        if self.b is None:
            self.b = "0"
        if self.transparency is None:
            self.transparency = "0"
        if self.transparent_background is None:
            self.transparent_background = "0"
        if self.font_height is None:
            self.font_height = "0"

