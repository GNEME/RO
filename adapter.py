#donness = {'Z': {'x1': 2.0, 'x2': 3.0}, 'C': [{'x1': 2.0, 'x2': 3.0, 'B': 39.0}, {'x1': 2.0, 'x2': -3.0, 'B': 55.0}], 'inegalite': ['<=', '>=']}

def z_fonction(dictionnaire):
    oneconstraint = ""
    i_len = len(dictionnaire)
    i = 1
    for t in dictionnaire:
        oneconstraint = oneconstraint + str(dictionnaire[t]) + '*' + t
        if i < i_len and dictionnaire[list(dictionnaire.keys())[i]] >= 0:
            oneconstraint = oneconstraint + '+'
        i = i + 1
    return oneconstraint

#print(z_fonction(donness['Z']))
def liste_constraints(donnes):
    constraints = []
    for k in range(len(donnes['C'])):
        oneconstraint = ""
        i_len = len(donnes['C'][k]) - 1
        i = 1
        for t in donnes['C'][k]:
            if t != 'B':
                oneconstraint = oneconstraint + str(donnes['C'][k][t]) + '*' + t
            if i < i_len and donnes['C'][k][list(donnes['C'][k].keys())[i]] >= 0:
                oneconstraint = oneconstraint + '+'
            i = i + 1
            if t == 'B':
                oneconstraint = oneconstraint + donnes['inegalite'][k] + str(donnes['C'][k][t])
        constraints.append(oneconstraint)
    return constraints

#print(liste_constraints(donness))