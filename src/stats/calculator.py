"""
Stats Calculator for PLO Mastery Suite
Calculates all 88 stats from hand history data
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import logging

from .definitions import STAT_DEFINITIONS, get_essential_stats

logger = logging.getLogger(__name__)


class StatsCalculator:
    """
    Calculates poker statistics from hand histories
    """

    def __init__(self, min_sample_size: int = 50):
        """
        Initialize stats calculator

        Args:
            min_sample_size: Minimum hands required for reliable stats
        """
        self.min_sample_size = min_sample_size
        self.counters = self._initialize_counters()

    def _initialize_counters(self) -> Dict[str, int]:
        """Initialize all stat counters to zero"""
        counters = defaultdict(int)

        # Core counters
        counters['total_hands'] = 0
        counters['saw_flop'] = 0
        counters['saw_turn'] = 0
        counters['saw_river'] = 0
        counters['showdowns'] = 0
        counters['showdowns_won'] = 0

        # Preflop counters
        counters['voluntary_preflop_actions'] = 0
        counters['preflop_raises'] = 0
        counters['opportunities_to_3bet'] = 0
        counters['three_bets'] = 0
        counters['faced_3bet'] = 0
        counters['folds_to_3bet'] = 0
        counters['faced_3bet_ip'] = 0
        counters['folds_to_3bet_ip'] = 0
        counters['faced_3bet_oop'] = 0
        counters['folds_to_3bet_oop'] = 0
        counters['opportunities_to_4bet'] = 0
        counters['four_bets'] = 0
        counters['faced_4bet'] = 0
        counters['folds_to_4bet'] = 0

        # C-bet counters
        counters['cbet_opportunities'] = 0
        counters['cbets'] = 0
        counters['flop_cbet_opportunities'] = 0
        counters['flop_cbets'] = 0
        counters['turn_cbet_opportunities'] = 0
        counters['turn_cbets'] = 0
        counters['river_cbet_opportunities'] = 0
        counters['river_cbets'] = 0
        counters['turn_bets_after_flop_bet'] = 0
        counters['river_bets_after_turn_bet'] = 0

        # Defense counters
        counters['faced_cbet'] = 0
        counters['folds_to_cbet'] = 0
        counters['faced_flop_cbet'] = 0
        counters['folds_to_flop_cbet'] = 0
        counters['faced_turn_cbet'] = 0
        counters['folds_to_turn_cbet'] = 0
        counters['faced_river_cbet'] = 0
        counters['folds_to_river_cbet'] = 0

        return counters

    def calculate_stats(self, hands: List[Dict[str, Any]],
                       player_name: str,
                       essential_only: bool = False) -> Dict[str, Optional[float]]:
        """
        Calculate statistics for a player from a list of hands

        Args:
            hands: List of parsed hand dictionaries
            player_name: Name of player to calculate stats for
            essential_only: If True, only calculate 20 essential stats

        Returns:
            Dictionary of stat_name: value (or None if insufficient data)
        """
        # Reset counters
        self.counters = self._initialize_counters()

        # Process all hands
        for hand in hands:
            self._process_hand(hand, player_name)

        # Calculate final stats
        stats = self._calculate_final_stats(essential_only)

        # Add sample size and reliability
        stats['sample_size'] = self.counters['total_hands']
        stats['reliable'] = self.counters['total_hands'] >= self.min_sample_size

        return stats

    def _process_hand(self, hand: Dict[str, Any], player_name: str) -> None:
        """
        Process a single hand and update counters

        Args:
            hand: Parsed hand dictionary
            player_name: Player to track
        """
        self.counters['total_hands'] += 1

        actions = hand.get('actions', {})
        hero_name = hand.get('hero_name')
        hero_position = hand.get('hero_position')

        # Only process hands where we're tracking this player
        if hero_name != player_name:
            return

        # Determine which streets were seen
        has_flop = 'flop' in actions
        has_turn = 'turn' in actions
        has_river = 'river' in actions
        has_showdown = hand.get('showdown', False)

        if has_flop:
            self.counters['saw_flop'] += 1
        if has_turn:
            self.counters['saw_turn'] += 1
        if has_river:
            self.counters['saw_river'] += 1
        if has_showdown:
            self.counters['showdowns'] += 1
            # Check if hero won
            winners = hand.get('winner')
            if winners is not None:
                if isinstance(winners, str):
                    winners = [winners]
                if hero_name in winners:
                    self.counters['showdowns_won'] += 1

        # Process preflop actions
        self._process_preflop(actions.get('preflop', []), player_name, hero_position)

        # Process postflop actions
        if has_flop:
            self._process_postflop_street('flop', actions.get('flop', {}),
                                         actions.get('preflop', []), player_name)
        if has_turn:
            self._process_postflop_street('turn', actions.get('turn', {}),
                                         actions.get('flop', {}).get('actions', []), player_name)
        if has_river:
            self._process_postflop_street('river', actions.get('river', {}),
                                         actions.get('turn', {}).get('actions', []), player_name)

    def _process_preflop(self, preflop_actions: List[Dict[str, Any]],
                        player_name: str, position: str) -> None:
        """Process preflop actions for a player"""
        if not preflop_actions:
            return

        player_actions = [a for a in preflop_actions if a.get('player') == player_name]
        all_raises = [a for a in preflop_actions if a.get('action') == 'raise']

        # VPIP: Voluntary action (not blind)
        voluntary_actions = [a for a in player_actions
                           if a.get('action') not in ['blind', 'fold']]
        if voluntary_actions:
            self.counters['voluntary_preflop_actions'] += 1

        # PFR: Preflop raise
        player_raises = [a for a in player_actions if a.get('action') == 'raise']
        if player_raises:
            self.counters['preflop_raises'] += 1

        # 3-bet logic
        # Player faces a raise and can 3-bet
        if len(all_raises) >= 1:
            # Check if player acted after first raise
            first_raise_idx = next(i for i, a in enumerate(preflop_actions)
                                  if a.get('action') == 'raise')
            player_actions_after_raise = [a for a in player_actions
                                         if preflop_actions.index(a) > first_raise_idx]

            if player_actions_after_raise:
                self.counters['opportunities_to_3bet'] += 1

                # Did player 3-bet?
                if len(player_raises) > 0 and len(all_raises) >= 2:
                    # Check if player's raise was the second raise
                    if player_raises[0] == all_raises[1]:
                        self.counters['three_bets'] += 1

        # Fold vs 3-bet
        # Player raised, then faced a 3-bet
        if len(player_raises) > 0 and len(all_raises) >= 2:
            # If player's raise was first and there was another raise
            if player_raises[0] == all_raises[0]:
                self.counters['faced_3bet'] += 1

                # Determine if IP or OOP (simplified: BTN/CO = IP, others = OOP)
                is_ip = position in ['BTN', 'CO']
                if is_ip:
                    self.counters['faced_3bet_ip'] += 1
                else:
                    self.counters['faced_3bet_oop'] += 1

                # Did player fold?
                fold_actions = [a for a in player_actions if a.get('action') == 'fold']
                if fold_actions:
                    self.counters['folds_to_3bet'] += 1
                    if is_ip:
                        self.counters['folds_to_3bet_ip'] += 1
                    else:
                        self.counters['folds_to_3bet_oop'] += 1

        # 4-bet logic
        if len(all_raises) >= 2:
            # Player can 4-bet if they acted after second raise
            second_raise = all_raises[1]
            second_raise_idx = preflop_actions.index(second_raise)
            player_actions_after_second_raise = [a for a in player_actions
                                                if preflop_actions.index(a) > second_raise_idx]

            if player_actions_after_second_raise:
                self.counters['opportunities_to_4bet'] += 1

                # Did player 4-bet?
                if len(player_raises) > 0 and len(all_raises) >= 3:
                    if player_raises[-1] == all_raises[2]:
                        self.counters['four_bets'] += 1

        # Fold vs 4-bet
        if len(player_raises) >= 1 and len(all_raises) >= 3:
            # If player made second raise and there was a third raise
            if len(player_raises) > 0 and player_raises[-1] == all_raises[1]:
                self.counters['faced_4bet'] += 1

                # Did player fold?
                fold_actions = [a for a in player_actions if a.get('action') == 'fold']
                if fold_actions:
                    self.counters['folds_to_4bet'] += 1

    def _process_postflop_street(self, street: str, street_data: Dict[str, Any],
                                prev_street_actions: List[Dict[str, Any]],
                                player_name: str) -> None:
        """Process postflop actions for a specific street"""
        if not street_data:
            return

        street_actions = street_data.get('actions', [])
        if not street_actions:
            return

        player_actions = [a for a in street_actions if a.get('player') == player_name]

        # Determine if player was preflop raiser (eligible for c-bet)
        was_preflop_raiser = any(a.get('action') == 'raise' and a.get('player') == player_name
                                for a in prev_street_actions)

        # C-bet opportunity and execution
        if was_preflop_raiser:
            # Player has c-bet opportunity if they act first postflop or face a check
            first_action = street_actions[0] if street_actions else None

            has_cbet_opp = False
            if first_action and first_action.get('player') == player_name:
                has_cbet_opp = True
            elif any(a.get('action') == 'check' for a in street_actions):
                # Faced a check, can c-bet
                player_action_idx = next((i for i, a in enumerate(street_actions)
                                        if a.get('player') == player_name), None)
                if player_action_idx is not None:
                    actions_before = street_actions[:player_action_idx]
                    if any(a.get('action') == 'check' for a in actions_before):
                        has_cbet_opp = True

            if has_cbet_opp:
                self.counters['cbet_opportunities'] += 1

                if street == 'flop':
                    self.counters['flop_cbet_opportunities'] += 1
                elif street == 'turn':
                    self.counters['turn_cbet_opportunities'] += 1
                elif street == 'river':
                    self.counters['river_cbet_opportunities'] += 1

                # Did player c-bet?
                player_bets = [a for a in player_actions
                             if a.get('action') in ['bet', 'raise']]
                if player_bets:
                    self.counters['cbets'] += 1

                    if street == 'flop':
                        self.counters['flop_cbets'] += 1
                    elif street == 'turn':
                        self.counters['turn_cbets'] += 1
                        # Check if also bet flop (double barrel)
                        if self.counters['flop_cbets'] > 0:
                            self.counters['turn_bets_after_flop_bet'] += 1
                    elif street == 'river':
                        self.counters['river_cbets'] += 1
                        # Check if also bet turn (triple barrel)
                        if self.counters['turn_bets_after_flop_bet'] > 0:
                            self.counters['river_bets_after_turn_bet'] += 1

        # Defense vs c-bet
        # Check if player faced a c-bet
        for i, action in enumerate(street_actions):
            if action.get('player') == player_name:
                # Look at previous actions to see if facing a bet
                actions_before = street_actions[:i]
                facing_bet = any(a.get('action') in ['bet', 'raise']
                               for a in actions_before)

                if facing_bet:
                    self.counters['faced_cbet'] += 1

                    if street == 'flop':
                        self.counters['faced_flop_cbet'] += 1
                    elif street == 'turn':
                        self.counters['faced_turn_cbet'] += 1
                    elif street == 'river':
                        self.counters['faced_river_cbet'] += 1

                    # Did player fold?
                    if action.get('action') == 'fold':
                        self.counters['folds_to_cbet'] += 1

                        if street == 'flop':
                            self.counters['folds_to_flop_cbet'] += 1
                        elif street == 'turn':
                            self.counters['folds_to_turn_cbet'] += 1
                        elif street == 'river':
                            self.counters['folds_to_river_cbet'] += 1

                break  # Only count first action per street

    def _calculate_final_stats(self, essential_only: bool = False) -> Dict[str, Optional[float]]:
        """
        Calculate final percentage stats from counters

        Args:
            essential_only: If True, only calculate 20 essential stats

        Returns:
            Dictionary of stat values
        """
        stats = {}

        # Determine which stats to calculate
        if essential_only:
            stat_names = get_essential_stats()
        else:
            stat_names = list(STAT_DEFINITIONS.keys())

        # Calculate each stat
        for stat_name in stat_names:
            stats[stat_name] = self._calculate_stat(stat_name)

        return stats

    def _calculate_stat(self, stat_name: str) -> Optional[float]:
        """
        Calculate a specific stat from counters

        Args:
            stat_name: Name of stat to calculate

        Returns:
            Stat value or None if insufficient data
        """
        c = self.counters  # Shorthand

        try:
            if stat_name == 'vpip':
                return self._safe_percentage(c['voluntary_preflop_actions'], c['total_hands'])

            elif stat_name == 'pfr':
                return self._safe_percentage(c['preflop_raises'], c['total_hands'])

            elif stat_name == 'three_bet':
                return self._safe_percentage(c['three_bets'], c['opportunities_to_3bet'])

            elif stat_name == 'fold_vs_3bet':
                return self._safe_percentage(c['folds_to_3bet'], c['faced_3bet'])

            elif stat_name == 'fold_vs_3bet_ip':
                return self._safe_percentage(c['folds_to_3bet_ip'], c['faced_3bet_ip'])

            elif stat_name == 'fold_vs_3bet_oop':
                return self._safe_percentage(c['folds_to_3bet_oop'], c['faced_3bet_oop'])

            elif stat_name == 'four_bet':
                return self._safe_percentage(c['four_bets'], c['opportunities_to_4bet'])

            elif stat_name == 'fold_vs_4bet':
                return self._safe_percentage(c['folds_to_4bet'], c['faced_4bet'])

            elif stat_name == 'cbet_freq':
                return self._safe_percentage(c['cbets'], c['cbet_opportunities'])

            elif stat_name == 'cbet_freq_flop':
                return self._safe_percentage(c['flop_cbets'], c['flop_cbet_opportunities'])

            elif stat_name == 'cbet_freq_turn':
                return self._safe_percentage(c['turn_cbets'], c['turn_cbet_opportunities'])

            elif stat_name == 'cbet_freq_river':
                return self._safe_percentage(c['river_cbets'], c['river_cbet_opportunities'])

            elif stat_name == 'double_barrel':
                return self._safe_percentage(c['turn_bets_after_flop_bet'], c['flop_cbets'])

            elif stat_name == 'triple_barrel':
                return self._safe_percentage(c['river_bets_after_turn_bet'],
                                            c['turn_bets_after_flop_bet'])

            elif stat_name == 'fold_vs_cbet':
                return self._safe_percentage(c['folds_to_cbet'], c['faced_cbet'])

            elif stat_name == 'fold_vs_cbet_flop':
                return self._safe_percentage(c['folds_to_flop_cbet'], c['faced_flop_cbet'])

            elif stat_name == 'fold_vs_cbet_turn':
                return self._safe_percentage(c['folds_to_turn_cbet'], c['faced_turn_cbet'])

            elif stat_name == 'fold_vs_cbet_river':
                return self._safe_percentage(c['folds_to_river_cbet'], c['faced_river_cbet'])

            elif stat_name == 'wtsd':
                return self._safe_percentage(c['showdowns'], c['saw_flop'])

            elif stat_name == 'w_sd':
                return self._safe_percentage(c['showdowns_won'], c['showdowns'])

            else:
                logger.warning(f"Unknown stat: {stat_name}")
                return None

        except Exception as e:
            logger.error(f"Error calculating {stat_name}: {e}")
            return None

    def _safe_percentage(self, numerator: int, denominator: int,
                        min_sample: int = 10) -> Optional[float]:
        """
        Safely calculate percentage with divide-by-zero protection

        Args:
            numerator: Count of events
            denominator: Total opportunities
            min_sample: Minimum denominator for reliable stat

        Returns:
            Percentage (0-100) or None if insufficient data
        """
        if denominator < min_sample:
            return None

        if denominator == 0:
            return None

        return round((numerator / denominator) * 100, 2)

    def get_counter_summary(self) -> Dict[str, int]:
        """Get current counter values for debugging"""
        return dict(self.counters)
