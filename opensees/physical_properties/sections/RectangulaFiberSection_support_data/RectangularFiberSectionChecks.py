import PyMpc.IO

def geometry_check(w, h, c, sd):
	Wc = w - 2.0*(c+sd/2.0)
	Hc = h - 2.0*(c+sd/2.0)
	if Wc <= 0.0:
		raise Exception('Inconsistent geometry (2*Cover + StirrupRadius) >= Width')
	if Hc <= 0.0:
		raise Exception('Inconsistent geometry (2*Cover + StirrupRadius) >= Height')
