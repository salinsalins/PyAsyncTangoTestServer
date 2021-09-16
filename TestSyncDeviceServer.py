"""Demo Tango Device Server using asyncio green mode"""

import logging
import asyncio
import time
from asyncio import InvalidStateError

from tango import DevState, GreenMode
from tango.server import Device, command, attribute


class TestSyncDeviceServer(Device):

    def init_device(self):
        super().init_device()
        self.value = 0.0
        self.set_state(DevState.ON)

    @attribute
    def test_attribute(self):
        return self.value

    @test_attribute.write
    def write_test_attribute(self, value):
        self.value = value
        return True


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

    # run server
    TestSyncDeviceServer.run_server()
