"""
Example usage of QuikPython API
"""

import logging
import asyncio
from quik_python import Quik, LuaException
from quik_python.data_structures import CandleInterval, Candle, InfoParams

CLASS_CODE = "TQBR"   
# CLASS_CODE = "QJSIM"  ## for Demo Quik Junior Connection


async def main():
    """
    Пример использования QuikPython API
    """
    
    # Создаем подключение к QUIK
    # async with Quik(host="192.168.10.128") as quik:
    async with Quik(host="localhost") as quik:
        try:
            await quik.initialize()
            # Работа с QUIK
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return

        try:
            # Проверяем подключение
            if not quik.is_service_alive():
                print("Не удалось подключиться к QUIK")
                return

            if not await quik.service.is_connected():
                print("Quik не подключен к торгам")


            print("Подключение к QUIK успешно!")

            await test_candle(quik=quik)



        except LuaException as e:
            print(f"QUIK Lua error: {e}")
        except Exception as e:
            print(f"Error: {e}")



### test candle
async def test_candle(quik:Quik):
    received_candles = []
    
    def on_new_candle(candle: Candle):
        """Callback for new candle events"""
        if (candle.sec_code == "SBER" and candle.interval == CandleInterval.M1):
            print(f"New candle - Sec:{candle.sec_code}, Open:{candle.open}, "
                  f"Close:{candle.close}, Volume:{candle.volume}")
            received_candles.append(candle)

    try:
        # Проверяем подключение
        if not await quik.service.is_connected():
            print("QUIK не подключен к торгам")
            return
        
        print("QUIK service is connected")

        v = await quik.candles.get_last_candles(CLASS_CODE, "SBER", CandleInterval.M1, 10)
        print(f"Last candles: {v}")


        # Subscribe to new candle events
        quik.candles.add_new_candle_handler(on_new_candle)
        
        # Check if already subscribed and unsubscribe if needed
        is_subscribed = await quik.candles.is_subscribed(CLASS_CODE, "SBER", CandleInterval.M1)
        print(f"Is subscribed: {is_subscribed}")
        if is_subscribed:
            await quik.candles.unsubscribe(CLASS_CODE, "SBER", CandleInterval.M1)

        # Subscribe to minute candles
        await quik.candles.subscribe(CLASS_CODE, "SBER", CandleInterval.M1)

        # Verify subscribed
        is_subscribed = await quik.candles.is_subscribed(CLASS_CODE, "SBER", CandleInterval.M1)
        print(f"Is subscribed: {is_subscribed}")
        
        # Wait a bit for potential candles (but don't wait too long in tests)
        await asyncio.sleep(120) ## wait 180sec
        
        # Unsubscribe
        await quik.candles.unsubscribe(CLASS_CODE, "SBER", CandleInterval.M1)

        print(f"Received {len(received_candles)} candles during test")

    except Exception as e:
        print(f"Candle test error: {e}")


if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
        level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
        datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
    )

    
    print("QuikPython API Example")
    print("===========================")
    

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Main example error: {e}")
