'''
Created on 07/aug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition, Constraint_ArgType,\
    Constraint_ExactArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError


class Delete(Function):
    '''
    This function deletes the specified range from a multifield value.

    (delete$ <multifield-expression> <begin-integer-expression> <end-integer-expression>)

    The modified multifield value is returned, which is the 
    same as <multifield- expression> with the fields ranging 
    from <begin-integer-expression> to <end-integer-expression> removed. 
    To delete a single field, the begin range field should equal the end range field.
       
    @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading222
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theMultifield, theBegin, theEnd, *args, **kargs):
        """
        handler of the function
        @see: http://www.comp.rgu.ac.uk/staff/smc/teaching/clips/vol1/vol1-12.2.html#Heading222
        """

        
        theMultifield = self.semplify(theEnv, theMultifield, list, ("1", "multifield"))
        theBegin = self.resolve(theEnv, 
                                    self.semplify(theEnv, theBegin, types.Integer, ("2", "integer")))
        theEnd = self.resolve(theEnv, 
                                    self.semplify(theEnv, theEnd, types.Integer, ("3", "integer")))

        try:
            if theBegin != theEnd:
                # remove a slice of the multifield
                # check for index values first
                if theBegin - 1 >= len(theMultifield) or theEnd > len(theMultifield):
                    raise IndexError()
                del theMultifield[theBegin-1:theEnd]
            else:
                # remove a single item from the multifield
                del theMultifield[theBegin-1]
        except IndexError:
            # invalid field!
            raise InvalidArgValueError("Multifield index %s out of range 1..%d in function delete$"%(
                                            ("range %d..%d"%(theBegin, theEnd) if theBegin != theEnd else str(theBegin)),
                                            len(theMultifield)
                                        ))
        else:
            # no error, return the modified multifield
            return theMultifield
        
    
Delete.DEFINITION = FunctionDefinition("?SYSTEM?", "delete$", Delete(), list, Delete.do,
            [
                Constraint_ExactArgsLength(3),
                Constraint_ArgType(list, 0),
                Constraint_ArgType(types.Integer, 1),
                Constraint_ArgType(types.Integer, 2)
            ],forward=False)