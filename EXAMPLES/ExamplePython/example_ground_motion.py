import sys
sys.path.insert(0, '../../SRC/interpreter/')
# sys.path.insert(0, '../build/lib/')
import opensees as ops

import matplotlib.pyplot as plt
# import openseespy.opensees as ops
import numpy as np
#from scipy.integrate import cumulative_trapezoid as cumtrapz

ops.wipe()
ops.model('basic','-ndm',1,'-ndf',1)

mass=1.0
k=1.0
F=17.0
F_theta=2*np.pi
F_T=1.0

ops.node(1,0)
ops.node(2,0)
ops.fix(1,1)
ops.mass(2,mass)
ops.uniaxialMaterial("Elastic", 1, k)
ops.element('zeroLength',1,1,2,'-mat',1,'-dir',1,'-doRayleigh', 1)
times=np.arange(0,60.01,0.01)
values=F/F_theta*(1.0-np.cos(F_theta*times))
ops.timeSeries('Path',1,'-time',*times,'-values',*values,'-factor',1.0)
#pattern('UniformExcitation', patternTag, dir, '-disp', dispSeriesTag, '-vel', velSeriesTag, '-accel', accelSeriesTag, '-vel0', vel0, '-fact', fact)
ops.pattern('UniformExcitation', 1, 1,'-vel', 1,'-fact', -1.0)

lambda_ = ops.eigen("-fullGenLapack", 1)
omega = lambda_[0] ** 0.5
print("Omega: ", omega)
damping_ratio = 0.05
alpha = 2 * damping_ratio * omega
ops.rayleigh(alpha, 0., 0., 0.)
damping_coefficient=alpha*mass

ops.system("BandGeneral")
ops.numberer("Plain")
ops.constraints("Plain")
ops.algorithm("Newton")
ops.analysis("Transient")
ops.integrator("Newmark", 0.5, 0.25)

u = np.empty([0, 1])
v = np.empty([0, 1])
a = np.empty([0, 1])
time = np.empty([0, 1])

Nsteps=6000
dt=0.01
ops.reactions()
for i in range(Nsteps):
ok = ops.analyze(1, dt)
time = np.append(time, [ops.getTime()])
u = np.append(u, [ops.nodeDisp(2)], axis=0)
v = np.append(v, [ops.nodeVel(2)], axis=0)
a = np.append(a, [ops.nodeAccel(2)], axis=0)

plt.figure(figsize=(10, 4))
#plt.plot(t_exact, dis_exact, label="exact")
plt.plot(time, u,linestyle='--', label="opensees")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.xlim([0, 60])
plt.legend()
plt.show()

plt.savefig('ground_motion.png')