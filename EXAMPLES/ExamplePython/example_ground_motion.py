import sys
sys.path.insert(0, '../../SRC/interpreter/')
# sys.path.insert(0, '../build/lib/')
import opensees as ops

import matplotlib.pyplot as plt
# import openseespy.opensees as ops
import numpy as np
from scipy.integrate import cumulative_trapezoid as cumtrapz

# Create a basic model with a single node
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)
ops.node(1, 0, 0)
ops.mass(1, 1, 1, 1)

# Generate time, acceleration, velocity, and displacement arrays
time_values = np.linspace(0.0, 5.0, 251)
accel_values = np.sin(2 * np.pi * time_values)
vel_values = cumtrapz(accel_values, time_values, initial=0)
disp_values = cumtrapz(vel_values, time_values, initial=0)

# Create time series for acceleration, velocity, and displacement
ops.timeSeries('Path', 1, '-time', *time_values.tolist(), '-values', *accel_values.tolist(), '-factor', 1.0)
ops.timeSeries('Path', 2, '-time', *time_values.tolist(), '-values', *vel_values.tolist(), '-factor', 1.0)
ops.timeSeries('Path', 3, '-time', *time_values.tolist(), '-values', *disp_values.tolist(), '-factor', 1.0)

# Run cases and compare results
ts_type = ["-accel", "-vel", "-disp"]
plt.figure()

for i in range(1, 4):     
    print(f"Running case {i}")
    
    # Apply uniform excitation pattern
    ops.pattern('UniformExcitation', i, 1, ts_type[i - 1], i, "-factor", -1.0)
    ops.analysis('Transient', '-noWarnings')
    
    # Recorders for displacement
    ops.recorder('Node', '-file', f'groundD_{i}.out', '-time', '-node', 1, '-dof', 1, 'disp')

    # Run transient analysis
    T = time_values[-1]
    dt = time_values[1] - time_values[0]
    Nsteps = int(T / dt)
    ops.analyze(Nsteps, dt)
    
    # Remove load pattern and reset model for the next case
    ops.remove("loadPattern", i)
    ops.loadConst("-time", 0.0)
    ops.reset() 
    
    # Read output displacement from the file
    ground_disp = np.loadtxt(f'groundD_{i}.out')
    ground_time = ground_disp[:, 0]
    ground_disp_values = ground_disp[:, 1]

    # Add results to the plot
    plt.plot(ground_time, ground_disp_values, label=f"OpenSees Case {i}", linestyle='--', lw=2)

# Add analytical displacement to the plot
plt.plot(time_values, disp_values, label="Analytical Disp", linewidth=2, zorder=0)
plt.xlabel("Time")
plt.ylabel("Displacement")
plt.title("Comparison of Displacement for All Cases")
plt.legend()
plt.grid()
plt.show()
plt.savefig('./build/lib/ground_motion.png')