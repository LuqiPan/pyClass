import ast
import pdb
import pprint

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

debug = True

f = open("sample.py")
content = f.read()
tree = ast.parse(content)
if debug:
    print ast.dump(tree, False)

class ClassObject:
    def __init__(self, bases):
        self.class_dict = {}
        self.bases = bases

class Object:
    def __init__(self, klass):
        self.klass = klass
        self.object_dict = {}

def dprint(something):
    if debug:
        print(something)

def dpp(something):
    if debug:
        pp(something)

global_dict = {}

def lookup(id, class_dict=None):
    if class_dict is None:
        return global_dict[id]
    else:
        return (class_dict[id] or global_dict[id])

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
        return lookup(exp.id)

    # Name#Del
    if (type(exp) is Name) and (type(exp.ctx) is Del):
        return exp.id

    # Pass
    if type(exp) is Pass:
        dprint('---Pass')
        dprint('---')
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
        func = lookup(exp.func.id, class_dict)
        if isinstance(func, ClassObject):
            return Object(func)
        else:
            raise Exception("NYI")

    # Assign
    if type(exp) is Assign:
        dprint('---Assign')
        assert len(exp.targets) == 1
        dprint(exp.targets)
        dprint(exp.value)
        if class_dict is not None:
            class_dict[exp.targets[0].id] = evaluate(exp.value, class_dict)
        else:
            global_dict[exp.targets[0].id] = evaluate(exp.value)
        dprint('global_dict after Assign')
        dprint(global_dict)
        dprint('---')

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

for c in ast.iter_child_nodes(tree):
    evaluate(c)
