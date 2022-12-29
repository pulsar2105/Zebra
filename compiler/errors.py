operators = ["=", ".", "+", "-", "*", "/", "//", "%", "^", "<", ">", "<=", ">=", "!=", "==","and", "or", "xor", "in"]
operators_priority = [["="],
                      ["and", "or", "xor", "in"],
                      ["<", ">", "<=", ">=", "!=", "=="],
                      ["+", "-"],
                      ["*", "/", "//", "%"],
                      ["^"],
                      ["."]]
opening_characters = ["(", "[", "{"]
closing_characters = [")", "]", "}"]
opening_closing_characters = opening_characters + closing_characters

def string_error(string):
    # we check if the number of "\"" and/or "\'" is correct
    if string.count("\"") % 2 != 0:
        raise Exception("Error: \" expected")
    elif string.count("\'") % 2 != 0:
        raise Exception("Error: \' expected")

def errors(tokens):
    # we check if the number of brackets is correct
    if tokens.count("(") > tokens.count(")"):
        raise Exception("Error: Wrong parentheses \")\" expected")
    elif tokens.count("(") < tokens.count(")"):
        raise Exception("Error: Wrong parentheses \"(\" expected")

    # we check if the operators are well placed
    # initial case
    if tokens[0] in operators and tokens[0] != "-":
        raise Exception("Error: Wrong syntax")

    for i in range(1, len(tokens)):
        if tokens[i] in operators:
            if tokens[i-1] in operators and tokens[i] != "-":
                raise Exception("Error: Wrong syntax")
            elif tokens[i-1] in opening_characters and tokens[i] != "-":
                raise Exception("Error: Wrong syntax")

    # errors to dev :
    # -a = 10 => forbiden
    # <operator><operator> => forbiden