# Name: Ethan Rule

from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue


class PSOperators:
    def __init__(self, scoperule):
        # stack variables
        self.opstack = []  # assuming top of the stack is the end of the list
        self.dictstack = []  # assuming top of the stack is the end of the list
        self.scope = scoperule
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add": self.add,
            "sub": self.sub,
            "mul": self.mul,
            "mod": self.mod,
            "eq": self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch": self.exch,
            "pop": self.pop,
            "copy": self.copy,
            "count": self.count,
            "clear": self.clear,
            "stack": self.stack,  # Also, you will remove the following
            # operator methods from psoperators.py: `begin`, and `end`.
            "dict": self.psDict,
            "string": self.string,
            "length": self.length,
            "get": self.get,
            "put": self.put,
            "getinterval": self.getinterval,
            "putinterval": self.putinterval,
            "search": self.search,
            "def": self.psDef,
            "if": self.psIf,
            "ifelse": self.psIfelse,
            "for": self.psFor
        }
    # ------- Operand Stack Helper Functions --------------

    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    def opPush(self, value):
        self.opstack.append(value)

    def dictPop(self):
        if len(self.dictstack) > 0:
            x = self.dictstack[len(self.dictstack) - 1]
            self.dictstack.pop(len(self.dictstack) - 1)
            return x
        else:
            print("Error: dictPop - Operand stack is empty")

    def dictPush(self, d, index):
        self.dictstack.append((index, d))

    # You may need to change your `dictPush` to make it work with the new `dictstack`
    # structure.
    def define(self, name, value):
        if len(self.dictstack) == 0:
            self.dictstack.append((0, {}))
        self.dictstack[-1][1][name] = value

    # As discussed in class, variable lookups using static scope rules proceed by looking in the current
    # dictionary at the top of the dictionary stack and then following the static-link fields to other
    # dictionaries (instead of just looking at the dictionaries in order).
    # Note: In Lab3, you already implemented the lookup function using static scoping rule, where you
    # search the dictionaries following the index links in the tuples (i.e., following the static links).
    # - Using dynamic scope rules, the lookup will behave very much like SPS lookup. Of course, you
    # should change your lookup code for the new dictionary structure.
    # - The `dictstack` structure will be the same for both static and dynamic scope
    # implementations.
    # ▪ When the scoping rule is dynamic, the lookup should just look at the dictionaries on the
    # `dictstack` starting from top (ignoring the static links).

    def lookup(self, name):  # add another parameter? if so how do I use this parameter?
        name = '/' + name
        if self.scope == "dynamic":
            for ar_tuple in reversed(self.dictstack):  # top to bottom search
                if name in ar_tuple[1]:
                    return (ar_tuple[0],  ar_tuple[1][name])

        elif self.scope == "static":

            def helper(name, index):
                if name in self.dictstack[index][1]:
                    return index
                elif index == 0 and name not in self.dictstack[0][1]:
                    print("Error name not in static scope(lookup function)")
                    print(self.dictstack[0][1])
                    return None
                else:
                    return helper(name, self.dictstack[index][0])

            staticScopeIndex = helper(name, len(self.dictstack) - 1)
            return (staticScopeIndex, self.dictstack[staticScopeIndex][1][name])

    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op2 - op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op2 * op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op2 % op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, (int, bool)):
                if op1 == op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, StringValue):
                if op1.value == op2.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, DictionaryValue):
                if op1 is op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: Types are not correct")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: Expects 2 operands")

    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, (int, bool)):
                if op1 > op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, StringValue):
                if op1.value > op2.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, DictionaryValue):
                if op1 > op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: Types are not correct")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: Expects 2 operands")

    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, (int, bool)):
                if op1 < op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, StringValue):
                if op1.value < op2.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif isinstance(op1, DictionaryValue):
                if op1 < op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: Types are not correct")
                self.opPush(op2)
                self.opPush(op1)
        else:
            print("Error: Expects 2 operands")

    def pop(self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    def stack(self):
        print("===**opstack**===")
        for item in reversed(self.opstack):
            if not isinstance(item, tuple):
                print(item)
            else: print(item[1])
        print("===**dictstack**===")
        leng = len(self.dictstack) - 1
        for item in reversed(self.dictstack):
            print("----" + str(leng) + "----" + str(item[0]) + "----")

            for name in item[1]:
                print(name + "   " + str(item[1][name]))
            leng -= 1
        print("=================" + CEND)

    def dup(self):
        if (len(self.opstack) > 0):
            newVal = self.opstack[-1]
            self.opstack.append(newVal)
        else:
            print("Error: no items to dup")

    def copy(self):
        if (len(self.opstack) > 0):
            count = self.opPop()
            opCopy = self.opstack[-count:]
            self.opstack.extend(opCopy)
        else:
            print("Error: no items to pop")

    def count(self):
        self.opstack.append(len(self.opstack))

    def clear(self):
        self.opstack.clear()

    def exch(self):
        if len(self.opstack) >= 2:
            temp = self.opstack[-2]
            self.opstack[-2] = self.opstack[-1]
            self.opstack[-1] = temp
        else:
            print("Error: exch requires a minimum of two items")

    def string(self):
        strSize = self.opPop()
        newStr = "\0" * strSize
        self.opPush(StringValue("(" + newStr + ")"))

    def psDict(self):
        if len(self.opstack) >= 1:
            self.opPop()
            d = {}
            self.opPush(DictionaryValue(d))
        else:
            print("Error: opstack empty")

    def length(self):
        n = self.opPop()
        if isinstance(n, StringValue):
            self.opPush(len(n.value) - 2)
        elif isinstance(n, DictionaryValue):
            self.opPush(len(n.value.keys()))
        else:
            print(
                "Error: cannot determine length of a value that is not StringValue or DictionaryValue")

    def get(self):
        iKey = self.opPop()
        val = self.opPop()
        if isinstance(val, StringValue):
            self.opPush(ord(val.value[iKey + 1]))
        elif isinstance(val, DictionaryValue):
            self.opPush(val.value[iKey])
        else:
            print(
                "Error: cannot determine length of a value that is not StringValue or DictionaryValue")

    def put(self):
        item = self.opPop()
        iKey = self.opPop()
        val = self.opPop()
        if isinstance(val, StringValue):
            val.value = val.value[:iKey + 1] + \
                chr(item) + val.value[iKey + 2:len(val.value)]
        elif isinstance(val, DictionaryValue):
            val.value[iKey] = item
        else:
            print(
                "Error: cannot determine length of a value that is not StringValue or DictionaryValue")

    def getinterval(self):
        count = self.opPop()
        index = self.opPop() + 1
        strVal = self.opPop()
        newStr = strVal.value[index:index + count]
        newStr = '(' + newStr + ')'
        self.opPush(StringValue(newStr))

    def putinterval(self):
        substring = self.opPop()
        index = self.opPop() + 1
        val = self.opPop()
        if isinstance(val, StringValue):
            substring = substring.value[1:-1]
            val.value = val.value[:index] + substring + \
                val.value[index+len(substring):]
        else:
            print("Error: cannot determine length of a value that is not StringValue")

    def search(self):
        delimiter = self.opPop()
        inputstr = self.opPop()
        if isinstance(inputstr, StringValue):
            delimiter = delimiter.value[1:-1]
            if delimiter in inputstr.value:
                subStr = inputstr.value.split(delimiter, 1)
                self.opPush(StringValue('(' + subStr[1]))
                self.opPush(StringValue('(' + delimiter + ')'))
                self.opPush(StringValue(subStr[0] + ')'))
                self.opPush((True))
            else:
                self.opPush(inputstr)
                self.opPush((False))
        else:
            print(
                "Error: cannot determine length of a value that is not StringValue or DictionaryValue")

    def psDef(self):
        if len(self.dictstack) == 0:
            # place an empty tuple if the dictstack is empty
            self.dictPush({}, 0)
        val = self.opPop()
        name = self.opPop()
        self.dictstack[-1][1][name] = val  # add the /key: value

    def psIf(self):
        codeArrayValueObject = self.opPop()
        booleanValue = self.opPop()
        if booleanValue == True:
            # apply method introduces new empty tuple, and removes it on completion of the codeArray
            codeArrayValueObject.apply(self)

    def psIfelse(self):
        codeArrayValueObject1 = self.opPop()
        codeArrayValueObject2 = self.opPop()
        booleanValue = self.opPop()
        if booleanValue == True:
            # apply method introduces new empty tuple, and removes it on completion of the codeArray
            codeArrayValueObject2.apply(self)
        else:
            # apply method introduces new empty tuple, and removes it on completion of the codeArray
            codeArrayValueObject1.apply(self)

    def psFor(self):
        codeArrayValueObject = self.opPop()
        endIndex = self.opPop() + 1
        increment = self.opPop()
        beginIndex = self.opPop()
        staticLink = beginIndex[0]
        if isinstance(beginIndex, tuple):
            beginIndex = beginIndex[1]
        
       
        for i in range(beginIndex, endIndex, increment):
            self.opPush(i)
            # apply method introduces new empty tuple, and removes it on completion of the codeArray
            print("here")
            codeArrayValueObject.apply(self, staticLink)

    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self):
        if len(self.opstack) > 1:
            if self.opstack[-1] is None:
                self.opstack.pop()
