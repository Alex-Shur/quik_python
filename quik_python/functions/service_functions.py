"""
Service functions for QUIK interaction
"""

from typing import Optional, Union
from .base_functions import BaseFunctions
from ..data_structures.info_params import InfoParams


class ServiceFunctions(BaseFunctions):
    """
    Сервисные функции для взаимодействия с QUIK
    """

    async def get_working_folder(self) -> str:
        """
        Функция возвращает путь, по которому находится файл info.exe, исполняющий данный скрипт, без завершающего обратного слэша («\\»). Например, C:\\QuikFront.

        Returns:
            Путь к рабочей папке
        """
        result = await self.call_function("getWorkingFolder")
        return result['data'] or ""

    async def is_connected(self) -> bool:
        """
        Функция предназначена для определения состояния подключения клиентского места к серверу.

        Returns:
            True если подключен, False иначе
        """
        result = await self.call_function("isConnected")
        return bool(result['data'])

    async def get_script_path(self) -> str:
        """
        Функция возвращает путь, по которому находится запускаемый скрипт, без завершающего обратного слэша («\\»). Например, C:\\QuikFront\\Scripts

        Returns:
            Путь к скрипту
        """
        result = await self.call_function("getScriptPath")
        return result['data'] or ""

    async def get_info_param(self, param_name: Union[str, InfoParams]) -> Optional[str]:
        """
        Функция возвращает значения параметров информационного окна (пункт меню Связь / Информационное окно…).

        Args:
            param_name: Имя параметра (строка или InfoParams enum)

        Returns:
            Значение параметра
        """
        # Преобразуем enum в строку, если передан enum
        param_str = str(param_name) if isinstance(param_name, InfoParams) else param_name
        result = await self.call_function("getInfoParam", param_str)
        return result['data']

    async def message(self, text: str, icon_type: int = 1) -> None:
        """
        Функция отображает сообщения в терминале QUIK.

        Args:
            text: Текст сообщения
            icon_type: Тип иконки (1 - Info, 2 - Warning, 3 - Error)
        """
        if icon_type == 1:
            await self.call_function("message", text)
        elif icon_type == 2:
            await self.call_function("warning_message", text)
        elif icon_type == 3:
            await self.call_function("error_message", text)
        else:
            raise ValueError("Invalid icon type. Use 1 for Info, 2 for Warning, or 3 for Error.")


    async def print_dbg_str(self, message: str) -> None:
        """
        Функция выводит отладочное сообщение в терминал QUIK.

        Args:
            message: Текст сообщения
        """
        await self.call_function("printDbgStr", message)
        

    async def add_label(self, price: float, cur_date: str, cur_time: str, hint: str, path: str, tag: str, alignment: str, backgnd: float) -> float:
        """Добавить метку на график.

        Args:
            price (float): Цена метки.
            cur_date (str): Текущая дата.
            cur_time (str): Текущее время.
            hint (str): Подсказка для метки.
            path (str): Путь к изображению метки.
            tag (str): Тег метки.
            alignment (str): Выравнивание метки.  LEFT, RIGHT, TOP, BOTTOM
            backgnd (float): Фоновый цвет метки.  On =1, Off=0

        Returns:
            float: Идентификатор метки.
        """
        result = await self.call_function("addLabel", price, cur_date, cur_time, hint, path, tag, alignment, backgnd)
        return result['data'] or 0.0


    async def add_label2(self, chart_tag: str, y_value: float, str_date: str, str_time: str, text: str = "", image_path: str = "", alignment: str = "", hint: str = "",
                           r: int = -1, g: int = -1, b: int = -1, transparency: int = -1, tran_backgrnd: int = -1, font_name: str = "", font_height: int = -1) -> float:
        """Добавить метку на график (версия 2).

        Args:
            chart_tag (str): Тег графика.
            y_value (float): Значение по оси Y.
            str_date (str): Дата в строковом формате.
            str_time (str): Время в строковом формате.
            text (str, optional): Текст метки. Defaults to "".
            image_path (str, optional): Путь к изображению метки. Defaults to "".
            alignment (str, optional): Выравнивание метки. Defaults to "".
            hint (str, optional): Подсказка для метки. Defaults to "".
            r (int, optional): Красный цвет. Defaults to -1.
            g (int, optional): Зеленый цвет. Defaults to -1.
            b (int, optional): Синий цвет. Defaults to -1.
            transparency (int, optional): Прозрачность. Defaults to -1.
            tran_backgrnd (int, optional): Фоновый цвет. Defaults to -1.
            font_name (str, optional): Название шрифта. Defaults to "".
            font_height (int, optional): Высота шрифта. Defaults to -1.

        Returns:
            float: Идентификатор метки.
        """
        result = await self.call_function("addLabel2", chart_tag, y_value, str_date, str_time, text, image_path, alignment, hint,
                                           r, g, b, transparency, tran_backgrnd, font_name, font_height)
        return result['data'] or 0.0


    async def set_label_params(self, chart_tag: str, label_id: int, y_value: float, str_date: str, str_time: str, text: str = "", image_path: str = "", alignment: str = "", hint: str = "",
                                r: int = -1, g: int = -1, b: int = -1, transparency: int = -1, tran_backgrnd: int = -1, font_name: str = "", font_height: int = -1) -> bool:
        """Установить параметры метки на графике.

        Args:
            chart_tag (str): Тег графика.
            label_id (int): Идентификатор метки.
            y_value (float): Значение по оси Y.
            str_date (str): Дата в строковом формате.
            str_time (str): Время в строковом формате.
            text (str, optional): Текст метки. Defaults to "".
            image_path (str, optional): Путь к изображению метки. Defaults to "".
            alignment (str, optional): Выравнивание метки. Defaults to "".
            hint (str, optional): Подсказка для метки. Defaults to "".
            r (int, optional): Красный цвет. Defaults to -1.
            g (int, optional): Зеленый цвет. Defaults to -1.
            b (int, optional): Синий цвет. Defaults to -1.
            transparency (int, optional): Прозрачность. Defaults to -1.
            tran_backgrnd (int, optional): Фоновый цвет. Defaults to -1.
            font_name (str, optional): Название шрифта. Defaults to "".
            font_height (int, optional): Высота шрифта. Defaults to -1.

        Returns:
            bool: Успешность операции.
        """
        result = await self.call_function("setLabelParams", chart_tag, label_id, y_value, str_date, str_time, text, image_path, alignment, hint,
                                            r, g, b, transparency, tran_backgrnd, font_name, font_height)
        return result['data'] or False


    async def get_label_params(self, chart_tag: str, label_id: int) -> dict:
        """Получить параметры метки на графике.

        Args:
            chart_tag (str): Тег графика.
            label_id (int): Идентификатор метки.

        Returns:
            dict: Параметры метки.
        """
        result = await self.call_function("getLabelParams", chart_tag, label_id)
        return result['data'] or {}


    async def del_label(self, tag: str, id: float) -> bool:
        """Удалить метку с графика.

        Args:
            tag (str): Тег графика.
            id (float): Идентификатор метки.

        Returns:
            bool: Успешность операции.
        """
        result = await self.call_function("delLabel", tag, id)
        return result['data'] or False


    async def del_all_labels(self, tag: str) -> bool:
        """Удалить все метки с графика.

        Args:
            tag (str): Тег графика.

        Returns:
            bool: Успешность операции.
        """
        result = await self.call_function("delAllLabels", tag)
        return result['data'] or False


    # def initialize_correlation_id(self, start_correlation_id: int) -> None:
    #     """Инициализировать идентификатор корреляции.

    #     Args:
    #         start_correlation_id (int): Начальный идентификатор корреляции.
    #     """
    #     self.service.initialize_correlation_id(start_correlation_id)
    

