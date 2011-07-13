"""
The handler script.

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-07-13
@status: first stab
"""
import sys
sys.path.insert(0, 'lib')
import getopt
import logging
import os
import platform
import urllib
import urllib2
import StringIO
import datetime
import rdflib
from rdflib import Graph
from rdflib import Namespace
from rdflib import plugin
from rdflib.serializer import Serializer

class LinkedDataProfiler(object):

	def profile_it(self, ldid):
		print("Parsing [%s] for Linked Data interface description..." %ldid)

	def usage(self):
		print("Usage: python ldpro.py -l {path to Linked Data interface description file} ")
		print("Example: python ldpro.py -l lidl0.ttl")

if __name__ == "__main__":
	ldpro = LinkedDataProfiler()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hl:", ["help", "ldid"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				ldpro.usage()
				sys.exit()
			elif opt in ("-l", "--ldid"):

				ldpro.profile_it(arg)
				pass
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)