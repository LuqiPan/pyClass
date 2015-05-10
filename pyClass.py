import ast
import pdb
import pprint
from sys import argv

"""
A pretty-printing dump function for the ast module.  The code was copied from
the ast.dump function and modified slightly to pretty-print.

Alex Leone (acleone ~AT~ gmail.com), 2010-01-30

From http://alexleone.blogspot.co.uk/2010/01/python-ast-pretty-printer.html
"""

from ast import *

def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

def parseprint(code, filename="<string>", mode="exec", **kwargs):
    """Parse some code from a string and pretty-print it."""
    node = parse(code, mode=mode)   # An ode to the code
    print(dump(node, **kwargs))

# Short name: pp = parse, dump, print
pp = parseprint

debug = argv[2]

f = open(argv[1])
content = f.read()
tree = ast.parse(content)
if debug == 'true':
    print ast.dump(tree, False)

class ClassObject:
    def __init__(self, bases):
        self.class_dict = {}
        self.bases = bases

class Object:
    def __init__(self, klass):
        self.klass = klass
        self.object_dict = {}

class Function:
    def __init__(self, param, body):
        self.param = param
        self.body = body

class Method:
    def __init__(self, func):
        self.func = func

def dprint(something):
    if debug == 'true':
        print(something)

def dpp(something):
    if debug == 'true':
        pp(something)

global_dict = {}

def lookup(id, class_dict=None):
    if class_dict is None:
        return global_dict.get(id)
    else:
        return (class_dict.get(id) or global_dict.get(id))

def object_lookup(attr, object):
    result = object.object_dict.get(attr) or object.klass.class_dict.get(attr)
    if isinstance(result, Method):
        result.self_obj = object
    return result

def object_field_update(attr, val, object):
    object.object_dict[attr] = val
    #if object.object_dict.get(attr) is None:
        #if object.klass.class_dict.get(attr) is None:
            #object.object_dict[attr] = val
        #else:
            #object.klass.class_dict[attr] = val
    #else:
        #object.object_dict[attr] = val

def evaluate(exp, class_dict=None):
    dpp(exp)

    # Num
    if type(exp) is Num:
        dprint('---Num')
        dprint(exp.n)
        dprint('---')
        return exp.n

    # Name#Load
    if (type(exp) is Name) and (type(exp.ctx) is Load):
        dprint('---Name')
        dprint(exp.id)
        dprint('---')
        return lookup(exp.id, class_dict)

    # Name#Del
    if (type(exp) is Name) and (type(exp.ctx) is Del):
        dprint('---Del---')
        return exp.id

    # Pass
    if type(exp) is Pass:
        dprint('---Pass---')
        return None

    # Delete
    if type(exp) is Delete:
        dprint('---Delete')
        del global_dict[evaluate(exp.targets[0])]
        dprint('global_dict after Delete')
        dprint(global_dict)
        dprint('---')

    # func with class
    if (type(exp) is Call) and (type(exp.func) is Name):
        dprint('---Call')
        func = lookup(exp.func.id, class_dict)
        if isinstance(func, ClassObject):
            return Object(func)
        else:
            raise Exception("NYI")
        dprint('---')

    # Assign
    if type(exp) is Assign:
        dprint('---Assign')
        assert len(exp.targets) == 1
        dprint(exp.targets)
        dprint(exp.value)
        if type(exp.targets[0]) is Attribute:
            object = lookup(exp.targets[0].value.id, class_dict)
            object_field_update(exp.targets[0].attr, evaluate(exp.value), object)
        else:
            if class_dict is not None:
                class_dict[exp.targets[0].id] = evaluate(exp.value, class_dict)
            else:
                global_dict[exp.targets[0].id] = evaluate(exp.value)
        dprint('global_dict after Assign')
        dprint(global_dict)
        dprint('---')

    # Attribute
    if (type(exp) is Attribute) and (type(exp.ctx) is Load):
        dprint('---Attribute')
        object = evaluate(exp.value, class_dict)
        assert isinstance(object, Object)
        dprint(object)
        value = object_lookup(exp.attr, object)
        dprint('---')
        return value

    # Print
    if type(exp) is Print:
        dprint('---Print')
        assert len(exp.values) == 1
        dprint(exp.values)
        v = evaluate(exp.values[0])
        dprint('---')
        print v

    # ClassDef
    if type(exp) is ClassDef:
        dprint('---ClassDef')
        #TODO: handle inheritance
        class_object = ClassObject(exp.bases)
        dprint('class_dict after init')
        dprint(class_object.class_dict)
        global_dict[exp.name] = class_object
        for sub in exp.body:
            evaluate(sub, class_object.class_dict)
        dprint('class_dict after eval')
        dprint(class_object.class_dict)
        dprint('bases after eval')
        dprint(class_object.bases)
        dprint('global_dict after eval')
        dprint(global_dict)
        dprint('---')

    # Function Definition
    if type(exp) is FunctionDef:
        dprint('---FunctionDef')
        # only single parameter functions
        assert len(exp.args.args) == 1
        dprint('param is: ' + exp.args.args[0].id)
        dprint('body is')
        func = Function(exp.args.args[0].id, exp.body)
        for e in exp.body:
            dpp(e)
        if class_dict is not None:
            meth = Method(func)
            class_dict[exp.name] = meth
        else:
            global_dict[exp.name] = func
        dprint('class_dict after func def')
        dprint(class_dict)
        dprint('global_dict after func def')
        dprint(global_dict)
        dprint('---')

    #Function Call
    if (type(exp) is Expr) and (type(exp.value) is Call):
        dprint('---Function Call')
        func_or_meth = evaluate(exp.value.func)
        if isinstance(func_or_meth, Method):
            assert len(exp.value.args) == 0
            meth = func_or_meth
            assert isinstance(meth, Method)
            #store the old binding
            oldvalue = global_dict.get(meth.func.param)
            # FIXME
            #pdb.set_trace()
            global_dict[meth.func.param] = meth.self_obj
            for e in meth.func.body:
                evaluate(e)
            #restore the old binding
            global_dict[meth.func.param] = oldvalue
        else:
            if isinstance(func_or_meth, Function):
                assert len(exp.value.args) == 1
                func = func_or_meth
                assert isinstance(func, Function)
                #store the old binding
                oldvalue = global_dict.get(func.param)
                global_dict[func.param] = evaluate(exp.value.args[0])
                for e in func.body:
                    evaluate(e)
                #restore the old binding
                global_dict[func.param] = oldvalue
            else:
                #wrong
                assert 0 == 1

        #if type(exp.value.func) is Attribute:
            #assert len(exp.value.args) == 0
            #meth = evaluate(exp.value.func)
            #assert isinstance(meth, Method)
            ##store the old binding
            #oldvalue = global_dict.get(meth.func.param)
            ## FIXME
            #global_dict[meth.func.param] = evaluate(exp.value.func.value)
            #for e in meth.func.body:
                #evaluate(e)
            ##restore the old binding
            #global_dict[meth.func.param] = oldvalue
        #else:
            #assert len(exp.value.args) == 1
            #func = evaluate(exp.value.func)
            #assert isinstance(func, Function)
            ##store the old binding
            #oldvalue = global_dict.get(func.param)
            #global_dict[func.param] = evaluate(exp.value.args[0])
            #for e in func.body:
                #evaluate(e)
            ##restore the old binding
            #global_dict[func.param] = oldvalue
        dprint('---')

for c in ast.iter_child_nodes(tree):
    evaluate(c)
