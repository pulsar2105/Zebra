import re

import errors as err

operators = ["=", "=>",
             "+", "-",
             "*", "/", "//", "%", "^",
             "+=", "-=", "*=", "/=", "//=", "%=", "^=",
             "<", ">", "<=", ">=", "!=", "==",
             "and", "or", "xor", "in", "nand", "nor", "xnor", "nin"]

separators = [".", ",", ":", ";"]
opening_characters = ["(", "[", "{"]
closing_characters = [")", "]", "}"]
opening_closing_characters = opening_characters + closing_characters

# Lexer
def line_lexer(data):
    # we create the list of tokens (lexer)
    tokens = []

    while data != "":
        # comments are ignored
        if data[0] in ["#", "\n"]:
            break

        # spaces are ignored
        if data[0] == " ":
            data = data[1:]
            continue # skip spaces

        # we manage strings of characters
        if data[0] == '"' or data[0] == "'":
            i = 1
            while data[0] != data[i]:
                i += 1

                # escaped character \" or \'
                if data[i] == "\\":
                    continue # skip

                if i == len(data):
                    raise Exception("Error: Missing end of string")
            tokens.append(data[0:i+1])
            data = data[i+1:]
            continue

        # negative numbers are managed
        if len(data) > 0 and data[0] == "-":
            # if "-" is interpreted as a negative number
            if len(tokens) > 0:
                if not tokens[-1] in closing_characters and (not "'" in tokens[-1] and not '"' in tokens[-1]):
                    if data[1].isdigit():
                        _float = re.match(r"-?\d+\.\d+", data)
                        _int = re.match(r"-?\d+", data)

                        if _float and _float.group() == data[:len(_float.group())]:
                            tokens.append(_float.group())
                            data = data[len(_float.group()):]

                        elif _int and _int.group() == data[:len(_int.group())]:
                            tokens.append(_int.group())
                            data = data[len(_int.group()):]
            else:
                if data[1].isdigit():
                    _float = re.match(r"-?\d+\.\d+", data)
                    _int = re.match(r"-?\d+", data)

                    if _float and _float.group() == data[:len(_float.group())]:
                        tokens.append(_float.group())
                        data = data[len(_float.group()):]

                    elif _int and _int.group() == data[:len(_int.group())]:
                        tokens.append(_int.group())
                        data = data[len(_int.group()):]

        # positive numbers are managed
        elif len(data) > 0 and data[0].isdigit():
            _float = re.match(r"\d+\.\d+", data)
            _int = re.match(r"\d+", data)

            if _float and _float.group() == data[:len(_float.group())]:
                tokens.append(_float.group())
                data = data[len(_float.group()):]

            elif _int and _int.group() == data[:len(_int.group())]:
                tokens.append(_int.group())
                data = data[len(_int.group()):]

        # variable size operators are managed ("+" size 1) ("and" size 3) and separators are handled also (.,:;)
        for i in range(3, 0, -1):
            if data[:i] in operators + separators or data[:i] in opening_closing_characters:
                tokens.append(data[:i])
                data = data[i:]
                break

        # if the character is a letter, we see if it is a variable or a function
        if len(data) > 0 and data[0].isalpha():
            boolean = re.match(r"true|false", data)

            variable_function = re.match(r"\w+", data)

            if boolean:
                if boolean.group() == data[:len(boolean.group())]:
                    if boolean.group() == "true":
                        tokens.append(True)
                    elif boolean.group() == "false":
                        tokens.append(False)
                    data = data[len(boolean.group()):]

            elif variable_function:
                if variable_function.group() == data[:len(variable_function.group())]:
                    tokens.append(variable_function.group())
                    data = data[len(variable_function.group()):]

    return tokens

"""
# Test-----------------------
data = "b = -(-10 - value * (--3*32) - sin(5*10-19, 2) + (-a) + fact(10, 10) * cos(10 + 1) * 'abcde' - 10 - sun.value)"
# we check if there are errors natively in the line
err.string_error(data)
# we do the syntactic analysis
print(line_lexer(data))

# infinite mode
while True:
    data = input(">>> ")
    err.string_error(data)
    print(line_lexer(data))
"""