# ld-profiler

A dirt-simple Linked Data profiler. For now, a simple CLI that takes a Linked Data interface description (LDID) in [VoID](http://www.w3.org/TR/void/) format and performs two profiling tasks:

1. For all example resources given in the LDID a look-up is performed and the response times are displayed
2. For SPARQL end points announced in the LDID an array of generic queries is executed and the response times are displayed


## How does it work?

Invoke syntax is:

	python ldpro.py ( -h | -p (LDID) | -c (LDID) )  [r]

where:

	-h ... prints help
	-p ... loads LDID (the path to a local file), runs profiler and reports results
	-c ... loads LDID (the path to a local file) and reports on its content (use to verify LDID)
	 r ... optionally, specifies the number of runs (defaults to 3)
	
For example, to perform 5 profile runs for each of the profile targets described in a LDID that is provided in the [`test`](https://github.com/mhausenblas/ld-profiler/tree/master/test) directory, use the following command:

	python ldpro.py -p test/ldid-dbpedia.ttl 5

When the above command is issued, the result should look something like this:

	================================================================================

	I. Results for example resources:

	 Dereferencing http://dbpedia.org/data/Digital_Enterprise_Research_Institute.rdf

	  Run 0: 0.121638059616ms
	  Run 1: 0.0866210460663ms
	  Run 2: 0.0787258148193ms
	  Run 3: 0.0795500278473ms
	  Run 4: 0.079206943512ms
	  -------------------------
	  Average: 0.0891483783722ms

	 Dereferencing http://dbpedia.org/data/Galway.rdf

	  Run 0: 0.367477178574ms
	  Run 1: 0.36781001091ms
	  Run 2: 0.366918802261ms
	  Run 3: 0.396972179413ms
	  Run 4: 0.366279840469ms
	  -------------------------
	  Average: 0.373091602325ms

	II. Results for SPARQL end point:

	 Executing queries againt http://dbpedia.org/sparql

	 Query: SELECT ?s WHERE { ?s ?p ?o } LIMIT 1

	  Run 0: 0.0598089694977ms
	  Run 1: 0.0606231689453ms
	  Run 2: 0.0609130859375ms
	  Run 3: 0.0849769115448ms
	  Run 4: 0.0592401027679ms
	  -------------------------
	  Average: 0.0651124477386ms

	 Query: SELECT ?s WHERE { ?s a ?o } LIMIT 1

	  Run 0: 0.062292098999ms
	  Run 1: 0.0598909854889ms
	  Run 2: 0.0597748756409ms
	  Run 3: 0.0594980716705ms
	  Run 4: 0.0634031295776ms
	  -------------------------
	  Average: 0.0609718322754ms

	================================================================================


## Who is behind this?

When [Michael](https://profiles.google.com/Michael.Hausenblas) read Cary Millsap's excellent ACM Queue article [Thinking clearly about performance](http://queue.acm.org/detail.cfm?id=1810909) he was wondering if profiling in the Linked Data world has already been established. He looked around and didn't find much convincing stuff so he decided to write something himself.

## License

This software is in the Public Domain.

## Ideas

* JSON output
* GAE app with URI
	* Graphical representation of the results (bar chart, avg.)
	* Web service for interactive access
* Microdata support
* Measure throughput (?)
