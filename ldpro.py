"""
The handler script.

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-07-13
@status: fixed issues
"""
import sys
import os
sys.path.insert(0, os.getcwd() + '/lib/rdflib')
sys.path.insert(0, os.getcwd() + '/lib/rdfextras')
sys.path.insert(0, os.getcwd() + '/lib')
import getopt
import platform
import urllib
import urllib2
import uuid
import StringIO
import datetime
import time
import stopwatch
import rdflib
from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef
from rdflib import Literal
from rdflib import RDF
from rdflib import XSD
from rdflib.plugin import PluginException
from SPARQLWrapper import SPARQLWrapper

rdflib.plugin.register('sparql', rdflib.query.Processor, 'sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'sparql.query', 'SPARQLQueryResult')

class LinkedDataProfiler(object):
	
	DEBUG = False
	
	WORK_DIR = 'tmp/'
	
	NAMESPACES = {	'void' : Namespace('http://rdfs.org/ns/void#'), 
					'dc' : Namespace('http://purl.org/dc/terms/') 
	}

	LDID_QUERY = """SELECT ?ds ?title ?description ?sparqlep ?example WHERE { 
					?ds a void:Dataset ; 
						dc:title ?title; 
						dc:description ?description; 
						OPTIONAL { ?ds void:sparqlEndpoint ?sparqlep . }
						OPTIONAL { ?ds void:exampleResource ?example . } 
	}"""
	
	SPARQL_EP_QUERIES = {	'Q1' : 'SELECT ?s WHERE { ?s ?p ?o . } LIMIT 1',
							'Q2' : 'SELECT ?s WHERE { ?s a ?o . } LIMIT 1',
							'Q3' : 'SELECT ?s ?p ?o WHERE { ?s ?p ?o . FILTER( isURI(?o)) } LIMIT 1',
							'Q4' : 'SELECT ?s ?p ?o WHERE { ?s ?p ?o . FILTER( isLITERAL(?o)) } LIMIT 1',
							'Q5' : 'SELECT ?s1 WHERE { ?s1 ?p1 ?o1 . ?o1 ?p2 ?o2 . } LIMIT 1',
							'Q6' : 'SELECT ?s1 WHERE { ?s1 ?p1 ?o1 . ?o1 ?p2 ?o2 . FILTER( isURI(?o1)) } LIMIT 1'
	}
	
	
	def __init__(self):
		self.g = Graph()
		self.g.bind('void', LinkedDataProfiler.NAMESPACES['void'], True)
		self.g.bind('dc', LinkedDataProfiler.NAMESPACES['dc'], True)
		self.timr = { 'examples' : {}, 'sparql' : {} }

	def setup(self, ldid):
		if LinkedDataProfiler.DEBUG: print("Parsing [%s] for Linked Data interface description ..." %ldid)
		self.load_ldid(ldid)
		# if not os.path.exists(LinkedDataProfiler.WORK_DIR):
		# 	os.makedirs(LinkedDataProfiler.WORK_DIR)

	def profile_all(self, number_of_runs = 1):
		# profile all void:exampleResource ...
		if len(self.examples) > 0:
			print self.examples
			for ex in self.examples:
				runs = []
				for r in range(number_of_runs):
					runs.append(self.profile_example(ex))
					time.sleep(1) # politeness - wait 1s between each run
				self.timr['examples'][ex] = runs
			
		# profile the void:sparqlEndpoint ...
		for q in LinkedDataProfiler.SPARQL_EP_QUERIES:
			timing = []
			result = []
			for r in range(number_of_runs):
				(tim, res) = self.profile_sparql(LinkedDataProfiler.SPARQL_EP_QUERIES[q])
				timing.append(tim)
				result.append(res)
				time.sleep(1) # politeness - wait 1s between each run
			self.timr['sparql'][q] = {}
			self.timr['sparql'][q]['timing'] = timing
			self.timr['sparql'][q]['result'] = result

	def profile_sparql(self, query_str):
		sys.stdout.write('.')
		sys.stdout.flush()
		t = stopwatch.Timer()
		res = self.query_SPARQL_Endpoint(self.sparl_ep, query_str)
		t.stop()
		if LinkedDataProfiler.DEBUG: print("HTTP metadata: [%s]" %res)
		return (t, res)
	
	def query_SPARQL_Endpoint(self, endpoint_URI, query_str):
		try:
			sparql = SPARQLWrapper(endpoint_URI)
			sparql.setQuery(query_str)
			results = sparql.query().info()
			return results
		except Exception, e:
			if LinkedDataProfiler.DEBUG: print('I was not able to execute the SPARQL query against %s\nReason: %s' %(endpoint_URI,e))

	def profile_example(self, ex):
		g = Graph()
		sys.stdout.write('.')
		sys.stdout.flush()
		t = stopwatch.Timer()
		self.load_example(g, example_URI=ex)
		t.stop()
		# file_name = ''.join([LinkedDataProfiler.WORK_DIR, ex.split('/')[-1], '.ttl'])
		# self.store_example(g, file_name)
		return t

	def load_example(self, g, example_URI):
		# TODO: Accept RDF and follow redirects
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
		# ?ds ?title ?description ?sparqlep ?example
		for r in res:
			self.ds_uri = str(r[0])
			self.title = str(r[1])
			self.description = str(r[2])
			try:
				if r[3]:
					self.sparl_ep = str(r[3])
			except KeyError:
				pass
			try:
				if r[4]:
					self.examples.append(str(r[4]))
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
		
		print("I. Results for example resources\n")
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
		
		print("II. Results for SPARQL end point\n")
		print(" Executing queries against %s\n" %self.sparl_ep)
		
		for q in LinkedDataProfiler.SPARQL_EP_QUERIES:
			i = 0
			values = []
			print(" Query: %s\n" %(LinkedDataProfiler.SPARQL_EP_QUERIES[q]))
			for res in self.timr['sparql'][q]['result']:
				if res:
					t = self.timr['sparql'][q]['timing'][i]
					print("  Run %s: %sms" %(i, t.elapsed))
					values.append(t.elapsed)
				else:
					print("  Run %s: failed or timed out" %i)
					values.append(0)
				i = i + 1
			print('  ' +'-'*25)
			average = float(sum(values)) / len(values)
			print("  Average: %sms" %average)
			print("")
			
		print('\n' + '='*80 + '\n')

def usage():
	print("Usage: python ldpro.py -p {path to Linked Data interface description file} [number of runs (optional, defaults to 3)]")
	print("Example: python ldpro.py -p test/ldid-dbpedia.ttl")

if __name__ == "__main__":
	ldpro = LinkedDataProfiler()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:c:", ["help", "profile", "check"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				ldpro.usage()
				sys.exit()
			elif opt in ("-p", "--profile"):
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