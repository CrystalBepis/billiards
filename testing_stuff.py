import sys
from sympy import cos, sin, symbols, diff, simplify, pprint, Function, Matrix, zeros, latex

def sprint(expr):
	pprint(simplify(expr))

u, v = symbols('u v', real=True)

one_half = (1 + 0*u) / (2 + 0*u)

coords = [u, v]

f = Function('f')(u, v)

g = Matrix(2, 2, [f.diff(u, 2), f.diff(u).diff(v), f.diff(v).diff(u), f.diff(v, 2)])

# g[0,1] = 0*u
# g[1,0] = 0*u

g_inv = simplify(g**(-1))# * g.det()

pprint(g_inv)
print()
# sys.exit()

C = [[Matrix(2, 1, [0, 0]) for _ in range(2)] for _ in range(2)]

for i in range(2):
	for j in range(2):
		for k in range(2):
			val = 0*coords[0]
			for h in range(2):
				val += one_half * g_inv[k,h] * (g[h,i].diff(coords[j]) + g[h,j].diff(coords[i]) - g[i,j].diff(coords[h]))
			C[i][j][k] = simplify(val)

R = [[[Matrix(2, 1, [0, 0]) for _ in range(2)] for _ in range(2)] for _ in range(2)]

for b in range(2):
	for i in range(2):
		for j in range(2):
			for k in range(2):
				val1 = 0*coords[0]
				val2 = 0*coords[0]
				for h in range(2):
					val1 += C[j][b][h] * C[i][h][k]
					val2 += C[i][b][h] * C[j][h][k]
				R[b][i][j][k] = simplify(C[j][b][k].diff(coords[i]) - C[i][b][k].diff(coords[j]) + val1 - val2)

Ric = zeros(2)

for b in range(2):
	for j in range(2):
		val = 0*coords[0]
		for h in range(2):
			val += R[b][h][j][h]
		Ric[b,j] = simplify(val)

R_scalar = 0*coords[0]

for i in range(2):
	R_scalar += g_inv[i,i] * Ric[i,i]
R_scalar = simplify(R_scalar)

print(latex(C[0][0]))
print()
print(latex(C[0][1]))
print()
print(latex(C[1][1]))
print()

print(latex(R_scalar))
