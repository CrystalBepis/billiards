import sys
import shapes
import planar
from runner import runner
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

# init_point
# init_angle
# list of objects in scene

def produce_boundary_points(init_point: planar.Vec2, init_angle: float, num_points: int, object_list: 'list[shapes.shape]') -> 'list[list[float], list[float]]':
	runner1 = runner(init_point, init_angle, object_list, 1e-5, 1e5, 0.2)

	points = [runner1.pos]

	result = 1
	while len(points) < num_points:
		last_result = result

		while result == 0:
			result = runner1.march()
		
		if (last_result == 1) and (result == 1):
			runner1.pos = runner1.blind_march()
			result = runner1.march()
		elif (last_result == 0) and (result == 1):
			shape_index, safe_dist = runner1.closest_object()
			runner1.reflect(runner1.pos, shape_index)
			points.append(runner1.pos)
		elif result == 2:
			break

	points_x = []
	points_y = []
	for point in points:
		points_x.append(point.x)
		points_y.append(point.y)
	
	return points_x, points_y

def main():
	# rho0 = 1.0/5.0 - 2.0**(1.0/2.0)/20.0
	# rho1 = 1.0/5.0 + 2.0**(1.0/2.0)/20.0

	# phi0 = 2 * np.pi * rho0
	# phi1 = 2 * np.pi * rho1

	# R0 = float(np.sqrt(2.0 / (1 + np.cos(phi0))))
	# R1 = float(np.sqrt(2.0 / (1 + np.cos(phi1))))

	# print(R0, R1)

	# arc1 = shapes.arc(planar.Vec2(0, 0), R0, planar.Vec2(-1, 0), np.pi)
	# arc2 = shapes.arc(planar.Vec2(0, 0), R1, planar.Vec2(1, 0), np.pi)
	# line_seg1 = shapes.line_seg(planar.Vec2(0, R0), planar.Vec2(0, R1))
	# line_seg2 = shapes.line_seg(planar.Vec2(0, -R1), planar.Vec2(0, -R0))
	# # circle1 = shapes.circle(planar.Vec2(0, 0), 2.0)
	# # ellipse1 = shapes.ellipse(planar.Vec2(-1.5, 0), planar.Vec2(1.5, 0), 4.0)

	# # arc1 = shapes.arc(planar.Vec2(0, 0), 2.0, planar.Vec2(1, 1), np.pi / 2.0)
	# # arc2 = shapes.arc(planar.Vec2(0, 0), 1.0, planar.Vec2(-1, 1), np.pi / 2.0)
	# # line_seg1 = shapes.line_seg(planar.Vec2(0, 1), planar.Vec2(0, 2))
	# # line_seg2 = shapes.line_seg(planar.Vec2(-1, 0), planar.Vec2(2, 0))

	# temp_angle = 0*np.pi / 4

	# init_point = shapes.rot_vec(planar.Vec2(-R0, 0), temp_angle)
	# init_angle = (np.pi / 2.0 - phi0 / 2.0) + temp_angle

	# init_point = shapes.rot_vec(planar.Vec2(R1, 0), temp_angle)
	# init_angle = np.pi - (np.pi / 2.0 - phi1 / 2.0) + temp_angle

	# object_list1 = [arc1, arc2, line_seg1, line_seg2]

	alpha0 = 1.0 / 5.0 * np.pi

	init_point = planar.Vec2(-1, 0)

	object_list1 = [shapes.circle(planar.Vec2(0, 0), 1.0)]
	init_angle = np.pi / 2.0 - alpha0

	points_x, points_y = produce_boundary_points(init_point, init_angle, 6, object_list1)
	
	fig = plt.figure(dpi=240)
	ax = fig.gca()

	# camera = Camera(fig)
	# detail = 20
	# T = np.linspace(0, 2*np.pi, 100)
	# for i in range(-detail, detail):
	# 	print(i)
	# 	temp_angle = np.pi * i / (2*(detail + 1))
	# 	init_point = shapes.rot_vec(planar.Vec2(R1, 0), temp_angle)
	# 	init_angle = np.pi - (np.pi / 2.0 - phi1 / 2.0) + temp_angle
	# 	points_x, points_y = produce_boundary_points(init_point, init_angle, 30, object_list1)
	# 	runner1 = runner(init_point, init_angle, object_list1, 1e-5, 1e5, 0.2)
	# 	for object in runner1.objects:
	# 		ax.plot(*object.get_plot_data(100), 'r', linewidth=0.5)

	# 	ax.plot(points_x, points_y, 'b', linewidth=0.5)
	# 	ax.plot([points_x[0]], [points_y[0]], 'go', markersize=5)
	# 	ax.plot([points_x[-1]], [points_y[-1]], 'ro', markersize=5)

	# 	ax.plot(np.cos(T), np.sin(T), 'r', linewidth=0.5)

	# 	ax.set_aspect('equal')
	# 	camera.snap()
	
	# anim = camera.animate(blit=True)
	# anim.save('test1.mp4')

	runner1 = runner(init_point, init_angle, object_list1, 1e-5, 1e5, 0.2)
	for object in runner1.objects:
		ax.plot(*object.get_plot_data(100), 'r', linewidth=0.5)
	
	T = np.linspace(0, 2*np.pi, 100)
	U = np.cos(T) * 1.0 * np.cos(alpha0)
	V = np.sin(T) * 1.0 * np.cos(alpha0)

	ax.plot(U, V, 'g', linewidth=0.5)

	ax.plot(points_x, points_y, 'b', linewidth=0.5)
	ax.plot([points_x[0]], [points_y[0]], 'go', markersize=5)
	ax.plot([points_x[-1]], [points_y[-1]], 'ro', markersize=5)

	T = np.linspace(0, 2*np.pi, 100)
	ax.plot(np.cos(T), np.sin(T), 'r', linewidth=0.5)

	ax.set_aspect('equal')

	plt.show()

if __name__ == "__main__":
	main()
