import numpy as np
import planar

def J_transform(v: planar.Vec2):
	return planar.Vec2(-v.y, v.x)

def sgn_dist_circle(p: planar.Vec2, o: planar.Vec2, r: float) -> float:
	return (p-o).length - r

def dist_line_segment(p: planar.Vec2, a: planar.Vec2, b: planar.Vec2) -> float:
	l2 = (b-a).length2
	if l2 == 0:
		return p.distance_to(a)
	
	t = max([0, min(1, (p-a).dot(b-a) / l2)])
	projection = a + t*(b-a)
	return p.distance_to(projection)


