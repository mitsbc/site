#!/usr/bin/env python
from bs4 import BeautifulSoup
import ldap, json, os, requests
import ldap.filter

def get_mit_info(email):
		username = email[:email.find("@")]
		url = "http://web.mit.edu/bin/cgicso?options=general&query=%s" % (username)
		r = requests.get(url)
		html = r.text
		soup = BeautifulSoup(html)
		pre = soup.find("pre")
		if pre.text.find("No matches") == -1:
			l = [[y.strip() for y in x.split(":")] for x in pre.text.split("\n")]
			return {x[0]:x[1] for x in l if len(x) is 2}

def ldap_fetch(username):
	name,mail,number = ("",)*3

	con = ldap.open('ldap-too.mit.edu')
	con.simple_bind_s("", "")
	dn = "dc=mit,dc=edu"
	fields = ['cn', 'sn', 'givenName', 'mail', 'telephoneNumber']
	userfilter = ldap.filter.filter_format('uid=%s', [username])
	results = con.search_s('dc=mit,dc=edu', ldap.SCOPE_SUBTREE, userfilter, fields)[0][1]

	try:
		name = results['givenName'][0] + " " + results['sn'][0]
	except:
		pass
	try:
		mail = results['mail'][0]
	except:
		pass
	try:
		number = results['telephoneNumber'][0]
	except:
		pass

	return name,mail,number

try:
	id_email = os.getenv("SSL_CLIENT_S_DN_Email").lower()
	username = id_email.split("@")[0]
	name,mail,number = ldap_fetch(username)
except Exception:
	name,mail,number = ("",)*3

try:
	d = get_mit_info(mail)
except:
	d = {}

d.update({"name": name, "email": mail, "phone": number})

print "Access-Control-Allow-Origin: http://mitsbc.mit.edu"
print "Content-type: application/json"
print
print json.dumps(d)
