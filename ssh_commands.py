import paramiko
import time

class SSH:

    def __init__(self, machine, ssh_user, ssh_pass):
        self.machine = machine
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass
        
    def get_ssh_connection(self, ssh_machine, ssh_username, ssh_password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_machine, username=ssh_username, password=ssh_password, timeout=10)
        return client
    
    def add_user (self, username, password, sudo_password):
            client = self.get_ssh_connection(self.machine, self.ssh_user, self.ssh_pass)
            stdin, stdout, stderr = client.exec_command("sudo adduser " + username, get_pty=True)
            stdin.write(sudo_password + '\n')
            stdin.flush()
            time.sleep(2)
            stdin.write(password + '\n')
            stdin.flush()
            time.sleep(2)
            stdin.write(password + '\n')
            stdin.flush()
            time.sleep(2)
            stdin.write('\n\n\n\n\n')
            stdin.flush()
            stdin.write('y\n')
            time.sleep(5)
            client.close()
    
    def remove_user (self, username, sudo_password):
            client = self.get_ssh_connection(self.machine, self.ssh_user, self.ssh_pass)
            stdin, stdout, stderr = client.exec_command("sudo userdel " + username, get_pty=True)
            stdin.write(sudo_password + '\n')
            stdin.flush()
            time.sleep(5)
            client.close()