import numpy as np
from itertools import permutations

def main():
	perm = permutations([1, 2, 3, 4, 5], 2)

	for obj in list(perm):
		print(obj)

if __name__ == '__main__':
	main()