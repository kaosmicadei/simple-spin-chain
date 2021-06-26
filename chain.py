import numpy as np
from generators import HalfSpinOperator
from hamiltonian import XYModel

class Chain:
    def __init__(self, N, coupling_constant=1, omega=1, beta=1, message_state=None):
        self.__op = HalfSpinOperator(N)
        self.__hamiltonian = XYModel(self.__op, coupling_constant, omega)

        # Thermal chain:
        #       Since, chain = 1 ⊗ exp(-beta H0) ⟹ Tr chain = 2*Z, it's necessary "fix"
        #       the normalisation before add the initial state of the first spin.
        thermal_chain = np.exp(-beta * np.diag(self.__hamiltonian.H0))
        partition_function = np.sum(thermal_chain)
        thermal_chain = 2.0 * np.diag(thermal_chain / partition_function)

        # State to be transmited through the chain
        message_state = self.__op.z_projector[0][0] if not message_state.any() else np.kron(message_state, np.eye(2**(N-1)))

        # Whole initial system
        self.__initial_state = np.matmul(message_state, thermal_chain)
        self.__current_state = self.__initial_state

    def state(self, time_step):
        if time_step == 0:
            return self.__initial_state
        pass

    def bloch_vector(self, spin_index):
        x = np.trace(np.matmul(self.__op.sigma['x'][spin_index], self.__current_state))
        y = np.trace(np.matmul(self.__op.sigma['y'][spin_index], self.__current_state))
        z = np.trace(np.matmul(self.__op.sigma['z'][spin_index], self.__current_state))
        return (x,y,z)

    def __len__(self):
        return self.__op.dimension