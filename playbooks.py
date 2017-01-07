#File contains functions for the different playbooks added
#to the enviroment
#
#Change by making base fucntion for each and add ontop (how best?)
from config import pkey_location
import getpass
######UTILITY FUNCTIONS######
def password_read(password, stdout, stderr, stdin):
	stdin.write(password+'\n')
	stdin.flush()
	output = stdout.readlines()
	error = stdout.readlines()
	for line in error:
		print(line)
	for line in output:
		print(line)
#Base linux playbook info
def linux_base(playbook, *args):
	playbook = playbook+'.yml' #name of book on server
	if len(args) == 1:
		password,playbook = args[0]
		return password
	else:
		password = getpass.getpass('Enter become pass > ')
	return password, playbook

def windows_base(playbook, *args):
	playbook = playbook+'.yml' 
	if len(args) == 1:
		password = args[0]
		return password, playbook
	else:
		dapass='"' #domain user password "" for passwords that have spaces in them
		password = getpass.getpass('Enter local admin pass > ')
		domainadmin = input('Enter domain admin account > ')
		dapass = dapass+getpass.getpass('Enter DA password > ')
		dapass = dapass+'"'
		return password,playbook, domainadmin ,dapass
	

#######PLAYBOOK RUNNING FUNCTIONS########
def server_deploy(ssh, pcname , computer, playbook, *args): #for base server_deploy.yml playbook
	if len(args) == 1:
		password,playbook = linux_base(playbook, args[0])
	else: 
		print('test')
		password,playbook = linux_base(playbook)
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def jenkins_server(ssh, pcname, computer, playbook, *args): #for base jenkins_server.yml playbook
	password, playbook = linux_base(playbook,args[0])
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def jenkins_node(ssh,pcname,computer,playbook, *args):
	password, playbook = linux_base(playbook, args[0])
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)
	
def graylog_selfnode(ssh, pcname, computer, playbook, *args): #for base jenkins_server.yml playbook
	passsword, playbook = linux_base(playbook, args[0])
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def domain_con(ssh, pcname, computer, playbook, *args): #for base jenkins_server.yml playbook
	password, playbook, domainadmin, dapass = windows_base(playbook)
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass))
	password_read(password, stdout, stderr, stdin)

def windows_common(ssh, pcname, computer, playbook, *args): #for base jenkins_server.yml playbook
	if len(args) == 1:
		password, playbook = windows_base(playbook,args[0])
		stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer))
	else:
		password, playbook, domainadmin, dapass = windows_base(playbook)
		stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass))
	password_read(password, stdout, stderr, stdin)