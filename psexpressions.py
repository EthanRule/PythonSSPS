class Expr:

    def __init__(self, value):
        self.value = value

    def eval(self, ps_env):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)


class Literal(Expr):

    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        ps_env.opPush(self.value)

        pass

    def __str__(self):
        return str(self.value)


class PSString(Expr):

    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        ps_env.opPush(StringValue(self.value))
        pass

    def __str__(self):
        return str(self.value)


class PSName(Expr):
    def __init__(self, var_name):
        Expr.__init__(self, var_name)
        self.var_name = var_name

    def index_of_definitions_stack_entry(self, ps_env):
        # find the correct static link
        # lookup returns a tuple (index, {})

        index = ps_env.lookup(self.var_name)
        #print(index)
        return index[0]

    def eval(self, ps_env):
        if self.var_name[0] == '/':
            ps_env.opPush(str(self.var_name))
        elif self.var_name in ps_env.builtin_operators:
            ps_env.builtin_operators[self.var_name]()
        else:
            value = ps_env.lookup(self.var_name)  # value is a tuple
            if isinstance(value[1], CodeArrayValue):
                print(ps_env)
                print(self.index_of_definitions_stack_entry(ps_env))
                value[1].apply(ps_env, self.index_of_definitions_stack_entry(ps_env))
            else:
                ps_env.opPush(value)

    def __str__(self):
        return str(self.var_name)


class PSCodeArray(Expr):

    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, ps_env):
        ps_env.opPush(CodeArrayValue(self.value))
        pass

    def __str__(self):
        return str(self.value)


class Value:

    def __init__(self, value):
        self.value = value

    def apply(self, ps_env):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)


class StringValue(Value):

    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, ps_env):
        raise TypeError(
            "Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}('{}')".format(type(self).__name__, self.value)

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.value)

    def length(self):
        return len(self.value)


class DictionaryValue(Value):

    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, ps_env):
        raise TypeError(
            "Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.value)

    # returns length of the array value
    def length(self):
        return len(list(self.value.keys()))


class CodeArrayValue(Value):

    def __init__(self, body):
        Value.__init__(self, body)
        self.body = body

    def apply(self, ps_env, static_ind):
        # When `PSName`
        # object represents a function call (i.e., its value is a `CodeArrayValue`), before the
        # `CodeArrayValue` is applied, a new Activation Record (AR) with an empty dictionary should be
        # pushed onto the `dictstack
        # function to find the staticLinkIndex

        ps_env.dictPush({}, static_ind)
        for i in self.body:
            i.eval(ps_env)
            #print(i)
        # Pop the dict after function is done
        x = ps_env.dictPop()

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.body)
