"""gSTIMbox module demo."""

from sys import stdout, argv
from time import sleep
from gstimbox import *

def main():
    comport = 1
    argnum = len(argv)
    if argnum != 2:
        print "usage: %s COM_PORT" % argv[0]
        print "eg. %s 3" % argv[0]
        exit(-1)
    else:
        comport = int(argv[1])
    b = gSTIMbox(comport)
    print "Connected to gSTIMbox (serial port %d)" % comport
    print "Driver version %s, firmware version %s" % \
        (b.getDriverVersion(), b.getHWVersion())

    print "Micro-controller frequency demo running..."
    stdout.flush()
    port = [0, 1, 2, 3, 4, 5, 6, 7]
    freq = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    mode = [1, 1, 1, 1, 1, 1, 1, 1]
    b.reset()
    b.setFrequency(port, freq)
    b.setMode(port, mode)
    sleep(10)
    b.reset()
    print "Manual ON/OFF demo running..."
    stdout.flush()
    state = [0 for i in range(16)]
    for i in range(10):
        for j in range(8):
            state[j] = 1
            b.setPortState(state)
            sleep(0.1)
        for j in range(8):
            state[j] = 0
            b.setPortState(state)
            sleep(0.1)
    b.reset()
    print "Demos finished."

if __name__ == "__main__":
    main()
