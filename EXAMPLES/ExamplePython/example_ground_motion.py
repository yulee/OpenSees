import matplotlib.pyplot as plt
import openseespy.opensees as ops
import numpy as np
# import vfo.vfo as vfo
import utils.vfo.vfo as vfo

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)
ops.node( 1, 0.0, 0.0); ops.fix( 1, 0, 1)
ops.node(11, 0.0, 0.0); ops.fix(11, 1, 1)
ops.node(12, 1.0, 0.0); ops.fix(12, 0, 1)
ops.node(21, 0.0, 1.0); ops.fix(21, 1, 1)
ops.node(22, 1.0, 1.0); ops.fix(22, 0, 1)
ops.uniaxialMaterial('Elastic', 1, 100.0)
ops.element('zeroLength', 1, 11, 12, '-mat', 1, '-dir', 1)
ops.element('zeroLength', 2, 21, 22, '-mat', 1, '-dir', 1)
# vfo.createODB(model="model01", loadcase="static")
vfo.createODB(model="model01")
vfo.plot_model(model="model01", filename='model')
ops.equationConstraint(1, 1, -3.0, 12, 1, 1.0, 22, 1, 2.0)
ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(1,1.0)
ops.integrator('LoadControl', 1.0)
ops.constraints('Penalty', 1.0e10, 1.0e10)
ops.analysis('Static')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 12, 22, '-dof', 1, 'disp')
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
plt.savefig('ground_motion.png')