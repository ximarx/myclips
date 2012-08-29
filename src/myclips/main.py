'''
Created on 12/ago/2012

@author: Francesco Capozzo
'''
from myclips.shell.Shell import Shell

import sys
import os
from myclips import FunctionManifestGenerator
import unittest
from genericpath import exists
from myclips.shell.Interpreter import Interpreter
from myclips.rete.Network import Network

def main():

    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m myclips"
    
    
    usage = {
        "progName" : os.path.basename(sys.argv[0]),
        "modes" : "\n".join([
            "  shell                   Start a MyCLIPS's Shell",
            #"  xmlrpc                  Start a MyCLIPS XMLRPC server",
            "  batch filename          Load a batch and then (run) it",
            "  functions               Search for System Function and compile the manifest",
            "  tests                   Run MyCLIPS's unittests",        
        ]),
        "options" : ""
    }
    
    USAGE = """\
    Usage: %(progName)s [modes] [options]
    
    Modes:
    %(modes)s
    
    Options:
      -h, --help              Show this message
      -v, --verbose           Verbose output
      -q, --quiet             Minimal output
      -b, --background        Background service
    %(options)s
    Examples:
      %(progName)s                                   - Show this message
      %(progName)s shell                             - run a MyCLIPS shell
      %(progName)s xmlrpc                            - run a MyCLIPS XMLRPC daemon
      %(progName)s batch benchmark/manners.clpbat    - run a file in batch mode
    
    """%usage
    
    
    try:
        theMode = sys.argv[1]
    except:
        print USAGE
        sys.exit(-2)
        
    if theMode == "shell":
        Shell().loop()
    elif theMode == "batch" and len(sys.argv) >= 3:
        i = Interpreter(Network())
        i.evaluate("(batch \"%s\")"%sys.argv[2].strip('"'))
        i.evaluate("(run)")
    elif theMode == "functions":
        FunctionManifestGenerator.generate()
    elif theMode == "tests":
        if exists(os.path.dirname(__file__)+'/../../tests'):
            # prepare the sys.argv
            sys.argv = ["python -m unittest",
                        "discover",
                        "-p",
                        '*Test.py',
                        "-s",
                        "../tests/"]
            
            unittest.main(module=None)
        else:
            print "Expected a tests dir in `%s`, but nothing found"%(os.path.dirname(__file__)+'/../../tests')
    else:
        print USAGE
        
        
if __name__ == '__main__':
    main()