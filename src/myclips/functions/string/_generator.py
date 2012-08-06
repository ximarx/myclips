'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
import os
from genericpath import exists, isfile
from dircache import listdir
import pyclbr
import json

def generate():
    
    THIS_DIR = os.path.dirname(__file__)
    
    validClasses = []

    for theFile in [x for x in listdir(THIS_DIR) if isfile(THIS_DIR + "/" + x) and x[-3:] == '.py' and x[0] != '_']:
        
        theModule = theFile[0:-3]
        
        inModule = pyclbr.readmodule(theModule)
        
        for (theName, theClass) in inModule.items():
            if theClass.super[0] == "Function" \
                    or ( isinstance(theClass.super[0], pyclbr.Class) \
                         and  theClass.super[0].name == "Function"):
                
                validClasses.append({"module": "myclips.functions.string."+theModule,
                                     "class": theName})
                
        

    fr = open(THIS_DIR + "/functions.json", "w")
    json.dump(validClasses, fr, indent=4)
    fr.close()
    
    
if __name__ == '__main__':
    generate()    