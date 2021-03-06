
from __future__ import print_function

import os
import sys
import signal
import threading
import pyuv

if sys.version_info >= (3, 0):
    LINESEP = os.linesep.encode()
else:
    LINESEP = os.linesep

def on_read(handle, ip_port, data, error):
    data = data.strip()
    if data:
        ip, port = ip_port
        handle.send((ip, port), data+LINESEP)

def async_exit(async):
    async.close()
    signal_h.close()
    server.close()

def signal_cb(handle, signum):
    async.send()


print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()
async = pyuv.Async(loop, async_exit)

server = pyuv.UDP(loop)
server.bind(("0.0.0.0", 1234))
server.start_recv(on_read)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

t = threading.Thread(target=loop.run)
t.start()
t.join()

print("Stopped!")

