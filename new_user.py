import os
import getpass
import paramiko
import time

print ("LET'S ADD A NEW USER TO THE UBUNTU SERVERS\n")

serverListFile = open("serverList.txt", "r")
serverList = []

for x in serverListFile.readlines():
    x = x.rstrip('\n')
    serverList.append(x)

serverListFile.close()

print("Here's your servers: ", serverList)

username = input("Enter a username: ")

passwordList = []

isSamePass = input("Password the same for all servers? [y,n]\n")

if (isSamePass.lower() == "y"):
    singlePassword = getpass.getpass("Please enter your password:\n")
    for i in serverList:
        print(i)
        passwordList.append(singlePassword)
elif (isSamePass.lower() == "n"):
    print("Please enter your passwords for each server: ")
    for i in serverList:
        currentPass = getpass.getpass(i + ": ")
        passwordList.append(currentPass)
else:
    print("Dude, enter a valid thing")

diskSpaceFile = open("Disk_Space.txt", "w")
diskSpaceFile.write("UBUNTU SERVER STORAGE SIZE\n")

for i in range(len(serverList)):
    print(serverList[i]," ", username)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(serverList[i], "22", username, singlePassword)
    stdin, stdout, stderr = ssh.exec_command("df -h")
    lines = stdout.readlines()
    time.sleep(5)
    ssh.close()

    for line in lines:
        str(line)
    diskSpaceFile.write(serverList[i] + "\n")
    diskSpaceFile.writelines(lines)

diskSpaceFile.close()


