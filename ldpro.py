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
from rdflib import URIRef
from rdflib import Literal
from rdflib import RDF
from rdflib import XSD
from rdflib.plugin import PluginException
from SPARQLWrapper import SPARQLWrapper, JSON

rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

class LinkedDataProfiler(object):
	
	NAMESPACES = {	'void' : Namespace('http://rdfs.org/ns/void#'),
					'dcterms' : Namespace('http://purl.org/dc/terms/')
	}
	
	def __init__(self):
		self.g = Graph()
		self.g.bind('void', LinkedDataProfiler.NAMESPACES['void'], True)
		self.g.bind('dcterms', LinkedDataProfiler.NAMESPACES['dcterms'], True)

	def profile_it(self, ldid):
		print("Parsing [%s] for Linked Data interface description ..." %ldid)
		self.load_ldid(ldid)
		self.status_dump()
		
	def load_ldid(self, file_name):
		"""Loads the Linked Data interface description in VoID format from a file.
		"""
		self.g.parse(file_name, format='n3')
		querystr = """	SELECT * 
						WHERE { 
							?ds a void:Dataset ; 
								dcterms:title ?title; 
								OPTIONAL { ?ds void:sparqlEndpoint ?sparqlep . }
								OPTIONAL { ?ds void:exampleResource ?example . } 
						}
		"""
		res = self.g.query(querystr, initNs=LinkedDataProfiler.NAMESPACES)
		self.examples = []
		for r in res.bindings:
			if r['ds']: self.ds_uri = r['ds']
			if r['title']: self.title = r['title']
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
		print("Working with following Linked Data interface description:")
		print("Dataset: %s" %self.ds_uri)
		print("Title: %s" %self.title)
		print("SPARQL End point: %s" %self.sparl_ep)
		print("Example resources:")
		for ex in self.examples:
			print(" %s" %ex)

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
				ldpro.profile_it(arg)
				pass
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)