# -*- coding: utf-8 -*-

"""

SPARQL Wrapper exceptions

@authors: U{Ivan Herman<http://www.ivan-herman.net>}, U{Sergio Fernández<http://www.wikier.org>}, U{Carlos Tejo Alonso<http://www.dayures.net>}
@organization: U{World Wide Web Consortium<http://www.w3.org>} and U{Foundation CTIC<http://www.fundacionctic.org/>}.
@license: U{W3C® SOFTWARE NOTICE AND LICENSE<href="http://www.w3.org/Consortium/Legal/copyright-software">}

"""

import exceptions

class SPARQLWrapperException(exceptions.Exception):
	"""
	Base class for SPARQL Wrapper exceptions
	"""
	
	def __init__(self):
		Exception.__init__(self)
	
	def __str__(self):
		return "SPARQLWrapperException: an exception has occured"

class QueryBadFormed(SPARQLWrapperException):
	"""
	Query Bad Formed exceptions
	"""
	
	def __init__(self):
		SPARQLWrapperException.__init__(self)

	def __str__(self):
		return "QueryBadFormed: a bad request has been sent to the endpoint, probably the sparql query is bad formed"

class EndPointNotFound(SPARQLWrapperException):
	"""
	End Point Not Found exceptions
	"""
	
	def __init__(self):
		SPARQLWrapperException.__init__(self)

	def __str__(self):
		return "EndPointNotFound: it was impossible to connect with the endpoint in that address, check if it is correct"

