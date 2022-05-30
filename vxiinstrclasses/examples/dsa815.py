#!/usr/bin/python3
import sys
import argparse
from vxiinstrclasses.dsa815 import *
#
# Snap a screenshot from the DSA815
#
parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("--action", type=str, help="Specify identify or snap", default='identify')
parser.add_argument("--host", type=str, help="specify a host name or IP address for the dsa815",default='DSA-815')
parser.add_argument("--file", type=str, help="specify an output file name for the image file", default='dsa815.bmp')
args = parser.parse_args()

# instantiate a sds2000 object
sa = dsa815(args.host)

if(args.action == 'identify'):
    print(sa.identify())
elif(args.action == 'snap'):
    print("Saving screen snapshot...")
    sa.save_screendump(args.file)
