from  vxiinstrclasses.instrument import *

class dsa815(instrument):
    """This class controls a Rigol DSA815 spectrum analyzer"""
    def __init__(self, resourcehost):
        instrument.__init__(self, resourcehost)

        iid = self.identify()
        if(iid[0:25] != 'Rigol Technologies,DSA815'):
            raise InstrumentError('Instrument Manufacturer/Model Number Mismatch, '+iid)


    def console(self):
        """Debugging console"""
        self._console("Rigol Dsa815")

    def set_span(self, span):
        """Set the frequency span"""
        self._write('SENS:FREQ:SPAN '+str(span))

    def set_center_freq(self, center):
        """Set the center frequency"""
        self._write('SENS:FREQ:CENT '+str(center))

    def set_atten(self, atten):
        """Set the input attenuator"""
        if(atten == "auto"):
            self._write('SENS:POW:RF:ATT:AUTO ON')
        else:
            self._write('SENS:POW:RF:ATT '+str(atten))

    def set_preamp_off(self):
        """Disable the built in preamp"""
        self._write('SENS:POW:RF:GAIN OFF')

    def set_preamp_on(self):
        """Enable the built in preamp"""
        self._write('SENS:POW:RF:GAIN ON')

    def save_screendump(self, file):
        """Save a .bmp screenshot to a file"""
        # Get cont mode
        contmode = self._ask(':INIT:CONT?')
        # Set cont mode off
        self._write(':INIT:CONT 0')
        # Retrive the header and data for the snapshot
        res = self._ask_read_raw(':PRIV:SNAP?')

        # Split the header and data into separate arrays
        header = res[0:11]
        data = res[11:]
        # Get size from header
        size = int(header[2:])
        # Open the file to write the bitmap info into
        f = open(file, "wb")
        # Write the bitmap info into the file
        f.write(data)
        # Set the file size to what was sent in the header
        f.truncate(size)
        # Close the file
        f.close()
        # Restore the previous cont mode state
        self._write(':INIT:CONT {contmode}'.format(contmode=contmode))
        # Set local mode
        self._write(':SYST:COMM:BRMT 0')
        return


if __name__ == "__main__":
    specan = dsa815("dsa815")
    print(specan.identify())

    specan.set_atten(0)
    specan.set_preamp_off()
    specan.set_center_freq(440E6)
    specan.set_span(20E6)
    specan.save_screendump('/tmp/dsa815.bmp')





    specan.close()

