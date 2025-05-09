import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openseespy.opensees as ops
import numpy as np
# import utils.vfo.vfo as vfo

ops.model('basic', '-ndm', 2, '-ndf', 3)
ops.node( 1,-1.0, 0.0); ops.fix(1, 0, 1, 1)
ops.node(11, 0.0, 0.0); ops.fix(11, 1, 1, 1)
ops.node(12, 4.0, 0.0); ops.fix(12, 1, 1, 1)
ops.node(21, 0.0, 2.0)
ops.node(22, 4.0, 2.0)
ops.node(31, 0.0, 4.0)
ops.node(32, 4.0, 4.0)

# ops.nDMaterial('ElasticIsotropic', 1, 1000.0, 0.0)
# ops.nDMaterial('ElasticIsotropic', 2, 10.0, 0.0)

ops.geomTransf('Linear', 1)

ops.element('elasticBeamColumn', 11, 11, 21, 0.1, 1e5, 0.01, 1)
ops.element('elasticBeamColumn', 12, 12, 22, 0.1, 1e5, 0.01, 1)
ops.element('elasticBeamColumn', 13, 21, 22, 0.1, 1e5, 0.05, 1)
ops.element('elasticBeamColumn', 21, 21, 31, 0.1, 1e5, 0.01, 1)
ops.element('elasticBeamColumn', 22, 22, 32, 0.1, 1e5, 0.01, 1)
ops.element('elasticBeamColumn', 23, 31, 32, 0.1, 1e5, 0.05, 1)

ops.equationConstraint(31, 1, 1.0, 21, 1, -1.0, 1, 1, -1.0)

# vfo.createODB(model="model01", loadcase="static")
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(21, 1.0, 0.0, 0.0)
ops.load(31, 2.0, 0.0, 0.0)
ops.constraints('Penalty', 1.0e6, 1.0e6)
ops.integrator('DisplacementControl', 1, 1, 1e-3)
ops.analysis('Static')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 21, 31, '-dof', 1, 'disp')
ops.recorder('Element', '-file', 'force.out', '-time', '-ele', 11, 21, 'force')
ops.analyze(10)
ops.wipe()
# vfo.plot_deformedshape(model="model01", loadcase="static", scale=5, contour='x', filename = 'model')

disp = np.loadtxt('disp.out')
force = np.loadtxt('force.out')
plt.figure()
plt.plot(disp[:, 2] - disp[:, 1], force[:, 10])
plt.xlabel('Second-Story Shear Deformation')
plt.ylabel('Second-Story Shear Force')
plt.grid()
# plt.show()

#######
plt.savefig('ground_motion.png')