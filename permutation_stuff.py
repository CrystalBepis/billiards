from itertools import permutations

def filter(arr):
	for i in range(len(arr)-1):
		if arr[i+1]-arr[i] == 1:
			return True
	return False

def sign(arr):
	n = len(arr)
	count = 0
	for i in range(0, n):
		for j in range(i+1, n):
			if arr[i] > arr[j]:
				count += 1
	
	return count % 2


n = 4
perms = permutations([i for i in range(1, n+1)])

for perm in list(perms):
	if not filter(perm):
		print(perm, sign(perm))
