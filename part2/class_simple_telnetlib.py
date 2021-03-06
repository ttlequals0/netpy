#!/usr/bin/env python
'''
Script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command as a claass.
'''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6 

class TelnetConn(object):
	'''
	Establish telnet connection to network device
	'''
	def __init__(self, ip_addr, username, password):
		self.ip_addr = ip_addr
		self.username = username
		self.password = password

		try:
			self.remote_conn = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
		except socket.timeout:
			sys.exit("Connection timeout")

	def login(self):
		'''
		login to network device
		'''
		output = self.remote_conn.read_until("sername:", TELNET_TIMEOUT)
		self.remote_conn.write(self.username + "\n")
		output += self.remote_conn.read_until("ssword", TELNET_TIMEOUT)
		self.remote_conn.write(self.password + "\n")
		time.sleep(1)
		return output

	def send_command(self, cmd="\n", sleep_time=1):
		'''
		send command over telnet
		return response
		'''

		cmd = cmd.strip()
		self.remote_conn.write(cmd + "\n")
		time.sleep(sleep_time)
		return self.remote_conn.read_very_eager()


	def disable_paging(self, paging_cmd='terminal length 0'):
		'''
		disable the paging of output
		'''
		return self.send_command(paging_cmd)


	def close_conn(self):
		'''
		close remote connection
		'''
		self.remote_conn.close()


def main():
	'''
	Script that connects to router and runs 
	'show ip in brief.
	'''
	ip_addr = raw_input("IP address: ")
	ip_addr = ip_addr.strip()
	username = 'pyclass'
	password = getpass.getpass()

	my_conn = TelnetConn(ip_addr, username, password)
	my_conn.login()
	my_conn.send_command()
	my_conn.disable_paging()
	output = my_conn.send_command('show ip int brief')

	print "\n\n"
	print output
	print "\n\n"

	my_conn.close_conn()
	
if __name__ == "__main__":
	main()

