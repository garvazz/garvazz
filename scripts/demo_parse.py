#!/usr/bin/env python3
"""
Demo script to test hand history parsing and database operations
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.parsers import PokerStarsParser

def create_sample_hand():
    """Create a sample PokerStars hand for testing"""
    return """PokerStars Hand #123456789: Pot Limit Omaha ($0.50/$1.00 USD)
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Hero ($100 in chips)
Seat 2: Villain1 ($100 in chips)
Seat 3: Villain2 ($100 in chips)
Seat 4: Villain3 ($100 in chips)
Seat 5: Villain4 ($100 in chips)
Seat 6: Villain5 ($100 in chips)
Hero: posts small blind $0.50
Villain1: posts big blind $1
*** HOLE CARDS ***
Dealt to Hero [As Kh Qc Jd]
Villain2: folds
Villain3: raises $3 to $3
Villain4: folds
Villain5: folds
Hero: raises $9 to $12
Villain1: folds
Villain3: calls $9
*** FLOP *** [Ah Kd 2c]
Hero: bets $15
Villain3: folds
Uncalled bet ($15) returned to Hero
Hero collected $24.50 from pot
*** SUMMARY ***
Total pot $25.50 | Rake $1
Board [Ah Kd 2c]
Seat 1: Hero (button) (small blind) collected ($24.50)
Seat 2: Villain1 (big blind) folded before Flop
Seat 3: Villain2 folded before Flop (didn't bet)
Seat 4: Villain3 folded on the Flop
Seat 5: Villain4 folded before Flop (didn't bet)
Seat 6: Villain5 folded before Flop (didn't bet)
"""

def main():
    """Main demo function"""
    print("=" * 70)
    print("PLO MASTERY SUITE - Demo Script")
    print("=" * 70)
    print()

    # Initialize components
    print("1. Initializing database...")
    db = DatabaseManager("data/demo.db")
    print(f"   ✓ Database initialized: {db.db_path}")
    print()

    # Initialize parser
    print("2. Initializing PokerStars parser...")
    parser = PokerStarsParser()
    print(f"   ✓ Parser initialized: {parser.site_name}")
    print()

    # Parse sample hand
    print("3. Parsing sample hand...")
    sample_hand_text = create_sample_hand()
    try:
        hand = parser.parse_hand(sample_hand_text)
        print(f"   ✓ Hand parsed successfully!")
        print(f"   - Hand ID: {hand['hand_id']}")
        print(f"   - Game: {hand['game_type']}")
        print(f"   - Stakes: ${hand['stakes_sb']}/${hand['stakes_bb']}")
        print(f"   - Players: {len(hand['players'])}")
        print(f"   - Hero: {hand['hero_name']} at {hand['hero_position']}")
        print(f"   - Pot Type: {hand['pot_type']}")
        print()
    except Exception as e:
        print(f"   ✗ Error parsing hand: {e}")
        return

    # Insert into database
    print("4. Inserting hand into database...")
    try:
        success = db.insert_hand(hand)
        if success:
            print(f"   ✓ Hand inserted successfully!")
        else:
            print(f"   ! Hand already exists (duplicate)")
        print()
    except Exception as e:
        print(f"   ✗ Error inserting hand: {e}")
        return

    # Query database
    print("5. Querying database...")
    stats = db.get_database_stats()
    print(f"   ✓ Database stats:")
    print(f"   - Total hands: {stats['total_hands']}")
    print(f"   - Total players: {stats['total_players']}")
    print(f"   - Database size: {stats['db_size_mb']:.2f} MB")
    print()

    # Retrieve hand
    print("6. Retrieving hand from database...")
    retrieved_hand = db.get_hand(hand['hand_id'])
    if retrieved_hand:
        print(f"   ✓ Hand retrieved successfully!")
        hero_result_bb = retrieved_hand.get('hero_result_bb')
        if hero_result_bb is not None:
            print(f"   - Hero result: {hero_result_bb:.2f} BB")
        else:
            print(f"   - Hero result: N/A")
    print()

    print("=" * 70)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Implement stats calculation engine")
    print("  2. Build leak detection algorithm")
    print("  3. Create Excel export functionality")
    print()

    db.close()

if __name__ == "__main__":
    main()
