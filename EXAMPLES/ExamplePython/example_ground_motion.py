import matplotlib.pyplot as plt
import openseespy.opensees as ops
import numpy as np

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)
ops.node( 1, 0.0, 0.0)
ops.node(11, 1.0, 1.0); ops.node(12, 2.0, 1.0); ops.node(13, 3.0, 1.0); ops.node(14, 4.0, 1.0);
ops.node(21, 1.0, 2.0); ops.node(22, 2.0, 2.0); ops.node(23, 3.0, 2.0); ops.node(24, 4.0, 2.0);
ops.node(31, 1.0, 3.0); ops.node(32, 2.0, 3.0); ops.node(33, 3.0, 3.0); ops.node(34, 4.0, 3.0);
ops.node(41, 1.0, 4.0); ops.node(42, 2.0, 4.0); ops.node(43, 3.0, 4.0); ops.node(44, 4.0, 4.0);
ops.fix(22, 1, 1)
ops.nDMaterial('ElasticIsotropic', 1, 1000.0, 0.0)
ops.nDMaterial('ElasticIsotropic', 2, 100.0, 0.0)
ops.element('quad', 11, 11, 12, 22, 21, 'PlaneStress', 1)
ops.element('quad', 12, 12, 13, 23, 22, 'PlaneStress', 2)
ops.element('quad', 13, 13, 14, 24, 23, 'PlaneStress', 2)
ops.element('quad', 21, 21, 22, 32, 31, 'PlaneStress', 2)
ops.element('quad', 22, 22, 23, 33, 32, 'PlaneStress', 2)
ops.element('quad', 23, 23, 24, 34, 33, 'PlaneStress', 2)
ops.element('quad', 31, 31, 32, 42, 41, 'PlaneStress', 2)
ops.element('quad', 32, 32, 33, 43, 42, 'PlaneStress', 2)
ops.element('quad', 33, 33, 34, 44, 43, 'PlaneStress', 2)

ops.equationConstraint(14, 1, 1.0, 11, 1, -1.0, 1, 1, -1.0)
ops.equationConstraint(24, 1, 1.0, 21, 1, -1.0, 1, 1, -1.0)
ops.equationConstraint(34, 1, 1.0, 31, 1, -1.0, 1, 1, -1.0)
ops.equationConstraint(44, 1, 1.0, 41, 1, -1.0, 1, 1, -1.0)
ops.equationConstraint(41, 1, 1.0, 11, 1, -1.0)
ops.equationConstraint(42, 1, 1.0, 12, 1, -1.0)
ops.equationConstraint(43, 1, 1.0, 13, 1, -1.0)

ops.equationConstraint(41, 2, 1.0, 11, 2, -1.0, 1, 2, -1.0)
ops.equationConstraint(42, 2, 1.0, 12, 2, -1.0, 1, 2, -1.0)
ops.equationConstraint(43, 2, 1.0, 13, 2, -1.0, 1, 2, -1.0)
ops.equationConstraint(44, 2, 1.0, 14, 2, -1.0, 1, 2, -1.0)
ops.equationConstraint(14, 2, 1.0, 11, 2, -1.0)
ops.equationConstraint(24, 2, 1.0, 21, 2, -1.0)
ops.equationConstraint(34, 2, 1.0, 31, 2, -1.0)

ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(1, 1.0, 1.0)
ops.integrator('LoadControl', 1.0)
ops.constraints('Penalty', 1.0e10, 1.0e10)
ops.analysis('Static')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 21, 31, '-dof', 1, 'disp')
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