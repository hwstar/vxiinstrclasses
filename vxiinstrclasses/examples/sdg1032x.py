#!/usr/bin/python3
import sys
import argparse
import math
from vxiinstrclasses.sdg1032x import *
#
# Set up the SDG1032X
#
parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("action", type=str, help="Specify identify or 2tone", default='2tone')
parser.add_argument("--host", type=str, help="specify a host name or IP address for the dsa815", default='SDG-1032X')
parser.add_argument("--f1", type=str, help="specify first frequency")
parser.add_argument("--f2", type=str, help="specify second frequency", default=1000)
parser.add_argument("--dbm50", type=str, help="specify level in dBm (50 ohm system)")
parser.add_argument("--vpp", type=str, help="specify level in volts peak to peak")
parser.add_argument("--vrms", type=str, help="specify level in volts rms")
parser.add_argument("--pmw50", type=str, help="specify power in milliwatts (50 ohm system)")
parser.add_argument("--combine", type=str,help="combine into channel specified")
parser.add_argument("--sourcez", type=str, help='specify source impedance', default='600')


def exit(msg):
    print(msg)
    sys.exit(1)

def reset():
    sg.output_off(1)
    sg.output_off(2)
    sg.channel_combine(False, 1)
    sg.channel_combine(False, 2)

def dbm_to_vpp(dbm, r=50):
    pmw = 10 ** (dbm / 10)
    vrms = math.sqrt(pmw * (r / 1000))
    return 2 * (math.sqrt(2) * vrms)

def pmw_to_vpp(pmw, r=50):
    vrms = math.sqrt(pmw * (r / 1000))
    return 2 * (math.sqrt(2) * vrms)

args = parser.parse_args()

# instantiate a sdg1032 object
sg = sdg1032x(args.host)

if args.action == 'identify':
    print(sg.identify())
    sys.exit(0)

elif args.action == 'tone':
    if args.f1 is None:
        exit("Error: must specify --f1 ")
    if args.dbm50 is not None:
        vpp = dbm_to_vpp(float(args.dbm50))
    elif args.pmw50 is not None:
        vpp = pmw_to_vpp(float(args.pmw50))
    elif args.vpp is not None:
        vpp = float(args.vpp)
    elif args.vrms is not None:
        vpp = 2 * math.sqrt(2) * float(args.vrms)
    else:
        exit("Error: must specify an output level as --vpp, --vrms or --dbm50")

    reset()

    if args.dbm50 is not None or args.pmw50 is not None:
        sg.output_sourcez(1, 50)
    else:
        sg.output_sourcez(1, args.sourcez)
    sg.sine(1, float(args.f1), vpp)
    sg.output_on(1)
    sys.exit(0)

elif args.action == '2tone':
    if args.f1 is None or args.f2 is None :
        exit("Error: must specify both --f1 and --f2")
    if args.dbm50 is not None:
        vpp = dbm_to_vpp(float(args.dbm50))
    elif args.pmw50 is not None:
        vpp = pmw_to_vpp(float(args.pmw50))
    elif args.vpp is not None:
        vpp = float(args.vpp)
    elif args.vrms is not None:
        vpp = 2*math.sqrt(2)*float(args.vrms)
    else:
        exit("Error: must specify an output level as --vpp, --vrms or --dbm50")

    reset()

    if args.dbm50 is not None or args.pmw50 is not None:
        sg.output_sourcez(1, 50)
        sg.output_sourcez(2, 50)
    else:
        sg.output_sourcez(1, args.sourcez)
        sg.output_sourcez(2, args.sourcez)
    sg.sine(1, float(args.f1), vpp)
    sg.sine(2, float(args.f2), vpp)
    sg.output_on(2)
    sg.output_on(1)
    if args.combine is not None:
        if args.combine != '1' and args.combine != 2:
            exit("Error: Combine channel must be 1 or 2")
        else:
            sg.channel_combine(True, args.combine)
    sys.exit(0)
else:
    exit("Error: must specify a valid action")





