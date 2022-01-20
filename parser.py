### Functions for parsing an apx file

import sys

# Returns the name of an uncertain argument
# identified in an apx line
def parse_uncertain_arg(apx_line):
    return apx_line[5:-2]

# Returns the name of a certain argument
# identified in an apx line
def parse_certain_arg(apx_line):
    return apx_line[4:-2]

# Returns the names of the arguments in an uncertain attack
# identified in an apx line
def parse_uncertain_att(apx_line):
    arg_names = apx_line[5:-2]
    return arg_names.split(",")

# Returns the names of the arguments in a certain attack
# identified in an apx line
def parse_certain_att(apx_line):
    arg_names = apx_line[4:-2]
    return arg_names.split(",")

# Parses an apx file and returns the lists of
# certain arguments, uncertain arguments, certain attacks and uncertain attacks
def parse(filename):
    with open(filename) as apxfile:
        apx_lines = apxfile.read().splitlines()

    args = []
    u_args = []
    atts = []
    u_atts = []
    for apx_line in apx_lines:
        if apx_line != "":
            if apx_line[0:4] == "?arg":
                u_args.append(parse_uncertain_arg(apx_line))
            elif apx_line[0:3] == "arg":
                args.append(parse_certain_arg(apx_line))
            elif apx_line[0:4] == "?att":
                u_atts.append(parse_uncertain_att(apx_line))
            elif apx_line[0:3] == "att":
                atts.append(parse_certain_att(apx_line))
            else:
                sys.exit(f"Line cannot be parsed ({apx_line})")

    return args, u_args, atts, u_atts

