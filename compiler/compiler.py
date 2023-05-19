import lexer_parser as lp

# on détermine la ramification la plus longue et on la renvoie



# on ouvre le fichier
with open("C:/Users/vince/Desktop/projet langage de programmation/Langage Simp/compiler/test.simp", "r") as f:
    # on récupère toutes les lignes
    lines = f.readlines()
    # on supprime les commentaires et les retours à la ligne
    for i in range(len(lines)):
        lines[i] = lines[i].split("#")[0]
        if lines[i][-1:] == "\n":
            lines[i] = lines[i][:-1]
    # on supprime les lignes vides
    lines = [line for line in lines if line != "" and line != "\n"]

# on créer l'arbre global
global_tree = lp.parser_global(lines, 0)

# on optimise l'arbre
#for i in range(len(global_tree)):
#    global_tree[i] = lp.optimizer(global_tree[i])

# on affiche le fichier
for line in lines:
    print(line)

# on affiche l'arbre global
for line in global_tree:
    print(line)

print("\n")

# on parcoure l'arbre en profondeur et on créé une pile
#for line in global_tree:
#    print(browse(line))