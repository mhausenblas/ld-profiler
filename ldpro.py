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
import StringIO
import datetime
from timeit import Timer
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

	def setup(self, ldid):
		print("Parsing [%s] for Linked Data interface description ..." %ldid)
		self.load_ldid(ldid)
		self.status_dump()
		
	def profile_examples(self):
		for ex in self.examples:
			g = Graph()
			self.load_example(g, example_URI=ex)
			if g:
			 	print(g.serialize(format='n3'))

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

	def status_dump(self):
		print('='*80 + '\n')
		print("I'm currently working with following Linked Data interface description:\n")
		print(" Dataset: %s\n" %self.ds_uri)
		print(" Title: %s\n" %self.title)
		print(" Description: %s\n" %self.description)
		print(" SPARQL End point: %s\n" %self.sparl_ep)
		print(" Example resources:")
		for ex in self.examples:
			print("  + %s" %ex)
		print('\n' + '='*80 + '\n')

	def usage(self):
		print("Usage: python ldpro.py -l {path to Linked Data interface description file} ")
		print("Example: python ldpro.py -l test/ldid-dbpedia.ttl")

if __name__ == "__main__":
	ldpro = LinkedDataProfiler()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hl:", ["help", "ldid"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				ldpro.usage()
				sys.exit()
			elif opt in ("-l", "--ldid"):
				ldpro.setup(arg)
				print Timer("ldpro.profile_examples", "from __main__ import ldpro").timeit(number=100)
				pass
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)