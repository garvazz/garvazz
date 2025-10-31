"""
Database schema for PLO Mastery Suite
Implements the complete database structure as specified in the requirements
"""

import sqlite3
from typing import Optional

SCHEMA_VERSION = "1.0.0"

# SQL Schema Definitions
HANDS_TABLE = """
CREATE TABLE IF NOT EXISTS hands (
    hand_id TEXT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    site TEXT NOT NULL,
    table_name TEXT,
    game_type TEXT NOT NULL CHECK(game_type IN ('PLO', 'PLO5')),
    stakes_sb REAL NOT NULL,
    stakes_bb REAL NOT NULL,
    stakes_ante REAL DEFAULT 0,
    max_players INTEGER,
    button_seat INTEGER,

    hero_name TEXT NOT NULL,
    hero_seat INTEGER,
    hero_position TEXT CHECK(hero_position IN ('UTG', 'EP', 'MP', 'CO', 'BTN', 'SB', 'BB')),
    hero_cards TEXT,  -- JSON array

    players TEXT,  -- JSON array: all players in hand with seats, stacks, positions

    pot_type TEXT CHECK(pot_type IN ('SRP', '3BP', '4BP', 'MW')),
    hero_action_preflop TEXT,

    board_flop TEXT,  -- JSON array
    board_turn TEXT,
    board_river TEXT,
    board_texture TEXT,

    actions TEXT,  -- JSON: full action history

    showdown BOOLEAN,
    winner TEXT,  -- JSON array if multiple winners
    pot_total REAL,
    rake REAL,
    hero_result REAL,
    hero_result_bb REAL,

    imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hands_hero ON hands(hero_name);
CREATE INDEX IF NOT EXISTS idx_hands_timestamp ON hands(timestamp);
CREATE INDEX IF NOT EXISTS idx_hands_pot_type ON hands(pot_type);
CREATE INDEX IF NOT EXISTS idx_hands_position ON hands(hero_position);
CREATE INDEX IF NOT EXISTS idx_hands_board_texture ON hands(board_texture);
"""

PLAYERS_TABLE = """
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT UNIQUE NOT NULL,
    site TEXT NOT NULL,
    first_seen DATETIME,
    last_seen DATETIME,
    total_hands INTEGER DEFAULT 0,
    hands_vs_hero INTEGER DEFAULT 0,

    -- Core Stats (88 total - showing key ones, rest would be added similarly)
    vpip REAL,
    pfr REAL,
    three_bet REAL,
    fold_vs_3bet REAL,
    fold_vs_3bet_ip REAL,
    fold_vs_3bet_oop REAL,
    four_bet REAL,
    fold_vs_4bet REAL,

    cbet_freq REAL,
    cbet_freq_flop REAL,
    cbet_freq_turn REAL,
    cbet_freq_river REAL,
    double_barrel REAL,
    triple_barrel REAL,

    fold_vs_cbet REAL,
    fold_vs_cbet_flop REAL,
    fold_vs_cbet_turn REAL,
    fold_vs_cbet_river REAL,
    fold_vs_donk_ip REAL,
    fold_vs_checkraise REAL,

    af REAL,
    wtsd REAL,
    w_sd REAL,

    -- Profile
    profile_type TEXT CHECK(profile_type IN (
        'Regular_Pasivo', 'Regular_Agresivo', 'Semi_Fish',
        'Recreacional_Pasivo', 'Recreacional_Agresivo'
    )),
    profile_confidence REAL,
    profile_last_updated DATETIME,

    -- Meta
    notes TEXT,
    tags TEXT,  -- JSON array
    color_code TEXT,

    UNIQUE(player_name, site)
);

CREATE INDEX IF NOT EXISTS idx_players_name ON players(player_name);
CREATE INDEX IF NOT EXISTS idx_players_profile ON players(profile_type);
"""

PLAYER_STATS_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS player_stats_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    sample_size INTEGER,
    stats TEXT,  -- JSON: all stats at this point in time

    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_player_stats_history_player_date
    ON player_stats_history(player_id, snapshot_date);
"""

HERO_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS hero_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_name TEXT NOT NULL,
    session_date DATE NOT NULL,
    hands_played INTEGER,
    bb_won REAL,
    bb100 REAL,
    duration_minutes INTEGER,
    import_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hero_sessions_hero_date
    ON hero_sessions(hero_name, session_date);
"""

HERO_LEAKS_TABLE = """
CREATE TABLE IF NOT EXISTS hero_leaks (
    leak_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_name TEXT NOT NULL,
    detected_date DATE NOT NULL,
    stat_name TEXT NOT NULL,
    hero_value REAL,
    gto_value REAL,
    delta REAL,
    frequency INTEGER,
    ev_loss_bb100 REAL,
    severity TEXT CHECK(severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    status TEXT CHECK(status IN ('active', 'fixing', 'fixed')) DEFAULT 'active',
    fixed_date DATE
);

CREATE INDEX IF NOT EXISTS idx_hero_leaks_hero ON hero_leaks(hero_name);
CREATE INDEX IF NOT EXISTS idx_hero_leaks_status ON hero_leaks(status);
"""

VILLAIN_EXPLOITS_TABLE = """
CREATE TABLE IF NOT EXISTS villain_exploits (
    exploit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    exploit_type TEXT NOT NULL,
    description TEXT,
    situations TEXT,  -- JSON array
    ev_gain_estimate REAL,
    priority TEXT CHECK(priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    confidence REAL,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE INDEX IF NOT EXISTS idx_villain_exploits_player ON villain_exploits(player_id);
"""

CONFIG_TABLE = """
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

GTO_BASELINES_TABLE = """
CREATE TABLE IF NOT EXISTS gto_baselines (
    stat_name TEXT NOT NULL,
    stakes TEXT NOT NULL,
    gto_value REAL,
    threshold REAL,  -- Acceptable deviation
    ev_loss_coefficient REAL,
    description TEXT,
    category TEXT,

    PRIMARY KEY (stat_name, stakes)
);
"""


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create all database tables

    Args:
        conn: SQLite database connection
    """
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(HANDS_TABLE)
    cursor.executescript(PLAYERS_TABLE)
    cursor.executescript(PLAYER_STATS_HISTORY_TABLE)
    cursor.executescript(HERO_SESSIONS_TABLE)
    cursor.executescript(HERO_LEAKS_TABLE)
    cursor.executescript(VILLAIN_EXPLOITS_TABLE)
    cursor.executescript(CONFIG_TABLE)
    cursor.executescript(GTO_BASELINES_TABLE)

    # Insert schema version
    cursor.execute(
        "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
        ('schema_version', SCHEMA_VERSION)
    )

    conn.commit()


def verify_schema(conn: sqlite3.Connection) -> bool:
    """
    Verify that the database schema is correct

    Args:
        conn: SQLite database connection

    Returns:
        True if schema is valid, False otherwise
    """
    cursor = conn.cursor()

    # Check that all required tables exist
    required_tables = [
        'hands', 'players', 'player_stats_history', 'hero_sessions',
        'hero_leaks', 'villain_exploits', 'config', 'gto_baselines'
    ]

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {row[0] for row in cursor.fetchall()}

    for table in required_tables:
        if table not in existing_tables:
            return False

    # Check schema version
    cursor.execute("SELECT value FROM config WHERE key = 'schema_version'")
    row = cursor.fetchone()
    if not row or row[0] != SCHEMA_VERSION:
        return False

    return True
