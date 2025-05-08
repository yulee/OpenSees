import openseespy.opensees as ops
import utils.vfo.vfo as vfo

ops.model('basic', '-ndm', 2, '-ndf', 2)
ops.node(1, 0.0, 0.0)
nrow = 7; ncol = 7
for i in range(1, nrow + 1):
    for j in range(1, ncol + 1):
        ops.node(i * 10 + j, j, i)

ops.fix(22, 1, 1)
ops.nDMaterial('ElasticIsotropic', 1, 1000.0, 0.0)
ops.nDMaterial('ElasticIsotropic', 2, 10.0, 0.0)

for i in range(1, nrow):
    for j in range(1, ncol):
        i1 = i + 1; j1 = j + 1
        ops.element('quad', i * 10 + j, i * 10 + j, i * 10 + j1, i1 * 10 + j1, i1 * 10 + j, 1.0, 'PlaneStress', 1 if i < 3 and j < 3 else 2)

for i in range(1, nrow):
    ops.equationConstraint(i * 10 + ncol, 1, 1.0, i * 10 + 1, 1, -1.0, 1, 1, -1.0)
    ops.equationConstraint(i * 10 + ncol, 2, 1.0, i * 10 + 1, 2, -1.0)

ops.equationConstraint(nrow * 10 + ncol, 1, 1.0, nrow * 10 + 1, 1, -1.0, 1, 1, -1.0)

for j in range(1, ncol):
    ops.equationConstraint(nrow * 10 + j, 2, 1.0, 10 + j, 2, -1.0, 1, 2, -1.0)
    ops.equationConstraint(nrow * 10 + j, 1, 1.0, 10 + j, 1, -1.0)

ops.equationConstraint(nrow * 10 + ncol, 2, 1.0, 10 + ncol, 2, -1.0, 1, 2, -1.0)

vfo.createODB(model="model01", loadcase="static")
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(1, 10.0, 10.0)
# ops.constraints('Penalty', 1.0e6, 1.0e6)
ops.constraints('Lagrange')
ops.analysis('Static')
ops.analyze(1)
ops.wipe()
vfo.plot_deformedshape(model="model01", loadcase="static", scale=5, contour='x', filename = 'model')