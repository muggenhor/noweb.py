#!/usr/bin/env python

#
# noweb.py
# By Jonathan Aquino (jonathan.aquino@gmail.com)
#
# This program extracts code from a literate programming document in "noweb" format.
# It was generated from noweb.py.txt, itself a literate programming document.
# For more information, including the original source code and documentation,
# see http://jonaquino.blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html
#

import argparse
import re
parser = argparse.ArgumentParser('NoWeb command line options.')
parser.add_argument('-R', '--chunk',  dest='chunk_name', metavar='CHUNK', required=True,                            help='name of chunk to write to stdout')
parser.add_argument('infile',                            metavar='FILE',  type=argparse.FileType('r'),              help='input file to process, "-" for stdin')
parser.add_argument('-o', '--output', dest='outfile',    metavar='FILE',  type=argparse.FileType('w'), default='-', help='file to output to, "-" for stdout')

args = parser.parse_args()
chunk_re         = re.compile(r'<<(?P<name>[^>]+)>>')
chunk_def        = re.compile(chunk_re.pattern + r'=')
chunk_at         = re.compile(r'^@@(?=\s|$)')
chunk_end        = re.compile(r'^@(?=\s|$)')
chunk_invocation = re.compile(r'^(?P<indent>\s*)' + chunk_re.pattern + r'\s*$')

chunkName = None
chunks = {}

for line in args.infile:
    match = chunk_def.match(line)
    if match:
        chunkName = match.group('name')
        chunks[chunkName] = []
    else:
        if chunk_end.match(line):
            chunkName = None
        elif chunkName:
            line = chunk_at.sub('@', line)
            chunks[chunkName].append(line)

def expand(chunkName, indent=""):
    for line in chunks[chunkName]:
        match = chunk_invocation.match(line)
        if match:
            for line in expand(match.group('name'), indent + match.group('indent')):
                yield line
        else:
            yield indent + line

for line in expand(args.chunk_name):
    args.outfile.write(line)
