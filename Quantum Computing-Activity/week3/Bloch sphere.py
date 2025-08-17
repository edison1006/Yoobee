import numpy as np
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# plot_bloch_vector([1,0.0], title="new sphere")
plot_bloch_vector([1,np.pi/2,np.pi/2], coord_type="spherical")
plt.show()

