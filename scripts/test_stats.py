#!/usr/bin/env python3
"""
Test script for stats calculation engine
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.stats import StatsCalculator, STAT_DEFINITIONS, get_essential_stats


def main():
    """Test stats calculation with demo database"""
    print("=" * 70)
    print("STATS CALCULATION ENGINE - Test Script")
    print("=" * 70)
    print()

    # Initialize
    print("1. Initializing database and stats calculator...")
    db = DatabaseManager("data/demo.db")
    calculator = StatsCalculator(min_sample_size=1)  # Low threshold for testing
    print("   ✓ Initialized")
    print()

    # Get hero name
    cursor = db.conn.cursor()
    cursor.execute("SELECT DISTINCT hero_name FROM hands LIMIT 1")
    row = cursor.fetchone()

    if not row:
        print("   ! No hands found in database")
        print("   Run demo_parse.py first to populate database")
        return

    hero_name = row[0]
    print(f"2. Found hero: {hero_name}")
    print()

    # Get hands
    print("3. Retrieving hands from database...")
    hands = db.get_hero_hands(hero_name)
    print(f"   ✓ Retrieved {len(hands)} hands")
    print()

    # Calculate stats
    print("4. Calculating stats...")
    stats = calculator.calculate_stats(hands, hero_name, essential_only=True)
    print(f"   ✓ Calculated {len(stats)} stats")
    print()

    # Display results
    print("5. Stats Results:")
    print("-" * 70)

    # Group by category
    categories = {
        'preflop': 'PREFLOP STATS',
        'postflop_aggression': 'POSTFLOP AGGRESSION',
        'postflop_defense': 'POSTFLOP DEFENSE',
        'river': 'RIVER STATS'
    }

    for category_key, category_name in categories.items():
        print(f"\n{category_name}:")
        print("-" * 40)

        # Get stats in this category
        essential_stats = get_essential_stats()
        for stat_name in essential_stats:
            definition = STAT_DEFINITIONS.get(stat_name)
            if definition and definition['category'] == category_key:
                value = stats.get(stat_name)
                gto_baseline = definition['gto_baseline']

                if value is not None:
                    delta = value - gto_baseline
                    delta_str = f"({delta:+.1f})" if delta != 0 else ""
                    print(f"  {definition['name']:20s}: {value:6.1f}%  "
                          f"(GTO: {gto_baseline:.1f}%) {delta_str}")
                else:
                    print(f"  {definition['name']:20s}: N/A     "
                          f"(GTO: {gto_baseline:.1f}%) (insufficient data)")

    print()
    print("-" * 70)
    print(f"\nSample Size: {stats.get('sample_size', 0)} hands")
    print(f"Reliable: {'Yes' if stats.get('reliable', False) else 'No (< 50 hands)'}")
    print()

    # Show counter summary
    print("6. Counter Summary (for debugging):")
    print("-" * 70)
    counters = calculator.get_counter_summary()
    key_counters = [
        'total_hands', 'saw_flop', 'saw_river', 'showdowns',
        'voluntary_preflop_actions', 'preflop_raises',
        'opportunities_to_3bet', 'three_bets',
        'cbet_opportunities', 'cbets',
        'faced_cbet', 'folds_to_cbet'
    ]

    for counter in key_counters:
        print(f"  {counter:30s}: {counters.get(counter, 0)}")

    print()
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()

    db.close()


if __name__ == "__main__":
    main()
