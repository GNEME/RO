from re import split
from copy import deepcopy



def sign(string_expression, component):
    component_index = string_expression.find(component)

    if component_index == 0:
        sign = 1
    elif string_expression[component_index - 1] == '+':
        sign = 1
    else:
        sign = -1

    return sign

def extract_expression(string_expression):
    expression = dict()
    components = split(r'[+-]', string_expression)

    if '' in components:
        components.remove('')

    for c in components:
        if len(c.split('*')) == 1:
            variable = c.split('*')[0]
            coef = 1
        else:
            variable = c.split('*')[1]
            coef = c.split('*')[0]

        expression[variable] = sign(string_expression, c) * float(coef)

    return expression



class ConflictingConstraintsException(Exception):
    __slots__ = ['__CONSTRAINT_INDEX']

    def __init__(self,constraint_index):
        self.__CONSTRAINT_INDEX = constraint_index



class ConstraintTypeException(Exception):
    __slots__ = ['__CONSTRAINT_INDEX']

    def __init__(self,constraint_index):
        self.__CONSTRAINT_INDEX = constraint_index



class Tableau:
    __slots__ = ['__BASE','__VARIABLES','__CONSTRAINTS','__OBJ_FCT']

    def __init__(self,base,variables,constraints,function):
        self.__BASE = base
        self.__VARIABLES = variables
        self.__CONSTRAINTS = constraints
        self.__OBJ_FCT = function  #objective function or row

    def base(self):
        #returns a copy of the base associated to the tableau
        return deepcopy(self.__BASE)

    def variables(self):
        # returns a copy of the variables list associated to the tableau
        return deepcopy(self.__VARIABLES)

    def constraints(self):
        # returns a copy of the list of constraints associated to the tableau
        return deepcopy(self.__CONSTRAINTS)

    def objective_function(self):
        # returns a copy of the objective function associated to the tableau
        return deepcopy(self.__OBJ_FCT)

    def solution(self):
        # returns the solution associated to the tableau
        solution = list()

        for var in self.__VARIABLES:
            if var in self.__BASE:
                index_in_base = self.__BASE.index(var)
                value = self.__CONSTRAINTS[index_in_base]['B']
                solution.append((var,value))
            else:
                solution.append((var,0))

        solution.append(('Z',self.__OBJ_FCT['B']))

        return solution

    def data(self):
        tableau = deepcopy(self.__CONSTRAINTS)
        tableau.append(self.__OBJ_FCT)
        #Returns all the data present in the Tableau
        return tableau

    def __max_lenght(self):
        max_lenght = 0

        for line in self.__CONSTRAINTS + [self.__OBJ_FCT]:
            for var in line:
                if len(str(round(line[var],3))) > max_lenght:
                    max_lenght = len(str(round(line[var],3)))

        return max_lenght

    def __print_head(self,max_lenght):
        line = ['|']

        for i in range(max_lenght):
            line.append('_')

        line.append('|')

        for var in self.__VARIABLES + ['B']:
            line.append(var)

            for i in range(max_lenght - len(var)):
                line.append('_')

            line.append('|')

        line = ''.join(line)
        print(line)

    def __print_constraints(self,max_lenght):
        for i in range(len(self.__CONSTRAINTS)):
            line = ['|',self.__BASE[i]]

            for j in range(max_lenght - len(self.__BASE[i])):
                line.append(' ')

            line.append('|')

            for var in self.__VARIABLES + ['B']:
                string = str(round(self.__CONSTRAINTS[i][var],3))
                line.append(string)

                for k in range(max_lenght - len(string)):
                    line.append(' ')

                line.append('|')

            line = ''.join(line)
            print(line)

    def __print_function(self,max_lenght):
        line = ['|Cj']

        for i in range(max_lenght - 2):
            line.append('_')

        line.append('|')

        for var in self.__VARIABLES + ['B']:
            string = str(round(self.__OBJ_FCT[var],3))
            line.append(string)

            for i in range(max_lenght - len(string)):
                line.append('_')

            line.append('|')

        line = ''.join(line)
        print(line)

    def print_tableau(self):
        max_lenght = self.__max_lenght()
        line = list()

        for i in range((max_lenght+1)*(len(self.__VARIABLES)+2)+1):
            line.append('_')

        line = ''.join(line)
        print(line)
        self.__print_head(max_lenght)
        self.__print_constraints(max_lenght)
        self.__print_function(max_lenght)
        print('\n')

    def entering_variable(self,optimal_variables):
        entering = self.__VARIABLES[0]

        for var in self.__VARIABLES:
            if self.__OBJ_FCT[entering] < self.__OBJ_FCT[var]:
                entering = var
            elif self.__OBJ_FCT[entering] == self.__OBJ_FCT[var]:
                if self.is_final() and var not in optimal_variables:
                    entering = var
                    break

        if entering in self.__BASE or entering in optimal_variables:
            entering = None

        return entering

    def leaving_variable_index(self,entering):
        leaving_variable_index = 0

        for i in range(len(self.__CONSTRAINTS)):
            line = deepcopy(self.__CONSTRAINTS[i])

            if self.__CONSTRAINTS[leaving_variable_index][entering] != 0:
                constraint_ratio = self.__CONSTRAINTS[leaving_variable_index]['B']/self.__CONSTRAINTS[leaving_variable_index][entering]
            else:
                leaving_variable_index = i
                continue

            if line[entering] != 0:
                line['B/Col'] = line['B']/line[entering]
                #print(self.__CONSTRAINTS[leaving_variable_index][entering])

            if line[entering] <= 0:
                continue
            elif constraint_ratio < 0:
                leaving_variable_index = i
            elif line['B/Col'] < constraint_ratio:
                leaving_variable_index = i

        return leaving_variable_index

    def __new_base(self,entering,leaving_variable_index):
        new_base = deepcopy(self.__BASE)
        new_base[leaving_variable_index] = entering

        return  new_base

    def pivot(self,entering,leaving_variable_index):
        return self.__CONSTRAINTS[leaving_variable_index][entering]

    def __pivot_line(self,pivot,leaving_variable_index):
        line = deepcopy(self.__CONSTRAINTS[leaving_variable_index])

        for var in line:
            line[var] /= pivot

        return line

    def __new_line(self,line,entering_variable_line,entering):
        new_line = deepcopy(line)
        entering_line = deepcopy(entering_variable_line)

        for var in new_line:
            new_value = line[var] - line[entering]*entering_line[var]
            new_line[var] = new_value

        return new_line

    def nextTableau(self,pivot,entering,leaving_variable_index):
        tableau = self.data()
        new_base = self.__new_base(entering,leaving_variable_index)
        variables = self.variables()
        tableau[leaving_variable_index] = self.__pivot_line(pivot,leaving_variable_index)

        for i in range(len(tableau)):
            if i != leaving_variable_index:
                tableau[i] = self.__new_line(tableau[i],tableau[leaving_variable_index],entering)

        new_constraints = tableau[0:len(tableau)-1]
        new_function = tableau[len(tableau)-1]

        return Tableau(new_base,variables,new_constraints,new_function)

    def is_final(self):
        max_value = self.__OBJ_FCT[self.__VARIABLES[0]]

        for var in self.__VARIABLES:
            if max_value < self.__OBJ_FCT[var]:
                max_value = self.__OBJ_FCT[var]

        if max_value < 0:
            result = True
        else:
            result = False

        return result



class Problem:
    __slots__ = ['__constraints', '__obj_fct', '__MAX_PROBLEM', '__base_solution_variables','__VARIABLES','tableaux']

    def __init__(self, constraints, function, max_problem):
        self.__constraints = constraints
        self.__obj_fct = function
        self.__MAX_PROBLEM = max_problem
        self.__base_solution_variables = set()

    def __data(self):
        data = deepcopy(self.__constraints)
        data.append(self.__obj_fct)

        return data

    def __constraint_type(self,constraint_index):
        if '<=' in self.__constraints[constraint_index]:
            constraint_type = '<='
        elif '>=' in self.__constraints[constraint_index]:
            constraint_type = '>='
        elif '=' in self.__constraints[constraint_index]:
            constraint_type = '='
        else:
            raise ConstraintTypeException(constraint_index)

        return constraint_type

    def __extract_constraints(self):
        constraints = list()

        for i in range(len(self.__constraints)):
            constraint = split(r'[<|>|=]', self.__constraints[i])
            constraint_type = self.__constraint_type(i)

            if '' in constraint:
                constraint.remove('')

            first_member = extract_expression(constraint[0])
            second_member = float(constraint[1])
            constraint = first_member
            constraint['B'] = second_member
            self.__constraints[i] = [constraint,constraint_type]

    def __correct_constraints(self):
        for constraint in self.__constraints:
            if constraint[0]['B'] < 0:
                for var in constraint[0]:
                    constraint[0][var] *= -1

                if constraint[1] == '<=':
                    constraint[1] = '>='
                elif constraint[1] == '>=':
                    constraint[1] = '<='

    def __correct_function(self,base):
        if not self.__MAX_PROBLEM:
            for var in self.__VARIABLES + ['B']:
                self.__obj_fct[var] *= -1

        for i in range(len(base)):
            if 'A' in base[i]:
                for var in self.__VARIABLES + ['B']:
                    self.__obj_fct[var] += self.__constraints[i][var]*10000

    def __final_constraints(self):
        constraints = list()

        for i in range(len(self.__constraints)):
            if self.__constraints[i][1] == '<=':
                self.__constraints[i][0]['E' + str(i+1)] = 1
            elif self.__constraints[i][1] == '>=':
                self.__constraints[i][0]['E' + str(i+1)] = -1
                self.__constraints[i][0]['A' + str(i+1)] = 1
            else:
                self.__constraints[i][0]['A' + str(i + 1)] = 1

            constraint = self.__constraints[i][0]
            constraints.append(constraint)

        return constraints

    #This function returns the list of all the variables used in this problem
    def __variables(self):
        variables=list()

        #We first extract all the variables present in the objective function
        for var in self.__obj_fct:
            if var != 'B' and var not in variables:
                variables.append(var)

        #We then do the same in all the constraints
        for constraint in self.__constraints:
            for var in constraint:
                if var !=  'B' and var not in variables:
                    variables.append(var)

        self.__VARIABLES = variables

    def __complete_lines(self):
        self.__obj_fct['B'] = 0

        for var in self.__VARIABLES:
            for constraint in self.__constraints:
                if var not in constraint:
                    constraint[var] = 0

            if var not in self.__obj_fct:
                self.__obj_fct[var] = 0

            if 'A' in var:
                if self.__MAX_PROBLEM:
                    self.__obj_fct[var] = -10000
                else:
                    self.__obj_fct[var] = 10000


    """This method extracts all the data present in the 
    objective function and constraints which all strings"""
    def __extract_data(self):
        self.__obj_fct = extract_expression(self.__obj_fct)
        self.__extract_constraints()
        self.__correct_constraints()
        self.__constraints = self.__final_constraints()
        self.__variables()
        self.__complete_lines()

    def starting_base(self):
        base = list()

        for i in range(len(self.__constraints)):
            constraint = self.__constraints[i]

            if ('A'+str(i+1)) in constraint:
                var = 'A'+str(i+1)
            else:
                var = 'E'+str(i+1)

            base.append(var)

        return base

    def solve(self):
        self.__extract_data()
        tableaux = list()
        optimal_variables = set()
        starting_base = self.starting_base()
        self.__correct_function(starting_base)

        tableau = Tableau(starting_base,self.__VARIABLES,self.__constraints,self.__obj_fct)
        tableaux.append(tableau)

        if tableau.is_final():
            optimal_variables.update(tableau.base())

        entering = tableau.entering_variable(optimal_variables)

        if tableau.is_final():
            if tableau.objective_function()[entering] != 0:
                entering = None

        while(entering != None):
            leaving_index = tableau.leaving_variable_index(entering)

            if leaving_index == 0:
                if tableau.constraints()[0][entering] <= 0:
                    break

            pivot = tableau.pivot(entering,leaving_index)
            tableau = tableau.nextTableau(pivot,entering,leaving_index)
            tableaux.append(tableau)

            if tableau.is_final():
                optimal_variables.update(tableau.base())

            entering = tableau.entering_variable(optimal_variables)

        return  tableaux