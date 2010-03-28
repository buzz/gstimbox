"""gSTIMbox is a stimulator digital I/O box with USB 2.0
technology. The device supports 14 digital inputs and 16 digital
outputs. This module encapsulates proprietary Windows DLL calls that
control the device.

"""

from ctypes import *

class gSTIMbox:
    """Control a gSTIMbox device."""

    def __init__(self, port=1, callback=None):
        """Create a connection to the gSTIMbox.

        The serial port number defaults to 1. A callback function can
        be specified that handles signals from the input connectors.

        """
        self.input_callback = callback
        try:
            self.dll = cdll.LoadLibrary("gSTIMbox")
        except WindowsError:
            raise gSTIMboxError("Could not find gSTIMbox.dll. Exiting...")
        r = self.dll.gSTIMboxinit(port, None)
        if (r != None):
            self.device_handle = r
        else:
            raise gSTIMboxError("Could not connect to gSTIMbox.")

    def __del__(self):
        self.reset()
        self.close()

    def reset(self):
        """Reset device."""
        r = self.dll.gSTIMboxreset(self.device_handle)
        if (r != 1):
            raise gSTIMboxError("Could not disconnect from gSTIMbox.")

    def setMode(self, port, mode):
        """Set the operation mode of output ports.

        port is a list of port numbers to change (eg. [0, 2,
        3]). Valid port numbers are 0-15.

        modes is a list of modes for the ports defined in the port
        variable. A mode value can be either 0 (controlled manually,
        see portState()) or 1 (microprocessor controlled frequency,
        see setFrequency()).

        """
        num = len(port)
        if type(port) != list:
            raise TypeError("Argument port must be a list.")
        if type(mode) != list:
            raise TypeError("Argument mode must be a list.")
        if num != len(mode):
            raise ValueError(
                "Arguments port and mode must be of same length.")
        port_carr = (c_int * num)()
        mode_carr = (c_int * num)()
        for i in range(num):
            port_carr[i] = c_int(port[i])
            mode_carr[i] = c_int(mode[i])
        r = self.dll.gSTIMboxsetMode(
            self.device_handle, num, port_carr, mode_carr)
        if (r != 1):
            raise gSTIMboxError("Could not set modes on gSTIMbox.")

    def setPortState(self, state):
        """Set ON/OFF state for ports running in mode 0 (see
        setMode()).

        state is a list with a length of 16. Valid values for a state
        is an integer of either 0 or 1.

        eg. state = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        """
        if type(state) != list:
            raise TypeError("Argument state must be a list.")
        if len(state) != 16:
            raise TypeError("Argument state must be of length 16.")
        state_carr = (c_int * 16)()
        for i in range(16):
            state_carr[i] = c_int(state[i])
        r = self.dll.gSTIMboxsetPortState(self.device_handle, state_carr)
        if (r != 1):
            raise gSTIMboxError("Could not set port states on gSTIMbox.")

    def setFrequency(self, port, freq):
        """Set the frequencies for output ports.

        port - list of port numbers to change. Valid port numbers are
        0-15. (eg. [0, 6, 7])

        freq - list of frequencies which are to be assigned to the
        ports. Allowed values: 1-50. The function rounds these
        frequencies to one digit after the comma. The length of freq
        must equal the length of port list. (eg. [1, 2.7, 5.8])

        """
        num = len(port)
        if type(port) != list:
            raise TypeError("Argument port must be a list.")
        if type(freq) != list:
            raise TypeError("Argument freq must be a list.")
        if num != len(freq):
            raise ValueError(
                "Arguments port and freq must be of same length.")
        port_carr = (c_int * num)()
        freq_carr = (c_double * num)()
        for i in range(num):
            port_carr[i] = c_int(port[i])
            freq_carr[i] = c_double(freq[i])
        r = self.dll.gSTIMboxsetFrequency(
            self.device_handle, num, port_carr, freq_carr)
        if (r != 1):
            raise gSTIMboxError("Could not set frequencies on gSTIMbox.")

    def close(self):
        """Close device connection."""
        r = self.dll.gSTIMboxclose(self.device_handle)
        if (r != 1):
            raise gSTIMboxError("Could not disconnect from gSTIMbox.")

    def getHWVersion(self):
        """Returns firmware version."""
        fun = self.dll.gSTIMboxgetHWVersion
        fun.restype = c_double
        return fun()

    def getDriverVersion(self):
        """Returns API library version."""
        fun = self.dll.gSTIMboxgetDriverVersion
        fun.restype = c_double
        return fun()


class gSTIMboxError(Exception):
    """gSTIMbox device communication error."""
    pass
