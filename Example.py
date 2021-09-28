from simplex import Simplex

"""
Expected output:

Adding variable X1
Adding variable X2
Adding objective function: 18 * x1 + 12.5 * x2
Adding constraint: x1 + x2 <= 20
Adding constraint: x1 <= 12
Adding constraint: x2 <= 16

MAXIMISE 18 * x1 + 12.5 * x2
SUBJECT TO
     (None, 'x1 + x2 <= 20')
     (None, 'x1 <= 12')
     (None, 'x2 <= 16')


Basic         x1      x2    Ans.
x3           1.0     1.0    20.0
x4           1.0     0.0    12.0
x5           0.0     1.0    16.0
z           18.0    12.5     0.0

pivot column is x1
pivot row is row 2 (x4)

Basic         x1      x2    Ans.
x3           0.0     1.0     8.0
PIVOTED      1.0     0.0    12.0
x5           0.0     1.0    16.0
z            0.0    12.5

pivot column is x2
pivot row is row 1 (x3)

Basic         x1      x2    Ans.
PIVOTED      0.0     1.0     8.0
PIVOTED      1.0     0.0    12.0
x5           0.0     0.0     8.0
z            0.0     0.0

[18.0, 12.5, 0]


RESULT
X1: 12.0
X2: 8.0
max of 18 * x1 + 12.5 * x2 is:
    316.0
"""

if __name__ == '__main__':
    s = Simplex(show_tableau=True, verbose_output=True)
    s.add_decision_variable("desks")
    s.add_decision_variable("chairs")
    s.add_objective('100 * x2 + 400 * x1')
    s.add_constraint("5 * x1 +3 * x2 <= 40", "hours")
    s.add_constraint("2 * x1 + x2 <= 10", "hardwood_panels")
    s.add_constraint("3 * x1 - x2 <= 0", "storage")
    s.solve()
