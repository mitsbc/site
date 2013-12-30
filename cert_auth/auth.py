#!/usr/bin/env python
import ldap, json, os
import ldap.filter

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


print "Access-Control-Allow-Origin: http://mitsbc.mit.edu"
print "Content-type: application/json"
print
print json.dumps({"name": name, "email": mail, "phone": number})
