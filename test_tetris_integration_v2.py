#!/usr/bin/env python3
"""Test Tetris integration with improved selection rate"""

from spatial_ai_enhanced import EnhancedSpatialReasoningEngine, PlacementConstraints
from tetris_nsga2_placer import TetrisBlock
import json

def test_tetris_selection_rate():
    """Test how often Tetris is selected with new scoring bonus"""
    print("=" * 80)
    print("TETRIS INTEGRATION TEST V2: Adaptive + Scoring Bonus")
    print("=" * 80)

    engine = EnhancedSpatialReasoningEngine()

    # Pre-place some blocks to create constraints
    header_blocks = [
        {'id': 'header1', 'width': 200, 'height': 100, 'x': 0, 'y': 0, 'semantic_group': 'header', 'priority': 9},
        {'id': 'header2', 'width': 180, 'height': 100, 'x': 220, 'y': 0, 'semantic_group': 'header', 'priority': 9}
    ]

    content_blocks = [
        {'id': 'content1', 'width': 150, 'height': 200, 'x': 0, 'y': 120, 'semantic_group': 'content', 'priority': 5},
        {'id': 'content2', 'width': 160, 'height': 200, 'x': 170, 'y': 120, 'semantic_group': 'content', 'priority': 5}
    ]

    for block in header_blocks + content_blocks:
        engine.canvas_state.append(type('Block', (), block)())

    # Test placing 6 new blocks
    test_blocks = [
        {'id': 'new1', 'width': 150, 'height': 120, 'semantic_group': 'header', 'priority': 8},
        {'id': 'new2', 'width': 140, 'height': 130, 'semantic_group': 'content', 'priority': 5},
        {'id': 'new3', 'width': 160, 'height': 110, 'semantic_group': 'content', 'priority': 6},
        {'id': 'new4', 'width': 130, 'height': 140, 'semantic_group': 'footer', 'priority': 4},
        {'id': 'new5', 'width': 170, 'height': 100, 'semantic_group': 'header', 'priority': 7},
        {'id': 'new6', 'width': 150, 'height': 150, 'semantic_group': 'content', 'priority': 5}
    ]

    tetris_count = 0
    overlap_count = 0
    placements = []

    print("\n📍 PLACEMENT RESULTS:")
    print("-" * 80)

    for block in test_blocks:
        # Place block
        constraints = PlacementConstraints(
            max_width=800,
            max_height=600,
            min_padding=10,
            use_quantum_optimization=False  # Disable quantum to focus on Tetris
        )

        result = engine.calculate_optimal_placement(block, constraints)

        # Check if placement was made by Tetris (look for the method in recent logs)
        # We'll use the scoring bonus as a proxy - if score > 10000, it was Tetris
        if result and 'score' in result:
            score = result['score'] if isinstance(result['score'], dict) else {'total': result.get('total_score', 0)}
            if score.get('total', 0) > 10000:
                tetris_count += 1
                method = "TETRIS"
            else:
                method = "OTHER"
        else:
            method = "UNKNOWN"

        # Check for overlaps
        has_overlap = False
        if result and 'x' in result and 'y' in result:
            x, y = result['x'], result['y']
            width, height = block['width'], block['height']

            for existing in engine.canvas_state:
                if not (x + width <= existing.x or x >= existing.x + existing.width or
                        y + height <= existing.y or y >= existing.y + existing.height):
                    has_overlap = True
                    overlap_count += 1
                    break

            placements.append({
                'id': block['id'],
                'x': x,
                'y': y,
                'method': method,
                'overlap': has_overlap
            })

            # Add to canvas
            placed_block = type('Block', (), {
                'id': block['id'],
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'semantic_group': block['semantic_group']
            })()
            engine.canvas_state.append(placed_block)

            overlap_marker = "❌ OVERLAP" if has_overlap else "✅"
            print(f"{block['id']:8s} → ({x:5.1f}, {y:5.1f}) | Method: {method:7s} | {overlap_marker}")

    print("\n" + "=" * 80)
    print("📊 SUMMARY STATISTICS:")
    print("=" * 80)
    print(f"Total placements:     {len(test_blocks)}")
    print(f"Tetris placements:    {tetris_count} ({tetris_count/len(test_blocks)*100:.1f}%)")
    print(f"Other strategy uses:  {len(test_blocks) - tetris_count}")
    print(f"Total overlaps:       {overlap_count}")
    print(f"Overlap-free rate:    {(len(test_blocks) - overlap_count)/len(test_blocks)*100:.1f}%")

    # Calculate semantic coherence
    groups = {}
    for p in placements:
        block_data = next(b for b in test_blocks + header_blocks + content_blocks if b['id'] == p['id'])
        group = block_data.get('semantic_group', 'none')
        if group not in groups:
            groups[group] = []
        groups[group].append((p['x'], p['y']))

    total_within = 0
    total_between = 0
    count = 0

    for group1, positions1 in groups.items():
        for group2, positions2 in groups.items():
            for p1 in positions1:
                for p2 in positions2:
                    if p1 != p2:
                        dist = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
                        if group1 == group2:
                            total_within += dist
                        else:
                            total_between += dist
                        count += 1

    if total_within > 0 and total_between > 0:
        semantic_score = (total_between / total_within) * 100 / 3  # Normalize
        print(f"Semantic coherence:   {semantic_score:.2f}/100")

    print("\n" + "=" * 80)

    # Performance assessment
    if tetris_count >= 5:  # 83%+
        print("🎉 EXCELLENT: Tetris selection rate above 80%!")
    elif tetris_count >= 4:  # 67%+
        print("✅ GOOD: Tetris selection rate improved, but room for optimization")
    else:
        print("⚠️  NEEDS WORK: Tetris selection rate still low")

    if overlap_count == 0:
        print("🎯 PERFECT: Zero overlaps achieved!")
    elif overlap_count <= 1:
        print("👍 GREAT: Minimal overlaps")
    else:
        print(f"⚠️  WARNING: {overlap_count} overlaps detected")

    return {
        'tetris_rate': tetris_count / len(test_blocks),
        'overlap_count': overlap_count,
        'placements': placements
    }

if __name__ == "__main__":
    results = test_tetris_selection_rate()
