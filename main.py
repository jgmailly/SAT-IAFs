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

#### Direct solving with Pysat
clauses = encoding.get_clauses(args, u_args, atts, u_atts, semantics)

s = Solver(name='g4')
#print("Begin Clauses")
for clause in clauses:
#    print(clause)
    s.add_clause(clause)
#print("End Clauses")
    
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

#extensions = []
    
#for model in s.enum_models():
#    extension = []
#    for literal in model:
#        int_literal = int(literal)
#        if int_literal > 0 and int_literal <= nb_args:
#            arg_name = ""
#            if int_literal <= len(args):
#                arg_name = args[int_literal - 1]
#            else:
#                arg_name = u_args[int_literal - len(args) - 1]
#            extension.append(arg_name)
#    if extension not in extensions:
#        extensions.append(extension)

#if extensions == []:
#    print("NO")
#else:
#    print("[")
#    for extension in extensions:
#        encoding.print_extension(extension)
#    print("]")

s.delete()

##### Export encoding as Dimacs and run Sat4j
# dimacs = encoding.write_dimacs(args, u_args, atts, u_atts, semantics)

# tmp_file = open('tmp.cnf','w')
# print(dimacs, file = tmp_file)
# tmp_file.close()

# process = subprocess.run(["java", "-jar", "org.sat4j.core.jar", "tmp.cnf"], capture_output=True,encoding="UTF-8")

# #print(process.stdout)
# pb_out = process.stdout.split("\n")
# model = []
# has_solution = False
# for line in pb_out:
#     if line.startswith("v "):
#         #print(line)
#         has_solution = True
#         model = line.split(" ")[1:]

# #print(model)
# #print(decode_model(alloc_vars,pref_vars,model,objects,agents))
# if has_solution:
#     extension = []
#     for literal in model:
#         int_literal = int(literal)
#         if int_literal > 0 and int_literal <= nb_args:
#             arg_name = ""
#             if int_literal <= len(args):
#                 arg_name = args[int_literal - 1]
#             else:
#                 arg_name = u_args[int_literal - len(args) - 1]
#             extension.append(arg_name)

#     print(extension)
# else:
#     print("NO")
