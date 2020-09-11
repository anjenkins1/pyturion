"***************************************************************"
"    ************---------PYTURION--------***************       "
"    Python tool for accessing and administering multiple       "
"         linux servers quickly and efficiently                 "
"***************************************************************"

#!/usr/bin/env python3

"""
Module Docstring
"""

__author__ = "Andrew Jenkins"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import argparse
import paramiko

SERVERS = []

def printList(mylist):
    for x in mylist:
        print(x)

def get_server_file():
    serverListFile = open("serverList.txt", "r")

    for x in serverListFile.readlines():
        x = x.rstrip('\n')
        SERVERS.append(x)

    serverListFile.close()
    return SERVERS

def add_server_to_file(server):
    serverListFile = open("serverList.txt", "w")
    
    for x in SERVERS:
        serverListFile.write(x + "\n")

    serverListFile.write(server + "\n")
    serverListFile.close()

def main(args):
    if (args.list_servers): 
        print (SERVERS)
    
    print(args)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(prog="pyturion", description="Manage multiple linux servers remotely")

    parser.add_argument("-list-servers", 
                        action='store_true', 
                        dest='list_servers',
                        default=False,
                        help="List all saved servers")

    parser.add_argument("-add-server", 
                        action="append", dest='collection',
                        default=[],
                        help="Add a server to list")

    parser.add_argument("-remove-server", help="Remove a server from list")

    parser.add_argument("-list-users", help="List all saved users")

    parser.add_argument("-add-user", help="Add new user")

    parser.add_argument("-command", help="Send a command to all servers")

    args = parser.parse_args()
    main(args)