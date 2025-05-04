import sys
sys.path.insert(0, '../../SRC/interpreter/')
# sys.path.insert(0, '../build/lib/')
import opensees as ops

#######
import matplotlib.pyplot as plt
# import openseespy.opensees as ops
import numpy as np

ops.wipe()
ops.model('basic', '-ndm', 1, '-ndf', 1)
ops.node(1, 0.0); ops.fix(1, 1)
ops.node(2, 0.0);
ops.node(3, 0.0);
ops.node(4, 0.0);
ops.uniaxialMaterial('Elastic', 1, 100.0)
ops.element('zeroLength', 1, 1, 2, '-mat', 1, '-dir', 1)
ops.element('zeroLength', 2, 1, 3, '-mat', 1, '-dir', 1)
ops.equationConstraint(4,1,-3.0,2,1,1.0,3,1,2.0)
ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(4,1.0)
ops.integrator('LoadControl', 1.0)
ops.numberer('Penalty', 1.0e10, 1.0e10)
ops.analysis('Static')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 2, 3, '-dof', 1, 'disp')
ops.analyze(10)
ops.wipe()
data = np.loadtxt('disp.out')
plt.figure()
plt.plot(data[:, 0], data[:, 1])
plt.plot(data[:, 0], data[:, 2])
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.grid()
plt.show()

#######
plt.savefig('./build/lib/ground_motion.png')