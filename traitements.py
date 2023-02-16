#juice = {'Z': '+1/2*x1 - 3*x2', 'C': ['2*x1 + 3*x2 <= -39', '1/2*x1 + 3*x2 >= -10/2'], 'max_min': 1}  # for the beginning, sign might be come just before the number ('-12*x1' or '12*x1' or '+12*x1')

#Cette fonction inverse les signes des coefficients d'une
#contrainte si son segond membre est négatif
def ligne_corrigee(contrainte):
    coefs = contrainte
    
    for k in contrainte:
        coefs[k] *= -1
        
    return coefs

#print(ligne_corrigee(donnes['C'][0]))

def verify_variables(variables):
    if variables[0] == 'x' and variables[1:].isdigit():
        return 1
    return 0

def verify_coef(coef):
    for letter in coef:
        if not(letter.isdigit()) and letter != '/' and letter != '.':
            return 0
    return 1

def z_values_for_tabsimplexe(juice):
    juice_data = {}

    #Traitements pour z
    zexpression = juice['Z'].split(' ')
    zexpression_len = zexpression.__len__()
    if zexpression_len % 2 == 0:
        return {}
    if zexpression_len > 1:
        for i in range(1, zexpression_len, 2):
            if zexpression[i] != '+' and zexpression[i] != '-':
                return {}
    for i in range(0, zexpression_len, 2):
        elements = zexpression[i].split('*')
        if elements.__len__() != 2:
            return {}
        if i == 0:
            if verify_variables(elements[1]) == 0 or verify_coef(elements[0][1:]) == 0:
                return {}
        else:
            if verify_variables(elements[1]) == 0 or verify_coef(elements[0]) == 0:
                return {}
        if i == 0:
            juice_data[elements[1]] = float(eval(elements[0]))
        else:
            juice_data[elements[1]] = float(eval(zexpression[i - 1] + elements[0]))
    return juice_data

def utils_for_c(j, juice_data, data, inegal):
    if data != '':
        one_constraint = data.split(' ')
        my_len = one_constraint.__len__()
        if my_len < 3:
            return 0
        if (one_constraint[-1][0] == '+' or one_constraint[-1][0] == '-'):
            if verify_coef(one_constraint[-1][1:]) == 0:
                return 0
        if not(one_constraint[-1][0] == '+' or one_constraint[-1][0] == '-'):
            if verify_coef(one_constraint[-1]) == 0:
                return 0
        if not(one_constraint[-2] == '<=' or one_constraint[-2] == '>=' or one_constraint[-2] == '='):
            return 0
        
        expression = one_constraint[0:my_len-2]
        if (my_len - 2) % 2 == 0:
            return 0
        if (my_len - 2) > 1:
            for i in range(1, (my_len - 2), 2):
                if expression[i] != '+' and expression[i] != '-':
                    return 0
        for i in range(0, (my_len - 2), 2):
            elements = expression[i].split('*')
            if len(elements) != 2:
                return 0
            if i == 0:
                if verify_variables(elements[1]) == 0 or verify_coef(elements[0][1:]) == 0:
                    return 0
            else:
                if verify_variables(elements[1]) == 0 or verify_coef(elements[0]) == 0:
                    return 0
            if i == 0:
                juice_data[elements[1]] = float(eval(elements[0]))
                inegal.append(one_constraint[-2])
            else:
                juice_data[elements[1]] = float(eval(expression[i - 1] + elements[0]))
        juice_data['B'] = float(eval(one_constraint[-1]))
        if juice_data['B'] < 0:
            juice_data = ligne_corrigee(juice_data)
            if inegal[j] == '<=':
                inegal[j] = '>='
            elif inegal[j] == '>=':
                inegal[j] = '<='
        #print(juice_data)

def c_values_for_tabsimplexe(juice):
    juice_data_list = []
    inegal_list = []

    #Traitements pour les contraintes
    for i in range(juice['C'].__len__()):
        juice_data = {}
        k = utils_for_c(i, juice_data, juice['C'][i], inegal_list)
        if k == 0:
            return [],[]
        if juice_data != {}:
            juice_data_list.append(juice_data)
    return juice_data_list, inegal_list

def my_main(juice):
    juice_data = {}
    if juice['max_min'] == 0:
        z = ligne_corrigee(z_values_for_tabsimplexe(juice))
    else:
        z = z_values_for_tabsimplexe(juice)
    c, inegalite = c_values_for_tabsimplexe(juice)
    if z == {} or c == []:
        return {}
    juice_data['Z'] = z
    juice_data['C'] = c
    #juice_data['max_min'] = juice['max_min']
    juice_data['inegalite'] = inegalite
    return juice_data

#if __name__ == '__main__':
#    retour = my_main(juice)
#    print(retour)