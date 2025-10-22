"""
Базовые тесты для quik_python (интеграция с UV)
Простые тесты без зависимости от pytest
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from quik_python.quik import Quik
from quik_python.data_structures.info_params import InfoParams


class QuikServiceTests:
    """Базовые тесты сервисных функций QUIK"""
    
    def __init__(self):
        self.quik = None
        self.test_results = {}
    
    async def setup(self):
        """Инициализация подключения к QUIK"""
        print("🔌 Инициализация подключения к QUIK...")
        try:
            self.quik = Quik()
            await self.quik.initialize()
            
            # Проверяем подключение
            is_connected = await self.quik.debug.is_quik()
            if not is_connected:
                print("⚠️  QUIK не подключен - некоторые тесты будут пропущены")
                return False
            
            print("✅ Подключение к QUIK успешно")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка подключения к QUIK: {e}")
            return False
    
    async def teardown(self):
        """Закрытие подключения"""
        if self.quik:
            try:
                self.quik.stop_service()
                print("🔌 Подключение к QUIK закрыто")
            except Exception as e:
                print(f"⚠️  Ошибка при закрытии подключения: {e}")
    
    def record_test_result(self, test_name: str, success: bool, message: str = ""):
        """Записывает результат теста"""
        self.test_results[test_name] = {
            'success': success,
            'message': message
        }
    
    async def test_is_connected(self):
        """Тест проверки подключения к QUIK"""
        test_name = "is_connected"
        try:
            result = await self.quik.service.is_connected()
            print(f"📡 IsConnected: {result}")
            self.record_test_result(test_name, True, f"Result: {result}")
            return True
        except Exception as e:
            print(f"❌ IsConnected failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    async def test_get_working_folder(self):
        """Тест получения рабочей папки QUIK"""
        test_name = "get_working_folder"
        try:
            result = await self.quik.service.get_working_folder()
            print(f"📁 WorkingFolder: {result}")
            assert isinstance(result, str) and len(result) > 0
            self.record_test_result(test_name, True, f"Path: {result}")
            return True
        except Exception as e:
            print(f"❌ GetWorkingFolder failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    async def test_get_script_path(self):
        """Тест получения пути к скрипту"""
        test_name = "get_script_path"
        try:
            result = await self.quik.service.get_script_path()
            print(f"📂 ScriptPath: {result}")
            self.record_test_result(test_name, True, f"Path: {result}")
            return True
        except Exception as e:
            print(f"❌ GetScriptPath failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    async def test_info_params(self):
        """Тест получения информационных параметров"""
        test_name = "info_params"
        try:
            # Тестируем ключевые параметры
            key_params = [InfoParams.VERSION, InfoParams.TRADEDATE]
            results = {}
            
            for param in key_params:
                try:
                    value = await self.quik.service.get_info_param(param)
                    results[param.name] = value
                    print(f"ℹ️  {param.name}: {value}")
                except Exception as param_error:
                    results[param.name] = f"Error: {param_error}"
                    print(f"⚠️  {param.name}: {param_error}")
            
            self.record_test_result(test_name, True, f"Params: {results}")
            return True
            
        except Exception as e:
            print(f"❌ InfoParams test failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    async def test_messages(self):
        """Тест отправки сообщений"""
        test_name = "messages"
        try:
            # Тестируем разные типы сообщений
            await self.quik.service.message("UV Test: Info message", 1)
            await self.quik.service.message("UV Test: Warning message", 2)
            await self.quik.service.message("UV Test: Error message", 3)
            
            print("📨 Все типы сообщений отправлены успешно")
            self.record_test_result(test_name, True, "All message types sent")
            return True
            
        except Exception as e:
            print(f"❌ Messages test failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    def test_enum_values(self):
        """Тест значений enum InfoParams"""
        test_name = "enum_values"
        try:
            # Проверяем основные значения enum
            assert InfoParams.VERSION.value == "VERSION"
            assert InfoParams.TRADEDATE.value == "TRADEDATE"
            
            all_params = list(InfoParams)
            print(f"🔢 InfoParams содержит {len(all_params)} параметров")
            
            # Показываем первые несколько параметров
            for param in all_params[:5]:
                print(f"   - {param.name}: {param.value}")
            
            self.record_test_result(test_name, True, f"Enum has {len(all_params)} params")
            return True
            
        except Exception as e:
            print(f"❌ Enum test failed: {e}")
            self.record_test_result(test_name, False, str(e))
            return False

    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 ЗАПУСК ТЕСТОВ QUIK-PYTHON (UV Integration)")
        print("=" * 60)
        
        # Синхронные тесты (не требуют QUIK)
        print("\n📋 Синхронные тесты:")
        self.test_enum_values()
        
        # Асинхронные тесты (требуют QUIK)
        connected = await self.setup()
        
        if connected:
            print("\n🔗 Тесты с подключением к QUIK:")
            await self.test_is_connected()
            await self.test_get_working_folder()
            await self.test_get_script_path()
            await self.test_info_params()
            await self.test_messages()
        else:
            print("\n⚠️  Тесты с подключением пропущены - QUIK недоступен")
        
        await self.teardown()
        
        # Результаты
        print("\n📊 РЕЗУЛЬТАТЫ ТЕСТОВ:")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results.values() if result['success'])
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} {test_name}: {result['message']}")
        
        print(f"\n🎯 Итого: {successful_tests}/{total_tests} тестов пройдено")
        
        if successful_tests == total_tests:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            return True
        else:
            print("⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
            return False


async def main():
    """Главная функция для запуска тестов"""
    tester = QuikServiceTests()
    success = await tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
