import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openseespy.opensees as ops
import numpy as np

ops.model('basic', '-ndm', 2, '-ndf', 3)
ops.node( 1,-1.0, 0.0); ops.fix(1, 0, 1, 1)
ops.node(11, 0.0, 0.0); ops.fix(11, 1, 1, 1)
ops.node(12, 4.0, 0.0); ops.fix(12, 1, 1, 1)
ops.node(21, 0.0, 2.0)
ops.node(22, 4.0, 2.0)
ops.node(31, 0.0, 4.0)
ops.node(32, 4.0, 4.0)

ops.geomTransf('Linear', 1)
ops.uniaxialMaterial('Steel01', 1, 3e2, 2e5, 0.2)
ops.section('WFSection2d', 1, 1, 0.6, 0.05, 0.3, 0.1, 5, 1)
ops.beamIntegration('Lobatto', 1, 1, 5)
ops.uniaxialMaterial('Steel01', 2, 5e2, 2e5, 0.01)
ops.section('WFSection2d', 2, 2, 0.6, 0.05, 0.3, 0.1, 5, 1)
ops.beamIntegration('Lobatto', 2, 2, 5)

ops.element('forceBeamColumn', 11, 11, 21, 1, 1)
ops.element('forceBeamColumn', 12, 12, 22, 1, 1)
ops.element('elasticBeamColumn', 13, 21, 22, 0.1, 2e5, 0.05, 1)
ops.element('forceBeamColumn', 21, 21, 31, 1, 2)
ops.element('forceBeamColumn', 22, 22, 32, 1, 2)
ops.element('elasticBeamColumn', 23, 31, 32, 0.1, 2e5, 0.05, 1)

ops.equationConstraint(31, 1, 2.0, 21, 1, 1.0, 1, 1, -3.0)

# ops.timeSeries('Linear', 1)
ops.timeSeries('Path', 1, '-time', 0, 10, 30, '-values', 0, 10, -10)
ops.pattern('Plain', 1, 1)
ops.sp(1,1,0.01)
ops.constraints('Penalty', 1.0e6, 1.0e6)
ops.integrator('LoadControl',1.0)
ops.analysis('Static')
ops.recorder('Element', '-file', 'force1.out', '-time', '-ele', 11, 12, 'force')
ops.recorder('Element', '-file', 'force2.out', '-time', '-ele', 21, 22, 'force')
ops.analyze(30)
ops.wipe()

force1 = np.loadtxt('force1.out')
force2 = np.loadtxt('force2.out')
plt.figure()
plt.plot(force1[:, 0], force1[:, 4] + force1[:, 10], label = "Story 1")
plt.plot(force2[:, 0], force2[:, 4] + force2[:, 10], label = "Story 2")
plt.xlim(0, 20)
# plt.ylim(0, 30)
plt.xlabel('Time')
plt.ylabel('Shear')
plt.legend()
plt.grid()
# plt.show()

#######
plt.savefig('ground_motion.png')