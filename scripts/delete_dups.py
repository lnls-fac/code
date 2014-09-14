#!/usr/bin/python

import subprocess
import sys
import os

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
    	OKGREEN = '\033[92m'
    	WARNING = '\033[93m'
    	FAIL = '\033[91m'
    	ENDC = '\033[0m'
	@staticmethod 
	def purple(string):
		return bcolors.HEADER + string + bcolors.ENDC
	@staticmethod 
	def blue(string):
		return bcolors.OKBLUE + string + bcolors.ENDC		
	@staticmethod 
	def green(string):
		return bcolors.OKGREEN + string + bcolors.ENDC		
	@staticmethod 
	def yellow(string):
		return bcolors.WARNING + string + bcolors.ENDC		
	@staticmethod 
	def red(string):
		return bcolors.FAIL + string + bcolors.ENDC		



def get_size_str(size):
	if size < 1024:
		return '{0} bytes'.format(size)
	elif size < 1024*1024:
		return '{0:.1f} Kb'.format(1.0*size/1024.0)
	elif size < 1024*1024*1024:
		return '{0:.1f} Mb'.format(1.0*size/1024.0/1024.0)
	else:
		return '{0:.1f} Gb'.format(1.0*size/1024.0/1024.0/1024.0)

def grab_duplicates(folder, pname):

	try:
		p = subprocess.Popen(['fdupes', '-r', '-S', folder], 
			stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE)
	except OSError:
		print(''.join([pname, ': could not run fdupes command! Is package installed?']))
		sys.exit()
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode

	lines = output.split('\n')
	sizes, files = [],[]
	size = None
	for line in lines:
		if 'bytes each:' in line:
			if size is not None:
				sizes.append(size)
				files.append(dupfiles)
			words = line.split(' ')
			size = int(words[0])
			dupfiles = []
		elif len(line)>0:
			dupfiles.append(line)
	if size is not None:
		sizes.append(size)
		files.append(dupfiles)

	idx = sorted(range(len(sizes)), key=lambda k: sizes[k]*(len(files[k])-1), reverse = True)
	dups = [(sizes[i],files[i]) for i in idx]
	return dups



def select_files_simple(dups):

	size = 0
	for dup in dups:
		print(bcolors.yellow('size of each file: ' + get_size_str(dup[0])))
		for fname in dup[1]:
			print(fname)
		size += dup[0] * (len(dup[1]) - 1)
		print('')
	print(bcolors.yellow('selection has ' + get_size_str(size) + ' of duplicates.'))

def select_files_substring(dups, substring):

	size = 0
	files = []
	for dup in dups:
	
		''' checks how many of duplicate files are selected '''
		nr_included = 0
		for fname in dup[1]:
			if substring in fname:
				nr_included += 1
		if nr_included == 0:
			continue

		''' loops over files of duplicates that has at least one selection '''
		print(bcolors.yellow('size of each file: ' + get_size_str(dup[0])))					
		for fname in dup[1]:
			if substring in fname:
				print(bcolors.blue(fname))
				files.append(fname)
				size += dup[0]
			else:
				print(fname)

		''' in case all duplicate files are selected warns and exits '''
		if nr_included == len(dup[1]):
			print('')
			print(bcolors.red('selection of all files in duplicate is not allowed!'))
			sys.exit()

		print('')

	''' prints size of selection and returns list '''
	print(bcolors.yellow('selection has ' + get_size_str(size) + ' of duplicates.'))
	return files


def main():

	pname = sys.argv[0]
	folder = sys.argv[1]
	dups = grab_duplicates(folder, pname)
	
	if len(sys.argv) == 2:
		select_files_simple(dups)
	elif len(sys.argv) == 3:
		substring = sys.argv[2]
		substring = substring.strip('"')
		files = select_files_substring(dups, substring)
	elif (len(sys.argv) == 4) and (sys.argv[3] == 'delete'):
		substring = sys.argv[2]
		files = select_files_substring(dups, substring)
		for fname in files:
			os.remove(fname)


main()

	
