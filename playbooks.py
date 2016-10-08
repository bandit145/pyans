#File contains functions for the different playbooks added
#to the enviroment
#
from config import pkey_location
import getpass
def server_deploy(ssh): #for base server_deploy.yml playbook
	playbook = 'server_deploy.yml' #name of book on server
	computer = input('Enter address of target > ')
	pcname = input('Enter the desired name of the target machine > ')
	password = getpass.getpass('Enter become pass > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	for line in output:
		print(line)

def jenkins_server(ssh): #for base jenkins_server.yml playbook
	playbook = 'jenkins_server.yml' #name of book on server
	computer = input('Enter address of target > ')
	pcname = input('Enter the desired name of the target machine > ')
	password = getpass.getpass('Enter become pass > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	for line in output:
		print(line)