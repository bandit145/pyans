#!/usr/bin/env python3
#TODO: add error handling
import paramiko
from config import *
import sys
import json
import getpass
import http.client
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
		playbook = input('Enter playbook name > ')
		computer = input('Enter address of target > ')
		pcname = input('Enter the desired name of the target machine > ')
		password = getpass.getpass('Enter become pass > ')
		stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
		stdin.write(password+'\n')
		stdin.flush()
		output = stdout.readlines()
		for line in output:
			print(line)
		begin()
	except paramiko.SSHException:
		print('Error Establishing connection...')
	except paramiko.AuthenticationException:
		print('Auth Error...')

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
