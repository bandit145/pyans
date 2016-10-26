#!/usr/bin/env python3
#TODO: add error handling
import paramiko
from config import *
from playbooks import *
import sys
import json
import getpass
import http.client
import subprocess
import time
import os
books = {#function names go here 
	'server_deploy': [server_deploy,'linux'],
	'jenkins_server': [jenkins_server,'linux']
}


login = 0
pkey_pass = 0 
ssh=0
def begin(ssh):
	if login == 0:
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
		get_inventory(ssh)
	elif choice == '4':
		sys.exit()

def run_ans(ssh): #going to become "deployment function"
	try:
		choice = input('Enter playbook you would like to deploy > ')
		name = new_vm(books[choice][1])
		books[choice][0](ssh,name)
		begin(ssh)
	except paramiko.SSHException:
		print('Error Establishing connection...')
	except paramiko.AuthenticationException:
		print('Auth Error...')
	except KeyError:
		print('No playbook by that name...')
		begin(ssh)

def list_plays(ssh): #lists plays
	stdin, stdout, stderr = ssh.exec_command('ls *.yml *.yaml')
	print(stdout.readlines())
	begin(ssh)


def get_inventory(ssh): # connects to sensu and gets servers
	sensu = http.client.HTTPConnection(monitoring_location)
	sensu.request('GET','/clients')
	clients = sensu.getresponse()
	clients = json.loads(clients.readall().decode('utf-8'))
	for client in clients:
		print(client['name']+' - '+ client['address'])
	begin(ssh)


def ssh_connect(key):
	global login
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ans_server,username=username, pkey=key)
	#user becomes logged in
	login = 1
	return ssh

def new_vm(choice):#keep ip address together with ansible
	if choice == 'linux':
		template = 'debian-server'
	elif choice == 'windows':
		template = 'winserver2016'
	name = input('Enter computer name > ')
	subprocess.call(['powershell', 'Set-ExecutionPolicy Unrestricted'], shell=True)
	subprocess.call(['powershell', './vmdeploy.ps1','-server '+vcenter,'-template '+template,'-vmname '+name], shell=True)
	return name
	


begin(ssh)
