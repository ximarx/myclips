'''
Created on 11/ago/2012

@author: Francesco Capozzo
'''
from myclips.rete.Network import Network
import myclips.functions
import pyparsing as pp
import string
import sys
import re
import traceback
from myclips.shell.Interpreter import Interpreter
from myclips.MyClipsException import MyClipsException


class Completer(object):
    def __init__(self, words):
        self.words = words
        self.prefix = None
        self.previousPrefix = ""
        self._customAdd = set()
    def complete(self, prefix, index):
        #if prefix == "":
        #    return None
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.previousPrefix = self.prefix
            self.prefix = prefix
            self._updateMatches()
        try:
            theWord = self.matching_words[index]
            if theWord in self._customAdd:
                theWord = theWord.lstrip("?$")
            return theWord
        except IndexError:
            return -1
    def addWord(self, newWord):
        if newWord not in self._customAdd:
            self._customAdd.add(newWord)
            self.words.append(newWord)
            self._updateMatches()
            
    def _updateMatches(self):
        self.matching_words = [
            w for w in self.words if #w.startswith(self.prefix)
                self.prefix != None #and string.find(w, self.prefix) != -1
                    and ( w.startswith(self.prefix) 
                            or w.startswith(self.prefix, 1))
            ]
        
            
    def resetCustoms(self):
        self.words = list(set(self.words).difference(self._customAdd))
        self._customAdd = set()
            

class Shell(object):
    '''
    classdocs
    '''

    def __init__(self, aInterpreter=None, aCompleter=None, aNetwork=None):
        self._network = aNetwork or Network()
        self._parser = self._network.getParser()
        self._aMainItem = None
        self._completer = aCompleter or Completer(myclips.functions.SystemFunctionBroker.definitions().keys())
        self._readlineOn = False
        self._interpreter = aInterpreter or Interpreter()
        self._interpreter.setShell(self)
        self._interpreter.setNetwork(self._network)
        

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
            _, start, end = self._aMainItem.scanString(theString).next()
            return theString[start:end]
        except:
            return False
        
        
    def printHeader(self):
        print
        print "#--------------------------------------------------------#"
        print "|    MyCLIPS ({0})".format(myclips.VERSION).ljust(57, " ") + "|"
        print "|        <Ctrl>+D or (exit) to Exit                      |"
        print "|        <TAB> for functions and variables suggestion    |"
        print "|        (help) for help                                 |"
        print "#--------------------------------------------------------#"
        print

    
    
    def loop(self):


        try:
            import readline
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self._completer.complete)
            self._readlineOn = True
        except ImportError:
            # no readline, no autocompletation
            self._readlineOn = False
            
        try:
            
            self.printHeader()
            
            theBuffer = ""
            while True:
                theString = "".join(i if ord(i)<128 else "_" 
                                     for i in unicode(raw_input(">>> " if len(theBuffer) == 0 else "... " ), sys.stdin.encoding)) + "\n"
                
                theBuffer += theString
                
                theResult = self.isComplete(theBuffer)
                if  theResult is not False:
                    # process the string
                    # reset the buffer
                    # continue!
                    #print "Complete command: "
                    #print theResult
                    theBuffer = ""
                    self._completer.resetCustoms()
                    try:
                        theResult = self._interpreter.evaluate(theResult)
                    except MyClipsException, e:
                        print "[ERROR] ", e.message
                        #traceback.print_exc()
                        myclips.logger.warning(traceback.format_exc())
                    except Exception, e:
                        if hasattr(e, 'msg'):
                            print "[ERROR] ", e.msg
                            myclips.logger.error(traceback.format_exc())
                        else:
                            print "[ERROR] ", e
                            traceback.print_exc()
                    else:
                        if theResult is not None:
                            print theResult
                    
                else:
                    if self._readlineOn:
                        theVariables = re.findall(r"(?:^|\s)\$?\?[^)(\s]+", theString)
                        for aVar in theVariables:
                            #print>>sys.stderr, "Variabile: ", aVar.strip()
                            self._completer.addWord(aVar.strip())                    
                    
                
        except (EOFError, SystemExit):
            print "Bye!"
        except:
            print
            print "------ Error ------"
            print traceback.print_exc()
            
        

if __name__ == '__main__':
    
    Shell().loop()
            