"""
OmniSpatial Benchmark Suite
Comprehensive multi-dimensional benchmark for spatial cognition capabilities

Tests across 7 dimensions:
1. Scale Invariance - Performance across different canvas sizes
2. Density Resilience - Handling sparse to dense layouts
3. Topological Complexity - Simple to complex spatial structures
4. Temporal Consistency - Layout evolution over time
5. Semantic Coherence - Grouping and relationship preservation
6. Adversarial Robustness - Edge cases and challenging scenarios
7. Multi-objective Optimization - Balancing competing constraints
"""

import time
import json
import statistics
import numpy as np
from typing import Dict, List, Tuple, Any
import sys

from spatial_ai_enhanced import (
    EnhancedSpatialReasoningEngine,
    PlacementConstraints,
    CanvasBlock
)


class OmniSpatialBenchmark:
    """
    OmniSpatial: Comprehensive benchmark suite for spatial cognition
    """

    def __init__(self):
        self.results = {
            'scale_invariance': {},
            'density_resilience': {},
            'topological_complexity': {},
            'temporal_consistency': {},
            'semantic_coherence': {},
            'adversarial_robustness': {},
            'multi_objective': {},
            'overall_score': 0.0
        }

        self.weights = {
            'scale_invariance': 0.15,
            'density_resilience': 0.15,
            'topological_complexity': 0.20,
            'temporal_consistency': 0.10,
            'semantic_coherence': 0.15,
            'adversarial_robustness': 0.15,
            'multi_objective': 0.10
        }

    # ========================================================================
    # DIMENSION 1: SCALE INVARIANCE
    # ========================================================================

    def test_scale_invariance(self) -> Dict[str, Any]:
        """Test performance across different canvas scales"""
        print("\n" + "="*70)
        print("DIMENSION 1: SCALE INVARIANCE")
        print("="*70)
        print("Testing spatial reasoning across different canvas sizes...")

        scales = [
            (960, 540),    # Half HD
            (1920, 1080),  # Full HD
            (3840, 2160),  # 4K
            (7680, 4320)   # 8K
        ]

        results = {}
        for width, height in scales:
            engine = EnhancedSpatialReasoningEngine()

            # Add proportional number of blocks
            num_blocks = int((width * height) / (1920 * 1080) * 10)
            for i in range(num_blocks):
                x = (i % 5) * (width / 5)
                y = (i // 5) * (height / 5)
                engine.add_block({
                    'x': x, 'y': y,
                    'width': width / 10, 'height': height / 15,
                    'block_type': 'text', 'priority': 5,
                    'content': f'Block {i}'
                })

            # Test placement
            new_block = {
                'width': width / 8, 'height': height / 12,
                'priority': 6, 'type': 'text', 'content': 'Test'
            }
            constraints = PlacementConstraints(
                max_width=width, max_height=height,
                use_quantum_optimization=False
            )

            start = time.time()
            result = engine.calculate_optimal_placement(new_block, constraints)
            placement_time = (time.time() - start) * 1000

            results[f"{width}x{height}"] = {
                'time_ms': placement_time,
                'confidence': result['confidence'],
                'method': result['method_used'],
                'strategies': result['strategies_evaluated']
            }

            print(f"  {width}x{height}: {placement_time:.2f}ms, "
                  f"confidence={result['confidence']:.3f}, "
                  f"method={result['method_used']}")

        # Calculate scale invariance score (0-100)
        times = [r['time_ms'] for r in results.values()]
        confidences = [r['confidence'] for r in results.values()]

        time_variance = np.std(times) / np.mean(times) if np.mean(times) > 0 else 1
        confidence_variance = np.std(confidences)

        score = 100 * (1 - time_variance * 0.5 - confidence_variance * 0.5)
        score = max(0, min(100, score))

        print(f"\n  Scale Invariance Score: {score:.1f}/100")

        self.results['scale_invariance'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # DIMENSION 2: DENSITY RESILIENCE
    # ========================================================================

    def test_density_resilience(self) -> Dict[str, Any]:
        """Test handling of sparse to dense layouts"""
        print("\n" + "="*70)
        print("DIMENSION 2: DENSITY RESILIENCE")
        print("="*70)
        print("Testing performance from sparse to dense layouts...")

        densities = [5, 10, 25, 50, 100]
        results = {}

        for num_blocks in densities:
            engine = EnhancedSpatialReasoningEngine()

            # Create dense layout
            for i in range(num_blocks):
                x = 50 + (i % 10) * 180
                y = 50 + (i // 10) * 180
                engine.add_block({
                    'x': x, 'y': y,
                    'width': 150, 'height': 120,
                    'block_type': 'text', 'priority': (i % 10) + 1,
                    'semantic_group': f'group_{i % 3}',
                    'content': f'Block {i}'
                })

            # Test placement
            new_block = {
                'width': 150, 'height': 120, 'priority': 6,
                'type': 'text', 'content': 'New', 'semantic_group': 'group_1'
            }
            constraints = PlacementConstraints(use_quantum_optimization=False)

            start = time.time()
            result = engine.calculate_optimal_placement(new_block, constraints)
            placement_time = (time.time() - start) * 1000

            # Check for overlaps
            test_block = CanvasBlock(
                id='test', x=result['x'], y=result['y'],
                width=new_block['width'], height=new_block['height'],
                content='', block_type='text', priority=6
            )

            overlaps = 0
            for block in engine.canvas_state:
                if self._check_overlap(test_block, block):
                    overlaps += 1

            results[f"density_{num_blocks}"] = {
                'blocks': num_blocks,
                'time_ms': placement_time,
                'confidence': result['confidence'],
                'overlaps': overlaps,
                'method': result['method_used']
            }

            density_pct = (num_blocks * 150 * 120) / (1920 * 1080) * 100
            print(f"  {num_blocks} blocks ({density_pct:.1f}% density): "
                  f"{placement_time:.2f}ms, overlaps={overlaps}, "
                  f"confidence={result['confidence']:.3f}")

        # Calculate density resilience score
        overlap_count = sum(r['overlaps'] for r in results.values())
        avg_confidence = np.mean([r['confidence'] for r in results.values()])

        score = avg_confidence * 100 - overlap_count * 5
        score = max(0, min(100, score))

        print(f"\n  Density Resilience Score: {score:.1f}/100")

        self.results['density_resilience'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # DIMENSION 3: TOPOLOGICAL COMPLEXITY
    # ========================================================================

    def test_topological_complexity(self) -> Dict[str, Any]:
        """Test handling of various topological structures"""
        print("\n" + "="*70)
        print("DIMENSION 3: TOPOLOGICAL COMPLEXITY")
        print("="*70)
        print("Testing topological understanding and preservation...")

        test_cases = {
            'linear': self._create_linear_layout,
            'grid': self._create_grid_layout,
            'circular': self._create_circular_layout,
            'hierarchical': self._create_hierarchical_layout,
            'random': self._create_random_layout
        }

        results = {}
        for name, create_fn in test_cases.items():
            engine = create_fn()

            # Analyze topology before
            if engine.topological_cognition.topology_analyzer:
                blocks_before = [b.to_dict() for b in engine.canvas_state]
                topo_before = engine.topological_cognition.topology_analyzer.analyze_topology(blocks_before)

                # Add new block
                new_block = {
                    'width': 200, 'height': 150, 'priority': 6,
                    'type': 'text', 'content': 'Test'
                }
                constraints = PlacementConstraints(use_quantum_optimization=False)

                start = time.time()
                result = engine.calculate_optimal_placement(new_block, constraints)
                time_ms = (time.time() - start) * 1000

                # Analyze topology after
                engine.add_block({
                    'x': result['x'], 'y': result['y'],
                    'width': new_block['width'], 'height': new_block['height'],
                    'block_type': 'text', 'priority': 6, 'content': 'Test'
                })
                blocks_after = [b.to_dict() for b in engine.canvas_state]
                topo_after = engine.topological_cognition.topology_analyzer.analyze_topology(blocks_after)

                # Calculate topology preservation
                euler_change = abs(topo_after['euler_characteristic'] - topo_before['euler_characteristic'])
                betti_0_change = abs(topo_after['betti_0'] - topo_before['betti_0'])

                preservation_score = 100 - (euler_change * 10 + betti_0_change * 20)
                preservation_score = max(0, min(100, preservation_score))

                results[name] = {
                    'time_ms': time_ms,
                    'betti_0_before': topo_before['betti_0'],
                    'betti_0_after': topo_after['betti_0'],
                    'betti_1_before': topo_before['betti_1'],
                    'betti_1_after': topo_after['betti_1'],
                    'euler_before': topo_before['euler_characteristic'],
                    'euler_after': topo_after['euler_characteristic'],
                    'preservation_score': preservation_score,
                    'method': result['method_used']
                }

                print(f"  {name:12} topology: β₀={topo_before['betti_0']}→{topo_after['betti_0']}, "
                      f"β₁={topo_before['betti_1']}→{topo_after['betti_1']}, "
                      f"χ={topo_before['euler_characteristic']}→{topo_after['euler_characteristic']}, "
                      f"preservation={preservation_score:.1f}/100")
            else:
                results[name] = {'error': 'Topological analyzer not available'}

        # Calculate overall topological complexity score
        if results and 'error' not in list(results.values())[0]:
            avg_preservation = np.mean([r['preservation_score'] for r in results.values()])
            score = avg_preservation
        else:
            score = 0

        print(f"\n  Topological Complexity Score: {score:.1f}/100")

        self.results['topological_complexity'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # DIMENSION 4: TEMPORAL CONSISTENCY
    # ========================================================================

    def test_temporal_consistency(self) -> Dict[str, Any]:
        """Test consistency of placements over time"""
        print("\n" + "="*70)
        print("DIMENSION 4: TEMPORAL CONSISTENCY")
        print("="*70)
        print("Testing placement consistency in evolving layouts...")

        engine = EnhancedSpatialReasoningEngine()

        # Add blocks sequentially and track positions
        placements = []
        for i in range(10):
            new_block = {
                'width': 200, 'height': 150,
                'priority': (i % 5) + 5,
                'type': 'text',
                'content': f'Block {i}',
                'semantic_group': f'group_{i % 3}'
            }
            constraints = PlacementConstraints(
                use_quantum_optimization=False,
                enable_temporal_coherence=True
            )

            result = engine.calculate_optimal_placement(new_block, constraints)

            engine.add_block({
                'x': result['x'], 'y': result['y'],
                'width': new_block['width'], 'height': new_block['height'],
                'block_type': 'text', 'priority': new_block['priority'],
                'content': new_block['content']
            })

            placements.append({
                'step': i,
                'position': (result['x'], result['y']),
                'method': result['method_used'],
                'confidence': result['confidence']
            })

            print(f"  Step {i}: ({result['x']:.0f}, {result['y']:.0f}), "
                  f"method={result['method_used']}, "
                  f"confidence={result['confidence']:.3f}")

        # Calculate temporal consistency metrics
        methods_used = [p['method'] for p in placements]
        method_consistency = len(set(methods_used)) / len(methods_used)
        method_consistency_score = (1 - method_consistency) * 100

        confidences = [p['confidence'] for p in placements]
        confidence_variance = np.std(confidences)
        confidence_score = (1 - confidence_variance) * 100

        score = (method_consistency_score + confidence_score) / 2

        print(f"\n  Method Consistency: {method_consistency_score:.1f}/100")
        print(f"  Confidence Stability: {confidence_score:.1f}/100")
        print(f"  Temporal Consistency Score: {score:.1f}/100")

        self.results['temporal_consistency'] = {
            'score': score,
            'placements': placements,
            'method_consistency': method_consistency_score,
            'confidence_stability': confidence_score
        }

        return placements

    # ========================================================================
    # DIMENSION 5: SEMANTIC COHERENCE
    # ========================================================================

    def test_semantic_coherence(self) -> Dict[str, Any]:
        """Test preservation of semantic groupings"""
        print("\n" + "="*70)
        print("DIMENSION 5: SEMANTIC COHERENCE")
        print("="*70)
        print("Testing semantic grouping and relationship preservation...")

        engine = EnhancedSpatialReasoningEngine()

        # Create semantic groups
        groups = {
            'header': [(100, 100), (400, 100), (700, 100)],
            'content': [(100, 300), (400, 300), (700, 300)],
            'footer': [(100, 700), (400, 700), (700, 700)]
        }

        for group_name, positions in groups.items():
            for i, (x, y) in enumerate(positions):
                engine.add_block({
                    'x': x, 'y': y,
                    'width': 250, 'height': 150,
                    'block_type': 'text',
                    'priority': 7 if group_name == 'header' else 5,
                    'semantic_group': group_name,
                    'content': f'{group_name}_{i}'
                })

        # Test placement with semantic group
        results = {}
        for group_name in ['header', 'content', 'footer']:
            new_block = {
                'width': 250, 'height': 150,
                'priority': 6,
                'type': 'text',
                'content': f'New {group_name}',
                'semantic_group': group_name
            }
            constraints = PlacementConstraints(use_quantum_optimization=False)

            result = engine.calculate_optimal_placement(new_block, constraints)

            # Calculate proximity to same group
            same_group_blocks = [b for b in engine.canvas_state
                               if b.semantic_group == group_name]
            if same_group_blocks:
                distances = [
                    np.sqrt((result['x'] - b.x)**2 + (result['y'] - b.y)**2)
                    for b in same_group_blocks
                ]
                avg_distance = np.mean(distances)
            else:
                avg_distance = 0

            # Calculate proximity to different groups
            other_group_blocks = [b for b in engine.canvas_state
                                if b.semantic_group != group_name]
            if other_group_blocks:
                other_distances = [
                    np.sqrt((result['x'] - b.x)**2 + (result['y'] - b.y)**2)
                    for b in other_group_blocks
                ]
                avg_other_distance = np.mean(other_distances)
            else:
                avg_other_distance = 1000

            # Coherence score: should be close to same group, far from others
            coherence = min(100, (avg_other_distance / (avg_distance + 1)) * 20)

            results[group_name] = {
                'position': (result['x'], result['y']),
                'avg_distance_same_group': avg_distance,
                'avg_distance_other_groups': avg_other_distance,
                'coherence_score': coherence,
                'method': result['method_used']
            }

            print(f"  {group_name:8}: same_group_dist={avg_distance:.1f}px, "
                  f"other_group_dist={avg_other_distance:.1f}px, "
                  f"coherence={coherence:.1f}/100")

        # Overall semantic coherence score
        score = np.mean([r['coherence_score'] for r in results.values()])

        print(f"\n  Semantic Coherence Score: {score:.1f}/100")

        self.results['semantic_coherence'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # DIMENSION 6: ADVERSARIAL ROBUSTNESS
    # ========================================================================

    def test_adversarial_robustness(self) -> Dict[str, Any]:
        """Test handling of edge cases and adversarial scenarios"""
        print("\n" + "="*70)
        print("DIMENSION 6: ADVERSARIAL ROBUSTNESS")
        print("="*70)
        print("Testing edge cases and challenging scenarios...")

        test_cases = {
            'empty_canvas': lambda: EnhancedSpatialReasoningEngine(),
            'single_block': self._create_single_block_layout,
            'extreme_density': self._create_extreme_density_layout,
            'mismatched_sizes': self._create_mismatched_sizes_layout,
            'corner_placement': self._create_corner_layout
        }

        results = {}
        for name, create_fn in test_cases.items():
            try:
                engine = create_fn()

                new_block = {
                    'width': 200, 'height': 150, 'priority': 6,
                    'type': 'text', 'content': 'Adversarial Test'
                }
                constraints = PlacementConstraints(use_quantum_optimization=False)

                start = time.time()
                result = engine.calculate_optimal_placement(new_block, constraints)
                time_ms = (time.time() - start) * 1000

                # Check if placement is valid
                valid = (
                    20 <= result['x'] <= 1720 and
                    20 <= result['y'] <= 930 and
                    result['confidence'] > 0.5
                )

                results[name] = {
                    'success': True,
                    'valid': valid,
                    'time_ms': time_ms,
                    'position': (result['x'], result['y']),
                    'confidence': result['confidence'],
                    'method': result['method_used']
                }

                status = "✓" if valid else "✗"
                print(f"  {status} {name:20}: valid={valid}, "
                      f"confidence={result['confidence']:.3f}, "
                      f"time={time_ms:.2f}ms")

            except Exception as e:
                results[name] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"  ✗ {name:20}: FAILED - {str(e)[:50]}")

        # Calculate robustness score
        successful = sum(1 for r in results.values() if r.get('success', False))
        valid = sum(1 for r in results.values() if r.get('valid', False))
        score = (successful / len(test_cases)) * 50 + (valid / len(test_cases)) * 50

        print(f"\n  Adversarial Robustness Score: {score:.1f}/100")

        self.results['adversarial_robustness'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # DIMENSION 7: MULTI-OBJECTIVE OPTIMIZATION
    # ========================================================================

    def test_multi_objective(self) -> Dict[str, Any]:
        """Test balancing of competing optimization objectives"""
        print("\n" + "="*70)
        print("DIMENSION 7: MULTI-OBJECTIVE OPTIMIZATION")
        print("="*70)
        print("Testing balance of competing constraints...")

        engine = EnhancedSpatialReasoningEngine()

        # Create layout with competing objectives
        for i in range(15):
            engine.add_block({
                'x': 100 + (i % 5) * 350,
                'y': 100 + (i // 5) * 300,
                'width': 300, 'height': 200,
                'block_type': 'text',
                'priority': (i % 10) + 1,
                'semantic_group': f'group_{i % 3}',
                'content': f'Block {i}'
            })

        # Test with conflicting constraints
        test_scenarios = [
            ('high_priority_dense', {'priority': 10, 'semantic_group': 'group_0'}),
            ('low_priority_sparse', {'priority': 1, 'semantic_group': 'group_2'}),
            ('medium_priority_mixed', {'priority': 5, 'semantic_group': 'group_1'})
        ]

        results = {}
        for name, block_params in test_scenarios:
            new_block = {
                'width': 250, 'height': 180,
                'type': 'text', 'content': f'Test {name}',
                **block_params
            }
            constraints = PlacementConstraints(use_quantum_optimization=False)

            result = engine.calculate_optimal_placement(new_block, constraints)

            # Evaluate multiple objectives
            metrics = result['metrics']
            objectives = {
                'overlap_avoidance': metrics.get('overlap_penalty', 0) == 100,
                'aesthetic_quality': metrics.get('aesthetic_score', 0) > 50,
                'semantic_proximity': metrics.get('proximity_score', 0) > 50,
                'visual_balance': metrics.get('balance_score', 0) > 50,
                'flow_quality': metrics.get('flow_score', 0) > 50
            }

            balance_score = sum(objectives.values()) / len(objectives) * 100

            results[name] = {
                'objectives_met': sum(objectives.values()),
                'total_objectives': len(objectives),
                'balance_score': balance_score,
                'confidence': result['confidence'],
                'method': result['method_used'],
                'metrics': metrics
            }

            print(f"  {name:25}: {sum(objectives.values())}/{len(objectives)} objectives, "
                  f"balance={balance_score:.1f}/100, "
                  f"confidence={result['confidence']:.3f}")

        # Calculate multi-objective score
        score = np.mean([r['balance_score'] for r in results.values()])

        print(f"\n  Multi-Objective Optimization Score: {score:.1f}/100")

        self.results['multi_objective'] = {
            'score': score,
            'details': results
        }

        return results

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _check_overlap(self, block1: CanvasBlock, block2: CanvasBlock) -> bool:
        """Check if two blocks overlap"""
        return not (
            block1.x + block1.width < block2.x or
            block2.x + block2.width < block1.x or
            block1.y + block1.height < block2.y or
            block2.y + block2.height < block1.y
        )

    def _create_linear_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create linear layout"""
        engine = EnhancedSpatialReasoningEngine()
        for i in range(8):
            engine.add_block({
                'x': 100 + i * 220, 'y': 500,
                'width': 200, 'height': 150,
                'block_type': 'text', 'priority': 5,
                'content': f'Block {i}'
            })
        return engine

    def _create_grid_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create grid layout"""
        engine = EnhancedSpatialReasoningEngine()
        for i in range(12):
            engine.add_block({
                'x': 100 + (i % 4) * 450,
                'y': 100 + (i // 4) * 300,
                'width': 400, 'height': 250,
                'block_type': 'text', 'priority': 5,
                'content': f'Block {i}'
            })
        return engine

    def _create_circular_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create circular layout"""
        engine = EnhancedSpatialReasoningEngine()
        center_x, center_y = 960, 540
        radius = 400
        for i in range(8):
            angle = (i / 8) * 2 * np.pi
            x = center_x + radius * np.cos(angle) - 100
            y = center_y + radius * np.sin(angle) - 75
            engine.add_block({
                'x': x, 'y': y,
                'width': 200, 'height': 150,
                'block_type': 'text', 'priority': 5,
                'content': f'Block {i}'
            })
        return engine

    def _create_hierarchical_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create hierarchical layout"""
        engine = EnhancedSpatialReasoningEngine()
        # Top level
        engine.add_block({'x': 810, 'y': 50, 'width': 300, 'height': 150,
                         'block_type': 'text', 'priority': 10, 'content': 'Root'})
        # Second level
        for i in range(3):
            engine.add_block({
                'x': 260 + i * 600, 'y': 300,
                'width': 250, 'height': 120,
                'block_type': 'text', 'priority': 7,
                'content': f'Level2_{i}'
            })
        # Third level
        for i in range(6):
            engine.add_block({
                'x': 100 + i * 300, 'y': 550,
                'width': 200, 'height': 100,
                'block_type': 'text', 'priority': 5,
                'content': f'Level3_{i}'
            })
        return engine

    def _create_random_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create random layout"""
        engine = EnhancedSpatialReasoningEngine()
        np.random.seed(42)
        for i in range(10):
            engine.add_block({
                'x': np.random.randint(50, 1600),
                'y': np.random.randint(50, 800),
                'width': np.random.randint(150, 300),
                'height': np.random.randint(100, 200),
                'block_type': 'text', 'priority': np.random.randint(1, 10),
                'content': f'Block {i}'
            })
        return engine

    def _create_single_block_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create layout with single block"""
        engine = EnhancedSpatialReasoningEngine()
        engine.add_block({
            'x': 800, 'y': 400, 'width': 300, 'height': 200,
            'block_type': 'text', 'priority': 5, 'content': 'Single'
        })
        return engine

    def _create_extreme_density_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create extremely dense layout"""
        engine = EnhancedSpatialReasoningEngine()
        for i in range(50):
            engine.add_block({
                'x': 50 + (i % 10) * 180,
                'y': 50 + (i // 10) * 200,
                'width': 170, 'height': 190,
                'block_type': 'text', 'priority': 5,
                'content': f'Block {i}'
            })
        return engine

    def _create_mismatched_sizes_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create layout with mismatched block sizes"""
        engine = EnhancedSpatialReasoningEngine()
        sizes = [(800, 600), (100, 80), (500, 200), (150, 400)]
        positions = [(100, 100), (1000, 100), (100, 700), (700, 300)]
        for (w, h), (x, y) in zip(sizes, positions):
            engine.add_block({
                'x': x, 'y': y, 'width': w, 'height': h,
                'block_type': 'text', 'priority': 5, 'content': 'Block'
            })
        return engine

    def _create_corner_layout(self) -> EnhancedSpatialReasoningEngine:
        """Create layout with blocks in corners"""
        engine = EnhancedSpatialReasoningEngine()
        corners = [(50, 50), (1600, 50), (50, 850), (1600, 850)]
        for x, y in corners:
            engine.add_block({
                'x': x, 'y': y, 'width': 250, 'height': 180,
                'block_type': 'text', 'priority': 5, 'content': 'Corner'
            })
        return engine

    # ========================================================================
    # OVERALL SCORING
    # ========================================================================

    def calculate_overall_score(self) -> float:
        """Calculate weighted overall score"""
        print("\n" + "="*70)
        print("OVERALL OMNISPATIAL SCORE")
        print("="*70)

        dimension_scores = {}
        for dimension, weight in self.weights.items():
            score = self.results[dimension].get('score', 0)
            weighted_score = score * weight
            dimension_scores[dimension] = score
            print(f"  {dimension:25} {score:6.1f}/100 (weight={weight:.2f}) → {weighted_score:5.2f}")

        overall = sum(
            self.results[dim].get('score', 0) * weight
            for dim, weight in self.weights.items()
        )

        self.results['overall_score'] = overall
        self.results['dimension_scores'] = dimension_scores

        print(f"\n  {'='*70}")
        print(f"  OMNISPATIAL SCORE: {overall:.2f}/100")
        print(f"  {'='*70}")

        # Grade
        if overall >= 90:
            grade = "A+ (Exceptional)"
        elif overall >= 80:
            grade = "A (Excellent)"
        elif overall >= 70:
            grade = "B (Good)"
        elif overall >= 60:
            grade = "C (Satisfactory)"
        else:
            grade = "D (Needs Improvement)"

        print(f"\n  Grade: {grade}")

        return overall

    def run_full_benchmark(self):
        """Run complete OmniSpatial benchmark"""
        print("\n" + "="*70)
        print("OMNISPATIAL BENCHMARK SUITE")
        print("Comprehensive Multi-Dimensional Spatial Cognition Test")
        print("="*70)

        start_time = time.time()

        # Run all dimension tests
        self.test_scale_invariance()
        self.test_density_resilience()
        self.test_topological_complexity()
        self.test_temporal_consistency()
        self.test_semantic_coherence()
        self.test_adversarial_robustness()
        self.test_multi_objective()

        # Calculate overall score
        overall_score = self.calculate_overall_score()

        total_time = time.time() - start_time

        print(f"\n  Total benchmark time: {total_time:.2f} seconds")
        print(f"\n  ✓ OmniSpatial Benchmark Complete!")

        return self.results

    def save_results(self, filename: str = "omnispatial_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  📊 Results saved to {filename}")


def main():
    """Run OmniSpatial benchmark"""
    benchmark = OmniSpatialBenchmark()

    try:
        results = benchmark.run_full_benchmark()
        benchmark.save_results()

        # Return appropriate exit code based on score
        overall_score = results['overall_score']
        if overall_score >= 70:
            return 0  # Success
        else:
            return 1  # Needs improvement

    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
