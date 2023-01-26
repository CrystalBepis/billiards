import planar
import numpy as np
from abc import abstractmethod

def J(v: planar.Vec2) -> planar.Vec2:
	return planar.Vec2(-v.y, v.x)

def J_inv(v: planar.Vec2) -> planar.Vec2:
	return planar.Vec2(v.y, -v.x)

def rot_vec(v: planar.Vec2, theta: float) -> planar.Vec2:
	return planar.Vec2(np.cos(theta)*v.x - np.sin(theta)*v.y, np.sin(theta)*v.x + np.cos(theta)*v.y)

class shape:
	@abstractmethod
	def distance_to(self, point: planar.Vec2) -> float:
		pass

	# for when an exact distance is not possible
	@abstractmethod
	def measure_to(self, point: planar.Vec2) -> float:
		return self.distance_to(point)

	@abstractmethod
	def get_normal(self, pos: planar.Vec2) -> planar.Vec2:
		pass

	@abstractmethod
	def get_plot_data(self, detail: int) -> 'list[list[float], list[float]]':
		if detail <= 0:
			raise ValueError("detail must be strictly greater than 0")
		...
	
	

class circle(shape):
	def __init__(self, center: planar.Vec2, radius: float):
		if radius <= 0.0:
			raise ValueError("radius must be strictly greater than 0")
		self.__center = center
		self.__radius = radius
	
	@property
	def center(self) -> planar.Vec2:
		return self.__center
	
	@property
	def radius(self) -> float:
		return self.__radius

	def distance_to(self, point: planar.Vec2) -> float:
		return self.__center.distance_to(point) - self.__radius
	
	def measure_to(self, point: planar.Vec2) -> float:
		return super().measure_to(point)
	
	def __str__(self) -> str:
		# return ('circle with center %r and radius $.2f' % (self.center, self.radius))
		return 'circle with center ' + str(self.__center) + ' and radius ' + str(self.__radius)
	
	def get_normal(self, pos: planar.Vec2) -> planar.Vec2:
		if (pos - self.__center).is_null:
			raise ValueError("given position is center")
		return (pos - self.center).normalized()
	
	def get_plot_data(self, detail: int) -> 'list[list[float], list[float]]':
		super().get_plot_data(detail)
		T = np.linspace(0, 2*np.pi, detail)
		return self.__radius*np.cos(T) + self.__center.x, self.__radius*np.sin(T) + self.__center.y

class line_seg(shape):
	def __init__(self, point_a: planar.Vec2, point_b: planar.Vec2):
		if (point_a - point_b).is_null:
			raise ValueError("endpoints of line segment must be different")
		self.__point_a = point_a
		self.__point_b = point_b
		u1 = (point_b - point_a) / point_b.distance_to(point_a)
		self.__u1 = u1
		self.__u2 = planar.Vec2(-u1.y, u1.x)
	
	@property
	def point_a(self) -> planar.Vec2:
		return self.__point_a
	
	@property
	def point_b(self) -> planar.Vec2:
		return self.__point_b
	
	@property
	def u1(self):
		return self.__u1
	
	@property
	def u2(self):
		return self.__u2
	
	def distance_to(self, point: planar.Vec2) -> float:
		l2 = (self.__point_b-self.__point_a).length2
		t = max([0, min(1, (point-self.__point_a).dot(self.__point_b-self.__point_a) / l2)])
		projection = self.__point_a + t*(self.__point_b-self.__point_a)
		return point.distance_to(projection)
	
	def measure_to(self, point: planar.Vec2) -> float:
		return super().measure_to(point)
	
	def __str__(self) -> str:
		return 'line segment with endpoints ' + str(self.__point_a) + ' and ' + str(self.__point_b)
	
	def param(self, t: float) -> planar.Vec2:
		return (self.__point_b - self.__point_a)*t + self.__point_a
	
	def get_normal(self, pos: planar.Vec2) -> planar.Vec2:
		return self.__u2
	
	def get_plot_data(self, detail: int) -> 'list[list[float], list[float]]':
		super().get_plot_data(detail)
		return [[self.__point_a.x, self.__point_b.x], [self.__point_a.y, self.__point_b.y]]

class ellipse(shape):
	def __init__(self, focus1: planar.Vec2, focus2: planar.Vec2, dist: float) -> float:
		if (focus2 - focus1).is_null:
			raise ValueError("foci must be distinct")
		if dist**2 <= (focus2 - focus1).length2:
			raise ValueError("distance must be strictly greater than distance between foci")
		focus_dist = focus2.distance_to(focus1)
		u1 = (focus2 - focus1) / focus_dist
		self.__focus_dist = focus_dist
		self.__dist = dist
		self.__focus1 = focus1
		self.__focus2 = focus2

		self.__a = dist / 2.0
		self.__b = 0.5 * np.sqrt(dist**2 - focus_dist**2)
		self.__u1 = u1
		self.__u2 = planar.Vec2(-u1.y, u1.x)
		self.__center = (focus1 + focus2) / 2.0

	@property
	def focus_dist(self):
		return self.__focus_dist
	
	@property
	def dist(self):
		return self.__dist
	
	@property
	def major_axis_dist(self):
		return self.__a
	
	@property
	def minor_axis_dist(self):
		return self.__b
	
	def distance_to(self, point: planar.Vec2) -> float:
		raise NotImplementedError("no analytic way of doing this exists")

	
	def measure_to(self, point: planar.Vec2) -> float:
		return (point - self.__focus1).length + (point - self.__focus2).length - self.__dist
	
	def __str__(self) -> str:
		return 'ellipse with foci at' + self.__focus1 + ' and ' + self.__focus2 + ' with distance parameter ' + str(self.__dist)
	
	def get_normal(self, pos: planar.Vec2) -> planar.Vec2:
		pos_c = pos - self.__center
		val_x = self.__u1.x * pos_c.x + self.__u1.y * pos_c.y
		val_y = -self.__u1.y * pos_c.x + self.__u1.x * pos_c.y
		x_component = (self.__u1.x / self.__a**2) * val_x - (self.__u1.y / self.__b**2) * val_y
		y_component = (self.__u1.y / self.__a**2) * val_x + (self.__u1.x / self.__b**2) * val_y
		return planar.Vec2(x_component, y_component).normalized()
	
	def get_plot_data(self, detail: int) -> 'list[list[float], list[float]]':
		super().get_plot_data(detail)
		T = np.linspace(0, 2*np.pi, detail)
		return self.__a*np.cos(T)*self.__u1.x + self.__b*np.sin(T)*self.__u2.x + self.__center.x, self.__a*np.cos(T)*self.__u1.y + self.__b*np.sin(T)*self.__u2.y + self.__center.y

class arc(circle):
	def __init__(self, center: planar.Vec2, radius: float, cut_dir: planar.Vec2, cut_angle: float):
		super().__init__(center, radius)
		if cut_dir.is_null:
			raise ValueError("cut_dir must be a non-zero vector")
		if not ((0 < cut_angle) and (cut_angle < 2 * np.pi)):
			raise ValueError("cut_angle must be in (0, 2*pi)")
		cut_dir = cut_dir / cut_dir.length
		self.__cut_dir = cut_dir
		self.__v = -cut_dir # tells us whether to use regular circle distance
		self.__u = planar.Vec2(-cut_dir.y, cut_dir.x) # tells us which point to measure distance to
		self.__cut_angle = cut_angle
		self.__intersection_a = radius * rot_vec(cut_dir, -cut_angle / 2.0) + center
		self.__intersection_b = radius * rot_vec(cut_dir, cut_angle / 2.0) + center

	@property
	def u(self) -> planar.Vec2:
		return self.__u
	
	@property
	def v(self) -> planar.Vec2:
		return self.__v
	
	@property
	def cut_angle(self) -> float:
		return self.__cut_angle
	
	@property
	def intersection_a(self) -> planar.Vec2:
		return self.__intersection_a
	
	@property
	def intersection_b(self) -> planar.Vec2:
		return self.__intersection_b
	
	def distance_to(self, point: planar.Vec2) -> float:
		if (point - self.center).dot(self.__cut_dir) / (point - self.center).length > np.cos(self.__cut_angle / 2.0):
			return super().distance_to(point)
		elif (point - self.center).dot(self.__u) > 0:
			return self.__intersection_b.distance_to(point)
		else:
			return self.__intersection_a.distance_to(point)
	
	def measure_to(self, point: planar.Vec2) -> float:
		return self.distance_to(point)
	
	def get_normal(self, pos: planar.Vec2) -> planar.Vec2:
		return super().get_normal(pos)
	
	def get_plot_data(self, detail: int) -> 'list[list[float], list[float]]':
		cut_dir_angle = np.arccos(self.__cut_dir.x)
		T = np.linspace(cut_dir_angle - self.__cut_angle / 2.0, cut_dir_angle + self.__cut_angle / 2.0, detail)
		return self.radius * np.cos(T) + self.center.x, self.radius * np.sin(T) + self.center.y

