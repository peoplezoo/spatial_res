"""
Tetris-inspired NSGA-II Placement System
Combines gravity-based collision detection with multi-objective optimization

Key Innovation: NSGA-II optimizes DROP POSITION (x-coordinate + rotation),
Tetris physics naturally enforces zero-overlap constraint.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from copy import deepcopy
import random


@dataclass
class TetrisBlock:
    """Block that can be dropped Tetris-style"""
    id: str
    width: float
    height: float
    x: float = 0.0
    y: float = 0.0
    semantic_group: Optional[str] = None
    priority: int = 5
    rotation: int = 0  # 0, 90, 180, 270

    def get_corners(self) -> List[Tuple[float, float]]:
        """Get four corners of the block"""
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]

    def intersects(self, other: 'TetrisBlock') -> bool:
        """Check if this block overlaps with another"""
        return not (
            self.x + self.width <= other.x or
            self.x >= other.x + other.width or
            self.y + self.height <= other.y or
            self.y >= other.y + other.height
        )

    def rotate_90(self):
        """Rotate block 90 degrees (swap width/height)"""
        self.width, self.height = self.height, self.width
        self.rotation = (self.rotation + 90) % 360


@dataclass
class TetrisSolution:
    """Represents a complete placement solution"""
    blocks: List[TetrisBlock] = field(default_factory=list)
    objectives: Dict[str, float] = field(default_factory=dict)
    rank: int = 0
    crowding_distance: float = 0.0

    def dominates(self, other: 'TetrisSolution') -> bool:
        """Check if this solution Pareto-dominates another"""
        at_least_one_better = False
        for obj_name in self.objectives:
            if self.objectives[obj_name] < other.objectives[obj_name]:
                return False  # Other is better in this objective
            if self.objectives[obj_name] > other.objectives[obj_name]:
                at_least_one_better = True
        return at_least_one_better

    def copy(self) -> 'TetrisSolution':
        """Deep copy of solution"""
        return TetrisSolution(
            blocks=[deepcopy(b) for b in self.blocks],
            objectives=self.objectives.copy(),
            rank=self.rank,
            crowding_distance=self.crowding_distance
        )


class TetrisPhysicsEngine:
    """Handles gravity-based block placement with collision detection"""

    def __init__(self, canvas_width: float = 1920, canvas_height: float = 1080):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.gravity_step = 5  # Pixels per drop iteration

    def drop_block(self, block: TetrisBlock, placed_blocks: List[TetrisBlock],
                   target_y: Optional[float] = None) -> TetrisBlock:
        """
        Drop block from top using Tetris physics.
        Returns block with final resting position.
        """
        # Start at top of canvas
        block.y = 0

        # If target_y specified (semantic layer), try to get close to it
        if target_y is not None:
            # Drop until we hit target or collision
            while block.y < target_y and block.y + block.height < self.canvas_height:
                if self._check_collision(block, placed_blocks):
                    break
                block.y += self.gravity_step
        else:
            # Drop until collision or bottom
            while block.y + block.height < self.canvas_height:
                # Try moving down
                block.y += self.gravity_step

                # Check collision
                if self._check_collision(block, placed_blocks):
                    # Move back up to last valid position
                    block.y -= self.gravity_step
                    break

        return block

    def _check_collision(self, block: TetrisBlock,
                        placed_blocks: List[TetrisBlock]) -> bool:
        """Check if block collides with any placed blocks"""
        for placed in placed_blocks:
            if block.intersects(placed):
                return True
        return False

    def find_valid_drop_position(self, block: TetrisBlock,
                                placed_blocks: List[TetrisBlock],
                                semantic_layer: Optional[float] = None) -> Optional[TetrisBlock]:
        """
        Find valid resting position for block at its current x-coordinate.
        Returns None if no valid position exists.
        """
        # Try dropping at current x position
        test_block = deepcopy(block)
        test_block = self.drop_block(test_block, placed_blocks, semantic_layer)

        # Verify no overlap
        if not self._check_collision(test_block, placed_blocks):
            return test_block

        return None


class NSGA2TetrisOptimizer:
    """
    NSGA-II optimizer for Tetris-style placement.
    Optimizes: drop x-position, rotation, target layer
    Physics handles: collision-free final placement
    """

    def __init__(self,
                 canvas_width: float = 1920,
                 canvas_height: float = 1080,
                 population_size: int = 50,
                 n_generations: int = 30):

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.population_size = population_size
        self.n_generations = n_generations

        self.physics = TetrisPhysicsEngine(canvas_width, canvas_height)

        # Semantic layer targets (y-coordinates)
        self.semantic_layers = {
            'header': 100,
            'content': canvas_height / 2,
            'footer': canvas_height - 200,
            None: canvas_height / 2  # Default
        }

    def optimize_placement(self,
                          blocks_to_place: List[TetrisBlock],
                          existing_blocks: List[TetrisBlock]) -> TetrisSolution:
        """
        Main optimization loop using NSGA-II + Tetris physics.
        """
        print(f"🎮 NSGA-II Tetris Optimization: {len(blocks_to_place)} blocks")

        # Initialize population
        population = self._initialize_population(blocks_to_place, existing_blocks)

        best_solution = None
        best_overlap = float('inf')

        for gen in range(self.n_generations):
            # Evaluate objectives for all solutions
            for solution in population:
                self._evaluate_objectives(solution, existing_blocks)

            # Non-dominated sorting
            fronts = self._fast_non_dominated_sort(population)

            # Calculate crowding distance
            for front in fronts:
                self._calculate_crowding_distance(front)

            # Track best zero-overlap solution
            for solution in population:
                overlap = solution.objectives.get('overlap_penalty', float('inf'))
                if overlap < best_overlap:
                    best_overlap = overlap
                    best_solution = solution.copy()

            if gen % 5 == 0:
                print(f"  Gen {gen}: Best overlap={best_overlap:.1f}, "
                      f"Fronts={len(fronts)}, "
                      f"Pareto size={len(fronts[0]) if fronts else 0}")

            # Generate next generation
            if gen < self.n_generations - 1:
                population = self._generate_offspring(fronts)

        # Return best solution from final Pareto front
        if fronts and fronts[0]:
            # Prefer zero-overlap solutions with best semantic coherence
            zero_overlap = [s for s in fronts[0]
                          if s.objectives.get('overlap_penalty', 1) == 0]

            if zero_overlap:
                best_solution = max(zero_overlap,
                                  key=lambda s: s.objectives.get('semantic_coherence', 0))
            else:
                best_solution = fronts[0][0]

        print(f"  ✅ Final: Overlap={best_solution.objectives.get('overlap_penalty', 0):.1f}")
        return best_solution

    def _initialize_population(self, blocks_to_place: List[TetrisBlock],
                               existing_blocks: List[TetrisBlock]) -> List[TetrisSolution]:
        """Create initial population with random drop positions"""
        population = []

        for _ in range(self.population_size):
            solution = TetrisSolution()
            placed = existing_blocks.copy()

            for block in blocks_to_place:
                # Random drop x-position
                x = random.uniform(20, self.canvas_width - block.width - 20)

                # Random rotation (0 or 90 degrees for simplicity)
                rotation = random.choice([0, 90])

                # Create test block
                test_block = deepcopy(block)
                test_block.x = x
                if rotation == 90:
                    test_block.rotate_90()

                # Get semantic target layer
                target_layer = self.semantic_layers.get(block.semantic_group)

                # Drop using physics
                final_block = self.physics.drop_block(test_block, placed, target_layer)

                solution.blocks.append(final_block)
                placed.append(final_block)

            population.append(solution)

        return population

    def _evaluate_objectives(self, solution: TetrisSolution,
                            existing_blocks: List[TetrisBlock]):
        """
        Evaluate all objectives for a solution.
        Objectives (maximize):
        1. Zero overlaps (HARD CONSTRAINT)
        2. Semantic coherence
        3. Aesthetic balance
        4. Flow quality
        """
        all_blocks = existing_blocks + solution.blocks

        # Objective 1: Overlap penalty (minimize, should be 0)
        overlap_penalty = 0
        for i, block in enumerate(all_blocks):
            for other in all_blocks[i+1:]:
                if block.intersects(other):
                    overlap_penalty += 100

        # Objective 2: Semantic coherence (maximize)
        semantic_coherence = self._calculate_semantic_coherence(all_blocks)

        # Objective 3: Aesthetic balance (maximize)
        aesthetic_balance = self._calculate_aesthetic_balance(all_blocks)

        # Objective 4: Flow quality (maximize)
        flow_quality = self._calculate_flow_quality(all_blocks)

        solution.objectives = {
            'overlap_penalty': -overlap_penalty,  # Negative because we maximize
            'semantic_coherence': semantic_coherence,
            'aesthetic_balance': aesthetic_balance,
            'flow_quality': flow_quality
        }

    def _calculate_semantic_coherence(self, blocks: List[TetrisBlock]) -> float:
        """Calculate how well semantic groups cluster together"""
        groups = {}
        for block in blocks:
            group = block.semantic_group
            if group:
                if group not in groups:
                    groups[group] = []
                groups[group].append(block)

        if not groups:
            return 50.0

        coherence_scores = []
        for group, group_blocks in groups.items():
            if len(group_blocks) < 2:
                continue

            # Calculate avg distance within group
            same_dists = []
            for i, b1 in enumerate(group_blocks):
                for b2 in group_blocks[i+1:]:
                    dist = np.sqrt((b1.x - b2.x)**2 + (b1.y - b2.y)**2)
                    same_dists.append(dist)

            if not same_dists:
                continue

            # Calculate avg distance to other groups
            other_blocks = [b for b in blocks if b.semantic_group != group]
            other_dists = []
            for b1 in group_blocks:
                for b2 in other_blocks:
                    dist = np.sqrt((b1.x - b2.x)**2 + (b1.y - b2.y)**2)
                    other_dists.append(dist)

            if same_dists and other_dists:
                avg_same = np.mean(same_dists)
                avg_other = np.mean(other_dists)
                ratio = avg_other / (avg_same + 1e-6)
                coherence = min(100, ratio * 25)  # Target 4:1 ratio = 100 score
                coherence_scores.append(coherence)

        return np.mean(coherence_scores) if coherence_scores else 50.0

    def _calculate_aesthetic_balance(self, blocks: List[TetrisBlock]) -> float:
        """Calculate visual balance of layout"""
        if not blocks:
            return 50.0

        # Calculate center of mass
        total_area = sum(b.width * b.height for b in blocks)
        com_x = sum(b.x * b.width * b.height for b in blocks) / total_area
        com_y = sum(b.y * b.width * b.height for b in blocks) / total_area

        # Score based on how close COM is to canvas center
        canvas_center_x = self.canvas_width / 2
        canvas_center_y = self.canvas_height / 2

        dist_from_center = np.sqrt(
            (com_x - canvas_center_x)**2 +
            (com_y - canvas_center_y)**2
        )

        max_dist = np.sqrt(canvas_center_x**2 + canvas_center_y**2)
        balance_score = 100 * (1 - dist_from_center / max_dist)

        return balance_score

    def _calculate_flow_quality(self, blocks: List[TetrisBlock]) -> float:
        """Calculate reading flow quality (top-left to bottom-right)"""
        if not blocks:
            return 50.0

        # Sort by reading order (top-left to bottom-right)
        sorted_blocks = sorted(blocks, key=lambda b: (b.y, b.x))

        # Score monotonic progression
        flow_violations = 0
        for i in range(len(sorted_blocks) - 1):
            curr = sorted_blocks[i]
            next_block = sorted_blocks[i + 1]

            # Check if next block is generally down-right
            if next_block.x < curr.x and next_block.y < curr.y:
                flow_violations += 1

        flow_score = 100 * (1 - flow_violations / max(len(blocks) - 1, 1))
        return flow_score

    def _fast_non_dominated_sort(self, population: List[TetrisSolution]) -> List[List[TetrisSolution]]:
        """NSGA-II fast non-dominated sorting"""
        fronts = [[]]

        for p in population:
            p.domination_count = 0
            p.dominated_solutions = []

            for q in population:
                if p.dominates(q):
                    p.dominated_solutions.append(q)
                elif q.dominates(p):
                    p.domination_count += 1

            if p.domination_count == 0:
                p.rank = 0
                fronts[0].append(p)

        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in p.dominated_solutions:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 1
                        next_front.append(q)
            i += 1
            if next_front:
                fronts.append(next_front)
            else:
                break

        return fronts

    def _calculate_crowding_distance(self, front: List[TetrisSolution]):
        """Calculate crowding distance for diversity"""
        if len(front) == 0:
            return

        # Initialize distances
        for solution in front:
            solution.crowding_distance = 0

        # For each objective
        for obj_name in front[0].objectives.keys():
            # Sort by objective value
            front.sort(key=lambda s: s.objectives[obj_name])

            # Boundary points get infinite distance
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')

            # Calculate distance for middle points
            obj_range = front[-1].objectives[obj_name] - front[0].objectives[obj_name]
            if obj_range == 0:
                continue

            for i in range(1, len(front) - 1):
                distance = (front[i+1].objectives[obj_name] -
                          front[i-1].objectives[obj_name]) / obj_range
                front[i].crowding_distance += distance

    def _generate_offspring(self, fronts: List[List[TetrisSolution]]) -> List[TetrisSolution]:
        """Generate offspring using selection, crossover, and mutation"""
        offspring = []

        # Flatten fronts for selection
        all_solutions = []
        for front in fronts:
            all_solutions.extend(front)

        while len(offspring) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_select(all_solutions)
            parent2 = self._tournament_select(all_solutions)

            # Crossover
            child1, child2 = self._crossover(parent1, parent2)

            # Mutation
            child1 = self._mutate(child1)
            child2 = self._mutate(child2)

            offspring.extend([child1, child2])

        return offspring[:self.population_size]

    def _tournament_select(self, population: List[TetrisSolution]) -> TetrisSolution:
        """Binary tournament selection"""
        candidates = random.sample(population, min(2, len(population)))

        # Prefer better rank
        candidates.sort(key=lambda s: (s.rank, -s.crowding_distance))
        return candidates[0].copy()

    def _crossover(self, parent1: TetrisSolution,
                   parent2: TetrisSolution) -> Tuple[TetrisSolution, TetrisSolution]:
        """Single-point crossover on block positions"""
        if len(parent1.blocks) != len(parent2.blocks) or len(parent1.blocks) <= 1:
            return parent1.copy(), parent2.copy()

        point = random.randint(1, len(parent1.blocks) - 1)

        child1 = TetrisSolution()
        child2 = TetrisSolution()

        # Swap drop x-positions at crossover point
        for i in range(len(parent1.blocks)):
            if i < point:
                child1.blocks.append(deepcopy(parent1.blocks[i]))
                child2.blocks.append(deepcopy(parent2.blocks[i]))
            else:
                # Swap x positions
                b1 = deepcopy(parent2.blocks[i])
                b2 = deepcopy(parent1.blocks[i])
                child1.blocks.append(b1)
                child2.blocks.append(b2)

        return child1, child2

    def _mutate(self, solution: TetrisSolution) -> TetrisSolution:
        """Mutate drop positions"""
        mutation_rate = 0.2

        for block in solution.blocks:
            if random.random() < mutation_rate:
                # Mutate x position
                delta_x = random.gauss(0, 50)
                new_x = block.x + delta_x
                new_x = max(20, min(new_x, self.canvas_width - block.width - 20))
                block.x = new_x

                # Re-drop with physics
                placed = [b for b in solution.blocks if b != block]
                target_layer = self.semantic_layers.get(block.semantic_group)
                block = self.physics.drop_block(block, placed, target_layer)

        return solution


def demo_tetris_nsga2():
    """Demo the Tetris NSGA-II placement system"""
    print("="*70)
    print("TETRIS + NSGA-II PLACEMENT DEMO")
    print("="*70)

    # Create test blocks
    blocks_to_place = [
        TetrisBlock(id='header_1', width=200, height=100, semantic_group='header', priority=8),
        TetrisBlock(id='header_2', width=200, height=100, semantic_group='header', priority=8),
        TetrisBlock(id='content_1', width=250, height=150, semantic_group='content', priority=5),
        TetrisBlock(id='content_2', width=250, height=150, semantic_group='content', priority=5),
        TetrisBlock(id='footer_1', width=200, height=80, semantic_group='footer', priority=3),
        TetrisBlock(id='footer_2', width=200, height=80, semantic_group='footer', priority=3),
    ]

    # Optimize placement
    optimizer = NSGA2TetrisOptimizer(
        canvas_width=1920,
        canvas_height=1080,
        population_size=40,
        n_generations=20
    )

    solution = optimizer.optimize_placement(blocks_to_place, existing_blocks=[])

    # Print results
    print("\n" + "="*70)
    print("FINAL SOLUTION")
    print("="*70)
    print(f"\nObjectives:")
    for obj, value in solution.objectives.items():
        print(f"  {obj}: {value:.2f}")

    print(f"\nPlaced blocks:")
    for block in solution.blocks:
        print(f"  {block.id}: ({block.x:.0f}, {block.y:.0f}) "
              f"[{block.width:.0f}x{block.height:.0f}] "
              f"group={block.semantic_group}")

    # Verify zero overlaps
    overlaps = 0
    for i, b1 in enumerate(solution.blocks):
        for b2 in solution.blocks[i+1:]:
            if b1.intersects(b2):
                overlaps += 1
                print(f"  ⚠️ OVERLAP: {b1.id} x {b2.id}")

    print(f"\n{'✅ ZERO OVERLAPS!' if overlaps == 0 else f'❌ {overlaps} OVERLAPS'}")


if __name__ == "__main__":
    demo_tetris_nsga2()
