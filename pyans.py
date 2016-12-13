#!/usr/bin/env python3
#Streamline pyans to be more autonomous
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
import re
import logging
books = {#function names go here 
	'server_deploy': [server_deploy,'linux'],
	'jenkins_server': [jenkins_server,'linux'],
	'graylog_selfnode':[graylog_selfnode,'linux'],
	'domain_con':[domain_con,'windows'],
	'windows_common':[windows_common,'windows']
}


login = 0
pkey_pass = 0 
ssh=0
ipv4addr = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
logging.basicConfig(level=logging.CRITICAL)
def begin(ssh):
	try:
		if login == 0:
			print('Initialize connection to Ansible server...')
			pkey_pass= getpass.getpass('Enter pkey pass > ')
			key = paramiko.RSAKey(filename=priv_key_file, password=pkey_pass)
			ssh = ssh_connect(key)
		print(menu)
		choice = input('> ')
		if choice == '1':
			run_ans(ssh,choice)
		elif choice == '2':
			list_plays(ssh)
		elif choice == '3':
			get_inventory(ssh)
		elif choice == '4':
			run_ans(ssh,choice)
		elif choice == '5':
			sys.exit()
	except paramiko.ssh_exception.SSHException:
		print('[x] Password incorrect')
		sys.exit()
	except KeyboardInterrupt:
		print('[x] Exiting...')
def run_ans(ssh, choice): #going to become "deployment function"
	try:
		playbook = input('Enter playbook you would like to deploy > ')
		if choice == '1':
			name, ip = new_vm(books[playbook][1])
			books[playbook][0](ssh, name ,ip)
			begin(ssh)
		elif choice == '4':
			name = input('Enter Computer Name > ')
			ip = input('Enter ip of machine > ')
			books[playbook][0](ssh, name ,ip)
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
	clients = json.loads(clients.read().decode('utf-8'))
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
		template = linux_template
	elif choice == 'windows':
		template = windows_template
	user = input('Enter username for vcenter > ')
	paswd =  getpass.getpass('Enter password for vcenter > ')
	name = input('Enter computer name > ')
	folder = input('Enter Folder name for vm > ')
	proc = subprocess.Popen('powershell', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	script = './vmdeploy.ps1 -server {vcenter} -template {template} -vmname {name} -user {user} -password "{paswd}" -folder "{folder}"'.format(vcenter=vcenter, template=template, name=name, user=user, paswd=paswd, folder=folder)
	output, err = proc.communicate(input=bytes(script+"\n",encoding='utf-8'))
	output = str(output)
	if "incorrect" in output:
		print('[x] Incorrect user name or password, restarting...')
		begin(ssh)
	output = ipv4addr.search(output)
	if output:
		logging.debug(output.group())
		ip = output.group()
	else:
		print('[x] No ip address found for {name}'.format(name=name))
		ip = input('[x] Enter ip address manually > ')
	return name, ip

begin(ssh)