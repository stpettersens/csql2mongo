#!/usr/bin/env jython
"""
csql2mongo
Utility to convert an SQL dump to a MongoDB JSON dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Tweaked for Jython.
"""
import sys
import os
import re
import getopt

signature = 'csql2mongo 1.0.1 [Jython] (https://github.com/stpettersens/csql2mongo)'

def displayVersion():
	print('\n' + signature);

def displayInfo():
	print(__doc__)

def csql2mongo(file, out, tz, verbose, version, info):

	if len(sys.argv) == 1:
		displayInfo()
		sys.exit(0)

	if file == None and out == None:
		if verbose == False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayVersion()

		sys.exit(0)

	if out == None: out = re.sub('.sql', '.json', file)

	if file.endswith('.sql') == False:
		print('File provided is not an SQL dump.')
		sys.exit(1)

	head, tail = os.path.split(file)
	collection = re.sub('.sql', '', tail)

	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	# Preprocess SQL dump so that is compatible for conversion.
	processed_lines = []
	for line in lines:
		l = line.lstrip()
		if l.startswith('--') or l.startswith('/*'): continue # Strip out comments.
		l = re.sub('VALUES \(', 'VALUES (\n', l)
		l = re.sub(',', ',\n', l)
		l = re.sub('\),', ')\nINSERT INTO `null` VALUES (\n', l)
		l = re.sub('\n\n', '\n', l)
		processed_lines.append(l);
	processed_lines = ''.join(processed_lines).split('\n')
	lines = []
	x = 0
	while x < len(processed_lines):
		processed_lines[x] = processed_lines[x].lstrip('(')
		x = x + 1

	fields = []
	inserts = []
	headers = False
	for line in processed_lines:

		pattern = re.compile('CREATE TABLE|UNLOCK TABLES')
		if pattern.match(line):
			headers = True

		m = re.search('(^[\`a-z0-9_]+)', line)
		if m and headers: 
			f = m.group(1)
			f = re.sub('\`', '', f)
			fields.append(f)
			
		pattern = re.compile('INSERT INTO')
		if pattern.match(line):
			headers = False

		m = re.search('(^[\d\"\'a-zA-Z\_\.][^(DROP)][^(INSERT)][^\n|,|)]+)', line)
		if m and headers == False:
			value = m.group(1)

			pattern = re.compile('\'[\d\w]{24}\'')
			if pattern.match(value):
				value = '{"$oid":' + value + '}'

			pattern = re.compile('\'\d{4}\-\d{2}\-\d{2}')
			if pattern.match(value):
				value = re.sub('\s', 'T', value)
				value = value[:-1]
				value += '.000'
				if tz: value += 'Z\''
				else: value += '+0000\''
				value = '{"$date":' + value + '}'

			inserts.append(value)

	fn = len(fields)
	x = 0
	rrecords = []
	inserts = ['@@'.join(inserts[i:i+fn]) for i in range(0, len(inserts), fn)]

	for insert in inserts:
		records = insert.split('@@')
		x = 0

		a_fields = []
		for record in records:
			for field in fields:
				a_fields.append(field)
		
		for record in records:
			r = '"' + a_fields[x] + '":' + record
			r = re.sub('\'', '"', r)
			rrecords.append(r)
			x = x + 1

	rrecords = ['@@'.join(rrecords[i:i+fn]) for i in range(0, len(rrecords), fn)]

	if verbose:
		print('\nGenerating MongoDB JSON dump file: \'%s\' from\nSQL dump file: \'%s\''
		% (out, file))

	f = open(out, 'w')
	for record in rrecords:
		record = re.sub('@@', ',', record)
		record = '{' + record + '}'
		f.write(record + '\n')

	f.close()


# Handle any command line arguments.
try:
	opts, args = getopt.getopt(sys.argv[1:], "f:o:tlvi")
except:
	print('Invalid option or argument.')
	displayInfo()
	sys.exit(2)

file = None
out = None
tz = False
verbose = False
version = False
info = False
for o, a in opts:
	if o == '-f':
		file = a
	elif o == '-o':
		out = a
	elif o == '-t':
		tz = True
	elif o == '-l':
		verbose = True
	elif o == '-v':
		version = True
	elif o == '-i':
		info = True
	else:
		assert False, 'unhandled option'

csql2mongo(file, out, tz, verbose, version, info)