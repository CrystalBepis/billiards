import numpy as np
import planar
import shapes

class runner:
	def __init__(self, init_pos: planar.Vec2, init_dir: float, objects: 'list[shapes.shape]', epsilon: float, omega: float, step_size: float):
		if objects == []:
			raise ValueError("list of objects is empty")
		if epsilon <= 0:
			raise ValueError("epsilon must be strictly greater than 0")
		if omega <= 0:
			raise ValueError("omega must be strictly greater than 0")
		if epsilon >= omega:
			raise ValueError("epsilon must be strictly lass than omega")
		if (step_size <= 0) or (step_size >= 1):
			raise ValueError("step size must be inside the interval (0, 1)")
		self.__pos = init_pos
		self.__direction = init_dir
		self.__objects = objects
		self.__epsilon = epsilon
		self.__omega = omega
		self.__step_size = step_size
	
	@property
	def pos(self) -> planar.Vec2:
		return self.__pos
	
	@property
	def direction(self) -> float:
		return self.__direction
	
	@pos.setter
	def pos(self, pos: planar.Vec2):
		self.__pos = pos
	
	@property
	def objects(self) -> 'list[shapes.shape]':
		return self.__objects

	@property
	def epsilon(self) -> float:
		return self.__epsilon
	
	@property
	def omega(self) -> float:
		return self.__omega
	
	@property
	def step_size(self) -> float:
		return self.__step_size
	
	def safe_radius(self) -> float:
		min_dist = abs(self.__objects[0].measure_to(self.__pos))
		for i in range(1, len(self.__objects)):
			min_dist = np.min([min_dist, abs(self.__objects[i].measure_to(self.__pos))])
		
		return min_dist
	
	def closest_object(self) -> 'tuple[int, float]':
		min_dist = abs(self.__objects[0].measure_to(self.__pos))
		min_index = 0
		for i in range(1, len(self.__objects)):
			check_dist = abs(self.__objects[i].measure_to(self.__pos))
			if check_dist < min_dist:
				min_dist = check_dist
				min_index = i
		
		return (min_index, min_dist)
	
	def get_dir_vector(self) -> planar.Vec2:
		return planar.Vec2(np.cos(self.__direction), np.sin(self.__direction))

	def march(self) -> int:
		safe_dist = self.safe_radius()
		if (safe_dist < self.__epsilon):
			return 1
		
		elif (self.__omega < safe_dist):
			return 2
		
		else:
			dir_vector = self.get_dir_vector()
			self.__pos = self.__pos + (safe_dist * self.__step_size) * dir_vector
			return 0
	
	# note because safe_dist is set to epsilon when it is 0 this could result in going through boundaries
	def blind_march(self) -> planar.Vec2:
		safe_dist = self.safe_radius()
		dir_vec = self.get_dir_vector()
		if safe_dist == 0:
			safe_dist = self.__epsilon
		return self.__pos + (safe_dist * self.__step_size) * dir_vec
	
	def reflect(self, pos: planar.Vec2, shape_index: int):
		normal_vec = self.__objects[shape_index].get_normal(pos)
		dir_vec = self.get_dir_vector()
		new_dir_vec = dir_vec - (2*(dir_vec.dot(normal_vec))) * normal_vec
		self.__direction = planar.Vec2(1,0).angle_to(new_dir_vec) * np.pi / 180.0

