"""
Database Manager for PLO Mastery Suite
Handles all database operations with transactions and error handling
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path
import logging

from .schema import create_tables, verify_schema, SCHEMA_VERSION

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages all database operations for the PLO Mastery Suite
    """

    def __init__(self, db_path: str = "data/plo_mastery.db"):
        """
        Initialize database manager

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize database connection and create tables if needed"""
        self.conn = sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.conn.row_factory = sqlite3.Row  # Enable column access by name

        # Create tables if they don't exist
        if not verify_schema(self.conn):
            logger.info("Creating database schema...")
            create_tables(self.conn)
            logger.info(f"Database schema v{SCHEMA_VERSION} created successfully")

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    # =====================================
    # HAND OPERATIONS
    # =====================================

    def insert_hand(self, hand_data: Dict[str, Any]) -> bool:
        """
        Insert a single hand into the database

        Args:
            hand_data: Dictionary containing hand information

        Returns:
            True if inserted successfully, False if duplicate or error
        """
        try:
            # Convert lists/dicts to JSON strings
            hand_data_copy = hand_data.copy()
            if 'hero_cards' in hand_data_copy and isinstance(hand_data_copy['hero_cards'], list):
                hand_data_copy['hero_cards'] = json.dumps(hand_data_copy['hero_cards'])
            if 'board_flop' in hand_data_copy and isinstance(hand_data_copy['board_flop'], list):
                hand_data_copy['board_flop'] = json.dumps(hand_data_copy['board_flop'])
            if 'players' in hand_data_copy and isinstance(hand_data_copy['players'], list):
                hand_data_copy['players'] = json.dumps(hand_data_copy['players'])
            if 'actions' in hand_data_copy and isinstance(hand_data_copy['actions'], dict):
                hand_data_copy['actions'] = json.dumps(hand_data_copy['actions'])
            if 'winner' in hand_data_copy and isinstance(hand_data_copy['winner'], list):
                hand_data_copy['winner'] = json.dumps(hand_data_copy['winner'])

            columns = ', '.join(hand_data_copy.keys())
            placeholders = ', '.join('?' * len(hand_data_copy))
            sql = f"INSERT INTO hands ({columns}) VALUES ({placeholders})"

            cursor = self.conn.cursor()
            cursor.execute(sql, list(hand_data_copy.values()))
            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            # Duplicate hand_id
            logger.debug(f"Hand {hand_data.get('hand_id')} already exists")
            return False
        except Exception as e:
            logger.error(f"Error inserting hand: {e}")
            self.conn.rollback()
            return False

    def insert_hands_batch(self, hands: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        Insert multiple hands in a batch

        Args:
            hands: List of hand dictionaries

        Returns:
            Tuple of (successful_inserts, duplicates)
        """
        successful = 0
        duplicates = 0

        for hand in hands:
            if self.insert_hand(hand):
                successful += 1
            else:
                duplicates += 1

        return successful, duplicates

    def get_hand(self, hand_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single hand by ID

        Args:
            hand_id: Hand identifier

        Returns:
            Hand data dictionary or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hands WHERE hand_id = ?", (hand_id,))
        row = cursor.fetchone()

        if row:
            hand = dict(row)
            # Parse JSON fields
            if hand.get('hero_cards'):
                hand['hero_cards'] = json.loads(hand['hero_cards'])
            if hand.get('board_flop'):
                hand['board_flop'] = json.loads(hand['board_flop'])
            if hand.get('players'):
                hand['players'] = json.loads(hand['players'])
            if hand.get('actions'):
                hand['actions'] = json.loads(hand['actions'])
            if hand.get('winner'):
                try:
                    hand['winner'] = json.loads(hand['winner'])
                except:
                    pass  # Keep as string if not JSON
            return hand
        return None

    def get_hero_hands(self, hero_name: str, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Get all hands for a specific hero with optional filters

        Args:
            hero_name: Hero player name
            filters: Optional filters (stakes, date_range, position, etc.)

        Returns:
            List of hand dictionaries
        """
        query = "SELECT * FROM hands WHERE hero_name = ?"
        params = [hero_name]

        if filters:
            if 'start_date' in filters:
                query += " AND timestamp >= ?"
                params.append(filters['start_date'])
            if 'end_date' in filters:
                query += " AND timestamp <= ?"
                params.append(filters['end_date'])
            if 'position' in filters:
                query += " AND hero_position = ?"
                params.append(filters['position'])
            if 'pot_type' in filters:
                query += " AND pot_type = ?"
                params.append(filters['pot_type'])
            if 'stakes_bb' in filters:
                query += " AND stakes_bb = ?"
                params.append(filters['stakes_bb'])

        query += " ORDER BY timestamp DESC"

        cursor = self.conn.cursor()
        cursor.execute(query, params)

        hands = []
        for row in cursor.fetchall():
            hand = dict(row)
            # Parse JSON fields
            if hand.get('hero_cards'):
                hand['hero_cards'] = json.loads(hand['hero_cards'])
            if hand.get('actions'):
                hand['actions'] = json.loads(hand['actions'])
            hands.append(hand)

        return hands

    def count_hands(self, filters: Optional[Dict] = None) -> int:
        """
        Count total hands with optional filters

        Args:
            filters: Optional filters

        Returns:
            Count of hands
        """
        query = "SELECT COUNT(*) FROM hands"
        params = []

        if filters:
            where_clauses = []
            if 'hero_name' in filters:
                where_clauses.append("hero_name = ?")
                params.append(filters['hero_name'])
            if 'site' in filters:
                where_clauses.append("site = ?")
                params.append(filters['site'])
            if 'pot_type' in filters:
                where_clauses.append("pot_type = ?")
                params.append(filters['pot_type'])

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()[0]

    # =====================================
    # PLAYER/VILLAIN OPERATIONS
    # =====================================

    def get_or_create_player(self, player_name: str, site: str) -> int:
        """
        Get player ID or create new player

        Args:
            player_name: Player name
            site: Poker site

        Returns:
            Player ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT player_id FROM players WHERE player_name = ? AND site = ?",
            (player_name, site)
        )
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            # Create new player
            cursor.execute(
                """INSERT INTO players (player_name, site, first_seen, last_seen)
                   VALUES (?, ?, ?, ?)""",
                (player_name, site, datetime.now(), datetime.now())
            )
            self.conn.commit()
            return cursor.lastrowid

    def update_player_stats(self, player_id: int, stats: Dict[str, float]) -> None:
        """
        Update player statistics

        Args:
            player_id: Player ID
            stats: Dictionary of stat_name: value
        """
        if not stats:
            return

        set_clauses = [f"{key} = ?" for key in stats.keys()]
        values = list(stats.values()) + [player_id]

        sql = f"""
            UPDATE players
            SET {', '.join(set_clauses)}, last_seen = ?
            WHERE player_id = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(sql, values + [datetime.now(), player_id])
        self.conn.commit()

    def get_player(self, player_name: str, site: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get player information

        Args:
            player_name: Player name
            site: Optional site filter

        Returns:
            Player data dictionary or None
        """
        cursor = self.conn.cursor()
        if site:
            cursor.execute(
                "SELECT * FROM players WHERE player_name = ? AND site = ?",
                (player_name, site)
            )
        else:
            cursor.execute(
                "SELECT * FROM players WHERE player_name = ?",
                (player_name,)
            )

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_villains(self, min_hands: int = 50) -> List[Dict[str, Any]]:
        """
        Get all villains with minimum hand count

        Args:
            min_hands: Minimum number of hands

        Returns:
            List of villain dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM players
               WHERE total_hands >= ?
               ORDER BY total_hands DESC""",
            (min_hands,)
        )

        return [dict(row) for row in cursor.fetchall()]

    # =====================================
    # LEAK TRACKING
    # =====================================

    def insert_leak(self, leak_data: Dict[str, Any]) -> int:
        """
        Insert a detected leak

        Args:
            leak_data: Leak information

        Returns:
            Leak ID
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO hero_leaks
               (hero_name, detected_date, stat_name, hero_value, gto_value,
                delta, frequency, ev_loss_bb100, severity, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                leak_data['hero_name'],
                leak_data.get('detected_date', datetime.now().date()),
                leak_data['stat_name'],
                leak_data['hero_value'],
                leak_data['gto_value'],
                leak_data['delta'],
                leak_data['frequency'],
                leak_data['ev_loss_bb100'],
                leak_data['severity'],
                leak_data.get('status', 'active')
            )
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_active_leaks(self, hero_name: str) -> List[Dict[str, Any]]:
        """
        Get active leaks for hero

        Args:
            hero_name: Hero name

        Returns:
            List of leak dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM hero_leaks
               WHERE hero_name = ? AND status = 'active'
               ORDER BY ev_loss_bb100 DESC""",
            (hero_name,)
        )

        return [dict(row) for row in cursor.fetchall()]

    # =====================================
    # GTO BASELINES
    # =====================================

    def load_gto_baselines(self, baselines: List[Dict[str, Any]]) -> None:
        """
        Load GTO baseline data into database

        Args:
            baselines: List of baseline dictionaries
        """
        cursor = self.conn.cursor()
        for baseline in baselines:
            cursor.execute(
                """INSERT OR REPLACE INTO gto_baselines
                   (stat_name, stakes, gto_value, threshold, ev_loss_coefficient, description, category)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    baseline['stat_name'],
                    baseline['stakes'],
                    baseline['gto_value'],
                    baseline.get('threshold', 2.0),
                    baseline.get('ev_loss_coefficient', 0.15),
                    baseline.get('description', ''),
                    baseline.get('category', '')
                )
            )
        self.conn.commit()

    def get_gto_baseline(self, stat_name: str, stakes: str = 'PLO100') -> Optional[Dict[str, Any]]:
        """
        Get GTO baseline for a stat

        Args:
            stat_name: Stat name
            stakes: Stakes level

        Returns:
            Baseline dictionary or None
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM gto_baselines WHERE stat_name = ? AND stakes = ?",
            (stat_name, stakes)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    # =====================================
    # UTILITIES
    # =====================================

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a custom SQL query

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            List of result dictionaries
        """
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return [dict(row) for row in cursor.fetchall()]

    def vacuum(self) -> None:
        """Optimize database"""
        self.conn.execute("VACUUM")

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with database stats
        """
        cursor = self.conn.cursor()

        stats = {}

        # Total hands
        cursor.execute("SELECT COUNT(*) FROM hands")
        stats['total_hands'] = cursor.fetchone()[0]

        # Total players
        cursor.execute("SELECT COUNT(*) FROM players")
        stats['total_players'] = cursor.fetchone()[0]

        # Database size
        stats['db_size_mb'] = self.db_path.stat().st_size / (1024 * 1024)

        # Date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM hands")
        row = cursor.fetchone()
        stats['earliest_hand'] = row[0]
        stats['latest_hand'] = row[1]

        return stats
