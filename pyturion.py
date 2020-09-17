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
import ssh_commands

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
        
        elif (user_input == 'remove_user'):
            remove_user(username)
            break
        else:
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
    new_password = '1' 
    new_password2 = '2'

    new_username = input("Please enter the username of the new user: \n")
    
    while (new_password != new_password2):
        new_password = getpass.getpass("Please enter their password: \n")
        new_password2 = getpass.getpass("Confirm the password: \n")
    
    for i in range(len(SERVERS)):
        print("Adding " + new_username + " to " + SERVERS[i])
        ssh = ssh_commands.SSH(SERVERS[i], username, PASSWORDS[i])
        ssh.add_user(new_username, new_password, PASSWORDS[i])

def remove_user(username):

    user_to_delete = input("Please enter the username of the user to delete: \n")

    for i in range(len(SERVERS)):
        print("Removing " + user_to_delete + " from " + SERVERS[i])
        ssh = ssh_commands.SSH(SERVERS[i], username, PASSWORDS[i])
        ssh.remove_user(user_to_delete, PASSWORDS[i])

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