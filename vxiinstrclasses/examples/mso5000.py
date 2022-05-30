#!/usr/bin/python3
import sys
import argparse
from vxiinstrclasses.mso5000 import *
#
# Snap a screenshot from the MSO5000
#

def exit(msg):
    print(msg)
    sys.exit(1)

parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("action", type=str, help="Specify identify or snap")
parser.add_argument("--host", type=str, help="specify a host name or IP address for the mso5000",default='MSO5000')
parser.add_argument("--file", type=str, help="specify an output file name for the image file", default='mso5000.bmp')
args = parser.parse_args()

# instantiate an mso5000 object
scope = mso5000(args.host)

if(args.action == 'identify'):
    print(scope.identify())
elif(args.action == 'snap'):
    print("Saving screen snapshot...")
    scope.save_screendump(args.file)
elif(args.action == 'reset'):
    for i in range(1,5):
        scope.set_channel_probe_atten(10, i)
        scope.set_channel_volts_perdiv(1, i)
else:
    exit("Invalid action command")





