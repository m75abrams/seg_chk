#!/usr/bin/python2

# help to ensure python compatability
from __future__ import absolute_import

# import necessary modules
import subprocess
import argparse
import sys
import fileinput
import os

# dev temp vars
#verbose = "True"

def subnet_info(mode, segment, logfile):
    # set variable null to catch stdout & stderr
    with open(os.devnull, "wb") as null:
        # set IP range
        sys.stdout.write("IP" + "\t\t\t" + "STATUS" + "\t\t" + "IP IN DNS?" + "\t\t" + "UPTIME/HRS")
        sys.stdout.write('\n')
        for ip in xrange(1,254):
            ip_num = str(ip)
            # build address into a proper IP of type 'string'
            address = segment + "." + ip_num
            # get $?
            ping_result = subprocess.Popen(["ping", "-w", "1", "-c", "1", address], stdout=null, stderr=null).wait()
            host_result = subprocess.Popen(["host", address], stdout=null, stderr=null).wait()
            # uptime_result() -> needs a function to check the logfile

            # assign result for UP or DN from icmp ping
            if ping_result:
                alive_result = "DN"
            else:
                alive_result = "UP"
            
            # assign result from DNS lookup and alive_result
            if host_result and alive_result == "DN":
                dns_result = "available"
            elif host_result:
                dns_result = "NO"

            # start iterating and acting on valid variables
            if mode == "-v":
#                sys.stdout.write(address + "\t\t" + alive_result + "\t\t" + dns_result + "\t\t\t" + "WIP")
                sys.stdout.write(address + "\t\t" + alive_result + "\t\t" + dns_result)
                sys.stdout.write('\n') 
            elif mode == '-a':
                if alive_result == "DN":
                    # this will be contingent on DNS presence, hours pingable as well...
#                    sys.stdout.write(address + "\t\t" + alive_result + "\t\t" + dns_result + "\t\t\t" + "WIP")
                    sys.stdout.write(address + "\t\t" + alive_result + "\t\t" + dns_result)
                    sys.stdout.write('\n')
            elif mode == "-q":
                    sys.stdout.write("not yet implemented")
                    sys.stdout.write('\n')
                    break

parser = argparse.ArgumentParser()
if len(sys.argv[1:]) < 3:           # check for no CLI args
    parser.print_help()             # if no cli args print built-in help
    sys.exit(1)
group = parser.add_mutually_exclusive_group()

# add valid CLI arg flags
group.add_argument('-q', '--quiet', action='store_true', help='quiet to run out of cron')
group.add_argument('-v', '--verbose', action='store_true', help='verbose list for terminal output')
group.add_argument('-a', '--available', action='store_true', help='available only list for terminal output')
parser.add_argument('segment', type=str, help='network segment to check')
parser.add_argument('logfile', type=str, help='desired logfile location')
args = parser.parse_args()

# assign args meaningful variable names to args
mode = sys.argv[1]
segment = sys.argv[2]
logfile = sys.argv[3]

# main program
if __name__ == '__main__':
    subnet_info(mode, segment, logfile)