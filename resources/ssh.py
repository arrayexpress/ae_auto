import paramiko
import time

__author__ = 'Ahmed G. Ali'



def retrieve_banana_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('banana.ebi.ac.uk', username='ahmed', password='enggemmy')
    chan = ssh.invoke_shell()
    chan.send('''sudo -u fg_cur -s\n''')
    return chan, ssh

def retrieve_plantain_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('plantain.ebi.ac.uk', username='ahmed', password='enggemmy')
    chan = ssh.invoke_shell()
    chan.send('''sudo -u fg_cur -s\n''')
    return chan, ssh


def retrieve_ena_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('plantain.ebi.ac.uk', username='ahmed', password='enggemmy')
    chan = ssh.invoke_shell()
    chan.send('''sudo -u fg_cur -s\n''')
    chan.send('''ssh oy-ena-login-1 \n''')
    return chan, ssh


def get_ssh_out(chan):
    buff = ''
    while not chan.exit_status_ready():
        time.sleep(1)
        if chan.recv_ready():
            resp = chan.recv(1024)
            buff += resp
        else:
            break
    return buff

def wait_execution(chan):
    buff = ''
    while not buff.endswith('$ '):
        while chan.recv_ready():
            resp = chan.recv(1024)
            # print resp
            buff += resp
            time.sleep(1)
        time.sleep(5)

    return buff.replace('\r', '')
