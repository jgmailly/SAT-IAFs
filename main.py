import parser
import encoding
import subprocess
import sys
from pysat.solvers import Solver

def get_extension_from_model(model, nb_args, args, u_args):
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
    return extension

problems_list = ["SE", "EE", "CE"]
semantics_list = ["CF_W", "CF_S", "AD_W", "AD_S", "CO_W", "CO_S", "ST_W", "ST_S"]
usage_message=f"Usage: python3 main.py <apx_file> <problem>-<semantics>\nPossible problems: {problems_list}\nPossible semantics: {semantics_list}"

if len(sys.argv) != 3:
    sys.exit(usage_message)

apx_file = sys.argv[1]
task = sys.argv[2]
task_split = task.split("-")
problem = task_split[0]
semantics = task_split[1]

if problem not in problems_list:
    print(f"Problem {problem} not supported.")
    sys.exit(usage_message)

if semantics not in semantics_list:
    print(f"Semantics {semantics} not supported.")
    sys.exit(usage_message)

args, u_args, atts, u_atts = parser.parse(apx_file)
nb_args = len(args) + len(u_args)

clauses = encoding.get_clauses(args, u_args, atts, u_atts, semantics)

s = Solver(name='g4')
for clause in clauses:
    s.add_clause(clause)

if problem == "SE":
    if s.solve():
        model = s.get_model()
        extension = get_extension_from_model(model, nb_args, args, u_args)
        encoding.print_extension(extension)
    else:
        print("NO")
elif problem == "EE":
    for model in s.enum_models():
        extension = get_extension_from_model(model, nb_args, args, u_args)
        encoding.print_extension(extension)
elif problem == "CE":
    counter = 0
    for model in s.enum_models():
        counter += 1
    print(counter)

s.delete()

