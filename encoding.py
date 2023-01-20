import sys

# Number of variables in the formula
n_vars = 0

# Clauses of the formula
clauses = []

## args[i] -> i+1
## u_args[i] -> len(args) + i + 1
## y_a -> x_a + nb_args

# Returns the integer value corresponding to an argument name
# Useful for building clauses to feed the SAT solver
def sat_var_from_arg_name(argname, args, u_args):
    if argname in args:
        return args.index(argname) + 1
    elif argname in u_args:
        return len(args) + u_args.index(argname) + 1
    else:
        sys.exit(f"Unknown argument name: ({argname})")

# Returns the set of certain attacks of an argument,
# i.e. the certain arguments that certainly attack it
def get_certain_attackers(argument, args, atts):
    attackers = []
    for attack in atts:
        if (attack[1] == argument) and (attack[0] in args):
            attackers.append(attack[0])
    return attackers

# Returns the set of attacks of an arguments
# Both certain and uncertain attacks, with certain or uncertain attack
def get_all_attackers(argument, args, u_args, atts, u_atts):
    attackers = []
    for attack in atts + u_atts:
        if attack[1] == argument:
            attackers.append(attack[0])
    return attackers


### The following functions modify the global variable clauses
### to contain the CNF encoding of the chosen semantics

##### Weak semantics
def weak_conflict_free(args, u_args, atts, u_atts):
    global n_vars
    global clauses
    n_vars = len(args) + len(u_args)
    for attack in atts:
        attacker = attack[0]
        target = attack[1]
        if (attacker in args) and (target in args):
            new_clause = [-sat_var_from_arg_name(attacker, args, u_args), -sat_var_from_arg_name(target, args, u_args)]
            clauses.append(new_clause)


def weak_admissible(args, u_args, atts, u_atts):
    global clauses
    weak_conflict_free(args, u_args, atts, u_atts)
    for argument in args + u_args :
        attackers = get_certain_attackers(argument, args, atts)
        for attacker in attackers:
            new_clause = [-sat_var_from_arg_name(argument, args, u_args)]
            defenders = get_certain_attackers(attacker, args, atts)
            for defender in defenders:
                new_clause.append(sat_var_from_arg_name(defender, args, u_args))
            clauses.append(new_clause)

def define_y_variables(args, u_args, atts, u_atts, nb_args):
    global clauses
    for argument in args:
        attackers = get_certain_attackers(argument, args, atts)
        new_clause_long = [-(sat_var_from_arg_name(argument, args, u_args) + nb_args)]
        for attacker in attackers:
            new_clause = [-sat_var_from_arg_name(attacker, args, u_args), (sat_var_from_arg_name(argument, args, u_args) + nb_args)]
            clauses.append(new_clause)
            new_clause_long.append(sat_var_from_arg_name(attacker, args, u_args))
        clauses.append(new_clause_long)
            
def weak_complete(args, u_args, atts, u_atts):
    global clauses
    global n_vars
    weak_conflict_free(args, u_args, atts, u_atts)
    nb_args = n_vars
    n_vars *= 2
    define_y_variables(args, u_args, atts, u_atts, nb_args)
    for argument in args + u_args:
        attackers = get_certain_attackers(argument, args, atts)
        new_clause_long = [sat_var_from_arg_name(argument, args, u_args)]
        for attacker in attackers:
            new_clause = [-sat_var_from_arg_name(argument, args, u_args), (sat_var_from_arg_name(attacker, args, u_args) + nb_args)]
            clauses.append(new_clause)
            new_clause_long.append(-(sat_var_from_arg_name(attacker, args, u_args) + nb_args))
        clauses.append(new_clause_long)

        

def weak_stable(args, u_args, atts, u_atts):
    global clauses
    weak_conflict_free(args, u_args, atts, u_atts)
    for argument in args:
        attackers = get_certain_attackers(argument, args, atts)
        new_clause = []
        for attacker in attackers:
            new_clause.append(sat_var_from_arg_name(attacker, args, u_args))
        new_clause.append(sat_var_from_arg_name(argument, args, u_args))
        clauses.append(new_clause)

##### Strong semantics
def strong_conflict_free(args, u_args, atts, u_atts):
    global n_vars
    global clauses
    n_vars = len(args) + len(u_args)
    for attack in atts + u_atts:
        attacker = attack[0]
        target = attack[1]
        new_clause = [-sat_var_from_arg_name(attacker, args, u_args), -sat_var_from_arg_name(target, args, u_args)]
        clauses.append(new_clause)

def strong_admissible(args, u_args, atts, u_atts):
    global clauses
    strong_conflict_free(args, u_args, atts, u_atts)
    for argument in args + u_args :
        attackers = get_all_attackers(argument, args, u_args, atts, u_atts)
        for attacker in attackers:
            new_clause = [-sat_var_from_arg_name(argument, args, u_args)]
            defenders = get_certain_attackers(attacker, args, atts)
            for defender in defenders:
                new_clause.append(sat_var_from_arg_name(defender, args, u_args))
            clauses.append(new_clause)

def strong_complete(args, u_args, atts, u_atts):
    global clauses
    global n_vars
    strong_conflict_free(args, u_args, atts, u_atts)
    nb_args = n_vars
    n_vars *= 2
    define_y_variables(args, u_args, atts, u_atts, nb_args)
    for argument in args + u_args:
        attackers = get_all_attackers(argument, args, u_args, atts, u_atts)
        new_clause_long = [sat_var_from_arg_name(argument, args, u_args)]
        for attacker in attackers:
            new_clause = [-sat_var_from_arg_name(argument, args, u_args), (sat_var_from_arg_name(attacker, args, u_args) + nb_args)]
            clauses.append(new_clause)
            new_clause_long.append(-(sat_var_from_arg_name(attacker, args, u_args) + nb_args))
        clauses.append(new_clause_long)

def strong_stable(args, u_args, atts, u_atts):
    global clauses
    strong_conflict_free(args, u_args, atts, u_atts)
    for argument in args:
        attackers = get_certain_attackers(argument, args, atts)
        new_clause = []
        for attacker in attackers:
            new_clause.append(sat_var_from_arg_name(attacker, args, u_args))
        new_clause.append(sat_var_from_arg_name(argument, args, u_args))
        clauses.append(new_clause)
    for argument in u_args:
        attackers = get_certain_attackers(argument, args, atts)
        new_clause = []
        for attacker in attackers:
            new_clause.append(sat_var_from_arg_name(attacker, args, u_args))
        new_clause.append(sat_var_from_arg_name(argument, args, u_args))
        clauses.append(new_clause)


##### Encoding generation
# Returns the string representation of a clause
# in Dimacs format
def write_dimacs_clause(clause):
    dimacs_clause = ""
    for literal in clause:
        dimacs_clause += (str(literal) + " ")
    dimacs_clause += "0\n"
    return dimacs_clause

# Returns the CNF encoding in Dimacs format, for a given semantics
def write_dimacs(args, u_args, atts, u_atts, semantics):
    if semantics == "CF_W":
        weak_conflict_free(args, u_args, atts, u_atts)
    elif semantics == "CF_S":
        strong_conflict_free(args, u_args, atts, u_atts)
    elif semantics == "AD_W":
        weak_admissible(args, u_args, atts, u_atts)
    elif semantics == "AD_S":
        strong_admissible(args, u_args, atts, u_atts)
    elif semantics == "CO_W":
        weak_complete(args, u_args, atts, u_atts)
    elif semantics == "CO_S":
        strong_complete(args, u_args, atts, u_atts)
    elif semantics == "ST_W":
        weak_stable(args, u_args, atts, u_atts)
    elif semantics == "ST_S":
        strong_stable(args, u_args, atts, u_atts)
    else:
        sys.exit("Unkown semantics: ({semantics})")

    dimacs = f"p cnf {n_vars} {len(clauses)}\n"
    for clause in clauses:
        dimacs += write_dimacs_clause(clause)
    return dimacs

# Returns the list of the clauses corresponding to the encoding
# of a given semantics
def get_clauses(args, u_args, atts, u_atts, semantics):
    global clauses
    if semantics == "CF_W":
        weak_conflict_free(args, u_args, atts, u_atts)
    elif semantics == "CF_S":
        strong_conflict_free(args, u_args, atts, u_atts)
    elif semantics == "AD_W":
        weak_admissible(args, u_args, atts, u_atts)
    elif semantics == "AD_S":
        strong_admissible(args, u_args, atts, u_atts)
    elif semantics == "CO_W":
        weak_complete(args, u_args, atts, u_atts)
    elif semantics == "CO_S":
        strong_complete(args, u_args, atts, u_atts)
    elif semantics == "ST_W":
        weak_stable(args, u_args, atts, u_atts)
    elif semantics == "ST_S":
        strong_stable(args, u_args, atts, u_atts)
    else:
        sys.exit("Unkown semantics: ({semantics})")

    ### Tautological clauses with arguments identifiers
    ### for forcing the number of variables in the solver
    for i in range(len(args+u_args)):
        tautology = [(i+1), -(i+1)]
        clauses.append(tautology)
    
    return clauses

# Prints an extension to the standard output
def print_extension(extension):
    if extension == []:
        print("[]")
    else:
        print("[", end="")
        for i in range(len(extension) - 1):
            print(f"{extension[i]},", end="")
        print(f"{extension[len(extension)-1]}]")
