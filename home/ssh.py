import paramiko, base64, os

def subscribe(email):
	pubkey = "AAAAB3NzaC1yc2EAAAABIwAAAIEAyIC4b705cYi5ppJuGvojY1Ux7zbWDUjAXBEPjpXY9uK2FqYLDNGL0wnSOD2l55M8GX+3Ks3/eJVvQFegOt3tzZRkfi52TPAE0FRF/zbi7nnODNSf/kHhuwQwHJCTAhDIujhgXAgscIIY/tvllVyCrKEuWRAk58c5zAM4juS+MlM="
	paramiko_pubkey = paramiko.RSAKey(data=base64.b64decode(pubkey))
	client = paramiko.SSHClient()
	print os.environ['ssh_host']
	client.get_host_keys().add(os.environ['ssh_host'], 'ssh-rsa', paramiko_pubkey)
	client.connect(os.environ['ssh_host'], username=os.environ['ssh_user'], password=base64.b64decode(os.environ['ssh_pass']))
	client.exec_command('blanche sbc-web-subscribe -add '+email)
	client.close()