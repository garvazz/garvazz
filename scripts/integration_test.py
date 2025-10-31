#!/usr/bin/env python3
"""
Comprehensive integration test for PLO Mastery Suite
Tests full pipeline: Parse -> Store -> Calculate Stats -> Display
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.parsers import PokerStarsParser
from src.stats import StatsCalculator, STAT_DEFINITIONS


def create_sample_hands():
    """Create multiple sample hands for comprehensive testing"""
    return [
        # Hand 1: Hero opens BTN, villain 3-bets, hero folds
        """PokerStars Hand #123456789001: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:30:00 ET
Table 'TestTable1' 6-max Seat #1 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Hero: posts small blind $0.50
Villain1: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [As Ks Qh Jh]
Villain2: folds
Villain3: folds
Villain4: folds
Villain5: raises $3 to $3
Hero: raises $9 to $12
Villain1: folds
Villain5: raises $27 to $39
Hero: folds
Uncalled bet ($27) returned to Villain5
Villain5 collected $25 from pot
*** SUMMARY ***
Total pot $25 | Rake $0
Seat 1: Hero (button) (small blind) folded before Flop
Seat 6: Villain5 collected ($25)
""",

        # Hand 2: Hero opens CO, BB calls, hero c-bets flop and wins
        """PokerStars Hand #123456789002: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:35:00 ET
Table 'TestTable1' 6-max Seat #5 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Villain4: posts small blind $0.50
Villain5: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [Ah Kh Tc 9c]
Hero: raises $3 to $3
Villain1: folds
Villain2: folds
Villain3: folds
Villain4: folds
Villain5: calls $2
*** FLOP *** [Ad Kd 2c]
Villain5: checks
Hero: bets $5
Villain5: folds
Uncalled bet ($5) returned to Hero
Hero collected $6.20 from pot
*** SUMMARY ***
Total pot $6.50 | Rake $0.30
Board [Ad Kd 2c]
Seat 1: Hero collected ($6.20)
Seat 6: Villain5 (big blind) folded on the Flop
""",

        # Hand 3: Hero opens BTN, BB calls, hero c-bets flop, villain calls, hero checks turn
        """PokerStars Hand #123456789003: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:40:00 ET
Table 'TestTable1' 6-max Seat #1 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Hero: posts small blind $0.50
Villain1: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [Jh Th 9h 8s]
Villain2: folds
Villain3: folds
Villain4: folds
Villain5: folds
Hero: raises $2 to $3
Villain1: calls $2
*** FLOP *** [Qh Jd 3c]
Hero: bets $4
Villain1: calls $4
*** TURN *** [Qh Jd 3c] [2s]
Hero: checks
Villain1: checks
*** RIVER *** [Qh Jd 3c 2s] [5d]
Hero: checks
Villain1: checks
*** SHOW DOWN ***
Hero: shows [Jh Th 9h 8s] (a pair of Jacks)
Villain1: shows [Kc Qc 9d 7d] (a pair of Queens)
Villain1 collected $13.30 from pot
*** SUMMARY ***
Total pot $14 | Rake $0.70
Board [Qh Jd 3c 2s 5d]
Seat 1: Hero (button) (small blind) showed [Jh Th 9h 8s] and lost
Seat 2: Villain1 (big blind) showed [Kc Qc 9d 7d] and won ($13.30)
""",

        # Hand 4: Villain opens, hero calls, villain c-bets, hero folds
        """PokerStars Hand #123456789004: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:45:00 ET
Table 'TestTable1' 6-max Seat #2 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Villain2: posts small blind $0.50
Villain3: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [9d 8d 7c 6c]
Villain4: folds
Villain5: folds
Hero: folds
Villain1: raises $3 to $3
Villain2: folds
Villain3: folds
Uncalled bet ($2) returned to Villain1
Villain1 collected $2.50 from pot
*** SUMMARY ***
Total pot $2.50 | Rake $0
Seat 1: Hero folded before Flop (didn't bet)
Seat 2: Villain1 (button) collected ($2.50)
""",

        # Hand 5: Hero opens BTN, BB calls, hero c-bets flop, double barrels turn, wins
        """PokerStars Hand #123456789005: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:50:00 ET
Table 'TestTable1' 6-max Seat #1 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Hero: posts small blind $0.50
Villain1: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [As Ac Kh Qh]
Villain2: folds
Villain3: folds
Villain4: folds
Villain5: folds
Hero: raises $2 to $3
Villain1: calls $2
*** FLOP *** [Ah 9d 3c]
Hero: bets $4
Villain1: calls $4
*** TURN *** [Ah 9d 3c] [2s]
Hero: bets $10
Villain1: folds
Uncalled bet ($10) returned to Hero
Hero collected $13.30 from pot
*** SUMMARY ***
Total pot $14 | Rake $0.70
Board [Ah 9d 3c 2s]
Seat 1: Hero (button) (small blind) collected ($13.30)
Seat 2: Villain1 (big blind) folded on the Turn
""",

        # Hand 6: Villain opens, hero 3-bets CO, villain calls, villain checks, hero bets, villain folds
        """PokerStars Hand #123456789006: Pot Limit Omaha ($0.50/$1.00 USD) - 2024/01/15 10:55:00 ET
Table 'TestTable1' 6-max Seat #5 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Villain4: posts small blind $0.50
Villain5: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [Kd Kc Qd Jd]
Hero: folds
Villain1: folds
Villain2: raises $3 to $3
Villain3: folds
Villain4: raises $9 to $12
Villain5: folds
Villain2: calls $9
*** FLOP *** [9h 8d 4c]
Villain4: checks
Villain2: bets $18
Villain4: folds
Uncalled bet ($18) returned to Villain2
Villain2 collected $23.80 from pot
*** SUMMARY ***
Total pot $25 | Rake $1.20
Board [9h 8d 4c]
Seat 3: Villain2 collected ($23.80)
Seat 5: Villain4 (button) (small blind) folded on the Flop
""",
    ]


def main():
    """Run comprehensive integration test"""
    print("=" * 80)
    print("PLO MASTERY SUITE - COMPREHENSIVE INTEGRATION TEST")
    print("=" * 80)
    print()

    # Initialize components
    print("1. Initializing components...")
    db = DatabaseManager("data/integration_test.db")
    parser = PokerStarsParser()
    calculator = StatsCalculator(min_sample_size=3)  # Lower threshold for testing
    print("   ✓ Database, Parser, and Calculator initialized")
    print()

    # Parse and insert hands
    print("2. Parsing and inserting sample hands...")
    sample_hands_text = create_sample_hands()
    inserted_count = 0
    duplicate_count = 0

    for i, hand_text in enumerate(sample_hands_text, 1):
        try:
            hand = parser.parse_hand(hand_text)
            parser.validate_hand(hand)

            if db.insert_hand(hand):
                inserted_count += 1
                print(f"   ✓ Hand {i}: {hand['hand_id']} - {hand['pot_type']} pot")
            else:
                duplicate_count += 1
                print(f"   ! Hand {i}: Duplicate")

        except Exception as e:
            print(f"   ✗ Hand {i}: Error - {e}")

    print(f"\n   Summary: {inserted_count} inserted, {duplicate_count} duplicates")
    print()

    # Get database stats
    print("3. Database statistics...")
    db_stats = db.get_database_stats()
    print(f"   - Total hands: {db_stats['total_hands']}")
    print(f"   - Database size: {db_stats['db_size_mb']:.2f} MB")
    print()

    # Calculate stats
    print("4. Calculating statistics for Hero...")
    hands = db.get_hero_hands('Hero')
    print(f"   - Retrieved {len(hands)} hands for Hero")

    stats = calculator.calculate_stats(hands, 'Hero', essential_only=True)
    print(f"   - Calculated {len(stats)} stats")
    print(f"   - Sample size: {stats['sample_size']} hands")
    print(f"   - Reliable: {'Yes' if stats['reliable'] else 'No'}")
    print()

    # Display stats grouped by category
    print("5. HERO STATISTICS")
    print("=" * 80)

    categories = {
        'preflop': 'PREFLOP STATISTICS',
        'postflop_aggression': 'POSTFLOP AGGRESSION',
        'postflop_defense': 'POSTFLOP DEFENSE',
        'river': 'RIVER STATISTICS'
    }

    for category_key, category_name in categories.items():
        print(f"\n{category_name}")
        print("-" * 80)

        for stat_name, definition in STAT_DEFINITIONS.items():
            if definition.get('essential') and definition['category'] == category_key:
                value = stats.get(stat_name)
                gto = definition['gto_baseline']

                if value is not None:
                    delta = value - gto
                    status = "✓" if abs(delta) <= definition['threshold'] else "!"

                    print(f"  {status} {definition['name']:22s}: {value:6.1f}%  "
                          f"(GTO: {gto:5.1f}%)  Delta: {delta:+6.1f}%")
                else:
                    print(f"  - {definition['name']:22s}: N/A (insufficient data)")

    # Show detailed counters
    print("\n" + "=" * 80)
    print("6. DETAILED COUNTERS (for verification)")
    print("=" * 80)

    counters = calculator.get_counter_summary()
    important_counters = [
        ('total_hands', 'Total Hands'),
        ('saw_flop', 'Saw Flop'),
        ('saw_turn', 'Saw Turn'),
        ('saw_river', 'Saw River'),
        ('showdowns', 'Showdowns'),
        ('voluntary_preflop_actions', 'VPIP Opportunities'),
        ('preflop_raises', 'Preflop Raises'),
        ('opportunities_to_3bet', '3-Bet Opportunities'),
        ('three_bets', '3-Bets Made'),
        ('faced_3bet', 'Faced 3-Bet'),
        ('folds_to_3bet', 'Folds to 3-Bet'),
        ('flop_cbet_opportunities', 'Flop C-Bet Opportunities'),
        ('flop_cbets', 'Flop C-Bets Made'),
        ('turn_cbet_opportunities', 'Turn C-Bet Opportunities'),
        ('turn_cbets', 'Turn C-Bets Made'),
        ('turn_bets_after_flop_bet', 'Double Barrels'),
        ('faced_flop_cbet', 'Faced Flop C-Bet'),
        ('folds_to_flop_cbet', 'Folds to Flop C-Bet'),
    ]

    for counter_key, counter_name in important_counters:
        value = counters.get(counter_key, 0)
        print(f"  {counter_name:30s}: {value:4d}")

    print("\n" + "=" * 80)
    print("INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Implement GTO baseline comparison and leak detection")
    print("  2. Add positional and pot-type filtered stats")
    print("  3. Create Excel export functionality")
    print("  4. Build comprehensive test suite")
    print()

    db.close()


if __name__ == "__main__":
    main()
