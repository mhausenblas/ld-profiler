"""
The handler script.

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-07-13
@status: first stab
"""
import sys
import os
sys.path.insert(0, os.getcwd() + 'lib/')
import getopt
import logging

import platform
import urllib
import urllib2
import uuid
import StringIO
import datetime
import stopwatch
import rdflib
from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef
from rdflib import Literal
from rdflib import RDF
from rdflib import XSD
from rdflib.plugin import PluginException
from SPARQLWrapper import SPARQLWrapper, JSON

rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

class LinkedDataProfiler(object):
	
	DEBUG = False
	
	WORK_DIR = 'tmp/'
	
	NAMESPACES = { 'void' : Namespace('http://rdfs.org/ns/void#'), 'dc' : Namespace('http://purl.org/dc/terms/') }

	LDID_QUERY = """SELECT * WHERE { 
					?ds a void:Dataset ; 
						dc:title ?title; 
						dc:description ?description; 
						OPTIONAL { ?ds void:sparqlEndpoint ?sparqlep . }
						OPTIONAL { ?ds void:exampleResource ?example . } 
	}"""
	
	def __init__(self):
		self.g = Graph()
		self.g.bind('void', LinkedDataProfiler.NAMESPACES['void'], True)
		self.g.bind('dc', LinkedDataProfiler.NAMESPACES['dc'], True)
		self.timr = { 'examples' : {}, 'sparql' : [] }

	def setup(self, ldid):
		if LinkedDataProfiler.DEBUG: print("Parsing [%s] for Linked Data interface description ..." %ldid)
		self.load_ldid(ldid)
		if not os.path.exists(LinkedDataProfiler.WORK_DIR):
			os.makedirs(LinkedDataProfiler.WORK_DIR)

	def profile_all(self, number_of_runs = 1):
		for ex in self.examples:
			runs = []
			for r in range(number_of_runs):
				runs.append(ldpro.profile_example(ex))
			self.timr['examples'][ex] = runs

	def profile_example(self, ex):
		g = Graph()
		sys.stdout.write('.')
		sys.stdout.flush()
		t = stopwatch.Timer()
		self.load_example(g, example_URI=ex)
		t.stop()
		
		file_name = ''.join([LinkedDataProfiler.WORK_DIR, ex.split('/')[-1], '.ttl'])
		self.store_example(g, file_name)
		return t

	def load_example(self, g, example_URI):
		if example_URI.endswith('.rdf'):
			g.parse(location = example_URI)
		elif example_URI.endswith('.ttl') or example_URI.endswith('.n3') :
			g.parse(location = example_URI, format="n3")
		elif example_URI.endswith('.nt'):
			g.parse(location = example_URI, format="nt")
		elif example_URI.endswith('.html'):
			g.parse(location = example_URI, format="rdfa")
		else:
			g.parse(location = example_URI)

	def store_example(self, g, filename):
		ex_file = open(filename, 'w')
		ex_file.write(g.serialize(format='n3'))
		ex_file.close()
		
	def load_ldid(self, file_name):
		self.g.parse(file_name, format='n3')
		res = self.g.query(LinkedDataProfiler.LDID_QUERY, initNs=LinkedDataProfiler.NAMESPACES)
		self.examples = []
		for r in res.bindings:
			if r['ds']: self.ds_uri = r['ds']
			if r['title']: self.title = r['title']
			if r['description']: self.description = r['description']
			try:
				if r['sparqlep']:
					self.sparl_ep = r['sparqlep']
			except KeyError:
				pass
			try:
				if r['example']:
					self.examples.append(r['example'])
			except KeyError:
				pass

	def check(self):
		print('='*80 + '\n')
		print("I found the following Linked Data interface description:\n")
		print(" Dataset: %s\n" %self.ds_uri)
		print(" Title: %s\n" %self.title)
		print(" Description: %s\n" %self.description)
		print(" SPARQL End point: %s\n" %self.sparl_ep)
		print(" Example resources:")
		for ex in self.examples:
			print("  + %s" %ex)
		print('\n' + '='*80 + '\n')
		
	def report(self):
		print('\n' + '='*80 + '\n')
		print("Results for example resources:\n")
		for ex in self.examples:
			print(" Dereferencing %s\n" %ex)
			i = 0
			values = []
			for t in self.timr['examples'][ex]:
				print("  Run %s: %sms" %(i, t.elapsed))
				i = i + 1
				values.append(t.elapsed)
			print('  ' +'-'*25)
			average = float(sum(values)) / len(values)
			print("  Average: %sms" %average)
			
			print("")
		print('\n' + '='*80 + '\n')

	def usage(self):
		print("Usage: python ldpro.py -l {path to Linked Data interface description file} [number of runs (optional, defaults to 3)]")
		print("Example: python ldpro.py -l test/ldid-dbpedia.ttl")

if __name__ == "__main__":
	ldpro = LinkedDataProfiler()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hl:c:", ["help", "ldid", "check"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				ldpro.usage()
				sys.exit()
			elif opt in ("-l", "--ldid"):
				ldpro.setup(arg)
				try:
					number_of_runs = args[0]
				except:
					number_of_runs = 3 # default number of runs if not specified by user
				ldpro.profile_all(int(number_of_runs))
				ldpro.report()
			elif opt in ("-c", "--check"):
				ldpro.setup(arg)
				ldpro.check()
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)