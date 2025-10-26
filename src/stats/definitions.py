"""
Stat definitions and metadata for all PLO statistics
Defines formulas, descriptions, and GTO baselines for 88+ stats
"""

from typing import Dict, Any, List

# Stat categories for organization
STAT_CATEGORIES = {
    'preflop': 'Preflop Statistics',
    'postflop_aggression': 'Postflop Aggression',
    'postflop_defense': 'Postflop Defense',
    'river': 'River Statistics',
    'positional': 'Positional Statistics',
    'pot_type': 'Pot Type Statistics',
    'advanced': 'Advanced Statistics'
}

# Complete stat definitions
# Each stat has: name, description, formula, category, gto_baseline, format
STAT_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    # ==========================================
    # PREFLOP STATS (8 essential)
    # ==========================================
    'vpip': {
        'name': 'VPIP',
        'full_name': 'Voluntarily Put money In Pot',
        'description': 'Percentage of hands where player voluntarily puts money in pot preflop',
        'formula': '(voluntary_preflop_actions / total_hands) * 100',
        'category': 'preflop',
        'gto_baseline': 25.0,
        'threshold': 3.0,
        'format': 'percentage',
        'essential': True
    },
    'pfr': {
        'name': 'PFR',
        'full_name': 'Preflop Raise',
        'description': 'Percentage of hands where player raises preflop',
        'formula': '(preflop_raises / total_hands) * 100',
        'category': 'preflop',
        'gto_baseline': 20.0,
        'threshold': 3.0,
        'format': 'percentage',
        'essential': True
    },
    'three_bet': {
        'name': '3-Bet',
        'full_name': '3-Bet Percentage',
        'description': 'Percentage of times player 3-bets when facing a raise',
        'formula': '(three_bets / opportunities_to_3bet) * 100',
        'category': 'preflop',
        'gto_baseline': 8.0,
        'threshold': 2.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_3bet': {
        'name': 'Fold vs 3-Bet',
        'full_name': 'Fold vs 3-Bet',
        'description': 'Percentage of times player folds to a 3-bet after raising',
        'formula': '(folds_to_3bet / faced_3bet) * 100',
        'category': 'preflop',
        'gto_baseline': 55.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_3bet_ip': {
        'name': 'Fold vs 3-Bet IP',
        'full_name': 'Fold vs 3-Bet In Position',
        'description': 'Fold vs 3-bet when in position',
        'formula': '(folds_to_3bet_ip / faced_3bet_ip) * 100',
        'category': 'preflop',
        'gto_baseline': 52.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_3bet_oop': {
        'name': 'Fold vs 3-Bet OOP',
        'full_name': 'Fold vs 3-Bet Out of Position',
        'description': 'Fold vs 3-bet when out of position',
        'formula': '(folds_to_3bet_oop / faced_3bet_oop) * 100',
        'category': 'preflop',
        'gto_baseline': 58.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'four_bet': {
        'name': '4-Bet',
        'full_name': '4-Bet Percentage',
        'description': 'Percentage of times player 4-bets when facing a 3-bet',
        'formula': '(four_bets / opportunities_to_4bet) * 100',
        'category': 'preflop',
        'gto_baseline': 12.0,
        'threshold': 3.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_4bet': {
        'name': 'Fold vs 4-Bet',
        'full_name': 'Fold vs 4-Bet',
        'description': 'Percentage of times player folds to a 4-bet',
        'formula': '(folds_to_4bet / faced_4bet) * 100',
        'category': 'preflop',
        'gto_baseline': 65.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },

    # ==========================================
    # POSTFLOP AGGRESSION (6 essential)
    # ==========================================
    'cbet_freq': {
        'name': 'C-Bet',
        'full_name': 'Continuation Bet Frequency',
        'description': 'Overall continuation bet frequency across all streets',
        'formula': '(cbets / cbet_opportunities) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 55.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'cbet_freq_flop': {
        'name': 'C-Bet Flop',
        'full_name': 'Flop C-Bet Frequency',
        'description': 'Continuation bet frequency on the flop',
        'formula': '(flop_cbets / flop_cbet_opportunities) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 60.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'cbet_freq_turn': {
        'name': 'C-Bet Turn',
        'full_name': 'Turn C-Bet Frequency',
        'description': 'Continuation bet frequency on the turn',
        'formula': '(turn_cbets / turn_cbet_opportunities) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 45.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'cbet_freq_river': {
        'name': 'C-Bet River',
        'full_name': 'River C-Bet Frequency',
        'description': 'Continuation bet frequency on the river',
        'formula': '(river_cbets / river_cbet_opportunities) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 40.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'double_barrel': {
        'name': 'Double Barrel',
        'full_name': 'Double Barrel Frequency',
        'description': 'Frequency of betting flop and turn consecutively',
        'formula': '(turn_bets_after_flop_bet / flop_cbets) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 50.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'triple_barrel': {
        'name': 'Triple Barrel',
        'full_name': 'Triple Barrel Frequency',
        'description': 'Frequency of betting all three streets',
        'formula': '(river_bets_after_turn_bet / turn_bets_after_flop_bet) * 100',
        'category': 'postflop_aggression',
        'gto_baseline': 45.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },

    # ==========================================
    # POSTFLOP DEFENSE (4 essential)
    # ==========================================
    'fold_vs_cbet': {
        'name': 'Fold vs C-Bet',
        'full_name': 'Fold vs Continuation Bet',
        'description': 'Overall fold frequency when facing a c-bet',
        'formula': '(folds_to_cbet / faced_cbet) * 100',
        'category': 'postflop_defense',
        'gto_baseline': 45.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_cbet_flop': {
        'name': 'Fold vs C-Bet Flop',
        'full_name': 'Fold vs Flop C-Bet',
        'description': 'Fold frequency vs flop c-bet',
        'formula': '(folds_to_flop_cbet / faced_flop_cbet) * 100',
        'category': 'postflop_defense',
        'gto_baseline': 42.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_cbet_turn': {
        'name': 'Fold vs C-Bet Turn',
        'full_name': 'Fold vs Turn C-Bet',
        'description': 'Fold frequency vs turn c-bet',
        'formula': '(folds_to_turn_cbet / faced_turn_cbet) * 100',
        'category': 'postflop_defense',
        'gto_baseline': 48.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
    'fold_vs_cbet_river': {
        'name': 'Fold vs C-Bet River',
        'full_name': 'Fold vs River C-Bet',
        'description': 'Fold frequency vs river c-bet',
        'formula': '(folds_to_river_cbet / faced_river_cbet) * 100',
        'category': 'postflop_defense',
        'gto_baseline': 52.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },

    # ==========================================
    # RIVER STATS (2 essential)
    # ==========================================
    'wtsd': {
        'name': 'WTSD',
        'full_name': 'Went to Showdown',
        'description': 'Percentage of hands that went to showdown',
        'formula': '(showdowns / saw_flop) * 100',
        'category': 'river',
        'gto_baseline': 25.0,
        'threshold': 3.0,
        'format': 'percentage',
        'essential': True
    },
    'w_sd': {
        'name': 'W$SD',
        'full_name': 'Won money at Showdown',
        'description': 'Percentage of showdowns won',
        'formula': '(showdowns_won / showdowns) * 100',
        'category': 'river',
        'gto_baseline': 50.0,
        'threshold': 5.0,
        'format': 'percentage',
        'essential': True
    },
}


def get_essential_stats() -> List[str]:
    """Get list of 20 essential stats for Sprint 2"""
    return [name for name, definition in STAT_DEFINITIONS.items()
            if definition.get('essential', False)]


def get_stats_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """Get all stats for a specific category"""
    return {name: definition for name, definition in STAT_DEFINITIONS.items()
            if definition['category'] == category}


def get_stat_definition(stat_name: str) -> Dict[str, Any]:
    """Get definition for a specific stat"""
    return STAT_DEFINITIONS.get(stat_name, {})
