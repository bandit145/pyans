from paramiko import paramiko.client.SSHClient
from config import *

def begin():
	print(menu)
	choice = input('> ')
	if choice == 1:
		run_ans()

def run_ans(): #This needs to be split up playbook... maybe
	try:
		playbook = input('Enter playbook name > ')
		computer = input('Enter address of target > ')
		pcname = input('Enter the name ')
		pkey_pass= input('Enter pkey > ')
		ssh = SSHClient()
		ssh.connect(ans_server, password=pkey_pass, pkey=priv_key_file)
		stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} --extra-vars "hosts={host} host_name={name}"'.format(playbook=playbook, hosts=computer, name=pcname))
		print(stdout.rstrip('\n'))
	except paramiko.client.SSHException:
		print('Error Establishing connection...')
	except paramiko.client.AuthenticationException:
		print('Auth Error...')

def list_ans():


def ssh_connect():
	ssh = SSHClient()
	ssh.connect(ans_server, password=pkey_pass, pkey=priv_key_file)