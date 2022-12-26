import math
import re

import lexer
import errors as err

operators = ["=", "+", "-", "*", "/", "//", "%", "^", "<", ">", "<=", ">=", "!=", "==","and", "or", "xor"]
operators_priority = [["="],
                      ["<", ">", "<=", ">=", "!=", "=="],
                      ["and", "or", "xor"],
                      ["+", "-"],
                      ["*", "/", "//", "%"],
                      ["^"]]

opening_characters = ["(", "[", "{"]
closing_characters = [")", "]", "}"]
opening_closing_characters = opening_characters + closing_characters

# on détermine le niveau de parenthèses le plus bas
def determine_lower_para_influences(tokens):
    parentheses_influence = 0
    influences = []

    for t in  tokens:
        if t == "(":
            parentheses_influence += 1
            influences.append(parentheses_influence)
        elif t == ")":
            influences.append(parentheses_influence)
            parentheses_influence -= 1
        else:
            influences.append(parentheses_influence)

    # si le niveau d'influence des parenthèses est supérieur à 0
    # on soustrait 1, n fois
    if min(influences) > 0:
        for i in range(min(influences)):
            tokens = tokens[1:-1]
            for iflu in range(len(influences)):
                influences[iflu] = influences[iflu] - 1

        return tokens, min(influences), influences

    return tokens, min(influences), influences

# on recherche l'opérateur de priorité le moins élevé à l'exterieur des parenthèses
def search_min_priority(tokens, operators, operators_priority):
    tokens, min_para_influence, influences = determine_lower_para_influences(tokens)

    # on vérifie si il reste des opérateurs
    good = False
    for token in tokens:
        if token in operators:
            good = True
    if not good:
        return None, -1

    # on recherche l'opérateur de priorité le moins élevé,
    # l'opérateur qui est fait en dernié (le plus à droite)
    for operators in operators_priority:
        for i in range(len(tokens) - 1, 0, -1):
            for operator in operators:
                if type(tokens[i]) == str:
                    if tokens[i] == operator and influences[i] == min_para_influence:
                        return operator, i

# Parser
def line_parser(tokens):
    # on vérifie la presence de fonctions
    if len(tokens) == 1 and type(tokens[0]) == str:
        function = re.match(r'\w+\(.*\)', tokens[0])

        # on vérifie si il y a une fonction et si oui,
        # si la fonction est bien détecter sur l'ensemble de la chine de caractère
        if function and function.group() == tokens[0]:

            # on récupère la fonction et ses arguments
            action = re.match(r"\w+", tokens[0]).group()
            arguments = re.search(r'\(.*\)', tokens[0]).group()[1:-1].split(",")

            # on gère les arguments
            for i in range(len(arguments)):
                arguments[i] = line_parser(lexer.line_lexer(arguments[i]))

            # "*" is for unpack all elements
            return [action, *arguments]

    # on trouve l'operateur qui est fait en DERNIER
    operator, pos = search_min_priority(tokens, operators, operators_priority)

    tokens, min_para_influence, influences = determine_lower_para_influences(tokens)

    # si il ne reste plus d'opérateurs
    if operator == None and pos == -1:
        return tokens[0]

    # on liste les arguments en fonction de l'opérateur/action
    action = operator
    arguments = [tokens[:pos], tokens[pos + 1:]]

    arguments[0] = line_parser(arguments[0])
    arguments[1] = line_parser(arguments[1])

    # "*" is for unpack all elements
    return [action, *arguments]

# on créer l'arbre d'un fichier entier
def parser_global(lines, indent_level):
    global_tree = []
    i = 0
    while i < len(lines) and lines[i].startswith(" " * indent_level):
        # on récupère la ligne
        line = lines[i]

        # on gère les conditions
        if line[:indent_level * 4 + 3] == "    " * indent_level + "if ":
            # on créé l'arbre de la condition
            condition = re.match(r".+\:", line[indent_level * 4 + 3:]).group()[:-1]
            condition = line_parser(lexer.line_lexer(condition))
            # on créé l'arbre de la suite
            i += 1
            suite = parser_global(lines[i:], indent_level + 1)
            i += len(suite)
            global_tree.append(["if", condition] + suite)

        # on gère la boucle while
        elif line[:indent_level * 4 + 5] == "    " * indent_level + "while ":
            # on créé l'arbre de la condition
            condition = re.match(r".+\:", line[indent_level * 4 + 5:]).group()[:-1]
            condition = line_parser(lexer.line_lexer(condition))
            # on créé l'arbre de la suite
            i += 1
            suite = parser_global(lines[i:], indent_level + 1)
            i += len(suite)
            global_tree.append(["while", condition] + suite)

        else:
            # on créé l'arbre de la ligne
            global_tree.append(line_parser(lexer.line_lexer(line)))

        i += 1

    return global_tree

# Teste
data = "b = (-3*32) + sin(5*10-19) + a + fact(10) * cos(10 + 1)"
# on vérifie si il y des erreurs nativement dans la ligne
err.string_error(data)
# on fait l'analyse syntaxique
tokens = lexer.line_lexer(data)
print(tokens)
# on contrôle la syntaxe
err.errors(tokens)
# on créé l'arbre d'instruction
tree = line_parser(tokens)
print(tree)


# mode infinie
while True:
    data = input(">>> ")
    err.string_error(data)
    tokens = lexer.line_lexer(data)
    print(tokens)
    err.errors(tokens)
    tree = line_parser(tokens)
    print(tree)