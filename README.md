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

	Results for example resources:

	 Dereferencing http://dbpedia.org/data/Digital_Enterprise_Research_Institute.rdf

	  Run 0: 0.216471910477ms
	  Run 1: 0.0791869163513ms
	  Run 2: 0.0769400596619ms
	  Run 3: 0.0776801109314ms
	  Run 4: 0.0769898891449ms
	  -------------------------
	  Average: 0.105453777313ms

	 Dereferencing http://dbpedia.org/data/Galway.rdf

	  Run 0: 0.568041086197ms
	  Run 1: 0.368092060089ms
	  Run 2: 0.369071006775ms
	  Run 3: 0.954349994659ms
	  Run 4: 2.14417719841ms
	  -------------------------
	  Average: 0.880746269226ms

	================================================================================


## Who is behind this?

When [Michael](https://profiles.google.com/Michael.Hausenblas) read Cary Millsap's excellent ACM Queue article [Thinking clearly about performance](http://queue.acm.org/detail.cfm?id=1810909) he was wondering if profiling in the Linked Data world has already been established. He looked around and didn't find much convincing stuff so he decided to write something himself.

## License

This software is in the Public Domain.

## Ideas

* Web service?
* Graphical representation?
