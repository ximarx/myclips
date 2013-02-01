MyClips
==============

A Rete-based, CLIPS clone, inference engine in Python.


Features
------------
	* Rete-based pattern matcher
	
	* Rete network plotter for better understanding of the rules compilation
	
	* Compatibility with CLIPS grammar (COOLS is not included)
	
	* Support for Template/Ordered Fact
	
	* Support for Multifields (max 1 multifield per slot definition is allowed)
	
	* Full compatibility with CLIPS modules behaviour
	
	* Terminal Shell with function and variable suggestion [and arrow keys work!!!]
	
	* XMLRPC-Server module (in myclips-server repository)
	
	* Easy integration with Java applications through XMLRPC-Server module + Java wrapper library (in myclips-javalib repository)
	
	* Multiple CRS available (breadth, depth, mea, lex, simplicity, complexity, random)  	



Dependencies:
------------

	PyParsing: for CLIPS grammar parser 

	BList (>=1.3.4): for non-depth|breadth strategies (optional)
		https://github.com/DanielStutzbach/blist or `easy_install blist`
	
	NetworkX and MathplotLib: for Rete network plotting only (optional) 


Benchmarks results
------------

MyClips + CPython 2.7.x (both 64/32 bit) is much slower than CLIPS (20-120x time slower)

MyClips + PyPy 2.0beta is comparable with CLIPS (5-10x time slower) 



[![screencast](http://i1.ytimg.com/vi/h8QmrQbJTg8/3.jpg?time=1344682028698)](http://www.youtube.com/watch?v=h8QmrQbJTg8)