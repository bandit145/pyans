menu = '''
[>] WELCOME TO THE HOMELAB [<]
[>]1.DEPLOY MACHINE        [<] 
[>]2.LIST ANSIBLE PLAYBOOKS[<]
[>]3.CHECK INVENTORY       [<]
[>]4.RUN PLAYBOOK          [<]
[>]5.EXIT                  [<]
         	'''
server_pass=''#not in use currently
username='phil'
ans_server='192.168.1.14'
priv_key_file='E:/github/pyans/puttyansible'
ans_playbooklocation='/home/server/'
monitoring_location='sensu.meme.com:4567'
pkey_location='/home/phil/ansible_keys/anspriv'
vcenter = 'vcenter.meme.com'
windows_template = 'winserver2012'
linux_template = 'debian-server'