import math
import re
import os

operators = ["=", "+", "-", "*", "/", "//", "%", "^", "!", "and", "or", "xor"]
operators_priority = [["="], ["and", "or", "xor"], ["+", "-"], ["*", "/", "//", "%"], ["^", "!"]]
opening_characters = ["(", "[", "{"]
closing_characters = [")", "]", "}"]
opening_closing_characters = ["(", ")", "[", "]", "{", "}"]

def errors(tokens):
    # we check if the number of brackets is corrects
    if tokens.count("(") > tokens.count(")"):
        raise Exception("Error: Wrong parentheses \")\" expected")
    elif tokens.count("(") < tokens.count(")"):
        raise Exception("Error: Wrong parentheses \"(\" expected")

    # we check if the operators are well placeds
    for i in range(len(tokens)):
        if tokens[i] in operators:
            if i == 0:
                raise Exception("Error: Wrong syntax")
            elif tokens[i-1] in operators:
                raise Exception("Error: Wrong syntax")
            elif tokens[i-1] in opening_characters and tokens[i] not in ["^", "!", "="]:
                raise Exception("Error: Wrong syntax")

# Lexer
def lexer(data):
    # delete unnecessary bracketss
    error = re.search(r"\(\)", data)
    if error:
        data = data.replace(error.group(), "")

    # we delete the spacess
    data = data.replace(" ", "")
    tokens = []

    while data != "":
        # comments are ignored
        if data[0] == "#":
            break

        # we manage the sign inversion with "-" at the beginning of the strings
        if tokens == [] and data[0] == "-":
            tokens.append(0)
            tokens.append(data[0])
            data = data[1:]

        # negative numbers are handleds
        if data[0] == "-":
            if tokens[-1] in operators or tokens[-1] in closing_characters:
                if data[1].isdigit():
                    _float = re.match(r"-?\d+\.\d+", data)
                    _int = re.match(r"-?\d+", data)

                    if _float and _float.group() == data[:len(_float.group())]:
                        tokens.append(float(_float.group()))
                        data = data[len(_float.group()):]

                    elif _int and _int.group() == data[:len(_int.group())]:
                        tokens.append(int(_int.group()))
                        data = data[len(_int.group()):]

                    else:
                        raise Exception("Error: Wrong syntax")

        # positive numbers are managed
        elif data[0].isdigit():
            _float = re.match(r"\d+\.\d+", data)
            _int = re.match(r"\d+", data)

            if _float and _float.group() == data[:len(_float.group())]:
                tokens.append(float(_float.group()))
                data = data[len(_float.group()):]

            elif _int and _int.group() == data[:len(_int.group())]:
                tokens.append(int(_int.group()))
                data = data[len(_int.group()):]

            else:
                raise Exception("Error: Wrong syntax")

        # variable size operators are manageds
        for i in range(3, 0, -1):
            if data[:i] in operators or data[:i] in opening_closing_characters:
                tokens.append(data[:i])
                data = data[i:]
                break

        # if the character is a letter, we see if it is a variable or a functions
        if len(data) > 0 and data[0].isalpha():
            boolean = re.match(r"true|false", data)
            function = re.match(r'[a-zA-Z0-9]+\([\w\\(\)[\]\-\+\*\!\^\%\/., "{}]*\)', data)
            variable = re.match(r"\w+", data)

            if boolean:
                if boolean.group() == data[:len(boolean.group())]:
                    if boolean.group() == "true":
                        tokens.append(True)
                    elif boolean.group() == "false":
                        tokens.append(False)
                    data = data[len(boolean.group()):]

            elif function:
                if function.group() == data[:len(function.group())]:
                    tokens.append(function.group())
                    data = data[len(function.group()):]

            elif variable:
                if variable.group() == data[:len(variable.group())]:
                    tokens.append(variable.group())
                    data = data[len(variable.group()):]
            else:
                raise Exception("Error: Unknown character")

    return tokens

# determine the lowest level of brackets and remove the unnecessary brackets around them
def remove_unnecessary_parentheses(tokens):
    min_para_influence = 1

    while min_para_influence > 0:
        min_para_influence = 0
        parentheses_influence = 0
        influences = []
        for i in range(len(tokens)):
            if tokens[i] == "(":
                parentheses_influence += 1
                influences.append(1)
            elif tokens[i] == ")":
                parentheses_influence -= 1
                influences.append(1)
            else:
                influences.append(parentheses_influence)
        if len(influences) > 0:
            min_para_influence = min(influences)
        else:
            min_para_influence = 0

        # remove unnecessary brackets around it if the lowest bracket level is greater than 0s
        if min_para_influence > 0:
            tokens = tokens[1:-1]
        if min_para_influence < 0:
            raise Exception("Error: Wrong parentheses")

    return tokens, min_para_influence, influences

# search for the lowest priority operator outside the parentheses
def search_min_priority(tokens):
    tokens, min_para_influence, influences = remove_unnecessary_parentheses(tokens)

    # the operator with the lowest priority is soughts
    for operators in operators_priority:
        for i in range(len(tokens) - 1, 0, -1):
            for operator in operators:
                if type(tokens[i]) == str:
                    if tokens[i] in operator and influences[i] == min_para_influence:
                        return operator, i

# Parser
def parser(tokens):
    tokens = remove_unnecessary_parentheses(tokens)[0]

    if len(tokens) == 1 and type(tokens[0]) == str:
        function = re.match(r'[a-zA-Z0-9]+\([\w\\(\)[\]\-\+\*\!\^\%\/., "{}]*\)', tokens[0])
        if function and function.group() == tokens[0]:
            action = re.match(r"[a-zA-Z0-9]+", tokens[0]).group()
            arguments = re.search(r'\([\w\\(\)[\]\-\+\*\!\^\%\/., "{}]*\)', tokens[0]).group()[1:-1].split(",")

            # operators with n arguments are manageds
            for i in range(len(arguments)):
                arguments[i] = parser(lexer(arguments[i]))
            # "*" is for unpack all elements
            return [action, *arguments]

    # we check if there are any operators lefts
    good = True
    for token in tokens:
        if token in operators:
            good = False
    if good:
        return tokens[0]

    operator, i = search_min_priority(tokens)

    # the arguments are listed according to the operator/actions
    if operator == "!":
        action = operator
        arguments = [tokens[:i]]
    else:
        action = operator
        arguments = [tokens[:i], tokens[i + 1:]]

    # operators with n arguments are managed
    for i in range(len(arguments)):
        arguments[i] = parser(arguments[i])

    # "*" is for unpack all elements
    return [action, *arguments]

# a factorial is calculated
def fact(n):
    if n == 0:
        return 1
    for i in range(1, n):
        n *= i
    return n

# we calculate the PGCD
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# the tree is optimiseds
def optimizer(tree):
    # élement seul
    if type(tree) != list:
        return tree

    # we manage the case of the factorials
    if tree[0] == "!":
        return fact(optimizer(tree[1]))

    # all arguments are optimised if possibles
    for i in range(1, len(tree)):
        if type(tree[i]) == list:
            tree[i] = optimizer(tree[i])

    # we check if the arguments are ints or floats or bools
    good = True
    for i in range(1, len(tree)):
        if not type(tree[i]) in [int, float, bool]:
            good = False

    # standard operators (with two arguments) are managed
    result = ""
    if good:
        # we apply the operations
        if tree[0] == "and":
            result = tree[1] and tree[2]
        elif tree[0] == "or":
            result = tree[1] or tree[2]
        elif tree[0] == "xor":
            result = tree[1] ^ tree[2]
        elif tree[0] == "+":
            result = tree[1] + tree[2]
        elif tree[0] == "-":
            result = tree[1] - tree[2]
        elif tree[0] == "*":
            result = tree[1] * tree[2]
        elif tree[0] == "/":
            result = tree[1] / tree[2]
        elif tree[0] == "//":
            result = tree[1] // tree[2]
        elif tree[0] == "%":
            result = tree[1] % tree[2]
        elif tree[0] == "^":
            result = tree[1] ** tree[2]

        # more exotic action
        elif tree[0] == "sin":
            result = math.sin(tree[1])
        elif tree[0] == "cos":
            result = math.cos(tree[1])
        elif tree[0] == "tan":
            result = math.tan(tree[1])
        elif tree[0] == "asin":
            result = math.asin(tree[1])
        elif tree[0] == "acos":
            result = math.acos(tree[1])
        elif tree[0] == "atan":
            result = math.atan(tree[1])
        elif tree[0] == "pgcd":
            result = pgcd(tree[1], tree[2])

        if result != "":
            return result
        else:
            return tree

    else:
        return tree

# calculator for fun
print("calculator for fun :")
while True:
    tokens = lexer(input(">>> "))
    tree = parser(tokens)
    print(optimizer(tree))

    # on gère le cas de l'arrêt
    if tree == "exit":
        break
    elif tree == "clear":
        os.system("cls")