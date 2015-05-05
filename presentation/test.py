import ast
import pdb

tree = ast.parse("print('hello')")
print ast.dump(tree, False)
