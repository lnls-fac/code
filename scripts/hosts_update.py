#!/usr/bin/env python3

import subprocess
import os
import sys

def get_ip_address():
	output = subprocess.check_output(['ifconfig'])
	text   = output.decode('utf-8')
	lines  = text.split('\n')
	for line in lines:
		line = line.strip()
		if ('inet addr' in line) and ('127.0.0' not in line):
			words = line.split(' ')
			ip_address = words[1].replace('addr:','')
	return ip_address


def get_hostname():
	output = subprocess.check_output(['cat', '/etc/hostname'])	
	text   = output.decode('utf-8')
	lines  = text.split('\n')
	return lines[0].strip()


def import_hosts():

	hostname   = get_hostname()
	output = subprocess.check_output(['ssh', 'lnls82-linux', 'cat /etc/hosts'])
	text  = output.decode('utf-8')
	lines = text.split('\n')
	new_text = []
	for line in lines:
		line = line.strip()
		if ('lnls82-linux' in line) and ('127.0.1.1' in line):
			line = '#' + line
		if (hostname in line) and ('127.0.1.1' in line):
			line = line[1:]
		new_text.append(line)

	return new_text

def save_hosts(text):

	fp = open('/etc/hosts','w')
	for line in text:
		fp.write(line + '\n')

hosts = import_hosts()
save_hosts(hosts)


