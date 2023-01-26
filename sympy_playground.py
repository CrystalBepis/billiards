from sympy import symbols, pprint, cos, sin, Matrix, Function, simplify, sqrt, expand

a1, a2, b1, b2, x, y = symbols('a_1 a_2 b_1 b_2 x y', real=True)
d = symbols('d', real=True, positive=True)

expr1 = sqrt((x-a1)**2 + (y-a2)**2) + sqrt((x-b1)**2 + (y-b2)**2)
expr2 = (x-a1)**2 + (y-a2)**2 + (x-b1)**2 + (y-b2)**2 + 2*sqrt(((x-a1)**2 + (y-a2)**2)*((x-b1)**2 + (y-b2)**2))
expr3 = ((x-a1)**2 + (y-a2)**2)*((x-b1)**2 + (y-b2)**2)

pprint(simplify(expand(expr3)))
