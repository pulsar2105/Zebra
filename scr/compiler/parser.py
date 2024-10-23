import re

import lexer as lex
import errors as err

operators = ["=", ".",
             "+", "-",
             "*", "/", "//", "%", "^",
             "+=", "-=", "*=", "/=", "//=", "%=", "^=",
             "<", ">", "<=", ">=", "!=", "==",
             "and", "or", "xor", "in", "nand", "nor", "xnor", "nin"]

operators_priority = [["="],
                      ["and", "or", "xor", "in", "nand", "nor", "xnor", "nin"],
                      ["not"],
                      ["<", ">", "<=", ">=", "!=", "=="],
                      ["+", "-"],
                      ["*", "/", "//", "%"],
                      ["^"],
                      ["."]]

opening_characters = ["(", "[", "{"]
closing_characters = [")", "]", "}"]
opening_closing_characters = opening_characters + closing_characters

# the lowest level of brackets is determined
def determine_lower_para_influences(tokens):
    parentheses_influence = 0
    influences = []

    for t in tokens:
        if t == "(":
            parentheses_influence += 1
            influences.append(parentheses_influence)
        elif t == ")":
            influences.append(parentheses_influence)
            parentheses_influence -= 1
        else:
            influences.append(parentheses_influence)

    # if the level of influence of the brackets is greater than 0
    # ask to remove the extra brackets again
    if min(influences) > 0:
        # don't remove brackets if there is comma in there
        if min(influences) == 1:
            for i in range(len(tokens)):
                if tokens[i] == "," and influences[i] == min(influences):
                    return tokens, min(influences), influences

        tokens = tokens[1:-1]
        return determine_lower_para_influences(tokens)

    return tokens, min(influences), influences

# search for the lowest priority operator outside the parentheses
def search_min_priority(tokens, operators, operators_priority):
    tokens, min_para_influence, influences = determine_lower_para_influences(tokens)

    # check if there are any operators left
    good = False
    for token in tokens:
        if token in operators:
            good = True
    if not good:
        return None, -1

    # the lowest priority operator is sought
    for operators in operators_priority:
        for i in range(len(tokens)):
            for operator in operators:
                if tokens[len(tokens) - 1 - i] in operators:
                    if tokens[len(tokens) - 1 - i] == operator and influences[len(tokens) - 1 - i] == min_para_influence:
                        return operator, len(tokens) - 1 - i

# search if tokens list are a big function, ex: ["sin", "(", "10", ")"]
def if_one_function(tokens):
    # first check
    if type(tokens) == list and len(tokens) > 1:
        if type(tokens[0]) == str:
            if re.match(r"\w+", tokens[0]) and tokens[1] == "(" and not tokens[0] in operators:
                # if the last parenthesis is to the function
                influ = 0
                for i in range(1, len(tokens)):
                    if tokens[i] == "(":
                        influ += 1
                    if tokens[i] == ")":
                        influ -= 1

                    if influ == 0 and i == len(tokens) - 1:
                        # get arguments function
                        arguments = []
                        i = 2 # 2 because we skip the fonction name and the first "("
                        check_point = 2
                        while tokens[i] != ")":
                            if tokens[i] == ",":
                                # if there isn't an argument we replace it with "None"
                                if tokens[check_point:i] != []:
                                    arguments.append(tokens[check_point:i])
                                else:
                                    arguments.append("None")

                                check_point = i+1
                            i += 1

                        if tokens[check_point:i] != []:
                            arguments.append(tokens[check_point:i])

                        return True, arguments

                    elif influ == 0 and i != len(tokens) - 1:
                        return False, None
            else:
                return False, None
        else:
            return False, None
    else:
        return False, None

# search if tokens list are a access to a list or dictionnary, ex: ["my_list", "[", "10", "]"]
def if_access(tokens):
    # first check
    if type(tokens) == list and len(tokens) > 1:
        if type(tokens[0]) == str:
            if re.match(r"\w+", tokens[0]) and tokens[1] == "[" and not tokens[0] in operators:
                # if the last parenthesis is to the function
                influ = 0
                for i in range(1, len(tokens)):
                    if tokens[i] == "[":
                        influ += 1
                    if tokens[i] == "]":
                        influ -= 1

                    if influ == 0 and i == len(tokens) - 1:

                        # get arguments
                        arguments = []
                        i = 2 # 2 because we skip the fonction name and the first "("
                        check_point = 2
                        while tokens[i] != "]":
                            if tokens[i] in ":,":
                                # if there isn't an argument we replace it with "None"
                                if tokens[check_point:i] != []:
                                    arguments.append(tokens[check_point:i])
                                else:
                                    arguments.append("None")

                                check_point = i+1
                            i += 1

                        if tokens[check_point:i] != []:
                            arguments.append(tokens[check_point:i])

                        return True, arguments

                    elif influ == 0 and i != len(tokens) - 1:
                        return False, None
            else:
                return False, None
        else:
            return False, None
    else:
        return False, None

# search if tokens list are a big function, ex: ["sin", "(", "10", ")"]
def is_list_dict(tokens, opening_character, closing_character):
    # control check (to avoid error)
    if type(tokens) == list and len(tokens) > 1:
        # first check
        if tokens[0] == opening_character:
            # list/dict empty
            if tokens[1] == closing_character:
                return True, []
            else:
                # get the list/dict/tuple elements
                arguments = []
                influ = 1
                check_point = 1
                i = 1
                while influ != 0 and i != len(tokens):
                    # add an argument (little or big) to the list
                    if tokens[i] in [",", "=>", closing_character] and influ == 1:
                        arguments.append(tokens[check_point:i])
                        check_point = i+1

                    # stop at the end off arguemnts ex: (10,) for avoid null arguement
                    if tokens[i] == "," and tokens[i+1] == closing_character:
                        break

                    if tokens[i] in opening_characters:
                        influ += 1
                    elif tokens[i] in closing_characters:
                        influ -= 1

                    i += 1

                return True, arguments
        else:
            return False, None
    else:
        return False, None

# search if tokens list are a tuple, ex: ["(", "10", ",", "25", ")"]
def is_tuple(tokens):
    # control check (to avoid error)
    if type(tokens) == list and len(tokens) > 1:

        # check
        good = False
        influ = 0
        for token in tokens:
            if token == "(":
                influ += 1
            elif token == ")":
                influ -= 1
            elif token == "," and influ == 1:
                good = True

        if good and tokens[0] == "(":
            # tuple empty
            if tokens == ["(", ",", ")"]:
                return True, []
            else:
                # get the tuple elements
                arguments = []
                influ = 1
                check_point = 1
                i = 1
                while influ != 0 and i != len(tokens):
                    # add an argument (little or big) to the list
                    if tokens[i] in [",", ")"] and influ == 1:

                        # if there isn't an argument we replace it with "None"
                        if tokens[check_point:i] != []:
                            arguments.append(tokens[check_point:i])
                        else:
                            arguments.append("None")

                        check_point = i+1

                    # stop at the end off arguemnts ex: (10,) for avoid null arguement
                    if tokens[i] == "," and tokens[i+1] == ")":
                        break

                    if tokens[i] in "(":
                        influ += 1
                    elif tokens[i] in ")":
                        influ -= 1

                    i += 1

                return True, arguments
        else:
            return False, None
    else:
        return False, None


# Parser
def line_parser(tokens):

    # detect floats number to avoid parsing "."
    if type(tokens) == str:
        return tokens

    # check for the presence of functions
    if if_one_function(tokens)[0]:
        # get the function and its arguments
        action = tokens[0]
        arguments = if_one_function(tokens)[1]

        # arguments are parsed
        for i in range(len(arguments)):
            arguments[i] = line_parser(arguments[i])

        # "*" is for unpack all elements
        return [action, *arguments]

    # check for the presence of tuple
    elif is_tuple(tokens)[0]:
        action = "tuple"
        arguments = is_tuple(tokens)[1]

        # arguments are parsed
        for i in range(len(arguments)):
            arguments[i] = line_parser(arguments[i])

        # "*" is for unpack all elements
        return [action, *arguments]

    # check for the presence of list
    elif is_list_dict(tokens, "[", "]")[0]:
        action = "list"
        arguments = is_list_dict(tokens, "[", "]")[1]

        # arguments are parsed
        for i in range(len(arguments)):
            arguments[i] = line_parser(arguments[i])

        # "*" is for unpack all elements
        return [action, *arguments]

    # check for the presence of dict
    elif is_list_dict(tokens, "{", "}")[0]:
        action = "dict"
        arguments = is_list_dict(tokens, "{", "}")[1]

        # arguments are parsed
        for i in range(len(arguments)):
            arguments[i] = line_parser(arguments[i])

        # "*" is for unpack all elements
        return [action, *arguments]

    # check for the presence of access
    elif if_access(tokens)[0]:
        action = "access"

        arguments = if_access(tokens)[1]

        # arguments are parsed
        for i in range(len(arguments)):
            arguments[i] = line_parser(arguments[i])

        # "*" is for unpack all elements
        return [action, tokens[0], *arguments]

    # operators part
    # find the operator who is made in LAST
    operator, pos = search_min_priority(tokens, operators, operators_priority)

    tokens, min_para_influence, influences = determine_lower_para_influences(tokens)

    # if there are no operators left
    if operator == None and pos == -1:
        return tokens[0]
    elif operator == "-" and pos == 0:
        action = operator
        arguments = [tokens[1:]]
        arguments[0] = line_parser(arguments[0])
    else:
        # the arguments are listed according to the operator/action
        action = operator
        arguments = [tokens[:pos], tokens[pos + 1:]]

        arguments[0] = line_parser(arguments[0])
        arguments[1] = line_parser(arguments[1])

    # "*" is for unpack all elements
    return [action, *arguments]


# Test----------------------------------------

data = "b = -(10 - value * (--3*32) - sin(5*10-19, 2) + (-a) + fact(10) * cos(10 + 1) * 'abcde' - 10 - sun.mass) * abcf_g[0:10:-1]"

# check if there are errors natively in the line
err.string_error(data)
# do the syntactic analysis
tokens = lex.line_lexer(data)
print(tokens)
# the syntax is checked
err.errors(tokens)
# create the instruction tree
tree = line_parser(tokens)
print(tree)

# infinite mode
while True:
    data = input(">>> ")
    #err.string_error(data)
    tokens = lex.line_lexer(data)
    print(tokens)
    #err.errors(tokens)
    tree = line_parser(tokens)
    print(tree)
