import parser
import encoding
import subprocess
import sys
from pysat.solvers import Solver

semantics_list = ["CF_W", "CF_S", "AD_W", "AD_S", "CO_W", "CO_S", "ST_W", "ST_S"]
usage_message=f"Usage: python3 main.py <apx_file> <semantics>\nPossible semantics: {semantics_list}"

if len(sys.argv) != 3:
    sys.exit(usage_message)

apx_file = sys.argv[1]
semantics = sys.argv[2]


args, u_args, atts, u_atts = parser.parse(apx_file)
nb_args = len(args) + len(u_args)

clauses = encoding.get_clauses(args, u_args, atts, u_atts, semantics)

s = Solver(name='g4')
for clause in clauses:
    s.add_clause(clause)
    
if s.solve():
     model = s.get_model()
     extension = []
     for literal in model:
         int_literal = int(literal)
         if int_literal > 0 and int_literal <= nb_args:
             arg_name = ""
             if int_literal <= len(args):
                 arg_name = args[int_literal - 1]
             else:
                 arg_name = u_args[int_literal - len(args) - 1]
             extension.append(arg_name)

     encoding.print_extension(extension)
else:
     print("NO")



s.delete()

