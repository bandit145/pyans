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
def linux_base(playbook):
	playbook = playbook+'.yml' #name of book on server
	password = getpass.getpass('Enter become pass > ')
	return password, playbook

def windows_base(playbook):
	playbook = playbook+".yml"
	dapass='"' #domain user password "" for passwords that have spaces in them
	password = getpass.getpass('Enter admin pass > ')
	domainadmin = input('Enter domain admin account > ')
	dapass = dapass+getpass.getpass('Enter DA password > ')
	dapass = dapass+'"'
	return password,playbook, domainadmin ,dapass
	

#######PLAYBOOK RUNNING FUNCTIONS########
def server_deploy(ssh, pcname , computer, playbook, admin): #for base server_deploy.yml playbook
	password,playbook = linux_base(playbook)
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def jenkins_server(ssh, pcname, computer, playbook, admin): #for base jenkins_server.yml playbook
	password, playbook = linux_base(playbook)
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def jenkins_node(ssh,pcname,computer,playbook, admin):
	password, playbook = linux_base(playbook)
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)
	
def graylog_selfnode(ssh, pcname, computer, playbook, admin): #for base graylog_selfnode.yml playbook
	passsword, playbook = linux_base(playbook)
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location))
	password_read(password, stdout, stderr, stdin)

def domain_con(ssh, pcname, computer, playbook,admin): #for base jenkins_server.yml playbook
	password, playbook, domainadmin, dapass = windows_base(playbook)
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass} remote_user={admin}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass, admin=admin))
	password_read(password, stdout, stderr, stdin)

def windows_common(ssh, pcname, computer, playbook, admin): #for base jenkins_server.yml playbook
	password, playbook, domainadmin, dapass = windows_base(playbook)
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass} remote_user={admin}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass, admin=admin))
	password_read(password, stdout, stderr, stdin)

def scheduled_windows(ssh, pcname, computer, playbook, admin): #for base jenkins_server.yml playbook
	password, playbook, domainadmin, dapass = windows_base(playbook)
	stdin, stdout, stderr= ssh.exec_command("ansible-playbook {playbook} -i {hosts}, --extra-vars 'name={name} winadmin={user} password={loginpass} remote_user={admin}' --ask-pass --connection=winrm -e ansible_winrm_server_cert_validation=ignore".format(playbook=playbook,hosts=computer, name=pcname, user=domainadmin, loginpass=dapass, admin=admin))
	password_read(password, stdout, stderr, stdin)


def sensu_server(ssh, pcname , computer, playbook, admin): #for base sensu_server.yml playbook
	password,playbook = linux_base(playbook)
	dash_pass = getpass.getpass('Enter uchiwa dashboard password > ')
	stdin, stdout, stderr= ssh.exec_command('ansible-playbook {playbook} -i {hosts}, --extra-vars "host_name={name} dash_pass={dash_pass}" --ask-become-pass --private-key {pkey}'.format(playbook=playbook, hosts=computer, name=pcname, pkey=pkey_location, dash_pass=dash_pass))
	password_read(password, stdout, stderr, stdin)
