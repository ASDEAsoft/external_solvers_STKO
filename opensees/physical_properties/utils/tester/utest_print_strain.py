from StrainHistory import *

s = StrainHistoryCyclicEN12512()
p = s.getDefaultParams()
p.target_strain = -0.002
p.num_divisions = 1
p.scale_pos = 1.0
s.build(p)

e = s.strain
for ie in e:
	print(ie)