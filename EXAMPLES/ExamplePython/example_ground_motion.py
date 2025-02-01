import sys
sys.path.insert(0, '../../SRC/interpreter/')
# sys.path.insert(0, '../build/lib/')
import opensees as ops

#######
import matplotlib.pyplot as plt
# import openseespy.opensees as ops
import numpy as np

# Create a basic model with a single node
ops.wipe()
ops.model('basic', '-ndm', 1, '-ndf', 1)
ops.node(1, 0.0); ops.fix(1, 1)
ops.node(2, 0.0); ops.mass(2, 1.0)
ops.node(3, 0.0); ops.mass(3, 1.0)
ops.uniaxialMaterial('Elastic', 1, 100.0)
ops.damping('Uniform', 1, 0.05, 1.0, 100.0)
ops.element('zeroLength', 1, 1, 2, '-mat', 1, '-dir', 1)
ops.element('zeroLength', 2, 1, 3, '-mat', 1, '-dir', 1)
ops.region(1, '-ele', 1, 2, '-damp', 1)
ops.parameter(1, 'region', 1, 'damping', 'dampingRatio')
ops.timeSeries('Sine', 1, 0.0, 100.0, 0.628, '-factor', -10.0)
ops.pattern('UniformExcitation', 1, 1, '-accel', 1)
ops.analysis('Transient')
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 3, '-dof', 1, 'disp')

ops.analyze(1000, 0.01)
ops.updateParameter(1, 0.02)
ops.analyze(2000, 0.01)

ops.wipe()
data = np.loadtxt('disp.out')
plt.figure()
plt.plot(data[:, 0], data[:, 1])
plt.annotate('damping updated', xy=(10.0, 0.8), xytext=(10, 1.6), ha='center',
             arrowprops=dict(facecolor='black', arrowstyle='-|>'))
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.grid()
plt.show()

#######
plt.savefig('./build/lib/ground_motion.png')