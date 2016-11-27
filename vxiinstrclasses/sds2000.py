from  vxiinstrclasses.instrument import *

class sds2000(instrument):
    """This class controls a Siglent SDS2000 Scope"""
    def __init__(self, resourcehost):

        instrument.__init__(self, resourcehost)

        iid = self.identify()
        if(iid[5:17] != "SIGLENT,SDS2"):
            raise InstrumentError("Instrument Manufacturer/Model Number Mismatch, "+iid)


    def set_timediv(self, val=1E-3):
        """Sets the time per division"""
        if (val <= 1.0E-9):
            timediv = '1.0NS'
        elif (val <= 2.5E-9):
            timediv = '2.5NS'
        elif (val <= 5.0E-9):
            timediv = '5NS'
        elif (val <= 10.0E-9):
            timediv = '10NS'
        elif (val <= 25.0E-9):
            timediv = '25NS'
        elif (val <= 50.0E-9):
            timediv = '50NS'
        elif (val <= 100.0E-9):
            timediv = '100NS'
        elif (val <= 250.0E-9):
            timediv = '250NS'
        elif (val <= 500.0E-9):
            timediv = '500NS'

        elif (val <= 1.0E-6):
            timediv = '1US'
        elif (val <= 2.5E-6):
            timediv = '2.5US'
        elif (val <= 5.0E-6):
            timediv = '5US'
        elif (val <= 10.0E-6):
            timediv = '10US'
        elif (val <= 25.0E-6):
            timediv = '25US'
        elif (val <= 50.0E-6):
            timediv = '50US'
        elif (val <= 100.0E-6):
            timediv = '100US'
        elif (val <= 250.0E-6):
            timediv = '250US'
        elif (val <= 500.0E-6):
            timediv = '500US'

        elif (val <= 1.0E-3):
            timediv = '1MS'
        elif (val <= 2.5E-3):
            timediv = '2.5MS'
        elif (val <= 5.0E-3):
            timediv = '5MS'
        elif (val <= 10.0E-3):
            timediv = '10MS'
        elif (val <= 25.0E-3):
            timediv = '25MS'
        elif (val <= 50.0E-3):
            timediv = '50MS'
        elif (val <= 100.0E-3):
            timediv = '100MS'
        elif (val <= 250.0E-3):
            timediv = '250MS'
        elif (val <= 500.0E-3):
            timediv = '500MS'

        elif (val <= 1.0E0):
            timediv = '1S'
        elif (val <= 2.0E0):
            timediv = '2.5S'
        elif (val <= 5.0E0):
            timediv = '5S'
        elif (val <= 10.0E0):
            timediv = '10S'
        elif (val >= 25.0E0):
            timediv = '25S'
        else:
            timediv = '50S'

        command = 'TDIV %s' % (timediv)

        self._write(command)

    def set_voltdiv(self, chan=1, val=2):
        """Sets the volts per division on a specific channel"""
        if (val  <= 1.0E-3):
            voltDiv = '1MV'
        elif (val <= 2.0E-3):
            voltDiv = '2MV'
        elif (val  <= 5.0E-3):
            voltDiv = '5MV'
        elif (val <= 10.0E-3):
            voltDiv = '10MV'
        elif (val <= 20.0E-3):
            voltDiv = '20MV'
        elif (val <= 50.0E-3):
            voltDiv = '50MV'
        elif (val <= 100.0E-3):
            voltDiv = '100MV'
        elif (val <= 200.0E-3):
            voltDiv = '200MV'
        elif (val <= 500.0E-3):
            voltDiv = '500MV'
        elif (val <= 1.0E0):
            voltDiv = '1V'
        elif (val <= 2.0E0):
            voltDiv = '2V'
        elif (val <= 5.0E0):
            voltDiv = '5V'
        else:
            voltDiv = '10V'


        command = 'C%s:VDIV %s' % (chan, voltDiv)

        self._write(command)

    def set_trigmode(self, mode="auto"):
        """Set trigger mode: auto, norm, single, stop"""
        command = 'TRMD' + ' ' + mode.upper()
        self._write(command)


    def set_trigslope(self, slope, chan=1):
        """Set the trigger slope"""
        command = 'C%s:TRSL %s' % (chan, slope.upper())
        self._write(command)


    def get_triglevel(self):
        """Return the channel and trigger level"""
        "Broken: Bug in siglent firmware. Returns values an order of magnitude off"
        res = self._ask("TRLV?")
        res = res[:-2]
        print(res)
        return {'channel':int(res[1]), 'level':float(res[8:])}

    def set_triglevel(self, level=0.5E+00, chan=1):
        """Set the trigger level in volts"""
        command= 'C%s:TRLV %1.3fV' % (chan, level)
        self._write(command)

    def save_screendump(self, file):
        """Save a screendump to a file. Screendump file is in .bmp format"""
        f = open(file, "wb")
        res = self._ask_read_raw('SCDP')
        f.write(res)
        f.close()

    def console(self):
        self._console("Siglent SDS2000")

if __name__ == "__main__":
    scope = sds2000("sds2000")
    #print(scope.identify())
    #scope.set_triglevel(2.0)
    print(scope.get_triglevel())
    #scope.set_timediv(10E-3)
    #scope.waveform()
    #scope.console()
    res = scope.save_screendump('/tmp/siglent.bmp')

    scope.close()


