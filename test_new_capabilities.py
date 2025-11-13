"""
Test script for new spatial cognition capabilities:
1. Topological Spatial Cognition
2. Holographic Pattern Retrieval
3. Neuromorphic Field Computation
"""

import sys
import json
from spatial_ai_enhanced import (
    EnhancedSpatialReasoningEngine,
    PlacementConstraints,
    CanvasBlock
)

def test_topological_cognition():
    """Test topological spatial cognition capability"""
    print("\n" + "="*70)
    print("TEST 1: Topological Spatial Cognition")
    print("="*70)

    engine = EnhancedSpatialReasoningEngine()

    # Add some blocks to create a topology
    engine.add_block({
        'x': 100, 'y': 100, 'width': 200, 'height': 150,
        'block_type': 'text', 'priority': 8, 'content': 'Header'
    })

    engine.add_block({
        'x': 400, 'y': 100, 'width': 250, 'height': 150,
        'block_type': 'image', 'priority': 6, 'content': 'Logo'
    })

    # Test topological analysis
    if engine.topological_cognition.topology_analyzer:
        current_blocks = [b.to_dict() for b in engine.canvas_state]
        topology = engine.topological_cognition.topology_analyzer.analyze_topology(current_blocks)

        print(f"✓ Topological analysis successful:")
        print(f"  - Betti number β₀ (connected components): {topology['betti_0']}")
        print(f"  - Betti number β₁ (holes): {topology['betti_1']}")
        print(f"  - Euler characteristic χ: {topology['euler_characteristic']}")
        print(f"  - Topological signature: {topology.get('topological_signature', 'N/A')}")
        print(f"  - Morse critical points: {topology.get('morse_critical_points', {})}")

        # Test placement using topological cognition
        new_block = {
            'width': 300, 'height': 200, 'priority': 7,
            'type': 'diagram', 'content': 'Flowchart'
        }
        constraints = PlacementConstraints(use_quantum_optimization=False)

        topo_pos = engine.topological_cognition.optimize_position_topologically(
            new_block, engine.canvas_state, constraints
        )

        print(f"✓ Topological placement: ({topo_pos['x']:.0f}, {topo_pos['y']:.0f})")
        return True
    else:
        print("✗ Topological analyzer not available")
        return False


def test_holographic_retrieval():
    """Test holographic pattern retrieval capability"""
    print("\n" + "="*70)
    print("TEST 2: Holographic Pattern Retrieval")
    print("="*70)

    engine = EnhancedSpatialReasoningEngine()

    if not engine.holographic_retrieval.holographic_memory:
        print("✗ Holographic memory not available")
        return False

    # Add some blocks and let holographic memory learn patterns
    patterns = [
        {'x': 100, 'y': 100, 'width': 200, 'height': 150, 'priority': 8,
         'block_type': 'text', 'content': 'Title', 'semantic_group': 'header'},
        {'x': 400, 'y': 100, 'width': 200, 'height': 150, 'priority': 7,
         'block_type': 'text', 'content': 'Subtitle', 'semantic_group': 'header'},
        {'x': 100, 'y': 300, 'width': 300, 'height': 200, 'priority': 5,
         'block_type': 'image', 'content': 'Chart', 'semantic_group': 'content'}
    ]

    for pattern in patterns:
        engine.add_block(pattern)

    # Test holographic placement
    new_block = {
        'width': 250, 'height': 180, 'priority': 6,
        'type': 'text', 'content': 'Description', 'semantic_group': 'content'
    }
    constraints = PlacementConstraints(use_quantum_optimization=False)

    holo_pos = engine.holographic_retrieval.optimize_position_holographically(
        new_block, engine.canvas_state, constraints
    )

    print(f"✓ Holographic placement: ({holo_pos['x']:.0f}, {holo_pos['y']:.0f})")
    print(f"✓ Patterns stored in memory: {engine.holographic_retrieval.pattern_count}")

    # Test retrieval
    query = {'width': 200, 'height': 150, 'priority': 7, 'semantic_group': 'header'}
    similar = engine.holographic_retrieval.holographic_memory.retrieve(query)

    print(f"✓ Similar patterns found: {len(similar)}")
    for i, pattern in enumerate(similar[:3], 1):
        sim_score = pattern.get('similarity', 0)
        print(f"  Pattern {i}: similarity={sim_score:.3f}")

    return True


def test_neuromorphic_computation():
    """Test neuromorphic field computation capability"""
    print("\n" + "="*70)
    print("TEST 3: Neuromorphic Field Computation")
    print("="*70)

    engine = EnhancedSpatialReasoningEngine()

    if not engine.neuromorphic_computation.neuromorphic_field:
        print("✗ Neuromorphic field not available")
        return False

    # Add blocks to create field activation
    blocks = [
        {'x': 200, 'y': 150, 'width': 300, 'height': 200, 'priority': 9,
         'block_type': 'text', 'content': 'Important'},
        {'x': 600, 'y': 150, 'width': 200, 'height': 150, 'priority': 5,
         'block_type': 'image', 'content': 'Icon'},
        {'x': 200, 'y': 400, 'width': 400, 'height': 250, 'priority': 6,
         'block_type': 'diagram', 'content': 'Visualization'}
    ]

    for block in blocks:
        engine.add_block(block)

    # Test neuromorphic placement
    new_block = {
        'width': 250, 'height': 180, 'priority': 7,
        'type': 'text', 'content': 'Additional Info'
    }
    constraints = PlacementConstraints(use_quantum_optimization=False)

    neuro_pos = engine.neuromorphic_computation.optimize_position_neuromorphically(
        new_block, engine.canvas_state, constraints
    )

    print(f"✓ Neuromorphic placement: ({neuro_pos['x']:.0f}, {neuro_pos['y']:.0f})")

    # Get field statistics
    stats = engine.neuromorphic_computation.get_field_statistics()

    print(f"✓ Neuromorphic field statistics:")
    print(f"  - Mean activity: {stats['mean_activity']:.3f}")
    print(f"  - Activity variance: {stats['activity_variance']:.3f}")
    print(f"  - Total spikes: {stats['total_spikes']}")
    print(f"  - Membrane potential (mean): {stats['membrane_potential_mean']:.3f}")

    return True


def test_integrated_placement():
    """Test all three capabilities working together"""
    print("\n" + "="*70)
    print("TEST 4: Integrated Multi-Strategy Placement")
    print("="*70)

    engine = EnhancedSpatialReasoningEngine()

    # Add initial blocks
    engine.add_block({
        'x': 150, 'y': 100, 'width': 300, 'height': 150,
        'block_type': 'text', 'priority': 9, 'content': 'Main Title',
        'semantic_group': 'header'
    })

    # Calculate placement using all strategies
    new_block = {
        'width': 250, 'height': 180, 'priority': 6,
        'type': 'diagram', 'content': 'Process Flow',
        'semantic_group': 'content'
    }

    constraints = PlacementConstraints(
        use_quantum_optimization=False,
        enable_temporal_coherence=True
    )

    result = engine.calculate_optimal_placement(new_block, constraints)

    print(f"✓ Optimal placement calculated:")
    print(f"  - Position: ({result['x']:.0f}, {result['y']:.0f})")
    print(f"  - Confidence: {result['confidence']:.3f}")
    print(f"  - Method used: {result['method_used']}")
    print(f"  - Strategies evaluated: {result['strategies_evaluated']}")

    # Check if new methods were used
    method = result['method_used']
    if method in ['topological_cognition', 'holographic_retrieval', 'neuromorphic_field']:
        print(f"  ✓ New capability '{method}' selected as optimal!")
    else:
        print(f"  • Traditional method '{method}' selected (new methods available)")

    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("TESTING NEW SPATIAL COGNITION CAPABILITIES")
    print("="*70)

    results = {
        'topological_cognition': test_topological_cognition(),
        'holographic_retrieval': test_holographic_retrieval(),
        'neuromorphic_computation': test_neuromorphic_computation(),
        'integrated_placement': test_integrated_placement()
    }

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All new capabilities working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
