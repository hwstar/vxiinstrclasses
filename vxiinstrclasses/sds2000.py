from  vxiinstrclasses.instrument import *

class sds2000(instrument):
    """This class controls a Siglent SDS2000 Scope"""
    def __init__(self, resourcehost):

        instrument.__init__(self, resourcehost)

        iid = self.identify()
        if(iid[5:17] != "SIGLENT,SDS2"):
            raise InstrumentError("Instrument Manufacturer/Model Number Mismatch, "+iid)


    def set_time_perdiv(self, val=1E-3):
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

    def set_channel_volts_perdiv(self, val=2, chan=1):
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

    def set_channel_invert(self, invert=False, math=False, chan=1):
        "Set the channel or math pseudo channel invert true or false"
        state = "OFF"
        if(invert == True):
            state = "ON"
        if(math == True):
            self._write("MATH:INVS {state}".format(state=state))
        else:
            self._write("C{chan}:INVS {state}".format(chan=chan, state=state))




    def set_channel_probe_atten(self, atten=10, chan=1):
        """ Set the probe attenuation"""
        #Broken: Bug in Siglent firmware. Can only set 0.1, 0.2, 0,5, 1,2,5 and 10 yet others selectable from scope UI.
        if atten not in [0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]:
            return
        self._write("C{chan}:ATTN {atten}".format(chan=chan, atten=atten))


    def set_channel_coupling(self, coupling="dc", fiftyohms=False, chan=1):
        "Set channel coupling"

        #Determine coupling letter
        acl = "D"
        if(coupling.upper() == "AC"):
            acl = "A"
        elif(coupling.upper() == "DC"):
            pass
        elif(coupling.upper() == "GND"):
            # If GND is specified, then forget about sending the channel impedance
            self._write("C{chan}:CPL GND".format(chan=chan))
            return
        else:
            return

        # Determine impedance code
        z = "1M"
        if(fiftyohms == True):
            z = "50"

        self._write("C{chan}:CPL {acl}{z}".format(chan=chan, acl=acl, z=z ))

    def set_channel_bandwidth_limit(self, state=False, chan=1):
        "Set the bandwidth limit. The sds2000 only supports on and off"
        bwl = "OFF"
        if(state == True):
            bwl = "ON"

        self._write("BWL C{chan},{bwl}".format(chan=chan, bwl=bwl))

    def set_channel_skew(self, nanoseconds = 0, chan = 1):
        "Set the skew of a channel"

        #broken. SDS2000 recognizes the command, but does not update UI
        self._write("C{chan}:SKEW {nanoseconds}NS".format(chan=chan, nanoseconds= nanoseconds))

    def set_channel_units(self, units="V", chan=1):
        """ Set the units per vertical division (V or A)"""
        if(units == 'V' or units == 'A'):
            self._write("C{chan}:UNIT {units}".format(chan=chan, units=units))


    def set_trigger_mode(self, mode="auto"):
        """Set trigger mode: auto, norm, single, stop"""
        command = 'TRMD' + ' ' + mode.upper()
        self._write(command)


    def set_trigger_slope(self, slope, chan=1):
        """Set the trigger slope"""
        command = 'C%s:TRSL %s' % (chan, slope.upper())
        self._write(command)



    def get_trigger_level(self):
        """Return the channel and trigger level"""
        #Broken: Bug in siglent firmware. Returns values an order of magnitude off
        res = self._ask("TRLV?")
        res = res[:-2]
        print(res)
        return {'channel':int(res[1]), 'level':float(res[8:])}

    def set_trigger_level(self, level=0.5E+00, chan=1):
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
    scope.debug(True)
    #print(scope.identify())
    #scope.console()
    #res = scope.save_screendump('/tmp/siglent.bmp')
    #scope.set_channel_coupling(coupling="dc", fiftyohms=False)
    #scope.set_channel_bandwidth_limit(False)
    #scope.set_channel_probe_atten()
    #scope.set_channel_invert(invert=False)
    #scope.set_channel_skew(0)
    #scope.set_channel_units('V')



    scope.close()


