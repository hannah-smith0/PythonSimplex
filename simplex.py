import numpy as np


class Simplex:

    def __init__(self, objective_type='max', show_tableau=False, verbose_output=False):
        self.objective = None
        self.objective_type = objective_type  # Can be 'min' or 'max'
        self.show_tableau = show_tableau
        self.verbose_output = verbose_output
        self.variables = []  # Stores the real names for the decision variables
        self.constraints = []
        self.A = []  # The array used to store the variables
        self.b = []  # List to compute the answers
        self.B = []  # List of the basic variables
        self.N = []  # List of the nonbasic variables
        self.c = []  # List that represents the objective function
        self.x = {}  # Dictionary that will output the results for each real variable

    def add_decision_variable(self, name):
        """
        Adds a decision variable to the simplex - these represent the real variables.
        :param name: describes the variable
        """
        print('Adding variable ' + name)
        n = len(self.N)
        self.variables.append(name)
        self.N.append('x' + str(n+1))
        self.c.append(0)  # dummy value

    def add_objective(self, expression):
        """
        Adds an objective function
        :param expression: The objective function as a string.
        """
        if len(self.N) < 2:
            print('You need to add the decision variables first')
            return

        print('Adding objective function: ' + expression)

        # Splits the values in the expression, replacing subtraction with a negative coefficient
        new_expression = expression.replace(' ', '').replace('-', '+-')
        list1 = new_expression.split('+')

        # Matches the values with the decision variables
        for n in self.N:
            for item in list1:
                if item.find(n) > -1:
                    new_value = item[:item.find(n)].replace('*', '')
                    if new_value:
                        if self.objective_type == 'max':
                            self.c[self.N.index(n)] = float(new_value)
                        if self.objective_type == 'min':
                            self.c[self.N.index(n)] = float(new_value * -1)
        self.objective = expression
        self.c.append(0)  # dummy value

    def add_constraint(self, expression, name=None):
        """
        Adds a constraint. The LHS of the equation will be represented as an array with each row representing
        one constraint as a list of the coefficients. The RHS value (a constant) will be added to self.b
        :param expression: The constraint equation as a string, with a lesser than equality sign.
        :param name: Optional label
        """
        if len(self.N) < 2:
            print('You need to add the decision variables first')
            return
        print('Adding constraint: ' + expression)
        self.constraints.append((name, expression))

        lhs = expression[:expression.find('<=')]
        lhs_variables = lhs.replace(' ', '').replace('-', '+-')
        variables_list = lhs_variables.split('+')

        coefficients = [0] * len(self.N)
        for n in self.N:
            for variable in variables_list:
                if variable.find(n) > -1:
                    new_value = variable[:variable.find(n)].replace('*', '')
                    if new_value:
                        try:
                            coefficients[self.N.index(n)] = float(new_value)
                        except ValueError:
                            coefficients[self.N.index(n)] = float(new_value + '1')
                    else:
                        coefficients[self.N.index(n)] = 1
        self.A.append(coefficients)

        rhs = expression[expression.find('<=')+2:].replace(' ', '')
        self.b.append(int(rhs))

    def tableau(self, A, b, c):
        """
        Outputs a tableau to the terminal.
        :param A: the current state of the coefficients array
        :param b: the current state of the answers list (the RHS constants)
        :param c: the current state of the objective function coefficients
        """
        tab = '{:<8}'.format('Basic') + ''.join(['{:>8}'.format(i) for i in self.N])+ '{:>8}'.format('Ans.')
        tab += '\n'
        for i in range(len(self.A)):
            tab += '{:<8}'.format(self.B[i]) + ''.join(['{:>8.1f}'.format(item) for item in A[i]]) + '{:>8.1f}'.format(b[i])
            tab += '\n'
        tab += '{:<8}'.format('z') + ''.join(['{:>8.1f}'.format(item) for item in c]) + '\n'
        print(tab)

    def pivot(self, N, B, A, b, c, l, e):
        """
        Pivots the array around the point in the array
        :param l: The nonbasic variable or row pivot
        :param e: The basic variable or column pivot
        :return: Updated A, N, B, b and c
        """
        newA = []
        m = len(B)
        n = len(N)
        for i in range(m):
            newA.append([])
            for j in range(n):
                newA[i].append(0)

        newb = [0] * m  # dummy array with 0s
        newb[l] = b[l] / A[l][e]

        for j in range(len(N)):
            if j != e:
                newA[l][j] = A[l][j] / A[l][e]
        newA[l][e] = 1

        for i in range(len(B)):
            if i != l:
                newb[i] = A[l][e] * b[i] - A[i][e] * b[l]
                for j in range(len(N)):
                    if j != e:
                        newA[i][j] = A[l][e] * A[i][j] - A[i][e] * A[l][j]

        newc = [0] * n  # dummy array with 0s
        for j in range(len(N)):
            if j != e:
                newc[j] = A[l][e] * c[j] - c[e] * A[l][j]

        B[l] = 'PIVOTED'

        return N, B, newA, newb, newc

    def simplex(self, N, B, A, b, c):
        """
        Uses the simplex algorithm to perform pivots until the list c has no more values greater than 0. Then,
        updates the array of coefficients and updates the answer array (which can be used to determine the values
        for the decision variables)
        :param N: The list of nonbasic variables
        :param B: The list of basic variables
        :param A: The array of coefficients from the constraints
        :param b: The constants from the constraints
        :param c: The objective function coefficients
        """
        delta = [np.inf] * len(b)
        while max(c) > 0:
            e = c.index(max(c))
            for i in range(len(B)):
                if B[i] != 'PIVOTED' and A[i][e] > 0:
                    delta[i] = b[i] / A[i][e]
                if B[i] == 'PIVOTED':
                    delta[i] = np.inf
            l = delta.index(min(delta))
            if l == np.inf:
                print('This equation cannot be solved - it is unbounded')
                return
            else:
                print('pivot column is ' + N[e])
                print('pivot row is row ' + str(l+1) + ' (' + B[l] + ')\n')
                N, B, A, b, c = self.pivot(N, B, A, b, c, l, e)
            if self.show_tableau:
                self.tableau(A, b, c)
        for i in range(len(c)):
            if c[i] != 0:
                self.c[i] = 0
        self.A = A
        self.b = b

    def verbose(self):
        """
        If the output is set to verbose, prints the result for each decision variable and the output of this when
        computed by the objective function
        """
        print('\n\nRESULT')
        total = 0
        for key in self.x.keys():
            print(key + ': ' + str(self.x[key][0]))
            total += self.x[key][1]
        print(self.objective_type + ' of ' + self.objective + ' is: ')
        print('    ' + str(total))

    def solve(self):

        # Check that the variables have been set up
        if len(self.N) < 2:
            print('You need to add the decision variables')
            return
        if self.objective is None:
            print('You need to add an objective function')
            return
        if self.constraints is []:
            print('You need to add constraints')
            return

        # Create the initial basic variables, which will be the slack variables and our objective function
        for i in range(len(self.A)):
            self.B.append('x' + str(i + 1 + len(self.N)))

        if self.objective_type == 'max':
            print('\nMAXIMISE ' + self.objective)
        if self.objective_type == 'mix':
            print('\nMINIMISE ' + self.objective)
        print('SUBJECT TO')
        for c in self.constraints:
            print('    ', c)
        print('\n')

        if self.show_tableau:
            self.tableau(self.A, self.b, self.c)

        self.simplex(self.N, self.B, self.A, self.b, self.c)

        print(self.c)
        for n in range(len(self.N)):
            for m in range(len(self.A)):
                if self.A[m][n] != 0 and self.variables[n] not in self.x.keys():
                    if self.c[n] == 0:
                        self.x[self.variables[n]] = 0, self.b[m]/self.A[m][n]*self.c[n]
                    else:
                        self.x[self.variables[n]] = self.b[m]/self.A[m][n], self.b[m]/self.A[m][n]*self.c[n]
        if self.verbose_output:
            self.verbose()

        return self.x
