#!/usr/bin/python3
import sys
import argparse
from vxiinstrclasses.sds2000 import *
#
# Snap a screenshot from the SDS2000
#

parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("action", type=str, help="Specify identify or snap")
parser.add_argument("--host", type=str, help="specify a host name or IP address for the sds2000",default='sds2000')
parser.add_argument("--file", type=str, help="specify an output file name for the image file", default='sds2000.bmp')
args = parser.parse_args()

# instantiate a sds2000 object
scope = sds2000(args.host)

if(args.action == 'identify'):
    print(scope.identify())
elif(args.action == 'snap'):
    print("Saving screen snapshot...")
    scope.save_screendump(args.file)





identity = scope.identify()


#scope.save_screendump("sds2000.png")
