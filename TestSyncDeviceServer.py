"""Demo Tango Device Server"""

import logging
import time

from tango import DevState
from tango.server import Device, attribute


class TestSyncDeviceServer(Device):

    def init_device(self):
        super().init_device()
        self.value = 0.0
        self.set_state(DevState.ON)

    @attribute
    def test_attribute(self):
        logger.debug('entry')
        return self.value

    @test_attribute.write
    def write_test_attribute(self, value):
        self.value = value
        return True

def looping():
    logger.debug('loop')
    time.sleep(0.001)
    pass

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
    # TestSyncDeviceServer.run_server(event_loop=looping)
    TestSyncDeviceServer.run_server()
