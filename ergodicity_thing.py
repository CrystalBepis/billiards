import numpy as np
import matplotlib.pyplot as plt

p1 = (2.0 - np.sqrt(2)/2) / 6.0
p2 = (2.0+np.sqrt(2)/3) / 6.0

v = 0.25 + p1/2.0 - p2

l = 2/5
# l = 1 - np.sqrt(2)/2

def mu(x):
	return (1/np.pi)*np.arccos(np.abs(np.sin(2*np.pi*x)))

def T(x):
	if (l<=0) or (1<=l):
		raise ValueError('invalid l')

	if (0<=x) and (x<l):
		return x+1-l
	elif (l<=x) and (x<1):
		return x-l
	else:
		raise ValueError('invalid x')

	

	# # CCW dir
	# if (0<h) and (h<0.5*(p2-p1)):
	# 	return ((-(h+p2) - 2*v + mu(h+p2+v)) % 1) - 1
	# elif (0.5*(p2-p1)<h) and (h<p2-p1):
	# 	return ((-0.25 - v - 0.5*mu(h+v) + p2) % 1) - 1
	# elif (p2-p1<h) and (h<p2-p1+0.5):
	# 	return (h+p1) % 1
	# elif (p2-p1+0.5<h) and (h<1):
	# 	return (h+p2) % 1

	# # CW dir
	# elif (-1+0<h) and (h<-1+0.5*(p2-p1)):
	# 	return (-(h+p2) - 2*v + mu(h+p2+v)) % 1
	# elif (-1+0.5*(p2-p1)<h) and (h<-1+p2-p1):
	# 	return (-0.25 - v - 0.5*mu(h+v) + p2) % 1
	# elif (-1+p2-p1<h) and (h<-1+p2-p1+0.5):
	# 	return ((h+p1) % 1) - 1
	# elif (-1+p2-p1+0.5<h) and (h<-1+1):
	# 	return ((h+p2) % 1) - 1
	
	# else:
	# 	raise ValueError('invalid input')

def f(x):
	return x
	
	# if (0.0<=x) and (x<l/2.0):
	# 	return 1.0
	# else:
	# 	return 0.0

	# return np.exp(2*np.pi*1j*x)

def main():

	x0 = -1.0
	step_size = 0.005
	n = 10**4

	points_x = np.array([])
	points_y = np.array([])

	while x0 < 1.0:
		try:
			x = x0
			val = 0
			for _ in range(0, n):
				val += f(x)
				x = T(x)
			points_x = np.append(points_x, x0)
			points_y = np.append(points_y, val/n)
			print(x0, val/n)
		except ValueError:
			pass
		x0 += step_size
	# print(points_x)
	# print(points_y)
	fig = plt.figure(dpi=240)
	ax = fig.gca()

	ax.plot(points_x, np.real(points_y))
	# ax.plot(points_x, np.imag(points_y))

	# ax.set_ylim((-0.25, 1.25))
	# ax.set_xlim((-0.25, 1.25))

	ax.set_aspect('equal')
	plt.show()


if __name__ == '__main__':
	main()