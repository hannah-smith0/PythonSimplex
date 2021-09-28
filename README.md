# PythonSimplex
This repository contains code for performing operations using the Simplex algorithm using Python. For information on the Simplex algorithm, see below.

simplex.py contains the code

example.py has an example and the expected output

## What is the Simplex algorithm?
Imagine you are a crafter who builds wooden products, like chairs and desks, who wants to maximise the profit on your work. Desks take 5 hours to build and need 2 hardwood panels, chairs take 3 hours and need 1 hardwood panel. Desks can be sold for a profit of $400 and chairs for a profit of $100. You have 10 panels and 40 hours a week to work on your products. Due to storage limits, you need to make at least 3 times as many chairs as desks. 

How can you work out how many chairs and desk to produce this week to maximise your profit?

This is an example of a linear optimisation problem. Given some linear constraints (usually time, money, or resources), what is the best way to achieve your objective? An objective might be a maximisation of profits, or a minimisation of costs. This can be done using the simplex algorithm, which was first developed to solve military planning problems in World War 2. It was later refined and published by George B. Dantzig in 1947.


## How does it work?
This picture shows a representation of a three-variable simplex. Faces of the simplex represent the variables and corners the potential solution. To solve the problem, you begin at the origin (0,0) and move along an edge to the most promising adjacent corner. This becomes the new pivot, and you repeat until your objective has been achieved. 

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/simplex.png" width="400">

[Figure1 https://web.stanford.edu/group/sisl/k12/optimization/MO-unit3-pdfs/]

Simplex algorithms are capable of solving problems with many variables, but it is difficult to visualise them graphically past three variables. The method of solving them is the same. When working by hand, these ‘pivots’ are calculated using tableaus.

Simplex algorithms require we turn inequality constraints into equality constraints. What is the difference? 
Represented graphically, an inequality will look like a line with a shaded area to represent the parts where there are no solutions. The figure here has three constraints, and the grey area represents where there are solutions, called the feasible region.

<img src="https://files.realpython.com/media/lp-py-fig-1.00f609c97aec.png" width="400">

[Figures 2-4 https://realpython.com/linear-programming-python/#linear-programming-examples]

The inequality constraints are:

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/constraints.png">

What happens when we add the equality constraint, `-x+5y=15`? 
We see this added as a line rather than a shaded area. Our optimal solution lies on the green line somewhere in the grey area.
The objective function, `max⁡〖z=x+2y〗` then tells us that our optimal solution is the maximum possible number, which is at the point located in figure 4 below.

<img src="https://files.realpython.com/media/lp-py-fig-5.11f20dcc5d6b.png" width="400">

Converting our inequality functions into equalities allow you to find the solution without using a graph, which therefore allows you to solve problems with more than three variables.

## How can we use it?
### 1. Convert your word problem into inequality constraints and an objective function
Using our earlier example, lets represent the constraints representing the number of desks as `x1` and the number of chairs as `x2`.

First, our objective function. This represents the relationship between the real-world variables.

* Profit: `max⁡〖400x1 + 100x2 〗`

For the other constraints, we create linear inequalities representing the limits we have on materials and the fact that we cannot have a negative number of chairs or desk.

* Building hours: `5x1 + 3x2 ≤ 40`

* Materials (hardwood panels): `2x1 + x2 ≤ 10`

* Storage limits: `3x1 ≤ x2`

* `x1,x2 ≥ 0`

### 2. Convert the objective function, add slack variables, build an initial tableau.
To use it in the initial tableau, rewrite the objective function to have all nonzero terms on the LHS and a zero on the RHS.

* `Max⁡〖400x1 + 100x2 = 0〗`

Since we changed our equations to equalities, we need to represent the possible difference in value that an inequality sign indicates. To do this, we add “slack” variables. All variables should go on the LHS of your equations, with constants on the RHS. We don’t need to convert the constraint x_1,x_2≥0, but we can assume all variables will be positive.
* `5x1 + 3x2 + x3 = 40`
* `2x1 + x2 + x4 = 10`
* `3x1 - x2 + x5 = 0`
Now we can set up the initial simplex tableau by creating a matrix from the equations, placing the equation for the objective function last. Since our objective function is being maximised, the coefficients from that equation are negative in the matrix. The constraints were all lesser (`<` or `≤`) so the slack variables have positive coefficients. We are aiming to maximise the bottom right cell’s value, since this is the objective function (labelled as `f` here).

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/t1.png">

### 3. Choose a pivot and 
To find the pivot column, look in the bottom row for the most negative indicator.

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/t2.png">

To find the pivot row, choose the number above the bottom row that is neither negative nor 0, but has the smallest ratio when the answer is divided by that column. Below, we have `40 ÷ 5 = 8`, `10 ÷ 2 = 5`, or `0 ÷ 3 = 0`.

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/t3.png">

If you can’t find any numbers above 0 in a column with negative indicators, there isn’t a feasible solution for this problem. If there are two possible pivots, choose the higher one. After pivoting, the column value in the other row will become 0. If the basic variable in that row has negative coefficient, multiply the row by -1.

### 4. Pivot
Pivoting is done by moving from one vertex on the simplex to another by making one of our slack variables nonbasic, in exchange for making one of our “real” variables basic. The basic variables are the ones that are ‘in the basis’ around which our current table is pivoted. They are found in the columns where there is only one number and the rest are 0s. In our initial tableau, the basic variables are our slack variables x_3, x_4, x_5 and the objective function when it is equal to 0. This is how all simplex tableaus begin.

To make a number basic, it must transform to have a single number in the column, with the rest being zeros. You can multiply or divide any row by any number or replace any row with a sum of itself and another row. However, you must include the pivot row in these operations and the answer column must always remain positive. If you do get a negative value there, multiply that row by -1.
  
1. First row = (3 * first row) – (5 * pivot row)
1. Second row = (3 * second row) - (2 * pivot row)
1. Fourth row = (3 * fourth row) - (-400 * pivot row)
1. Divide the pivot row by the value in the pivot column so it becomes 1 (this step is optional)

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/t4.png">

### 5. Repeat steps 3-4 until done
If negative elements still exist in the bottom row, repeat steps 3 and 4.
1.	First row = (5 * first row) – (14 * pivot row)
1.	Third row = (5 * third row) - (-1/3 * pivot row)
1.	Fourth row = (5 * fourth row) - (-700 * pivot row)

The tableau below is what you will end up with if you don’t divide the pivot rows to get a 1 in the column. If you do this, you simply need to divide the answer by whatever is in the column for each real variable.

<img src="https://github.com/hannah-smith0/PythonSimplex/blob/main/t5.png">

When the final matrix has been obtained, determine the final basic solutions. This will give the maximum value for the objective function and the values of the variables where this maximum occurs

Using our tableau above, our solutions are `x1 = 10 ÷ 5 = 2`, `x2 = 6 ÷ 1 = 6`, `f = 21000 ÷ 15 = 1400`. This means our maximum profit is $1400. We can confirm this by checking against the original equation – if we make 2 desks and 6 chairs (which will fulfill our constrain of having at least 3 times as many chairs as desks) we will have `400x1 + 100x2` or `400×2 + 100 × 6 = 800 + 600 = 1400`. 

## Sources
1. Background info on the Simplex https://web.stanford.edu/group/sisl/k12/optimization/MO-unit3-pdfs/ 
1. Ideas for how to display the Simplex tableau https://notebook.community/infimath/optimization-method/Simplex%20Tableau%20in%20Python 
1. Information on Simplex in Python tools https://realpython.com/linear-programming-python/#linear-programming-examples
1. The simplex and pivot algorithms [CLRS] Coreman, T. and Leiserson, C. and Rivest, R. and Stein, C. Linear Programming, Chapter 29 

