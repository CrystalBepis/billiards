from re import I
import sys
import numpy as np

def GCD(x: int, y: int) -> int:
	while y:
		x, y = y, x % y
	
	return abs(x)

def LCM(x: int, y: int) -> int:
	return int(x*y / GCD(x, y))

def largest_prime_factor(n: int) -> int:
	i = 2
	while i*i <= n:
		if n % i:  # if n is not divisible by i then add 1 to i
			i += 1
		else:  # if n is divisible by i then divide n by i
			n //= i
	
	return n

def smallest_prime_factor(n: int) -> int:
	if n % 2 == 0:
		return 2
	
	i = 3
	while i*i <= n:
		if n % i == 0:
			return i
		i += 2
	
	return n

def prime_factorization(n: int) -> int:
	factor_list = []

	while n > 1:
		p = smallest_prime_factor(n)
		k = 0
		while n % p == 0:
			n = int(n / p)
			k += 1
		factor_list.append((p, k))
	
	return factor_list

def main(order: int):
	# print(order)
	p_fact = prime_factorization(order)
	print(p_fact)
	for p, n in p_fact:
		m = int(order / p**n)

		print(p, n, m)

		Np = 1
		while Np*Np <= m:
			if m % Np == 0:
				if (Np - 1) % p == 0:
					print(Np, end=', ')
			Np += 1
		
		print('\n')


if __name__ == '__main__':
	main(int(input()))
	# main(0)