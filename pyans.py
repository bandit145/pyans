#!/usr/bin/env python3
#TODO: add error handling
import paramiko
from config import *
from playbooks import *
import sys
import json
import getpass
import http.client
books = {#function names go here 
	'server_deploy': server_deploy
}
login = 0
pkey_pass = 0 
def begin():
	if login == 0:
		print(login)
		print('Initialize connection to Ansible server...')
		pkey_pass= getpass.getpass('Enter pkey pass > ')
		key = paramiko.RSAKey(filename=priv_key_file, password=pkey_pass)
		ssh = ssh_connect(key)
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
		choice = input('Enter playbook you would like to deploy > ')
		books[choice](ssh)
		begin()
	except paramiko.SSHException:
		print('Error Establishing connection...')
	except paramiko.AuthenticationException:
		print('Auth Error...')
	except KeyError:
		print('No playbook by that name...')
		begin()

def list_plays(ssh): #lists plays
	stdin, stdout, stderr = ssh.exec_command('ls *.yml *.yaml')
	print(stdout.read())
	begin()


def get_inventory(): # connects to sensu and gets servers
	sensu = http.client.HTTPConnection(monitoring_location)
	sensu.request('GET','/clients')
	clients = sensu.getresponse()
	clients = json.loads(clients.readall().decode('utf-8'))
	for client in clients:
		print(client['name']+' - '+ client['address'])
	begin()


def ssh_connect(key):
	global login
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ans_server, password=pkey_pass, pkey=key)
	#user becomes logged in
	login = 1
	return ssh

begin()
