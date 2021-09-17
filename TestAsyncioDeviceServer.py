"""Demo Tango Device Server using asyncio green mode"""

import logging
import asyncio
import time
from asyncio import InvalidStateError

from tango import DevState, GreenMode
from tango.server import Device, command, attribute


def entryexit(f):
    def wrapper():
        logger.debug('entry %s', f)
        t0 = time.time()
        f()
        dt = (time.time() - t0) * 1000.0
        logger.debug('exit %s %6.3f ms', f, dt)

    return wrapper


class TestAsyncioDeviceServer(Device):
    green_mode = GreenMode.Asyncio

    async def init_device(self):
        await super().init_device()
        self.value = time.time()
        self._lock = asyncio.Lock()
        self.set_state(DevState.ON)

    @command
    async def long_running_command(self):
        self.set_state(DevState.OPEN)
        await asyncio.sleep(2)
        self.set_state(DevState.CLOSE)

    @command
    async def background_task_command(self):
        loop = asyncio.get_event_loop()
        future = loop.create_task(self.coroutine_target())

    async def coroutine_target(self):
        self.set_state(DevState.INSERT)
        await asyncio.sleep(3)
        self.set_state(DevState.EXTRACT)

    @attribute(green_mode=GreenMode.Asyncio, read_green_mode=GreenMode.Asyncio, write_green_mode=GreenMode.Asyncio)
    async def test_attribute(self):
        #logger.debug('entry')
        #await asyncio.sleep(0.1)
        #logger.debug('exit')
        return self.value

    @test_attribute.write
    async def write_test_attribute(self, value):
        #logger.debug('entry')
        self.value = value
        # await asyncio.sleep(0.2)
        #logger.debug('exit')
        return True

    @attribute
    async def test_attribute_2(self):
        logger.debug('entry')
        await asyncio.sleep(0)
        logger.debug('exit')
        return self.value

    @test_attribute_2.write
    async def write_test_attribute_2(self, value):
        logger.debug('entry')
        self.value = value
        await asyncio.sleep(0)
        logger.debug('exit')
        return True


async def loop_tasks(delay=0.0, verbose=False, threshold=-1, delta=True, exc=False, stack=True, no_self=True):
    tasks = {}
    n0 = 0
    while True:
        last_tasks = tasks
        n1 = n0
        tasks = asyncio.all_tasks()
        if no_self:
            try:
                tasks.discard(TestAsyncioDeviceServer.loop_task)
            except:
                pass
        n0 = len(tasks)
        delta_flag = False
        if delta:
            for task in last_tasks:
                if task not in tasks:
                    delta_flag = True
            for task in tasks:
                if task not in last_tasks:
                    delta_flag = True
        if n0 > threshold or delta_flag or verbose:
            logger.debug("********************  Tasks in loop: %s (%s)", n0, n1)
            if delta_flag:
                for task in last_tasks:
                    if task not in tasks:
                        logger.debug(' - %s %s', id(task), task)
                    if exc:
                        try:
                            ex = task.exception()
                            if ex is not None:
                                raise ex
                        except InvalidStateError:
                            # task is not done yet
                            pass
                        except:
                            logger.debug("Exception in the task", exc_info=True)
            for task in tasks:
                if task not in last_tasks:
                    if delta_flag:
                        logger.debug(' + %s %s', id(task), task)
                        if stack:
                            logger.debug(str(task.get_stack()))
                    elif verbose:
                        logger.debug("   %s %s", id(task), task)
                elif verbose:
                    logger.debug("   %s %s", id(task), task)
            logger.debug("********************\n")
        await asyncio.sleep(delay)



if __name__ == '__main__':
    # configure logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    f_str = '%(asctime)s,%(msecs)3d %(levelname)-7s [%(process)d:%(thread)d] %(filename)s ' \
            '%(funcName)s(%(lineno)s) %(message)s'
    log_formatter = logging.Formatter(f_str, datefmt='%H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.debug('Start')
    # run server
    TestAsyncioDeviceServer.run_server()
