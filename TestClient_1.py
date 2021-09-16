# coding: utf-8
import time

import tango

d_name = 'binp/nbi/asyncio01'
d_name = 'binp/test/sync01'
# d_name = 'sys/tg_test/1'
d_proxy = tango.DeviceProxy(d_name)
ping1 = d_proxy.ping()
print(d_name, 'ping', ping1, 's')
a_name = 'test_attribute'
# a_name = 'state'
# a_name = 'double_scalar'
print(' ')

n = 1
t = 0.0
n1 = 1
t1 = 0.0
for i in range(200000):
    t0 = time.time()
    v = d_proxy.read_attribute(a_name)
    dt = (time.time() - t0) * 1000.0
    t += dt
    n += 1
    ar = t/n
    t1 += dt
    n1 += 1
    ar1 = t1/n1
    # print('Reading', d_name, a_name, v.value, int(dt), 'ms')
    print('\rRead: %s/%s = %s; %6.3fms; avg=%6.3fms; avg5=%6.3fms %d' % (d_name, a_name, v.value, dt, ar, ar1, n), end='')
    # if dt > 3.0 * ar:
    #     print('\nLong reading', ar, dt)
    if t1 > 5000.0:
        t1 = 0.0
        n1 = 0.0


