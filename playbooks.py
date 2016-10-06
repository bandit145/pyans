#File contains functions for the different playbooks added
#to the enviroment
#

def server_deploy(): #for base serverdeploy.yml playbook
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