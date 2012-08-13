'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
from genericpath import exists, isfile, isdir
from dircache import listdir
import json
import inspect
import importlib
import myclips.functions
import sys
import time


class Logger(object):
        def __init__(self, filename="REPORT.txt"):
            self.terminal = sys.stdout
            self.log = open(filename, "w")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

def getPaths(basePath, pathsVector):
    
    thisDirPaths = [basePath + "/" + x for x in listdir(basePath) if isdir(basePath + "/" + x)]
    for path in thisDirPaths:
        if exists(path + "/functions.json"):
            pathsVector.append(path)
        else:
            # search inside
            getPaths(path, pathsVector)
    return pathsVector
    

def generate():
    
    FUNCS_DIR = myclips.functions.FUNCTIONS_DIR
    
    validDirs = getPaths(FUNCS_DIR, [])
    
    stats = {"functions": 0,
             "groups": {}}
    
    sys.stdout = Logger(FUNCS_DIR+"/REPORT.txt")

    print "MyCLIPS system functions discovery report: ", time.asctime()
    print
    
    for singleDir  in validDirs:
        
        theRelativePackage = singleDir.replace(FUNCS_DIR, "").replace("/", ".")
        
        print "myclips.functions"+theRelativePackage
        
        stats['groups'][theRelativePackage] = 0
        
        validClasses = []
        
        for theFile in [x for x in listdir(singleDir) if isfile(singleDir + "/" + x) and x[-3:] == '.py' and x[0] != '_']:
        
            theModule = theFile[0:-3]
            
            theModuleComplete = "myclips.functions%s.%s"%(theRelativePackage, theModule)
            
            print "\t|--- ."+theModule
            
            try:
                theModuleObject = importlib.import_module(theModuleComplete, "myclips.functions")
            except ImportError:
                # if error ignore this module
                continue
            else:
                for theName, theClass in [(x,y) for (x,y) in inspect.getmembers(theModuleObject) if isinstance(y, type)]:
                    from myclips.functions.Function import Function
                    if issubclass(theClass, Function) and theClass != Function and theClass.DEFINITION is not None :
                        print "\t:   \t|--- ."+theName+" (%s)"%theClass.DEFINITION.name
                        validClasses.append({"module": "myclips.functions%s.%s"%(theRelativePackage, theModule),
                                             "class": theName})
                        stats['functions'] += 1
                        stats['groups'][theRelativePackage] += 1
                        
            # time to update the json
            fr = open(singleDir + "/functions.json", "w")
            json.dump(validClasses, fr, indent=4)
            fr.close()


    # time to update the main manifest
    
    fr = open(FUNCS_DIR + "/" + myclips.functions.FUNCTIONS_MANIFEST, "w")
    json.dump([dict([('import', ".%s/functions.json"%x.replace(FUNCS_DIR, ""))]) for x in validDirs], fr, indent=4)
    fr.close()
    
    statsString = """
================================
Number of groups: {1}
{2}

Number of functions: {0}

Main manifest file: `{3}`
Per-group manifest: `{4}`
================================
"""

    perGroupString = "  |- {0}: {1}"
    
    print statsString.format(str(stats['functions']), #{0}
                             str(len(stats['groups'])), #{1}
                             "\n".join([perGroupString.format(group, str(funcs)) for (group, funcs) in stats['groups'].items()]), #{2}
                             FUNCS_DIR + "/" + myclips.functions.FUNCTIONS_MANIFEST, #{3}
                             "%s/{GROUP_NAME}/functions.json"%FUNCS_DIR #{4}
                             )
    
        

if __name__ == '__main__':
    generate()    