"""
A device driver implementation for the CETONI mobile dosage unit

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 18.05.2022
"""

import asyncio
import logging
import time
from queue import Queue
from typing import Any, AsyncGenerator, Coroutine, Generator, Tuple, Union

from .abc import BatteryInterface, BatteryReplacementFailed

try:
    import coloredlogs
except (ModuleNotFoundError, ImportError):
    pass

from threading import Event, Thread

logger = logging.getLogger(__name__)


def _ipc(message: Union[str, bytes]) -> Generator[str, None, None]:
    """
    Handles the IPC to the firmware of the mob dos

        :param message: The message to send to the firmware

        :return: A generator with the received message(s) from the firmware
    """

    async def async_ipc() -> AsyncGenerator[str, None]:
        """
        The asynchronous IPC part

            :returns: A generator with the received messages
        """
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

            logger.debug(f"Send: {message!r}")
            writer.write(message if isinstance(message, bytes) else message.encode())

            while True:
                data = await reader.read(100)
                if data == b"":
                    break
                logger.debug(f"Received: {data.decode()!r}")
                yield data.decode()

            logger.debug("Closing connection")
            writer.close()
        except (ConnectionRefusedError, ConnectionResetError) as err:
            logger.error(err)

    def sync_generator(async_gen: AsyncGenerator[Any, None]) -> Generator[Any, None, None]:
        """
        Creates a synchronous generator from an async generator

        Adapted from https://stackoverflow.com/a/63595496 and https://stackoverflow.com/a/41901796 (for the part with
        the additional thread that executes the async event loop in case this function is called from a non-main thread)

            :param async_gen: The async generator to convert
        """

        def iter_over_async(async_gen: AsyncGenerator[Any, None]) -> Generator[Any, None, None]:
            """
            Iterates over the async generator `async_gen` and yields the values in a synchronous manner

                :param async_gen: The async generator to iterate over

                :return: A synchronous generator with the values from the `async_gen`
            """

            ait = async_gen.__aiter__()

            async def get_next():
                try:
                    obj = await ait.__anext__()
                    return False, obj
                except StopAsyncIteration:
                    return True, None

            sentinel = object()
            queue = Queue()

            def thread_entry_point():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                while True:
                    done, obj = loop.run_until_complete(get_next())
                    if done:
                        break
                    try:
                        queue.put(obj)
                    except Exception as e:
                        queue.put((sentinel, e))
                        break
                loop.close()
                queue.put(sentinel)

            Thread(target=thread_entry_point, name="async_iter_thread").start()
            while True:
                val = queue.get()
                if val is sentinel:
                    return
                if isinstance(val, tuple) and len(val) == 2 and val[0] is sentinel:
                    raise val[1]
                yield val

        return iter_over_async(async_gen)

    yield from sync_generator(async_ipc())


class MobDosBattery(BatteryInterface):
    """
    Adaptor class that talks to the firmware of the mob dos and provides the battery specific values
    """

    __stop_event: Event
    __ipc_polling_thread: Thread

    __POLLING_TIMEOUT: float = 0.5  #: seconds

    def __init__(self):
        super().__init__()

        self.__stop_event = Event()

        def poll(stop_event: Event):
            while not stop_event.is_set():
                try:
                    # time.sleep(self.__POLLING_TIMEOUT)
                    self._is_connected = eval(next(_ipc("BAT_CONN")))
                    logger.debug(f"bat connected {self._is_connected}")
                    self._is_secondary_source_connected = eval(next(_ipc("EXT_CONN")))
                    logger.debug(f"ext connected {self._is_secondary_source_connected}")
                    self._voltage = float(next(_ipc("BAT_VOLTAGE")))
                    logger.debug(f"voltage {self._voltage}")
                    self._temperature = float(next(_ipc("BAT_TEMP")))
                    logger.debug(f"temp {self._temperature}")
                    self._locking_pin_state = next(_ipc("LP_POS"))
                    logger.debug(f"pin state {self._locking_pin_state}")
                except StopIteration:
                    logger.info(f"stop iteration, {stop_event.is_set()}")
                    pass

        self.__ipc_polling_thread = Thread(target=poll, name="ipc_polling_thread", args=(self.__stop_event,))
        self.__ipc_polling_thread.start()

    def replace_battery(self) -> Generator[Tuple[int, str, bool], None, None]:
        for message in _ipc("REPLACE_BAT"):
            progress, status = message.split(":")
            if progress == "Error":
                yield (100, status, True)
            else:
                yield (int(progress), status, False)

    def stop(self):
        self.__stop_event.set()
        self.__ipc_polling_thread.join()


if __name__ == "__main__":
    logging_level = logging.INFO
    LOGGING_FORMAT = "%(asctime)s [%(threadName)-12.12s] %(levelname)-8s| %(name)s %(module)s.%(funcName)s: %(message)s"
    try:
        coloredlogs.install(fmt=LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S,%f", level=logging_level)
    except NameError:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging_level)

    battery_driver = MobDosBattery()
    for _ in battery_driver.replace_battery():
        pass
    battery_driver.stop()
