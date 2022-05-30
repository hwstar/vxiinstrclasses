from  vxiinstrclasses.instrument import *

class mso5000(instrument):
    """This class controls a RIGOL MSO5000 Scope"""
    def __init__(self, resourcehost):

        instrument.__init__(self, resourcehost)

        iid = self.identify()
        if not iid.startswith('RIGOL TECHNOLOGIES,MSO50'):
            raise InstrumentError("Instrument Manufacturer/Model Number Mismatch, "+iid)

    def lock(self, state=False):
        val = 1 if state is True else 0
        self.write(":SYST{chan}:LOCK {scale}".format(chan=chan, scale=val))


    def get_sample_status(self):
        pass


    def set_memory_depth(self, size=14000):
        pass


    def get_sample_rate(self):
        pass

    def set_trace_visibility(self, trace=1, state=True):
        pass


    def set_time_perdiv(self, val=1E-3):
        pass

    def set_channel_offset(self, offset=0.0, channel=1):
        pass


    def get_channel_sample_points(self, channel=1):
        pass




    def set_channel_volts_perdiv(self, val=1.0, chan=1):
        if val not in [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]:
            raise InstrumentError("Invalid vertical scale value")
        self._write(":CHAN{chan}:SCAL {scale}".format(chan=chan, scale=val))


    def set_channel_invert(self, invert=False, math=False, chan=1):
        pass


    def set_channel_probe_atten(self, atten=10, chan=1):
        """ Set the probe attenuation"""
        if atten not in [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000, 20000, 50000]:
            raise InstrumentError("Invalid probe attenuation value")
        self._write(":CHAN{chan}:PROB {atten}".format(chan=chan, atten=atten))


    def set_channel_coupling(self, coupling="dc", fiftyohms=False, chan=1):
        pass

    def set_channel_bandwidth_limit(self, state=False, chan=1):
        pass

        self._write("BWL C{chan},{bwl}".format(chan=chan, bwl=bwl))

    def set_channel_skew(self, nanoseconds = 0, chan = 1):
        pass

    def set_channel_units(self, units="V", chan=1):
        pass


    def set_trigger_mode(self, mode="auto"):
        pass

    def arm_trigger(self):
        pass

    def set_trigger_slope(self, tsource, slope="pos",):
        pass


    def set_trigger_coupling(self, tsource, mode="dc"):
        pass


    def get_trigger_level(self):
        pass

    def set_trigger_level(self, level=0.5E+00, chan=1):
        pass


    def save_screendump(self, filename):
        """Save a screendump to a file. Screendump file is in .bmp format"""
        f = open(filename, "wb")
        res = self._ask_read_raw(':DISP:DATA?')
        # Split the header and data into separate arrays
        header = res[0:11]
        data = res[11:]
        # Get size from header
        size = int(header[2:])
        # Open the file to write the bitmap info into
        f = open(filename, "wb")
        # Write the bitmap info into the file
        f.write(data)
        # Set the file size to what was sent in the header
        f.truncate(size)
        # Close the file
        f.close()



    def console(self):
        self._console("RIGOL MSO5000")


