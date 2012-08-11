'''
Created on 11/ago/2012

@author: Francesco Capozzo
'''
from myclips.rete.Network import Network
import myclips.functions
import pyparsing as pp
import string
import sys


class Completer(object):
    def __init__(self, words):
        self.words = words
        self.prefix = None
        self._customAdd = set()
    def complete(self, prefix, index):
        #if prefix == "":
        #    return None
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.prefix = prefix
            self._updateMatches()
        try:
            theWord = self.matching_words[index]
            if theWord in self._customAdd:
                theWord = theWord.lstrip("?$")
            return theWord
        except IndexError:
            return None
    def addWord(self, newWord):
        if newWord not in self._customAdd:
            self._customAdd.add(newWord)
            self.words.append(newWord)
            self._updateMatches()
            
    def _updateMatches(self):
        self.matching_words = [
            w for w in self.words if #w.startswith(self.prefix)
                self.prefix != None and string.find(w, self.prefix) != -1
            ]
        
            
    def resetCustoms(self):
        self.words = list(set(self.words).difference(self._customAdd))
        self._customAdd = set()
            

class Shell(object):
    '''
    classdocs
    '''

    def __init__(self):
        self._network = Network()
        self._parser = self._network.getParser()
        self._aMainItem = None
        self._completer = Completer(myclips.functions.SystemFunctionBroker.definitions().keys())

    def isComplete(self, theString):

        if self._aMainItem is None:
        
            aSymbol = pp.Word("".join([ c for c in string.printable if c not in string.whitespace and c not in "\"()" ]))
            
            aString = pp.QuotedString('"', '\\', None, True, True)
            
            self._aMainItem = pp.Forward()
            aParens = pp.nestedExpr("(", ")", content=self._aMainItem)
            self._aMainItem << (aString
                                    | aSymbol 
                                    | aParens)
        
        try:
            self._aMainItem.parseString(theString)
            return True
        except:
            return False
    
    
    def loop(self):

        import readline
        import re
        
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._completer.complete)        
            
        try:
            theBuffer = ""
            while True:
                theString = "".join(i if ord(i)<128 else "_" 
                                     for i in unicode(raw_input("MyCLIPS> " if len(theBuffer) == 0 else "." * (len("MyCLIPS") + 1) +" "), sys.stdin.encoding)) + "\n"
                
                theBuffer += theString
                
                if self.isComplete(theBuffer):
                    # process the string
                    # reset the buffer
                    # continue!
                    print "Complete command: "
                    print theBuffer.rstrip("\n")
                    theBuffer = ""
                    self._completer.resetCustoms()
                else:
                    theVariables = re.findall(r"(?:^|\s)\$?\?[^)(\s]+", theString)
                    for aVar in theVariables:
                        print>>sys.stderr, "Variabile: ", aVar.strip()
                        self._completer.addWord(aVar.strip())                    
                    
                
        except EOFError:
            print "Bye!"
            
        

if __name__ == '__main__':
    
    Shell().loop()
            