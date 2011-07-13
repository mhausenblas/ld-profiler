# ld-profiler

A dirt-simple Linked Data profiler. For now, a simple CLI that takes a Linked Data interface description (LDID) in [VoID](http://www.w3.org/TR/void/) format and performs two profiling tasks:

1. For all example resources given in the LDID a look-up is performed and the response times are displayed
2. For SPARQL end points announced in the LDID an array of generic queries is executed and the response times are displayed

## Who is behind this?

When [Michael](https://profiles.google.com/Michael.Hausenblas) read Cary Millsap's excellent ACM Queue article [Thinking clearly about performance](http://queue.acm.org/detail.cfm?id=1810909) he was wondering if profiling in the Linked Data world has already been established. He looked around and didn't find much convincing stuff so he decided to write something himself.

## License

This software is in the Public Domain.

## Ideas

* Web service?
* Graphical representation?
