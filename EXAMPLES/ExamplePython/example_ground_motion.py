import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openseespy.opensees as ops
import numpy as np
import utils.vfo.vfo as vfo

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)
ops.node( 1, 0.0, 0.0)
nrow = 3; nrow1 = nrow + 1
ncol = 3; ncol1 = ncol + 1
for i in range(1, nrow1):
    for j in range(1, ncol1):
        ops.node(i * 10 + j, j, i)

ops.fix(22, 1, 1)

ops.nDMaterial('ElasticIsotropic', 1, 1000.0, 0.0)
ops.nDMaterial('ElasticIsotropic', 2, 10.0, 0.0)

for i in range(1, nrow):
    for j in range(1, ncol):
        i1 = i + 1; j1 = j + 1;
        ops.element('quad', i * 10 + j, i * 10 + j, i * 10 + j1, i1 * 10 + j, i1 * 10 + j1, 1.0, 'PlaneStress', 1 if i == 1 and j == 1 else 2)

vfo.createODB(model="model01", loadcase="static")
vfo.plot_model(model = "model01", line_width = 5, filename = 'model')

for i in range(1, nrow):
    ops.equationConstraint(i * 10 + ncol1, 1, 1.0, i * 10 + 1, 1, -1.0, 1, 1, -1.0)
    ops.equationConstraint(i * 10 + ncol1, 2, 1.0, i * 10 + 1, 2, -1.0)

ops.equationConstraint(nrow1 * 10 + ncol1, 1, 1.0, nrow1 * 10 + 1, 1, -1.0, 1, 1, -1.0)

for j in range(1, ncol):
    ops.equationConstraint(nrow1 * 10 + j, 2, 1.0, 10 + j, 2, -1.0, 1, 2, -1.0)
    ops.equationConstraint(nrow1 * 10 + j, 1, 1.0, 10 + j, 1, -1.0)

ops.equationConstraint(nrow1 * 10 + ncol1, 2, 1.0, 10 + ncol1, 2, -1.0, 1, 2, -1.0)

ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(1, 1.0, 1.0)
# ops.integrator('LoadControl', 1.0)
ops.constraints('Penalty', 1.0e10, 1.0e10)
ops.analysis('Static')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 21, 31, '-dof', 1, 'disp')
ops.analyze(10)
ops.wipe()
print('Analysis completed')
data = np.loadtxt('disp.out')
plt.figure()
plt.plot(data[:, 0], data[:, 1])
plt.plot(data[:, 0], data[:, 2])
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.grid()
# plt.show()

#######
plt.savefig('ground_motion.png')
print('Plot completed')
