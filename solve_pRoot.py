def solve_pRoot(p, x): 
	u = 1
	while u ** p <= x: u *= 2

	l = u // 2
	while l < u:
		mid = (l + u) // 2
		mid_pth = mid ** p
		if l < mid and mid_pth < x:
			l = mid
		elif u > mid and mid_pth > x:
			u = mid
		else:
			return mid
	return mid + 1
