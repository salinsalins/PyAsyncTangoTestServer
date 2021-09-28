# coding: utf-8
import time

import tango
from matplotlib import pyplot as plt
import numpy as np

d_name = 'binp/nbi/asyncio01'
d_name = 'binp/test/sync01'
d_name = 'sys/tg_test/1'
d_proxy = tango.DeviceProxy(d_name)
ping1 = d_proxy.ping()
print(d_name, 'ping', ping1, 's')
a_name = 'test_attribute'
a_name = 'state'
a_name = 'double_scalar'
print(' ')

N = 200000
y = np.zeros(N)
n = 1
t = 0.0
n1 = 1
t1 = 0.0
tmin = 1e60
tmax = -1.0

for i in range(N):
    t0 = time.perf_counter()
    a = d_proxy.read_attribute(a_name)
    # a = 10**100
    dt = (time.perf_counter() - t0) * 1000.0
    v = a.value
    # v = a / 1e100
    y[i] = dt
    t += dt
    n += 1
    ar = t/n
    t1 += dt
    n1 += 1
    ar1 = t1/n1
    tmin = min(tmin, dt)
    tmax = max(tmax, dt)
    print('\rRead: %s/%s = %19.14f; %9.6fms; avg=%6.3fms; avg5=%6.3fms; min=%9.6fms; max=%6.3fms %d'
          % (d_name, a_name, v, dt, ar, ar1, tmin, tmax, n), end='')
    # if dt > 3.0 * ar:
    #     print('\nLong reading', ar, dt)
    if t1 > 5000.0:
        t1 = 0.0
        n1 = 0.0

# plot data
x = np.arange(N)
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set(xlabel='N', ylabel='time (ms)',
       title='About as simple as it gets, folks')
ax.grid()
fig.savefig("test.png")
plt.show()

# the histogram of the data
num_bins = 500
fig, ax = plt.subplots()
n, bins, patches = ax.hist(y, num_bins, density=True)
# # add a 'best fit' line
# z = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
#      np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
# ax.plot(bins, y, '--')
ax.set_xlabel('Smarts')
ax.set_ylabel('Probability density')
ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
