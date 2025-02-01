import sys
sys.path.insert(0, '../../SRC/interpreter/')
# sys.path.insert(0, '../build/lib/')
import opensees as ops
import math

import matplotlib.pyplot as plt
# import openseespy.opensees as ops
import numpy as np

# Create a basic model with a single node
ops.wipe()
ops.model('basic', '-ndm', 1, '-ndf', 1)
ops.node(1, 0.0);  ops.fix(1, 1)
ops.node(2, 0.0); ops.mass(2, 1.0)
ops.geomTransf('Linear', 1)
ops.uniaxialMaterial('Elastic', 1, 1000.0)
ops.damping('Uniform', 1, 0.05, 1.0, 100.0)
ops.element('zeroLength', 1, 1, 2, '-mat', 1, '-dir', 1, '-damp', 1)
ops.timeSeries('Sine', 1, 0.0, 100.0, 0.2*math.pi, '-factor', 0.01)
ops.pattern('UniformExcitation', 1, 1, '-accel', 1)
ops.analysis('Transient')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 2, '-dof', 1, 'disp')

T = 10
dt = 0.01
Nsteps = int(T/dt)

for i in range(Nsteps):
  ops.analyze(1,dt)

ops.wipe()
data = np.loadtxt('disp.out')
time = data[:, 0]
disp = data[:, 1]

plt.figure()
plt.plot(time, disp, label="disp", linestyle='--', lw=2)
plt.xlabel("Time")
plt.ylabel("Displacement")
# plt.title("Comparison of Displacement for All Cases")
# plt.legend()
plt.grid()
plt.show()
plt.savefig('./build/lib/ground_motion.png')