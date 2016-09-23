!#/usr/bin/env python3
from paramiko import SSHClient
from config import *
import sys
import requests
import json

def begin():
	print('Initialize connection to Ansible server...')
	pkey_pass= input('Enter pkey pass > ')
	ssh = SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ans_server, password=pkey_pass, pkey=priv_key_file)
	print(menu)
	choice = input('> ')
	if choice == '1':
		run_ans(ssh)
	elif choice == '2':
		list_plays(ssh)
	elif choice == '3':
		get_inventory()
	elif choice == '4':
		sys.exit()

def run_ans(ssh): #This needs to be split up playbook... maybe
	try:
		playbook = input('Enter playbook name > ')
		computer = input('Enter address of target > ')
		pcname = input('Enter the desired name of the target machine > ')
		stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass'.format(playbook=playbook, hosts=computer, name=pcname))
		stdin.write(password)
		stdin.flush()
		print(stdout.rstrip('\n'))
		begin()
	except paramiko.client.SSHException:
		print('Error Establishing connection...')
	except paramiko.client.AuthenticationException:
		print('Auth Error...')

def list_plays(ssh):
	stdin, stdout, stderr = ssh.exec_command('ls *.yml *.yaml')
	if (str(stderr.read())) > 5:
		print('No playbooks detected...')
	else:
		print(str(stdout))
	begin()


def get_inventory():#replace with requests
	data = requests.get(monitoring_location)
	clients = data.json()
	print(clients['name'])
	begin()

#might turn into
def ssh_connect():
	ssh = SSHClient()
	ssh.connect(ans_server, password=pkey_pass, pkey=priv_key_file)

begin()