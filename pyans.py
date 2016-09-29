#!/usr/bin/env python3
#TODO: add error handling
import paramiko
from config import *
import sys
import http.client
import json
import getpass

def begin():
	print('Initialize connection to Ansible server...')
	pkey_pass= getpass.getpass('Enter pkey pass > ')
	ssh = paramiko.SSHClient()
	key = paramiko.RSAKey(filename=priv_key_file, password=pkey_pass)
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ans_server, password=pkey_pass, pkey=key)
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
		stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
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
	print(stdout.read())
	begin()


def get_inventory():#replace with requests
	sensu = http.client.HTTPConnection(monitoring_location)
	sensu.request('GET','/clients')
	clients = sensu.getresponse()
	clients = json.loads(clients.readall().decode('utf-8'))
	for client in clients:
		print(client['name']+'  '+ client['address'])
	begin()

#might turn into
def ssh_connect():
	ssh = SSHClient()
	ssh.connect(ans_server, password=pkey_pass, pkey=priv_key_file)

begin()