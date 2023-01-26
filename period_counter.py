import functools
import sys
import numpy as np
import typing

epsilon = 10**(-7)

def mu(p):
	return (1.0 / np.pi) * np.arccos(np.abs(np.sin(2*np.pi*p)))

def std_interval(h):
	return ((h - 0.5) % 1) - 0.5

def g(h, p1, p2):
	v = 0.25 + p1/2.0 - p2

	# CCW dir
	if (0<h) and (h<0.5*(p2-p1)):
		return ((-(h+p2) - 2*v + mu(h+p2+v)) % 1) - 1
	elif (0.5*(p2-p1)<h) and (h<p2-p1):
		return ((-0.25 - v - 0.5*mu(h+v) + p2) % 1) - 1
	elif (p2-p1<h) and (h<p2-p1+0.5):
		return (h+p1) % 1
	elif (p2-p1+0.5<h) and (h<1):
		return (h+p2) % 1

	# CW dir
	elif (-1+0<h) and (h<-1+0.5*(p2-p1)):
		return (-(h+p2) - 2*v + mu(h+p2+v)) % 1
	elif (-1+0.5*(p2-p1)<h) and (h<-1+p2-p1):
		return (-0.25 - v - 0.5*mu(h+v) + p2) % 1
	elif (-1+p2-p1<h) and (h<-1+p2-p1+0.5):
		return ((h+p1) % 1) - 1
	elif (-1+p2-p1+0.5<h) and (h<-1+1):
		return ((h+p2) % 1) - 1
	
	else:
		raise ValueError('invalid input')

def g0(h: float, d: bool, p1: float, p2: float):
	v = 0.25 + 0.5*p1 - p2
	h_std = std_interval(h)

	if d:  # if CCW
		if (0 < h_std-v) and (h_std - v < p2-p1):
			return (h + (-2*h_std + 2*(0.5*(p2-p1) + v)), False)
		elif (p2-p1 < h_std-v) and (h_std-v < 0.5-v):
			return (h+p1, True)
		elif (p2-p1+0.5-1 < h_std-v) and (h_std-v < 0):
			return (h+p2, True)
		elif (-0.5-v < h_std-v) and (h_std-v < p2-p1+0.5-1):
			return (h+p1, True)
		else:
			raise ValueError('invalid input')
	else:  # if CW
		if (-(p2-p1) < h_std+v) and (h_std+v < 0):
			return (h + (-2*h_std - 2*(0.5*(p2-p1) + v)), True)
		elif (0 < h_std+v) and (h_std+v < 1-(p2-p1+0.5)):
			return (h-p2, False)
		elif (1-(p2-p1+0.5) < h_std+v) and (h_std+v < 0.5+v):
			return (h-p1, False)
		elif (-0.5+v < h_std+v) and (h_std+v < -(p2-p1)):
			return (h-p1, False)
		else:
			raise ValueError('invalid input')


def produce_period(h0, p1, p2) -> typing.Tuple[int, int]:
	bad_attempt = False

	P0 = 0.0
	P12 = 0.5*(p2-p1)
	P1 = p2-p1
	P2 = p2-p1+0.5

	Q0 = -1+0.0
	Q12 = -1+0.5*(p2-p1)
	Q1 = -1+p2-p1
	Q2 = -1+p2-p1+0.5

	important_vals = (P0, P12, P1, P2, Q0, Q12, Q1, Q2)

	for val in important_vals:
		if abs(h0 - val) < epsilon:
			bad_attempt = True
			break

	adj_per_count = 0
	per_count = 0
	htemp = h0

	while not bad_attempt:
		for val in important_vals:
			if abs(htemp - val) < epsilon:
				bad_attempt = True
				break

		try:
			htemp = g(htemp, p1, p2)
		except ValueError:
			bad_attempt = True
			break
		
		adj_per_count = adj_per_count + 1

		if ((0<htemp) and (htemp<p2-p1)) or ((-1+0<htemp) and (htemp<-1+p2-p1)):
			per_count = per_count + 2
		else:
			per_count = per_count + 1

		if (abs(htemp - h0) < epsilon) or bad_attempt:
			break
	
	if bad_attempt:
		return (-1, -1)
	else:
		return (adj_per_count, per_count)

def from_pq_to_std(h, p1, p2):
	v = 0.25 + 0.5*p1 - p2
	if (h<-1) or (1<=h):
		raise ValueError('invalid input; must be in [-1,1)')
	if (0<=h) and (h<1):
		return (std_interval(h+v), True)
	elif (-1<=h) and (h<0):
		return (std_interval(-(h+v)), False)

def produce_period_with_winding_number(h0, p1, p2) -> typing.Tuple[int, int, int]:
	bad_attempt = False

	P0 = 0.0
	P12 = 0.5*(p2-p1)
	P1 = p2-p1
	P2 = p2-p1+0.5

	Q0 = -1+0.0
	Q12 = -1+0.5*(p2-p1)
	Q1 = -1+p2-p1
	Q2 = -1+p2-p1+0.5

	important_vals = (P0, P12, P1, P2, Q0, Q12, Q1, Q2)

	for val in important_vals:
		if abs(h0 - val) < epsilon:
			bad_attempt = True
			break

	adj_per_count = 0
	per_count = 0
	winding_number = 0
	htemp = h0
	htemp_w = h0_std = from_pq_to_std(h0, p1, p2)

	while not bad_attempt:
		for val in important_vals:
			if abs(htemp - val) < epsilon:
				bad_attempt = True
				break

		try:
			htemp = g(htemp, p1, p2)
			htemp_w = g0(*htemp_w, p1, p2)
		except ValueError:
			bad_attempt = True
			break
		
		adj_per_count = adj_per_count + 1

		if ((0<htemp) and (htemp<p2-p1)) or ((-1+0<htemp) and (htemp<-1+p2-p1)):
			per_count = per_count + 2
		else:
			per_count = per_count + 1

		if (abs(htemp - h0) < epsilon) or bad_attempt:
			break
	
	winding_number = int(htemp_w[0] - h0_std[0])

	if bad_attempt:
		return (-1, -1, -1)
	else:
		return (adj_per_count, per_count, winding_number)

def produce_period_set(p1, p2, step_size) -> typing.Set[typing.Tuple[int, int]]:
	per_set = set()

	h0 = -1
	while h0 < 1:
		adj_per_count, per_count = produce_period(h0, p1, p2)

		if adj_per_count != -1:
			per_set.add((adj_per_count, per_count))
		
		h0 = h0 + step_size

	return per_set

def produce_period_set_with_winding_number(p1, p2, step_size) -> typing.Set[typing.Tuple[int, int, int]]:
	per_set = set()

	h0 = -1
	while h0 < 1:
		adj_per_count, per_count, winding_number = produce_period_with_winding_number(h0, p1, p2)

		if adj_per_count != -1:
			per_set.add((adj_per_count, per_count, winding_number))
		
		h0 = h0 + step_size
	
	return per_set

def gcd(x: int, y: int) -> int:
	while y:
		x, y = y, x % y
	
	return abs(x)

def GCD(*arg: int) -> int:
	if len(arg) == 1:
		return arg[0]
	elif len(arg) == 2:
		return gcd(*arg)
	else:
		return functools.reduce(lambda x, y: gcd(x, y), arg)

def lcm(x: int, y: int) -> int:
	return int(abs(x*y) / gcd(x, y))

def LCM(*arg: int) -> int:
	if len(arg) == 1:
		return arg[0]
	elif len(arg) == 2:
		return lcm(*arg)
	else:  # len(arg) > 2
		return functools.reduce(lambda x, y: lcm(x, y), arg)

def is_prime(n: int) -> bool:
	for i in range(2, int(n/2) + 1):
		if n % i == 0:
			return False
	
	return True


def produce_data_adj_per(depth):
	data_list = []

	for b in range(1, depth+1):
		for d in range(1, depth+1):
			for a in range(1, depth+1):
				for c in range(1, depth+1):
					# 0 < a/b < c/d < 1/2
					# gcd(a,b)=1 and gcd(c,d)=1
					if rot_nums_condition(a, b, c, d):
						p1 = a/b
						p2 = c/d
						pers_set = produce_period_set(p1, p2, 0.01)
						adj_per_set = set(x[1] for x in pers_set)  # list(np.sort(list(x[0] for x in pers_set)))

						data_list.append([a, b, c, d, adj_per_set])

	new_data_list = []

	while len(data_list) > 0:
		a, b, c, d, adj_per_set = data_list[0]

		new_data_list.append([adj_per_set])

		j = 0
		while j < len(data_list):
			if data_list[j][4] == adj_per_set:
				a, b, c, d = data_list[j][0:4]
				new_data_list[-1].append([a, b, c, d])
				del data_list[j]
			else:
				j += 1
	
	# new_data_list.sort(key=lambda e: min(e[0]))
	new_data_list.sort(key=lambda e: LCM(*(e[0])))

	return new_data_list

def main():
	new_data_list = produce_data_adj_per(8)

	for i in range(len(new_data_list)):
		adj_per_set = new_data_list[i][0]
		print(adj_per_set)
		for a, b, c, d in new_data_list[i][1:]:
			print(str(a) + '/' + str(b), str(c) + '/' + str(d))
		print()
	
	# primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	# for b in primes:
	# 	for d in primes:
	# 		for a in range(1, b+1):
	# 			for c in range(1, d+1):
	# 				if rot_nums_condition(a, b, c, d):
	# 					per_set = produce_period_set_with_winding_number(a/b, c/d, 0.01)
	# 					gcd1 = GCD(a*d+b*c, b*d)
	# 					gcd2 = GCD(a*c, b*d)
	# 					print(str(a) + '/' + str(b), str(c) + '/' + str(d), per_set, str(int((a*d+b*c)/gcd1)) + '/' + str(int(b*d/gcd1)), str(int(a*c/gcd2)) + '/' + str(int(b*d/gcd2)))
	# 		print()
	
	

	# p1 = (2.0 - np.sqrt(2)/2) / 6.0
	# p2 = (2.0 + np.sqrt(2)/2) / 6.0

	# print(produce_period_set_with_winding_number(p1, p2, 0.01))



def rot_nums_condition(a, b, c, d):
	# 0 < a/b < c/d < 1/2
	# gcd(a,b)=1 and gcd(c,d)=1
	return (GCD(a, b) == 1) and (GCD(c,d) == 1) and (a*d < b*c) and (2*a < b) and (2*c < d) and (0 < a) and (0 < c)

if __name__ == '__main__':
	main()
