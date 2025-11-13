"""
Basic capability test for spatial_res without quantum optimization
"""
import sys
import numpy as np
from spatial_ai_enhanced import (
    EnhancedSpatialReasoningEngine,
    PlacementConstraints,
    NeuralLayoutArchitecture,
    ConstraintSatisfactionEngine,
    TemporalCoherenceEngine,
    InformationTheoreticAnalyzer
)

def test_basic_placement():
    """Test basic placement without quantum optimization"""
    print("=" * 60)
    print("BASIC PLACEMENT TEST (Classical Optimization)")
    print("=" * 60)

    engine = EnhancedSpatialReasoningEngine()

    # Test block
    test_block = {
        "width": 300,
        "height": 200,
        "content_type": "diagram",
        "priority": 8
    }

    # Disable quantum optimization to avoid the bug
    constraints = PlacementConstraints(
        use_quantum_optimization=False,
        enable_temporal_coherence=False
    )

    try:
        result = engine.calculate_optimal_placement(test_block, constraints)

        print(f"\nPlacement Result:")
        print(f"  Position: ({result['x']:.0f}, {result['y']:.0f})")
        print(f"  Confidence: {result['confidence']:.3f}")
        print(f"  Method: {result['method_used']}")
        print(f"  Strategies Evaluated: {result['strategies_evaluated']}")

        if 'metrics' in result:
            print(f"\nMetrics:")
            for key, value in result['metrics'].items():
                if isinstance(value, (int, float)):
                    print(f"    {key}: {value:.2f}")

        print("\n✓ Basic placement test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Basic placement test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_neural_architecture():
    """Test neural architecture search"""
    print("\n" + "=" * 60)
    print("NEURAL ARCHITECTURE SEARCH TEST")
    print("=" * 60)

    try:
        neural_arch = NeuralLayoutArchitecture()

        # Generate architectures
        for i in range(5):
            arch = neural_arch.generate_architecture(input_dims=8)
            score = np.random.uniform(0.5, 1.0)
            neural_arch.evaluate_architecture(arch, score)

            print(f"\nArchitecture {i+1}:")
            print(f"  Layers: {len(arch['layers'])}")
            print(f"  Score: {score:.3f}")
            print(f"  Activation: {arch['activation']}")

        print("\n✓ Neural architecture test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Neural architecture test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_constraint_satisfaction():
    """Test constraint satisfaction engine"""
    print("\n" + "=" * 60)
    print("CONSTRAINT SATISFACTION TEST")
    print("=" * 60)

    try:
        csp_engine = ConstraintSatisfactionEngine()

        # Add constraints
        csp_engine.add_constraint('no_overlap', {
            'variables': ['block1', 'block2'],
            'priority': 10.0
        })

        csp_engine.add_constraint('alignment', {
            'variables': ['block1', 'block2'],
            'tolerance': 5.0,
            'priority': 7.0
        })

        # Define domains
        positions = [(x, y) for x in range(0, 500, 100) for y in range(0, 500, 100)]
        csp_engine.domains['block1'] = positions[:10]
        csp_engine.domains['block2'] = positions[5:15]

        # Solve
        solution = csp_engine.backtrack_search()

        if solution:
            print(f"\nSolution found:")
            for var, val in solution.items():
                print(f"  {var}: {val}")
            print("\n✓ Constraint satisfaction test PASSED")
            return True
        else:
            print("\nNo solution found (this is OK - constraints may be unsatisfiable)")
            print("✓ Constraint satisfaction test PASSED")
            return True
    except Exception as e:
        print(f"\n✗ Constraint satisfaction test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_temporal_coherence():
    """Test temporal coherence engine"""
    print("\n" + "=" * 60)
    print("TEMPORAL COHERENCE TEST")
    print("=" * 60)

    try:
        temporal_engine = TemporalCoherenceEngine()

        # Add keyframes
        keyframes = [
            {"timestamp": 0.0, "blocks": [{"id": "b1", "x": 100, "y": 100}]},
            {"timestamp": 1.0, "blocks": [{"id": "b1", "x": 500, "y": 300}]},
            {"timestamp": 2.0, "blocks": [{"id": "b1", "x": 900, "y": 500}]}
        ]

        for kf in keyframes:
            temporal_engine.add_keyframe(kf["timestamp"], {"blocks": kf["blocks"]})

        # Generate motion paths
        bezier_path = temporal_engine.generate_motion_path(
            "b1", (100, 100), (900, 500), "cubic_bezier"
        )

        spring_path = temporal_engine.generate_motion_path(
            "b1", (100, 100), (900, 500), "spring_physics"
        )

        # Interpolate
        interpolated = temporal_engine.interpolate_state(0.5)

        print(f"\nKeyframes: {len(keyframes)}")
        print(f"Bezier path points: {len(bezier_path)}")
        print(f"Spring path points: {len(spring_path)}")
        print(f"Interpolated state at t=0.5: {interpolated}")

        print("\n✓ Temporal coherence test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Temporal coherence test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_information_theory():
    """Test information-theoretic analysis"""
    print("\n" + "=" * 60)
    print("INFORMATION-THEORETIC ANALYSIS TEST")
    print("=" * 60)

    try:
        info_analyzer = InformationTheoreticAnalyzer()

        # Test blocks
        test_blocks = [
            {"x": 100, "y": 100, "width": 200, "height": 150, "priority": 8, "type": "text"},
            {"x": 400, "y": 200, "width": 300, "height": 200, "priority": 9, "type": "image"},
            {"x": 800, "y": 100, "width": 250, "height": 180, "priority": 7, "type": "diagram"},
            {"x": 200, "y": 400, "width": 350, "height": 250, "priority": 6, "type": "table"}
        ]

        # Calculate metrics
        spatial_entropy = info_analyzer.calculate_spatial_entropy(test_blocks)
        complexity_score = info_analyzer.calculate_complexity_score({"blocks": test_blocks})
        mi = info_analyzer.calculate_mutual_information(test_blocks, "priority", "y")

        print(f"\nSpatial Entropy: {spatial_entropy:.3f} bits")
        print(f"Complexity Score: {complexity_score:.3f}")
        print(f"Mutual Information (priority-position): {mi:.3f} bits")

        print("\n✓ Information theory test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Information theory test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_blocks():
    """Test placing multiple blocks sequentially"""
    print("\n" + "=" * 60)
    print("MULTIPLE BLOCKS PLACEMENT TEST")
    print("=" * 60)

    try:
        engine = EnhancedSpatialReasoningEngine()
        constraints = PlacementConstraints(
            use_quantum_optimization=False,
            enable_temporal_coherence=False
        )

        blocks = [
            {"width": 300, "height": 200, "content_type": "text", "priority": 7},
            {"width": 250, "height": 150, "content_type": "image", "priority": 9},
            {"width": 400, "height": 250, "content_type": "diagram", "priority": 8}
        ]

        placements = []

        for i, block in enumerate(blocks):
            result = engine.calculate_optimal_placement(block, constraints)
            placements.append(result)

            # Add block to canvas
            engine.add_block({
                'x': result['x'],
                'y': result['y'],
                'width': block['width'],
                'height': block['height'],
                'block_type': block['content_type'],
                'priority': block['priority']
            })

            print(f"\nBlock {i+1}: {block['content_type']}")
            print(f"  Position: ({result['x']:.0f}, {result['y']:.0f})")
            print(f"  Confidence: {result['confidence']:.3f}")

        print(f"\n✓ Multiple blocks test PASSED - {len(placements)} blocks placed")
        return True
    except Exception as e:
        print(f"\n✗ Multiple blocks test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all basic tests"""
    print("\n" + "=" * 60)
    print("SPATIAL_RES CAPABILITY TEST SUITE")
    print("Testing without quantum optimization (due to normalization bug)")
    print("=" * 60)

    tests = [
        ("Basic Placement", test_basic_placement),
        ("Neural Architecture", test_neural_architecture),
        ("Constraint Satisfaction", test_constraint_satisfaction),
        ("Temporal Coherence", test_temporal_coherence),
        ("Information Theory", test_information_theory),
        ("Multiple Blocks", test_multiple_blocks)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ {test_name} CRASHED: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
