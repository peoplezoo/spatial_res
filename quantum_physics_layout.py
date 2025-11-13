"""
Copyright © Christopher Athans Crow. All rights reserved.

Quantum Physics Simulation for Spatial Layout
Advanced wave function collapse and quantum entanglement for optimal positioning
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import cmath
from dataclasses import dataclass
from enum import Enum

class QuantumOperator(Enum):
    """Quantum operators for layout optimization"""
    HADAMARD = "hadamard"
    PAULI_X = "pauli_x"
    PAULI_Y = "pauli_y"
    PAULI_Z = "pauli_z"
    CNOT = "cnot"
    PHASE = "phase"
    ROTATION = "rotation"
    TOFFOLI = "toffoli"

@dataclass
class QuantumCircuit:
    """Quantum circuit for spatial reasoning"""
    n_qubits: int
    gates: List[Tuple[QuantumOperator, List[int], Optional[float]]]
    measurement_basis: str = "computational"
    
class AdvancedQuantumOptimizer:
    """
    Advanced quantum computing simulation for spatial optimization
    Uses actual quantum mechanics principles for layout decisions
    """
    
    # Quantum gate matrices
    GATES = {
        'hadamard': (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex),
        'pauli_x': np.array([[0, 1], [1, 0]], dtype=complex),
        'pauli_y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'pauli_z': np.array([[1, 0], [0, -1]], dtype=complex),
        'phase': lambda theta: np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex),
        'rotation_x': lambda theta: np.array([
            [np.cos(theta/2), -1j * np.sin(theta/2)],
            [-1j * np.sin(theta/2), np.cos(theta/2)]
        ], dtype=complex),
        'rotation_y': lambda theta: np.array([
            [np.cos(theta/2), -np.sin(theta/2)],
            [np.sin(theta/2), np.cos(theta/2)]
        ], dtype=complex),
        'rotation_z': lambda theta: np.array([
            [np.exp(-1j * theta/2), 0],
            [0, np.exp(1j * theta/2)]
        ], dtype=complex)
    }
    
    def __init__(self, n_qubits: int = 12):
        """Initialize quantum system with n qubits"""
        self.n_qubits = n_qubits
        self.n_states = 2 ** n_qubits
        self.reset()
        
        # Entanglement tracking
        self.entanglement_map = {}
        self.decoherence_rate = 0.01
        
        # Quantum error correction
        self.error_correction_enabled = True
        self.syndrome_measurements = []
        
    def reset(self):
        """Reset quantum state to |0...0⟩"""
        self.state_vector = np.zeros(self.n_states, dtype=complex)
        self.state_vector[0] = 1.0
        self.measurement_history = []
        
    def apply_hadamard(self, qubit: int):
        """Apply Hadamard gate to create superposition"""
        gate_matrix = self._create_n_qubit_gate(self.GATES['hadamard'], qubit)
        self.state_vector = gate_matrix @ self.state_vector
        
    def apply_cnot(self, control: int, target: int):
        """Apply controlled-NOT gate for entanglement"""
        cnot_matrix = self._create_cnot_matrix(control, target)
        self.state_vector = cnot_matrix @ self.state_vector
        
        # Track entanglement
        if control not in self.entanglement_map:
            self.entanglement_map[control] = set()
        if target not in self.entanglement_map:
            self.entanglement_map[target] = set()
        
        self.entanglement_map[control].add(target)
        self.entanglement_map[target].add(control)
        
    def apply_phase_gate(self, qubit: int, phase: float):
        """Apply phase gate for quantum interference"""
        phase_matrix = self._create_n_qubit_gate(
            self.GATES['phase'](phase), qubit
        )
        self.state_vector = phase_matrix @ self.state_vector
        
    def apply_rotation(self, qubit: int, axis: str, angle: float):
        """Apply rotation gate around specified axis"""
        rotation_gate = self.GATES[f'rotation_{axis}'](angle)
        gate_matrix = self._create_n_qubit_gate(rotation_gate, qubit)
        self.state_vector = gate_matrix @ self.state_vector
        
    def apply_toffoli(self, control1: int, control2: int, target: int):
        """Apply Toffoli (CCNOT) gate for complex logic"""
        toffoli_matrix = self._create_toffoli_matrix(control1, control2, target)
        self.state_vector = toffoli_matrix @ self.state_vector
        
    def create_ghz_state(self, qubits: List[int]):
        """Create GHZ state for maximum entanglement"""
        if len(qubits) < 2:
            return
        
        # Start with Hadamard on first qubit
        self.apply_hadamard(qubits[0])
        
        # Apply CNOT chain
        for i in range(1, len(qubits)):
            self.apply_cnot(qubits[0], qubits[i])
            
    def create_w_state(self, qubits: List[int]):
        """Create W state for robust entanglement"""
        n = len(qubits)
        if n < 2:
            return
        
        # Initialize to |100...0⟩
        self.reset()
        self.state_vector[2**(self.n_qubits - qubits[0] - 1)] = 1.0
        
        # Apply controlled rotations
        for k in range(n - 1):
            angle = 2 * np.arccos(np.sqrt(1 / (n - k)))
            self.apply_rotation(qubits[k + 1], 'y', angle)
            self.apply_cnot(qubits[k + 1], qubits[k])
            
    def measure(self, qubits: Optional[List[int]] = None) -> int:
        """Perform quantum measurement with wave function collapse"""
        if qubits is None:
            qubits = list(range(self.n_qubits))
        
        # Calculate measurement probabilities
        probabilities = np.abs(self.state_vector) ** 2
        
        # Perform measurement
        outcome_index = np.random.choice(self.n_states, p=probabilities)
        
        # Collapse wave function
        self._collapse_to_outcome(outcome_index)
        
        # Extract qubit values
        result = 0
        for qubit in qubits:
            bit_value = (outcome_index >> (self.n_qubits - qubit - 1)) & 1
            result = (result << 1) | bit_value
        
        self.measurement_history.append((qubits, result))
        return result
        
    def calculate_entanglement_entropy(self, qubits: List[int]) -> float:
        """Calculate von Neumann entropy for entanglement measure"""
        # Create reduced density matrix
        rho = self._create_reduced_density_matrix(qubits)
        
        # Calculate eigenvalues
        eigenvalues = np.linalg.eigvalsh(rho)
        
        # Calculate entropy
        entropy = 0
        for eigenvalue in eigenvalues:
            if eigenvalue > 1e-10:
                entropy -= eigenvalue * np.log2(eigenvalue)
        
        return entropy
        
    def apply_decoherence(self):
        """Simulate environmental decoherence"""
        if self.decoherence_rate <= 0:
            return
        
        # Add random phase errors
        for i in range(self.n_states):
            phase_error = np.exp(1j * np.random.normal(0, self.decoherence_rate))
            self.state_vector[i] *= phase_error
        
        # Renormalize
        self.state_vector /= np.linalg.norm(self.state_vector)
        
    def apply_error_correction(self):
        """Apply quantum error correction using stabilizer codes"""
        if not self.error_correction_enabled:
            return
        
        # Simplified 3-qubit bit flip code
        if self.n_qubits >= 3:
            # Measure syndrome
            syndrome = self._measure_syndrome()
            
            # Apply correction based on syndrome
            if syndrome == 1:
                self.apply_pauli_x(0)
            elif syndrome == 2:
                self.apply_pauli_x(1)
            elif syndrome == 3:
                self.apply_pauli_x(2)
                
    def apply_pauli_x(self, qubit: int):
        """Apply Pauli-X (bit flip) gate"""
        gate_matrix = self._create_n_qubit_gate(self.GATES['pauli_x'], qubit)
        self.state_vector = gate_matrix @ self.state_vector
        
    def get_bloch_coordinates(self, qubit: int) -> Tuple[float, float, float]:
        """Get Bloch sphere coordinates for single qubit"""
        # Create reduced density matrix for single qubit
        rho = self._create_reduced_density_matrix([qubit])
        
        # Calculate Bloch vector components
        x = 2 * np.real(rho[0, 1])
        y = 2 * np.imag(rho[0, 1])
        z = np.real(rho[0, 0] - rho[1, 1])
        
        return (x, y, z)
        
    def quantum_walk(self, steps: int, position_qubits: int) -> List[float]:
        """Perform quantum walk for spatial exploration"""
        # Initialize coin qubit in superposition
        coin_qubit = 0
        self.apply_hadamard(coin_qubit)
        
        position_states = 2 ** position_qubits
        probability_distribution = []
        
        for _ in range(steps):
            # Coin flip
            self.apply_hadamard(coin_qubit)
            
            # Conditional shift based on coin state
            for pos in range(position_states):
                # Move right if coin is |1⟩
                self.apply_cnot(coin_qubit, pos % position_qubits + 1)
            
            # Apply decoherence
            self.apply_decoherence()
            
            # Measure position probability
            probs = self._get_position_probabilities(
                list(range(1, position_qubits + 1))
            )
            probability_distribution.append(probs)
        
        return probability_distribution
        
    def grover_search(self, oracle_function, iterations: Optional[int] = None) -> int:
        """Grover's algorithm for optimal solution search"""
        if iterations is None:
            iterations = int(np.pi/4 * np.sqrt(self.n_states))
        
        # Initialize uniform superposition
        for i in range(self.n_qubits):
            self.apply_hadamard(i)
        
        for _ in range(iterations):
            # Oracle
            self._apply_oracle(oracle_function)
            
            # Diffusion operator
            self._apply_diffusion()
        
        # Measure result
        return self.measure()
        
    def variational_quantum_eigensolver(
        self, hamiltonian: np.ndarray, 
        ansatz_params: List[float]
    ) -> float:
        """VQE for finding ground state energy"""
        # Apply parameterized ansatz
        self._apply_ansatz(ansatz_params)
        
        # Calculate expectation value
        expectation = np.real(
            np.conj(self.state_vector) @ hamiltonian @ self.state_vector
        )
        
        return expectation
        
    def quantum_approximate_optimization(
        self, cost_hamiltonian: np.ndarray,
        mixer_hamiltonian: np.ndarray,
        gammas: List[float],
        betas: List[float]
    ) -> int:
        """QAOA for combinatorial optimization"""
        p = len(gammas)  # Number of QAOA layers
        
        # Initialize to uniform superposition
        for i in range(self.n_qubits):
            self.apply_hadamard(i)
        
        # Apply QAOA layers
        for layer in range(p):
            # Cost Hamiltonian evolution
            self._evolve_hamiltonian(cost_hamiltonian, gammas[layer])
            
            # Mixer Hamiltonian evolution
            self._evolve_hamiltonian(mixer_hamiltonian, betas[layer])
        
        # Measure result
        return self.measure()
        
    # Helper methods
    def _create_n_qubit_gate(self, single_gate: np.ndarray, target_qubit: int) -> np.ndarray:
        """Create n-qubit gate matrix from single-qubit gate"""
        gate = np.array([[1]], dtype=complex)
        
        for i in range(self.n_qubits):
            if i == target_qubit:
                gate = np.kron(gate, single_gate)
            else:
                gate = np.kron(gate, np.eye(2, dtype=complex))
        
        return gate
        
    def _create_cnot_matrix(self, control: int, target: int) -> np.ndarray:
        """Create CNOT gate matrix for n qubits"""
        matrix = np.eye(self.n_states, dtype=complex)
        
        for state in range(self.n_states):
            control_bit = (state >> (self.n_qubits - control - 1)) & 1
            
            if control_bit == 1:
                # Flip target bit
                target_mask = 1 << (self.n_qubits - target - 1)
                flipped_state = state ^ target_mask
                matrix[state, state] = 0
                matrix[flipped_state, state] = 1
        
        return matrix
        
    def _create_toffoli_matrix(
        self, control1: int, control2: int, target: int
    ) -> np.ndarray:
        """Create Toffoli gate matrix for n qubits"""
        matrix = np.eye(self.n_states, dtype=complex)
        
        for state in range(self.n_states):
            control1_bit = (state >> (self.n_qubits - control1 - 1)) & 1
            control2_bit = (state >> (self.n_qubits - control2 - 1)) & 1
            
            if control1_bit == 1 and control2_bit == 1:
                # Flip target bit
                target_mask = 1 << (self.n_qubits - target - 1)
                flipped_state = state ^ target_mask
                matrix[state, state] = 0
                matrix[flipped_state, state] = 1
        
        return matrix
        
    def _collapse_to_outcome(self, outcome_index: int):
        """Collapse wave function to measured outcome"""
        # Set all amplitudes to zero except measured outcome
        new_state = np.zeros(self.n_states, dtype=complex)
        new_state[outcome_index] = 1.0
        self.state_vector = new_state
        
    def _create_reduced_density_matrix(self, qubits: List[int]) -> np.ndarray:
        """Create reduced density matrix by tracing out other qubits"""
        # Full density matrix
        rho_full = np.outer(self.state_vector, np.conj(self.state_vector))
        
        # Trace out unwanted qubits (simplified implementation)
        traced_qubits = [q for q in range(self.n_qubits) if q not in qubits]
        n_traced = len(traced_qubits)
        n_kept = len(qubits)
        
        rho_reduced = np.zeros((2**n_kept, 2**n_kept), dtype=complex)
        
        for i in range(2**n_kept):
            for j in range(2**n_kept):
                sum_val = 0
                for k in range(2**n_traced):
                    # Map indices appropriately
                    full_i = self._expand_index(i, qubits, k, traced_qubits)
                    full_j = self._expand_index(j, qubits, k, traced_qubits)
                    sum_val += rho_full[full_i, full_j]
                rho_reduced[i, j] = sum_val
        
        return rho_reduced
        
    def _expand_index(
        self, kept_index: int, kept_qubits: List[int],
        traced_index: int, traced_qubits: List[int]
    ) -> int:
        """Expand index from reduced space to full space"""
        full_index = 0
        
        # Place kept bits
        for i, qubit in enumerate(kept_qubits):
            bit = (kept_index >> (len(kept_qubits) - i - 1)) & 1
            full_index |= bit << (self.n_qubits - qubit - 1)
        
        # Place traced bits
        for i, qubit in enumerate(traced_qubits):
            bit = (traced_index >> (len(traced_qubits) - i - 1)) & 1
            full_index |= bit << (self.n_qubits - qubit - 1)
        
        return full_index
        
    def _measure_syndrome(self) -> int:
        """Measure error syndrome for error correction"""
        # Simplified syndrome measurement
        syndrome = 0
        
        # Check parity of pairs
        for i in range(min(3, self.n_qubits - 1)):
            parity = self._measure_parity(i, i + 1)
            syndrome |= parity << i
        
        return syndrome
        
    def _measure_parity(self, qubit1: int, qubit2: int) -> int:
        """Measure parity of two qubits without collapsing state"""
        parity = 0
        
        for state in range(self.n_states):
            if abs(self.state_vector[state]) > 1e-10:
                bit1 = (state >> (self.n_qubits - qubit1 - 1)) & 1
                bit2 = (state >> (self.n_qubits - qubit2 - 1)) & 1
                if (bit1 ^ bit2) == 1:
                    parity = 1
                    break
        
        return parity
        
    def _get_position_probabilities(self, position_qubits: List[int]) -> np.ndarray:
        """Get probability distribution over position qubits"""
        n_positions = 2 ** len(position_qubits)
        probabilities = np.zeros(n_positions)
        
        for state in range(self.n_states):
            position_value = 0
            for i, qubit in enumerate(position_qubits):
                bit = (state >> (self.n_qubits - qubit - 1)) & 1
                position_value |= bit << (len(position_qubits) - i - 1)
            
            probabilities[position_value] += abs(self.state_vector[state]) ** 2
        
        return probabilities
        
    def _apply_oracle(self, oracle_function):
        """Apply oracle for Grover's algorithm"""
        for state in range(self.n_states):
            if oracle_function(state):
                self.state_vector[state] *= -1
                
    def _apply_diffusion(self):
        """Apply diffusion operator for Grover's algorithm"""
        # Calculate average amplitude
        average = np.mean(self.state_vector)
        
        # Reflect about average
        self.state_vector = 2 * average - self.state_vector
        
    def _apply_ansatz(self, params: List[float]):
        """Apply parameterized ansatz for VQE"""
        param_index = 0
        
        # Example ansatz: RY-RZ layers with entangling gates
        for layer in range(len(params) // (2 * self.n_qubits)):
            # Single qubit rotations
            for qubit in range(self.n_qubits):
                if param_index < len(params):
                    self.apply_rotation(qubit, 'y', params[param_index])
                    param_index += 1
                if param_index < len(params):
                    self.apply_rotation(qubit, 'z', params[param_index])
                    param_index += 1
            
            # Entangling layer
            for qubit in range(self.n_qubits - 1):
                self.apply_cnot(qubit, qubit + 1)
                
    def _evolve_hamiltonian(self, hamiltonian: np.ndarray, time: float):
        """Time evolution under Hamiltonian"""
        # U = exp(-i H t)
        evolution_operator = cmath.exp(-1j * hamiltonian * time)
        self.state_vector = evolution_operator @ self.state_vector


class QuantumLayoutOptimizer:
    """
    High-level quantum optimizer for spatial layouts
    Bridges quantum mechanics with practical layout optimization
    """
    
    def __init__(self, canvas_width: int = 1920, canvas_height: int = 1080):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        
        # Initialize quantum system
        # Use enough qubits to encode positions (log2 of grid resolution)
        grid_resolution = 32  # 32x32 grid
        position_bits = int(np.log2(grid_resolution))
        self.quantum_system = AdvancedQuantumOptimizer(n_qubits=2 * position_bits)
        
        self.grid_resolution = grid_resolution
        self.position_bits = position_bits
        
    def find_optimal_position(
        self, 
        block_width: int,
        block_height: int,
        existing_blocks: List[Dict],
        constraints: Dict
    ) -> Tuple[float, float]:
        """Find optimal position using quantum optimization"""
        
        # Create cost function for Grover's search
        def oracle_function(state: int) -> bool:
            x, y = self._decode_position(state)
            
            # Check if position violates constraints
            if not self._is_valid_position(x, y, block_width, block_height, existing_blocks):
                return False
            
            # Check if position is optimal (simplified)
            score = self._score_position(x, y, block_width, block_height, existing_blocks, constraints)
            return score > constraints.get('min_score', 0.8)
        
        # Run Grover's algorithm
        result_state = self.quantum_system.grover_search(oracle_function)
        
        # Decode position
        x, y = self._decode_position(result_state)
        
        # Convert to canvas coordinates
        canvas_x = (x / self.grid_resolution) * self.canvas_width
        canvas_y = (y / self.grid_resolution) * self.canvas_height
        
        return canvas_x, canvas_y
    
    def optimize_with_qaoa(
        self,
        block_configurations: List[Dict],
        interaction_matrix: np.ndarray
    ) -> List[Tuple[float, float]]:
        """Use QAOA for multi-block placement optimization"""
        
        # Create cost Hamiltonian from interaction matrix
        cost_hamiltonian = self._create_cost_hamiltonian(interaction_matrix)
        
        # Create mixer Hamiltonian (transverse field)
        mixer_hamiltonian = self._create_mixer_hamiltonian()
        
        # QAOA parameters (can be optimized classically)
        p = 5  # Number of QAOA layers
        gammas = np.random.uniform(0, np.pi, p)
        betas = np.random.uniform(0, np.pi, p)
        
        # Run QAOA
        result = self.quantum_system.quantum_approximate_optimization(
            cost_hamiltonian, mixer_hamiltonian, gammas, betas
        )
        
        # Decode positions for all blocks
        positions = []
        for i, block in enumerate(block_configurations):
            block_state = (result >> (i * 2 * self.position_bits)) & ((1 << (2 * self.position_bits)) - 1)
            x, y = self._decode_position(block_state)
            
            canvas_x = (x / self.grid_resolution) * self.canvas_width
            canvas_y = (y / self.grid_resolution) * self.canvas_height
            positions.append((canvas_x, canvas_y))
        
        return positions
    
    def quantum_walk_exploration(
        self, 
        start_x: float, 
        start_y: float,
        steps: int = 10
    ) -> List[Tuple[float, float]]:
        """Use quantum walk to explore layout space"""
        
        # Initialize position at start
        start_state = self._encode_position(
            int(start_x * self.grid_resolution / self.canvas_width),
            int(start_y * self.grid_resolution / self.canvas_height)
        )
        
        # Perform quantum walk
        probability_distributions = self.quantum_system.quantum_walk(
            steps, 2 * self.position_bits
        )
        
        # Extract trajectory
        trajectory = []
        for probs in probability_distributions:
            # Find most probable position
            max_prob_state = np.argmax(probs)
            x, y = self._decode_position(max_prob_state)
            
            canvas_x = (x / self.grid_resolution) * self.canvas_width
            canvas_y = (y / self.grid_resolution) * self.canvas_height
            trajectory.append((canvas_x, canvas_y))
        
        return trajectory
    
    def calculate_quantum_metrics(self) -> Dict[str, float]:
        """Calculate quantum-specific metrics for the current state"""
        
        # Entanglement entropy (measure of quantum correlations)
        position_qubits = list(range(2 * self.position_bits))
        entanglement = self.quantum_system.calculate_entanglement_entropy(
            position_qubits[:self.position_bits]
        )
        
        # Get Bloch sphere coordinates for first qubit
        bloch_coords = self.quantum_system.get_bloch_coordinates(0)
        
        # Calculate coherence (distance from center of Bloch sphere)
        coherence = np.sqrt(sum(x**2 for x in bloch_coords))
        
        return {
            'entanglement_entropy': entanglement,
            'quantum_coherence': coherence,
            'bloch_x': bloch_coords[0],
            'bloch_y': bloch_coords[1],
            'bloch_z': bloch_coords[2],
            'measurement_count': len(self.quantum_system.measurement_history)
        }
    
    # Helper methods
    def _encode_position(self, x: int, y: int) -> int:
        """Encode grid position to quantum state index"""
        return (x << self.position_bits) | y
    
    def _decode_position(self, state: int) -> Tuple[int, int]:
        """Decode quantum state index to grid position"""
        mask = (1 << self.position_bits) - 1
        y = state & mask
        x = (state >> self.position_bits) & mask
        return x, y
    
    def _is_valid_position(
        self, x: int, y: int, 
        width: int, height: int,
        existing_blocks: List[Dict]
    ) -> bool:
        """Check if position is valid (no overlaps)"""
        
        # Convert grid to canvas coordinates
        canvas_x = (x / self.grid_resolution) * self.canvas_width
        canvas_y = (y / self.grid_resolution) * self.canvas_height
        
        # Check bounds
        if canvas_x + width > self.canvas_width or canvas_y + height > self.canvas_height:
            return False
        
        # Check overlaps
        for block in existing_blocks:
            if self._check_overlap(
                canvas_x, canvas_y, width, height,
                block['x'], block['y'], block['width'], block['height']
            ):
                return False
        
        return True
    
    def _check_overlap(
        self, x1: float, y1: float, w1: float, h1: float,
        x2: float, y2: float, w2: float, h2: float
    ) -> bool:
        """Check if two rectangles overlap"""
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)
    
    def _score_position(
        self, x: int, y: int,
        width: int, height: int,
        existing_blocks: List[Dict],
        constraints: Dict
    ) -> float:
        """Score a position based on multiple criteria"""
        
        canvas_x = (x / self.grid_resolution) * self.canvas_width
        canvas_y = (y / self.grid_resolution) * self.canvas_height
        
        score = 0.0
        
        # Golden ratio bonus
        golden_x = self.canvas_width * 0.618
        golden_y = self.canvas_height * 0.618
        distance_to_golden = np.sqrt((canvas_x - golden_x)**2 + (canvas_y - golden_y)**2)
        score += 1.0 / (1 + distance_to_golden / 100)
        
        # Balance score
        if existing_blocks:
            center_x = np.mean([b['x'] + b['width']/2 for b in existing_blocks])
            center_y = np.mean([b['y'] + b['height']/2 for b in existing_blocks])
            
            new_center_x = (center_x * len(existing_blocks) + canvas_x + width/2) / (len(existing_blocks) + 1)
            new_center_y = (center_y * len(existing_blocks) + canvas_y + height/2) / (len(existing_blocks) + 1)
            
            ideal_center_x = self.canvas_width / 2
            ideal_center_y = self.canvas_height / 2
            
            imbalance = np.sqrt((new_center_x - ideal_center_x)**2 + (new_center_y - ideal_center_y)**2)
            score += 1.0 / (1 + imbalance / 100)
        
        return score / 2.0  # Normalize to [0, 1]
    
    def _create_cost_hamiltonian(self, interaction_matrix: np.ndarray) -> np.ndarray:
        """Create cost Hamiltonian from interaction matrix"""
        n_states = self.quantum_system.n_states
        hamiltonian = np.zeros((n_states, n_states), dtype=complex)
        
        # Simplified: diagonal elements represent state energies
        for state in range(n_states):
            energy = 0
            for i in range(len(interaction_matrix)):
                for j in range(len(interaction_matrix)):
                    if i != j:
                        # Check if qubits i and j are both in state |1⟩
                        bit_i = (state >> i) & 1
                        bit_j = (state >> j) & 1
                        energy += interaction_matrix[i, j] * bit_i * bit_j
            
            hamiltonian[state, state] = energy
        
        return hamiltonian
    
    def _create_mixer_hamiltonian(self) -> np.ndarray:
        """Create mixer Hamiltonian (transverse field)"""
        n_states = self.quantum_system.n_states
        hamiltonian = np.zeros((n_states, n_states), dtype=complex)
        
        # Apply Pauli-X to each qubit
        for qubit in range(self.quantum_system.n_qubits):
            x_matrix = self.quantum_system._create_n_qubit_gate(
                self.quantum_system.GATES['pauli_x'], qubit
            )
            hamiltonian += x_matrix
        
        return hamiltonian
