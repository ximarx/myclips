'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
import os
from genericpath import exists

if __name__ == '__main__':
    
    skeletonClass = """
'''
Created on 05/ago/2012

@author: Francesco Capozzo
'''
from myclips.functions.predicate._TypeTesting import _TypeTesting
import myclips.parser.Types as types
from myclips.FunctionsManager import Constraint_ExactArgsLength,\
    FunctionDefinition

class {0}(_TypeTesting):
    '''
    The {1} function returns the symbol TRUE if its argument is a {2}, otherwise it returns the symbol FALSE.
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.1.html#Heading{3}
    '''
    pass
        
        
{0}.DEFINITION = FunctionDefinition("?SYSTEM?", "{1}", {0}(types.{2}), types.Symbol, {0}.do ,
            [
                Constraint_ExactArgsLength(1)
            ],forward=False)
"""    
    
    skeletonJson = """,{{
    "module":    "myclips.functions.predicate.{0}",
    "class":     "{0}"
}}"""
    
    funcs = [
             # ["CLASS_NAME", "FUNC_NAME", "TYPE_NAME", "DOC_HEADER_ID"]
             ['Numberp', 'numberp', 'Number', '186'],
             ['Floatp', 'floatp', 'Float', '187'],
             ['Integerp', 'integerp', 'Integer', '188'],
             ['Lexemep', 'lexemep', 'Lexeme', '189'],
             ['Stringp', 'stringp', 'String', '190'],
             ['Symbolp', 'symbolp', 'Symbol', '191'],
             ]
    
    
    for func in funcs:
        
        className, funcName, typeName, docId = func

        fileName = os.path.dirname(__file__)+'/'+className+".py"
        
        if not exists(fileName):
            fr = open(fileName, "w")
            fr.write(skeletonClass.format(className, funcName, typeName, docId))
            fr.close()
            
        print skeletonJson.format(className)
        
    
    
    