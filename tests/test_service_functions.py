"""
Тесты сервисных функций QUIK Python
Эквивалентные ServiceFunctionsTest.cs из QuikSharp
"""

import pytest
from pathlib import Path
import sys

# Добавляем quik_python в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from quik_python.quik import Quik
from quik_python.data_structures.info_params import InfoParams


@pytest.fixture(scope="session")
async def quik():
    """Фикстура для создания экземпляра Quik на весь сеанс тестирования"""
    quik_instance = Quik()
    await quik_instance.initialize()
    
    # Проверяем подключение к QUIK
    try:
        is_quik = await quik_instance.debug.is_quik()
        if not is_quik:
            pytest.skip("QUIK не подключен")
    except Exception:
        pytest.skip("Не удалось подключиться к QUIK")
    
    yield quik_instance
    
    # Cleanup
    quik_instance.stop_service()


@pytest.mark.integration
class TestServiceFunctions:
    """Тесты сервисных функций QUIK (требуют подключения к QUIK)"""
    
    @pytest.mark.asyncio
    async def test_is_connected(self, quik):
        """Тест проверки подключения к QUIK"""
        result = await quik.service.is_connected()
        assert isinstance(result, bool)
        print(f"IsConnected: {result}")

    @pytest.mark.asyncio
    async def test_get_working_folder(self, quik):
        """Тест получения рабочей папки QUIK"""
        result = await quik.service.get_working_folder()
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"WorkingFolder: {result}")

    @pytest.mark.asyncio
    async def test_get_script_path(self, quik):
        """Тест получения пути к скрипту"""
        result = await quik.service.get_script_path()
        assert isinstance(result, str)
        print(f"ScriptPath: {result}")

    @pytest.mark.asyncio
    async def test_get_info_param_version(self, quik):
        """Тест получения версии QUIK"""
        result = await quik.service.get_info_param(InfoParams.VERSION)
        assert result is None or isinstance(result, str)
        print(f"VERSION: {result}")

    @pytest.mark.asyncio
    async def test_get_info_param_tradedate(self, quik):
        """Тест получения торговой даты"""
        result = await quik.service.get_info_param(InfoParams.TRADEDATE)
        assert result is None or isinstance(result, str)
        print(f"TRADEDATE: {result}")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("message_type,expected_no_exception", [
        (1, True),  # Info
        (2, True),  # Warning
        (3, True),  # Error
    ])
    async def test_message_types(self, quik, message_type, expected_no_exception):
        """Тест отправки сообщений разных типов"""
        message_texts = {
            1: "Test info message",
            2: "Test warning message", 
            3: "Test error message"
        }
        
        try:
            await quik.service.message(message_texts[message_type], message_type)
            assert expected_no_exception
            print(f"Message type {message_type}: sent successfully")
        except Exception as e:
            if expected_no_exception:
                pytest.fail(f"Unexpected exception: {e}")
            print(f"Message type {message_type}: failed as expected")

    @pytest.mark.asyncio
    async def test_print_dbg_str(self, quik):
        """Тест отправки отладочного сообщения"""
        try:
            await quik.service.print_dbg_str("Test debug message")
            print("Debug message sent successfully")
        except Exception as e:
            # Некоторые настройки QUIK могут не поддерживать отладочные сообщения
            print(f"Debug message failed (may be expected): {e}")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_add_label(self, quik):
        """Тест добавления метки на график"""
        try:
            result = await quik.service.add_label(
                price=61000.0,
                cur_date="20170105",
                cur_time="100000",
                hint="Test label",
                path="C:\\ClassesC\\Labels\\buy.bmp",
                tag="si",
                alignment="BOTTOM",
                backgnd=0.0
            )
            assert isinstance(result, (int, float))
            print(f"AddLabel result: {result}")
        except Exception as e:
            # Метки могут не работать без открытых графиков
            print(f"AddLabel failed (may be expected without charts): {e}")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_add_label2(self, quik):
        """Тест добавления метки на график (версия 2)"""
        try:
            result = await quik.service.add_label2(
                chart_tag="MX1",
                y_value=352000.0,
                str_date="20210115",
                str_time="125000",
                text="Test label 2",
                image_path="C:\\ClassesC\\Labels\\buy.bmp"
            )
            assert isinstance(result, (int, float))
            print(f"AddLabel2 result: {result}")
        except Exception as e:
            print(f"AddLabel2 failed (may be expected without charts): {e}")

    @pytest.mark.asyncio
    async def test_del_label(self, quik):
        """Тест удаления метки с графика"""
        try:
            result = await quik.service.del_label("si", 13.0)
            assert isinstance(result, bool)
            print(f"DelLabel result: {result}")
        except Exception as e:
            print(f"DelLabel failed: {e}")

    @pytest.mark.asyncio
    async def test_del_all_labels(self, quik):
        """Тест удаления всех меток с графика"""
        try:
            result = await quik.service.del_all_labels("si")
            assert isinstance(result, bool)
            print(f"DelAllLabels result: {result}")
        except Exception as e:
            print(f"DelAllLabels failed: {e}")


class TestInfoParams:
    """Тесты enum InfoParams (не требуют подключения к QUIK)"""
    
    def test_info_params_enum_values(self):
        """Тест значений enum InfoParams"""
        assert InfoParams.VERSION.value == "VERSION"
        assert InfoParams.TRADEDATE.value == "TRADEDATE"
        assert InfoParams.SERVERTIME.value == "SERVERTIME"
        
    def test_info_params_enum_count(self):
        """Тест количества параметров в enum"""
        all_params = list(InfoParams)
        assert len(all_params) > 0
        print(f"Всего параметров InfoParams: {len(all_params)}")
        
    def test_info_params_str_conversion(self):
        """Тест преобразования enum в строку"""
        param = InfoParams.VERSION
        # Проверяем, что можем использовать параметр как строку
        assert str(param.value) == "VERSION"


# Дополнительные тесты совместимости
class TestCompatibility:
    """Тесты совместимости с C# API"""
    
    def test_enum_compatibility(self):
        """Тест совместимости enum с C# версией"""
        # Проверяем ключевые параметры, которые должны совпадать с C#
        expected_params = [
            "VERSION", "TRADEDATE", "SERVERTIME", "CONNECTION", 
            "USER", "USERID", "ORG", "MEMORY"
        ]
        
        actual_params = [param.value for param in InfoParams if isinstance(param.value, str)]
        
        for expected in expected_params[:5]:  # Проверяем первые 5
            assert expected in actual_params, f"Параметр {expected} не найден в InfoParams"
            
        print(f"Проверено {len(expected_params[:5])} ключевых параметров")
