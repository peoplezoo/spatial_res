"""
Comprehensive benchmark test for spatial cognition capabilities
Tests performance, accuracy, and quality across all strategies
"""

import time
import json
import statistics
from typing import Dict, List, Tuple
import sys

from spatial_ai_enhanced import (
    EnhancedSpatialReasoningEngine,
    PlacementConstraints,
    CanvasBlock
)


class SpatialCognitionBenchmark:
    """Benchmark suite for spatial cognition capabilities"""

    def __init__(self):
        self.results = {
            'strategies': {},
            'performance': {},
            'quality': {},
            'scalability': {}
        }

    def benchmark_single_placement(self, num_existing_blocks: int, iterations: int = 10):
        """Benchmark single block placement with varying canvas complexity"""
        print(f"\n{'='*70}")
        print(f"BENCHMARK: Single Placement ({num_existing_blocks} existing blocks)")
        print(f"{'='*70}")

        strategy_times = {
            'topological_cognition': [],
            'holographic_retrieval': [],
            'neuromorphic_field': [],
            'classical_enhanced': []
        }

        strategy_scores = {
            'topological_cognition': [],
            'holographic_retrieval': [],
            'neuromorphic_field': [],
            'classical_enhanced': []
        }

        for iteration in range(iterations):
            engine = EnhancedSpatialReasoningEngine()

            # Add existing blocks
            for i in range(num_existing_blocks):
                x = 100 + (i % 5) * 300
                y = 100 + (i // 5) * 250
                engine.add_block({
                    'x': x, 'y': y,
                    'width': 200 + i * 10,
                    'height': 150 + i * 5,
                    'block_type': 'text',
                    'priority': (i % 10) + 1,
                    'semantic_group': f'group_{i % 3}',
                    'content': f'Block {i}'
                })

            # Test block to place
            new_block = {
                'width': 250, 'height': 180, 'priority': 7,
                'type': 'diagram', 'content': 'Test Block',
                'semantic_group': 'group_1'
            }

            constraints = PlacementConstraints(
                use_quantum_optimization=False,
                enable_temporal_coherence=False
            )

            # Time full placement (all strategies)
            start = time.time()
            result = engine.calculate_optimal_placement(new_block, constraints)
            total_time = time.time() - start

            # Extract individual strategy info from result
            method_used = result['method_used']
            confidence = result['confidence']

            # Record for the winning strategy
            if method_used in strategy_times:
                strategy_times[method_used].append(total_time)
                strategy_scores[method_used].append(confidence)

        # Calculate statistics
        print(f"\nPerformance (avg over {iterations} iterations):")
        for strategy, times in strategy_times.items():
            if times:
                avg_time = statistics.mean(times) * 1000  # Convert to ms
                std_time = statistics.stdev(times) * 1000 if len(times) > 1 else 0
                print(f"  {strategy:25} {avg_time:6.2f} ± {std_time:5.2f} ms")

        print(f"\nQuality (confidence scores):")
        for strategy, scores in strategy_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                std_score = statistics.stdev(scores) if len(scores) > 1 else 0
                print(f"  {strategy:25} {avg_score:.3f} ± {std_score:.3f}")

        print(f"\nStrategy Selection:")
        for strategy, times in strategy_times.items():
            if times:
                selection_rate = len(times) / iterations * 100
                print(f"  {strategy:25} {selection_rate:5.1f}% selected")

        return strategy_times, strategy_scores

    def benchmark_individual_strategies(self):
        """Benchmark each strategy individually"""
        print(f"\n{'='*70}")
        print("BENCHMARK: Individual Strategy Performance")
        print(f"{'='*70}")

        engine = EnhancedSpatialReasoningEngine()

        # Setup canvas
        for i in range(5):
            engine.add_block({
                'x': 100 + i * 300, 'y': 100 + (i % 2) * 300,
                'width': 250, 'height': 180,
                'block_type': 'text', 'priority': 5 + i,
                'content': f'Block {i}'
            })

        new_block = {
            'width': 250, 'height': 180, 'priority': 6,
            'type': 'text', 'content': 'New Block'
        }
        constraints = PlacementConstraints(use_quantum_optimization=False)

        results = {}

        # 1. Topological Cognition
        if engine.topological_cognition.topology_analyzer:
            start = time.time()
            for _ in range(10):
                pos = engine.topological_cognition.optimize_position_topologically(
                    new_block, engine.canvas_state, constraints
                )
            time_topo = (time.time() - start) / 10 * 1000
            results['topological'] = {'time_ms': time_topo, 'position': pos}
            print(f"✓ Topological Cognition:    {time_topo:6.2f} ms/op")

        # 2. Holographic Retrieval
        if engine.holographic_retrieval.holographic_memory:
            start = time.time()
            for _ in range(10):
                pos = engine.holographic_retrieval.optimize_position_holographically(
                    new_block, engine.canvas_state, constraints
                )
            time_holo = (time.time() - start) / 10 * 1000
            results['holographic'] = {'time_ms': time_holo, 'position': pos}
            print(f"✓ Holographic Retrieval:     {time_holo:6.2f} ms/op")

        # 3. Neuromorphic Field
        if engine.neuromorphic_computation.neuromorphic_field:
            start = time.time()
            for _ in range(10):
                pos = engine.neuromorphic_computation.optimize_position_neuromorphically(
                    new_block, engine.canvas_state, constraints
                )
            time_neuro = (time.time() - start) / 10 * 1000
            results['neuromorphic'] = {'time_ms': time_neuro, 'position': pos}
            print(f"✓ Neuromorphic Field:        {time_neuro:6.2f} ms/op")

        return results

    def benchmark_memory_usage(self):
        """Test holographic memory capacity and retrieval"""
        print(f"\n{'='*70}")
        print("BENCHMARK: Holographic Memory Performance")
        print(f"{'='*70}")

        engine = EnhancedSpatialReasoningEngine()

        if not engine.holographic_retrieval.holographic_memory:
            print("✗ Holographic memory not available")
            return

        # Store patterns
        patterns_to_store = [100, 500, 1000]
        results = {}

        for num_patterns in patterns_to_store:
            # Store patterns
            start = time.time()
            for i in range(num_patterns):
                pattern = {
                    'x': 100 + (i % 20) * 80,
                    'y': 100 + (i % 10) * 90,
                    'width': 200 + (i % 5) * 20,
                    'height': 150 + (i % 4) * 15,
                    'priority': (i % 10) + 1,
                    'semantic_group': f'group_{i % 5}'
                }
                engine.holographic_retrieval.holographic_memory.store(
                    f'pattern_{i}', pattern
                )
            store_time = time.time() - start

            # Retrieve patterns
            query = {
                'width': 220, 'height': 165, 'priority': 5,
                'semantic_group': 'group_2'
            }
            start = time.time()
            retrieved = engine.holographic_retrieval.holographic_memory.retrieve(query)
            retrieve_time = (time.time() - start) * 1000

            results[num_patterns] = {
                'store_time': store_time,
                'retrieve_time_ms': retrieve_time,
                'patterns_found': len(retrieved)
            }

            print(f"\n{num_patterns} patterns:")
            print(f"  Store time:    {store_time:.3f} s")
            print(f"  Retrieve time: {retrieve_time:.2f} ms")
            print(f"  Found:         {len(retrieved)} similar patterns")

        return results

    def benchmark_topological_complexity(self):
        """Benchmark topological analysis with varying layout complexity"""
        print(f"\n{'='*70}")
        print("BENCHMARK: Topological Analysis Complexity")
        print(f"{'='*70}")

        engine = EnhancedSpatialReasoningEngine()

        if not engine.topological_cognition.topology_analyzer:
            print("✗ Topological analyzer not available")
            return

        block_counts = [5, 10, 20, 50]
        results = {}

        for num_blocks in block_counts:
            # Create layout
            engine_test = EnhancedSpatialReasoningEngine()
            for i in range(num_blocks):
                x = 100 + (i % 10) * 180
                y = 100 + (i // 10) * 200
                engine_test.add_block({
                    'x': x, 'y': y,
                    'width': 150, 'height': 120,
                    'block_type': 'text', 'priority': 5,
                    'content': f'Block {i}'
                })

            # Analyze topology
            blocks = [b.to_dict() for b in engine_test.canvas_state]
            start = time.time()
            topology = engine_test.topological_cognition.topology_analyzer.analyze_topology(blocks)
            analysis_time = (time.time() - start) * 1000

            results[num_blocks] = {
                'analysis_time_ms': analysis_time,
                'betti_0': topology['betti_0'],
                'betti_1': topology['betti_1'],
                'euler': topology['euler_characteristic']
            }

            print(f"\n{num_blocks} blocks:")
            print(f"  Analysis time: {analysis_time:.2f} ms")
            print(f"  Betti β₀:      {topology['betti_0']} (components)")
            print(f"  Betti β₁:      {topology['betti_1']} (holes)")
            print(f"  Euler χ:       {topology['euler_characteristic']}")

        return results

    def benchmark_neuromorphic_evolution(self):
        """Benchmark neuromorphic field evolution steps"""
        print(f"\n{'='*70}")
        print("BENCHMARK: Neuromorphic Field Evolution")
        print(f"{'='*70}")

        engine = EnhancedSpatialReasoningEngine()

        if not engine.neuromorphic_computation.neuromorphic_field:
            print("✗ Neuromorphic field not available")
            return

        # Add blocks to create field activation
        for i in range(10):
            engine.add_block({
                'x': 100 + i * 180, 'y': 100 + (i % 3) * 250,
                'width': 150, 'height': 120,
                'block_type': 'text', 'priority': 5,
                'content': f'Block {i}'
            })

        evolution_steps = [5, 10, 20, 50]
        results = {}

        for steps in evolution_steps:
            engine.neuromorphic_computation.evolution_steps = steps

            new_block = {
                'width': 200, 'height': 150, 'priority': 6,
                'type': 'text', 'content': 'Test'
            }
            constraints = PlacementConstraints(use_quantum_optimization=False)

            start = time.time()
            pos = engine.neuromorphic_computation.optimize_position_neuromorphically(
                new_block, engine.canvas_state, constraints
            )
            evolution_time = (time.time() - start) * 1000

            stats = engine.neuromorphic_computation.get_field_statistics()

            results[steps] = {
                'time_ms': evolution_time,
                'position': pos,
                'stats': stats
            }

            print(f"\n{steps} evolution steps:")
            print(f"  Time:           {evolution_time:.2f} ms")
            print(f"  Mean activity:  {stats['mean_activity']:.3f}")
            print(f"  Total spikes:   {stats['total_spikes']}")
            print(f"  Position:       ({pos['x']:.0f}, {pos['y']:.0f})")

        return results

    def benchmark_scalability(self):
        """Test scalability with increasing canvas complexity"""
        print(f"\n{'='*70}")
        print("BENCHMARK: Scalability Analysis")
        print(f"{'='*70}")

        canvas_sizes = [5, 10, 20, 50]
        results = {}

        for num_blocks in canvas_sizes:
            engine = EnhancedSpatialReasoningEngine()

            # Add blocks
            for i in range(num_blocks):
                x = 100 + (i % 10) * 180
                y = 100 + (i // 10) * 200
                engine.add_block({
                    'x': x, 'y': y,
                    'width': 150, 'height': 120,
                    'block_type': 'text', 'priority': (i % 10) + 1,
                    'semantic_group': f'group_{i % 3}',
                    'content': f'Block {i}'
                })

            # Measure placement time
            new_block = {
                'width': 200, 'height': 150, 'priority': 6,
                'type': 'text', 'content': 'New Block'
            }
            constraints = PlacementConstraints(use_quantum_optimization=False)

            start = time.time()
            result = engine.calculate_optimal_placement(new_block, constraints)
            placement_time = (time.time() - start) * 1000

            results[num_blocks] = {
                'placement_time_ms': placement_time,
                'strategies_evaluated': result['strategies_evaluated'],
                'method_used': result['method_used'],
                'confidence': result['confidence']
            }

            print(f"\n{num_blocks} blocks on canvas:")
            print(f"  Placement time:     {placement_time:.2f} ms")
            print(f"  Strategies tested:  {result['strategies_evaluated']}")
            print(f"  Best method:        {result['method_used']}")
            print(f"  Confidence:         {result['confidence']:.3f}")

        # Calculate scalability metrics
        if len(canvas_sizes) >= 2:
            times = [results[n]['placement_time_ms'] for n in canvas_sizes]
            print(f"\nScalability:")
            print(f"  5 → 10 blocks:  {times[1]/times[0]:.2f}x slowdown")
            if len(times) >= 3:
                print(f"  10 → 20 blocks: {times[2]/times[1]:.2f}x slowdown")
            if len(times) >= 4:
                print(f"  20 → 50 blocks: {times[3]/times[2]:.2f}x slowdown")

        return results

    def run_full_benchmark(self):
        """Run all benchmarks"""
        print("\n" + "="*70)
        print("SPATIAL COGNITION CAPABILITIES - COMPREHENSIVE BENCHMARK")
        print("="*70)

        start_total = time.time()

        # Run all benchmarks
        self.results['individual'] = self.benchmark_individual_strategies()
        self.results['memory'] = self.benchmark_memory_usage()
        self.results['topology'] = self.benchmark_topological_complexity()
        self.results['neuromorphic'] = self.benchmark_neuromorphic_evolution()
        self.results['scalability'] = self.benchmark_scalability()

        # Single placement benchmarks with different complexities
        print(f"\n{'='*70}")
        print("BENCHMARK: Multi-Complexity Placement Tests")
        print(f"{'='*70}")

        for num_blocks in [5, 10, 20]:
            self.benchmark_single_placement(num_blocks, iterations=5)

        total_time = time.time() - start_total

        # Summary
        print(f"\n{'='*70}")
        print("BENCHMARK SUMMARY")
        print(f"{'='*70}")
        print(f"Total benchmark time: {total_time:.2f} seconds")
        print(f"\n✓ All benchmarks completed successfully!")

        return self.results

    def save_results(self, filename: str = "benchmark_results.json"):
        """Save benchmark results to JSON file"""
        # Convert results to JSON-serializable format
        json_results = {}
        for category, data in self.results.items():
            if isinstance(data, dict):
                json_results[category] = {
                    str(k): v for k, v in data.items()
                }

        with open(filename, 'w') as f:
            json.dump(json_results, f, indent=2)

        print(f"\n📊 Results saved to {filename}")


def main():
    """Run benchmark suite"""
    benchmark = SpatialCognitionBenchmark()

    try:
        results = benchmark.run_full_benchmark()
        benchmark.save_results()
        return 0
    except Exception as e:
        print(f"\n❌ Benchmark failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
