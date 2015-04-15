#!/usr/bin/env python
"""
csql2mongo
Utility to convert a SQL dump to a MongoDB JSON dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Use -h switch for usage information.
"""
import sys
import os
import re
import argparse

signature = 'csql2mongo 1.0 (https://github.com/stpettersens/csql2mongo)'

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

	head, tail = os.path.split(file)
	collection = re.sub('.sql', '', tail)

	f = open(file, 'r')
	lines = f.readlines()
	f.close()

	fields = []
	inserts = []
	headers = False
	id = False
	for line in lines:

		pattern = re.compile('CREATE TABLE')
		if pattern.match(line):
			headers = True

		pattern = re.compile('_id')
		if pattern.match(line):
			fields.append('_id')
			id = True
		
		m = re.search('(^[a-z0-9_]+)', line)
		if m and headers and id == False: 
			fields.append(m.group(1))

		pattern = re.compile('INSERT INTO')
		if pattern.match(line):
			headers = False

		m = re.search('(^[\d\"\'a-zA-Z\_\.][^DROP][^INSERT][^\n|,|)]+)', line)
		if m and headers == False and id == False:
			value = m.group(1)

			pattern = re.compile('\'\d{3}\w{3}\d{3}')
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

		id = False

	fn = len(fields)
	rrecords = []
	inserts = ['§'.join(inserts[i:i+fn]) for i in range(0, len(inserts), fn)]
	for insert in inserts:
		records = insert.split('§')
		x = 0
		
		for field in fields:
			record = '"' + field + '":' + records[x]
			record = re.sub('\'', '"', record)
			rrecords.append(record)
			x = x + 1

	rrecords = ['§'.join(rrecords[i:i+fn]) for i in range(0, len(rrecords), fn)]

	if verbose:
		print('\nGenerating MongoDB JSON dump file: \'{0}\' from\nSQL dump file: \'{1}\''
		.format(out, file))

	f = open(out, 'w')
	for record in rrecords:
		record = re.sub('§', ',', record)
		record = '{' + record + '}'
		f.write(record + '\n')

	f.close()


# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to convert a SQL dump to a MongoDB JSON dump.')
parser.add_argument('-f', '--file', action='store', dest='file', metavar="FILE")
parser.add_argument('-o', '--out', action='store', dest='out', metavar="OUT")
parser.add_argument('-t', '--tz', action='store_true', dest='tz')
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

csql2mongo(argv.file, argv.out, argv.tz, argv.verbose, argv.version, argv.info)
