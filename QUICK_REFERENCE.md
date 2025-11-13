# SPATIAL_RES QUICK REFERENCE GUIDE

## Project Overview
**Type:** Quantum-Enhanced Spatial AI Layout Engine  
**Status:** Development Ready (7/10 - One critical bug)  
**LOC:** ~3,000 lines | **Modules:** 3 core + MCP server  
**Key Innovation:** Multi-strategy optimization using quantum, neural, and constraint-based approaches  

---

## Critical Quick Facts

### File Structure
```
spatial_ai_enhanced.py         Main engine + MCP server (1344 lines)
spatial_quantum_extension.py   Advanced quantum features (927 lines)
quantum_physics_layout.py      12-qubit quantum simulator (752 lines)
test_*.py                      Test suites (4 files)
```

### Core Classes
| Class | Purpose | Status | Location |
|-------|---------|--------|----------|
| `EnhancedSpatialReasoningEngine` | Main orchestrator | ✓ | spatial_ai_enhanced.py |
| `QuantumAnnealingOptimizer` | Quantum optimization | ⚠ Broken | spatial_ai_enhanced.py |
| `ConstraintSatisfactionEngine` | CSP solver | ✓ | spatial_ai_enhanced.py |
| `NeuralLayoutArchitecture` | Neural architecture search | ✓ | spatial_ai_enhanced.py |
| `TemporalCoherenceEngine` | Animation/timing | ✓ | spatial_ai_enhanced.py |
| `InformationTheoreticAnalyzer` | Quality metrics | ✓ | spatial_ai_enhanced.py |
| `NeuromorphicField` | Spiking neurons | Present | spatial_quantum_extension.py |
| `HolographicMemory` | Pattern storage | Present | spatial_quantum_extension.py |
| `TopologicalAnalyzer` | Topology analysis | Present | spatial_quantum_extension.py |
| `AdvancedQuantumOptimizer` | 12-qubit simulator | Present | quantum_physics_layout.py |

### Critical Bug
```
Location: QuantumState.__init__() in spatial_ai_enhanced.py:35
Issue: Normalization overflow in quantum state initialization
Error: ValueError: probabilities do not sum to 1
Workaround: Pass use_quantum_optimization=False to constraints
```

---

## Implementation Quick Guide

### Add New Optimization Strategy
```python
# Step 1: Create method in EnhancedSpatialReasoningEngine
def _my_strategy_optimize(self, new_block, constraints):
    # Your optimization logic
    return {'x': x, 'y': y}

# Step 2: Add to strategy evaluation in calculate_optimal_placement()
strategies_results.append({
    'method': 'my_strategy',
    'position': self._my_strategy_optimize(new_block, constraints),
    'score': self._enhanced_score_position(...)
})

# Step 3: Best position automatically selected via max(score)
```

### Add New MCP Tool
```python
# Step 1: Define tool in list_tools()
Tool(
    name="my_new_tool",
    description="What it does",
    inputSchema={"type": "object", "properties": {...}}
)

# Step 2: Handle in call_tool()
if name == "my_new_tool":
    result = engine.my_method(arguments)
    return [TextContent(type="text", text=json.dumps(result))]
```

### Add New Scoring Metric
```python
def _my_quality_metric(self, block, constraints):
    """Calculate quality score"""
    # Return float 0-100
    return score

# Update _enhanced_score_position() to include:
metrics['my_metric'] = self._my_quality_metric(test_block, constraints)

# Adjust weights in _get_learned_weights()
```

---

## Key Data Structures

### CanvasBlock
```python
CanvasBlock(
    id: str,                           # Unique identifier
    x: float,                          # X position (pixels)
    y: float,                          # Y position (pixels)
    width: float,                      # Width (pixels)
    height: float,                     # Height (pixels)
    content: str,                      # Content text
    block_type: str,                   # text|image|diagram|etc
    priority: int,                     # 1-10, higher = more important
    semantic_group: Optional[str],     # Related content grouping
    visual_weight: float,              # 0-1, visual prominence
    interaction_zones: List[Dict],     # Interactive regions
    metadata: Dict                     # Custom data
)
```

### PlacementConstraints
```python
PlacementConstraints(
    min_padding: float = 20.0,                # Minimum margin from edge
    max_width: float = 1920.0,                # Canvas width
    max_height: float = 1080.0,               # Canvas height
    alignment_preference: str = "hierarchical", # Grid, hierarchical, etc
    use_quantum_optimization: bool = True,   # Enable quantum (has bug)
    enable_temporal_coherence: bool = True,  # Enable animation tracking
    constraint_satisfaction_level: str = "strict" # CSP strictness
)
```

### Scoring Metric Weights
```python
{
    'overlap': 1.0,               # Overlap avoidance (critical)
    'aesthetic': 0.3,             # Visual appeal
    'proximity': 0.25,            # Semantic grouping
    'balance': 0.2,               # Spatial equilibrium
    'flow': 0.15,                 # Reading patterns (F/Z)
    'whitespace_quality': 0.2,    # Empty space distribution
    'tension': 0.1,               # Visual energy
    'hierarchy': 0.15             # Priority alignment
}
```

---

## MCP Tools Summary

| Tool | Status | Input | Output |
|------|--------|-------|--------|
| `calculate_optimal_placement` | ✓ | width, height, type, priority | x, y, confidence, method |
| `update_preferences` | ✓ | aesthetic, balance, flow, etc | updated model |
| `generate_animation_path` | ✓ | start/end coords, curve type | path points (30-50 frames) |
| `add_block_to_canvas` | ✓ | position, size, type, metadata | block added, total count |
| `get_layout_embedding` | ✗ | none | embedding vector |
| `get_canvas_statistics` | ✗ | none | stats, entropy, complexity |

---

## Testing

### Run Basic Tests (No Quantum)
```bash
python test_basic_capability.py
# Tests: placement, architecture, constraints, temporal, info theory, multiple blocks
# Expected: 6/6 PASS
```

### Run MCP Tools Tests
```bash
python test_mcp_tools.py
# Tests: 6 MCP tools
# Expected: 4/6 PASS (2 broken tools)
```

### Run Quantum Performance Tests
```bash
python test_quantum_performance.py
# Tests: Configurations explored, memory, patterns, temporal, learning
# Expected: 5/5 PASS
```

---

## Architecture Decision Map

### Choose Optimization Strategy By:
- **Quantum Annealing:** Global optimization, exploration favoring
- **Constraint Satisfaction:** Hard constraints, exact solutions
- **Classical:** Fast baseline, educational purposes
- **Best Practice:** Use all three (strategy pattern)

### Choose Constraint Satisfaction Level By:
- **"strict":** All constraints must be satisfied
- **"moderate":** Weighted constraint violations allowed
- **"relaxed":** Soft constraints only

### Choose Animation Curve By:
- **"cubic_bezier":** Smooth, easing-like motion (30 points)
- **"spring_physics":** Bouncy, natural feeling (50 points)

---

## Performance Characteristics

### Computation Time
- Single block placement: 15-20ms
- With quantum (if working): +50-100ms
- Temporal coherence: +5ms
- Information metrics: +10ms

### Scalability
- Tested up to 100 blocks (original test)
- Memory usage: Low (efficient numpy)
- Quantum: Exponential with qubits (8 qubits = 256 states)

### Quality Metrics
- Placement confidence: 0.95+ typical
- Spatial entropy: ~2.0 bits (good distribution)
- Complexity score: ~5.4 (moderate)
- Success rate: 100% (with quantum disabled)

---

## For Adding Three New Capabilities

### Integration Points
1. **Topological Spatial Cognition**
   - Location: New class in main engine
   - Hook: Add as strategy in `calculate_optimal_placement()`
   - Uses: Existing `TopologicalAnalyzer` from extension

2. **Holographic Pattern Retrieval**
   - Location: Wrapper around existing `HolographicMemory`
   - Hook: Query in placement, store after placement
   - Uses: Phase-encoded pattern vectors

3. **Neuromorphic Field Computation**
   - Location: New class using existing `NeuromorphicField`
   - Hook: Add as strategy in main engine
   - Uses: Spiking neural dynamics for position scoring

### Implementation Checklist
- [ ] Create new class with `__init__` and main method
- [ ] Follow existing pattern: `_generate_candidates()` → `_score()` → `best()`
- [ ] Add strategy to `calculate_optimal_placement()`
- [ ] Return dict with 'method', 'position', 'score'
- [ ] Add MCP tool if user-facing (optional)
- [ ] Write unit test
- [ ] Update this guide

---

## Common Tasks

### Task: Debug placement result
```python
# Enable detailed metrics
result = engine.calculate_optimal_placement(block, constraints)
print(f"Method: {result['method_used']}")
print(f"Strategies: {result['strategies_evaluated']}")
print(f"Metrics: {result['metrics']}")  # See individual scores
print(f"Quantum entropy: {result['quantum_state_entropy']}")
```

### Task: Disable quantum optimization
```python
constraints = PlacementConstraints(
    use_quantum_optimization=False,  # This line
    enable_temporal_coherence=True
)
```

### Task: Add custom preference weights
```python
engine.update_preference_model({
    'aesthetic': 0.8,      # High aesthetic weight
    'balance': 0.5,        # Medium balance
    'flow': 0.9,           # High flow
    'whitespace': 0.3,     # Low whitespace
    'hierarchy': 0.7       # High hierarchy
})
```

### Task: Extract layout embedding
```python
embedding = engine.export_layout_embedding()
print(f"Dimensions: {len(embedding)}")
# Contains: spatial stats, type distribution, info metrics
```

### Task: Generate animation
```python
path = engine.temporal_engine.generate_motion_path(
    block_id="block_1",
    start_pos=(100, 100),
    end_pos=(500, 500),
    curve_type="cubic_bezier"  # or "spring_physics"
)
# Returns ~30 (bezier) or ~50 (spring) coordinate pairs
```

---

## Key Dependencies

```python
import numpy as np                    # Array operations
from scipy.ndimage import convolve   # Neural field lateral interactions
from scipy.spatial import KDTree      # Topological neighbor finding
from scipy import ndimage             # Whitespace analysis
from mcp.server import Server         # MCP server framework
from dataclasses import dataclass     # Data structure definitions
from enum import Enum                 # Content type enums
from collections import deque         # History tracking
```

---

## Notes for Developers

- **Canvas Size:** 1920x1080 (fixed)
- **Grid Granularity:** 10 pixels (configurable via GRID_SNAP)
- **Quantum Qubits:** 8 qubits = 256 basis states
- **Neural Field:** 50x50 neurons (configurable)
- **Holographic Memory:** 512 dimensions
- **Temporal History:** Last 100 keyframes cached
- **Architecture Cache:** Last 1000 architectures scored

---

## Useful Debugging Commands

```python
# Check quantum bug
from spatial_ai_enhanced import QuantumState
try:
    qs = QuantumState(n_qubits=8)
    print("Quantum state OK")
except ValueError as e:
    print(f"Quantum bug: {e}")

# Get canvas state
for block in engine.canvas_state:
    print(f"{block.id}: ({block.x}, {block.y}) {block.width}x{block.height}")

# Check preference model
print("Learned preferences:", engine.preference_model)

# Temporal history
print(f"Keyframes stored: {len(engine.temporal_engine.keyframes)}")

# Information metrics
info = engine.info_analyzer.calculate_spatial_entropy(
    [b.to_dict() for b in engine.canvas_state]
)
print(f"Spatial entropy: {info:.3f} bits")
```

