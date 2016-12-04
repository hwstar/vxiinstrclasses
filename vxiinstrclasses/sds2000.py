from  vxiinstrclasses.instrument import *

class sds2000(instrument):
    """This class controls a Siglent SDS2000 Scope"""
    def __init__(self, resourcehost):

        instrument.__init__(self, resourcehost)
        self.externaltrigsources=["C1","C2","C3","C4","EX","EX5","LINE"]
        self.tracelist = ["C1", "C2", "C3", "C4", "TA", "TB", "TC", "TD"]
        self.channellist = ["C1","C2","C3","C4"]
        self.memory_sizes = {7000:"7K", 14000:"14K", 70000:"70K", 140000:"140K", 700000:"700K", 1400000:"1.4M",
                             7000000:"7M", 14000000:"14M"}

        iid = self.identify()
        if(iid[5:17] != "SIGLENT,SDS2"):
            raise InstrumentError("Instrument Manufacturer/Model Number Mismatch, "+iid)

    def lock(self, state=False):
        "Lock or unlock the scope front panel"

        sw = 'OFF'
        if (state):
            sw = 'ON'

        self._write("LOCK {sw}".format( sw=sw))

    def get_sample_status(self):
        " Get the scope's sample status"
        res = self._ask("SAST?")
        return res.split(' ')[1]

    def set_memory_depth(self, size=14000):
        "Set scope memory depth"
        if(size not in self.memory_sizes):
            raise InstrumentError("Invalid Memory Size")
        self._write("MSIZ {size}".format(size=self.memory_sizes[size]))


    def get_sample_rate(self):
        " Get the scope's sample status"
        res = self._ask("SARA?")
        return res.split(' ')[1]


    def set_trace_visibility(self, trace=1, state=True):
        """Turn a trace on or off"""
        index = int(trace - 1)

        if( index < 0 or index >= len(self.tracelist)):
            raise InstrumentError("Invalid trace index")

        sw = 'OFF'
        if(state):
            sw = 'ON'

        self._write("{tracecode}:TRA {sw}".format(tracecode=self.tracelist[index], sw=sw))


    def set_time_perdiv(self, val=1E-3):
        """Sets the time per division"""
        tdivdict = {1.0E-9:"1.0NS",2.5E-9:"2.5NS", 5.0E-9:"5.0NS",
                    10E-9: '10NS',25E-9:'25NS',50E-9: '50NS',
                    1000E-9: '100NS', 250E-9: '250NS', 500E-9: '500NS',
                    1.0E-6: "1.0US", 2.5E-6: "2.5US", 5.0E-6: "5.0US",
                    10E-6: '10US', 25E-6: '25US', 50E-6: '50US',
                    1000E-6: '100US', 250E-6: '250US', 500E-6: '500US',
                    1.0E-3: "1.0MS", 2.5E-3: "2.5MS", 5.0E-3: "5.0MS",
                    10E-3: '10MS', 25E-3: '25MS', 50E-3: '50MS',
                    1000E-3: '100MS', 250E-3: '250MS', 500E-3: '500MS',
                    1.0E0: "1.0S", 2.5E0: "2.5S", 5.0E0: "5.0S",
                    10E0: '10S', 25E0: '25S', 50E0: '50S'
                    }
        if(val not in tdivdict):
            raise InstrumentError("Invalid time per division: "+str(val))

        command = 'TDIV {tdiv}'.format(tdiv=tdivdict[val])

        self._write(command)

    def set_channel_offset(self, offset=0.0, channel=1):
        "Set the offset for a scope channel"
        if (channel < 1 or channel > 4):
            raise InstrumentError("Invalid channel number")
        res = self._write("{0}:OFST {1:.3f}V".format(self.channellist[channel - 1], offset))
        pass


    def get_channel_sample_points(self, channel=1):
        """Return the number of sampled points for a channel"""
        if(channel < 1 or channel > 4):
            raise InstrumentError("Invalid channel number")
        res = self._ask("SANU? {chid}".format(chid=self.channellist[channel - 1]))
        return res.split(" ")[1]




    def set_channel_volts_perdiv(self, val=2.0, chan=1):
        """Sets the volts per division on a specific channel"""
        # Bug: Can't set 1mV per division.
        # Note: Scope goes into fine volts per div mode.
        # Note: voltage is referenced to X1 probes
        vdivdict = {1.0E-3:"1MV'", 2.0E-3:"2MV", 5.0E-3:"5MV", 10.0E-3:"10MV", 20.0E-3:"20MV", 50E-3:"50MV",
                    100E-3:"100MV", 200E-3:"200MV", 500E-3:"500MV", 1.0E0:"1V", 2.0E0:"2V", 5.0E0:"5V",
                    1.0E1:"10V"}

        if(val not in vdivdict):
            raise InstrumentError("Invalid volts per division: "+str(val))

        command = "C{chan}:VDIV {vdiv}".format(chan=chan, vdiv=vdivdict[val])

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
            raise InstrumentError("Invalid probe attenuation value")
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
            raise InstrumentError("Bad coupling value: " + coupling)

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
        if(units == "V" or units == "A"):
            self._write("C{chan}:UNIT {units}".format(chan=chan, units=units))
        else:
            raise InstrumentError("Invalid value for units: "+units)


    def set_trigger_mode(self, mode="auto"):
        """Set trigger mode: auto, norm, single, stop"""
        validmodes = ["AUTO","NORM","SINGLE","STOP"]
        if(mode.upper() not in validmodes):
            raise InstrumentError("Invalid trigger mode: "+mode)
        command = 'TRMD' + ' ' + mode.upper()
        self._write(command)

    def arm_trigger(self):
        """ Arm the trigger for a single acquisition"""
        self._write("ARM")

    def set_trigger_slope(self, tsource, slope="pos",):
        """Set the trigger slope"""
        validslopes = ["NEG","POS","WINDOW"]

        if (tsource == None):
            tsource = 1
        if (isinstance(tsource, int)):
            stsource = "C" + str(tsource)
        elif (isinstance(tsource, str)):
            stsource = tsource.upper()
        else:
            raise (InstrumentError, "Invalid type for trigger source")

        if (stsource not in self.externaltrigsources):
            raise InstrumentError("Invalid trigger source " + stsource)


        if (slope.upper() not in validslopes):
            raise InstrumentError("Invalid trigger slope: " + slope)
        command = '{stsource}:TRSL {slope}'.format(stsource=stsource, slope=slope.upper())
        self._write(command)


    def set_trigger_coupling(self, tsource, mode="dc"):
        """Set trigger coupling"""

        if(tsource == None):
            tsource = 1
        if(isinstance(tsource, int)):
            stsource = "C"+str(tsource)
        elif(isinstance(tsource, str)):
            stsource = tsource.upper()
        else:
            raise(InstrumentError,"Invalid type for trigger source")

        if(stsource not in self.externaltrigsources):
            raise InstrumentError("Invalid trigger source "+stsource)

        validmodes = ["AC", "DC", "HFREJ", "LFREJ"]
        if(mode.upper() not in validmodes):
            raise InstrumentError("Invalid trigger mode: "+str(mode))

        self._write("{tsource}:TRCP {mode}".format(tsource=stsource, mode=str(mode).upper()))


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
    scope.set_memory_depth(7000)
    scope.set_channel_offset(0.0)
    #print(scope.identify())
    #scope.console()
    #res = scope.save_screendump('/tmp/siglent.bmp')
    #scope.set_channel_coupling(coupling="dc", fiftyohms=False)
    #scope.set_channel_bandwidth_limit(False)
    #scope.set_channel_probe_atten(1)
    #scope.set_channel_invert(invert=False)
    #scope.set_channel_skew(0)
    #scope.set_channel_units('V')
    #scope.set_channel_volts_perdiv(1E-0)
    #scope.set_time_perdiv(10E-6)
    #scope.set_trigger_slope(1, slope="pos")
    #scope.set_trigger_mode("auto")
    #scope.set_trigger_coupling(1,mode="dc")
    scope.set_trace_visibility(1,True)
    scope.arm_trigger()


    scope.close()


