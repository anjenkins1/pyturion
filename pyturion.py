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
import getpass
import time

SERVERS = []
PASSWORDS = []

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

def add_server(server):
    SERVERS.append(server)

    serverListFile = open("serverList.txt", "a")
    
    serverListFile.write(server + "\n")

    serverListFile.close()

def get_passwords():
    isSamePass = input("Password the same for all servers? [y,n]\n")

    if (isSamePass.lower() == "y"):
        singlePassword = getpass.getpass("Please enter your password:\n")
        for i in SERVERS:
            PASSWORDS.append(singlePassword)
    elif (isSamePass.lower() == "n"):
        print("Please enter your passwords for each server: ")
        for i in SERVERS:
            currentPass = getpass.getpass(i + ": ")
            PASSWORDS.append(currentPass)
    else:
        print("Dude, enter a valid thing")

def command_ssh(username):
    user_input = ""
    output_File = open("output.txt", "w")

    while(user_input != 'q'):

        user_input = input("Enter command (q to quit): \n")

        if (user_input == 'q'):
            break

        elif (user_input == 'add_user'):
            add_user(username)
            break

        for i in range(len(SERVERS)):
            print(SERVERS[i], " ", username)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(SERVERS[i], "22", username, PASSWORDS[i])
            stdin, stdout, stderr = ssh.exec_command(user_input)
            lines = stdout.readlines()
            time.sleep(5)
            ssh.close()

            for line in lines:
                str(line)
            output_File.write("\n" + SERVERS[i] + "\n\n")
            output_File.writelines(lines)
        
    output_File.close()

def add_user(username):
    new_username = input("Please enter the username of the new user: \n")
    new_password = getpass.getpass("Please enter that dude's password: \n")

    #THIS IS BROKEN AND IT CAUSES AN INFINITE LOOP
    for i in range(len(SERVERS)):
        print(SERVERS[i], " ", username)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(SERVERS[i], "22", username, PASSWORDS[i])

        stdin, stdout, stderr = ssh.exec_command("sudo su", get_pty=True)
        stdin.write(PASSWORDS[i] + '\n')
        ssh.exec_command("useradd " + new_username)
        ssh.exec_command("passwd " + new_username)
        ssh.exec_command(new_password)
        ssh.exec_command(new_password)

        for line in stdout:
            print(line)

        time.sleep(5)
        ssh.close()



def main(args):
    get_server_file()

    if (args.list_servers):
        print (SERVERS)
    
    if args.collection:
        for x in args.collection:
            add_server(x)
    
    if (args.send_command):
        username = input("Please enter a username: \n")
        get_passwords()
        command_ssh(username)

    print(SERVERS)
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

    parser.add_argument("-remove-server", 
                        help="Remove a server from list")

    parser.add_argument("-list-users", help="List all saved users")

    parser.add_argument("-add-user", help="Add new user")

    parser.add_argument("-command", 
                        help="Send a command to all servers",
                        action='store_true',
                        dest='send_command',
                        default=False)

    args = parser.parse_args()
    main(args)