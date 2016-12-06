#File contains functions for the different playbooks added
#to the enviroment
#
from config import pkey_location
import getpass

def server_deploy(ssh, pcname , computer): #for base server_deploy.yml playbook
	playbook = 'server_deploy.yml' #name of book on server
	password = getpass.getpass('Enter become pass > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)

def jenkins_server(ssh, pcname, computer): #for base jenkins_server.yml playbook
	playbook = 'jenkins_server.yml' #name of book on server
	password = getpass.getpass('Enter become pass > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)

def graylog_selfnode(ssh, pcname, computer): #for base jenkins_server.yml playbook
	playbook = 'graylog_selfnode.yml' #name of book on server
	password = getpass.getpass('Enter become pass > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)

def domain_con(ssh, pcname, computer): #for base jenkins_server.yml playbook
	dapass='"'
	playbook = 'domain_con.yml' #name of book on server
	password = getpass.getpass('Enter local admin pass > ')
	domainadmin = input('Enter domain admin account > ')
	dapass = dapass+getpass.getpass('Enter DA password > ')
	dapass = dapass+'"'
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)

def windows_common(ssh, pcname, computer): #for base jenkins_server.yml playbook
	dapass='"'
	playbook = 'windows_common.yml' #name of book on server
	password = getpass.getpass('Enter local admin pass > ')
	domainadmin = input('Enter domain admin account > ')
	dapass = dapass+getpass.getpass('Enter DA password > ')
	dapass = dapass+'"'
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)