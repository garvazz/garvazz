"""
PokerStars Hand History Parser
Parses PokerStars PLO hand histories
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser, ParsingError


class PokerStarsParser(BaseParser):
    """
    Parser for PokerStars hand histories
    """

    def __init__(self):
        super().__init__()
        self.site_name = "PokerStars"

        # Regex patterns
        self.hand_start_pattern = re.compile(r'PokerStars Hand #(\d+):')
        self.game_info_pattern = re.compile(
            r"Pot Limit Omaha(?:-5 Card)? \(\$?([\d.]+)/\$?([\d.]+)(?:\s+USD)?\)"
        )
        self.table_pattern = re.compile(r"Table '([^']+)'.*?Seat #(\d+) is the button")
        self.seat_pattern = re.compile(r"Seat (\d+): ([^\(]+) \(\$?([\d.]+) in chips\)")
        self.timestamp_pattern = re.compile(r"\[(\d{4}/\d{2}/\d{2} \d{1,2}:\d{2}:\d{2})")

    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Parse a PokerStars hand history file

        Args:
            filepath: Path to file

        Returns:
            List of parsed hands
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into individual hands
        hands_text = re.split(r'\n\n+', content)

        parsed_hands = []
        errors = []

        for hand_text in hands_text:
            if not hand_text.strip():
                continue

            # Check if this is actually a hand (starts with PokerStars Hand #)
            if not self.hand_start_pattern.search(hand_text):
                continue

            try:
                hand = self.parse_hand(hand_text)
                self.validate_hand(hand)
                parsed_hands.append(hand)
            except ParsingError as e:
                errors.append({
                    'text': hand_text[:100],
                    'error': str(e)
                })

        if errors:
            # Log errors but don't fail
            print(f"Parsed {len(parsed_hands)} hands with {len(errors)} errors")

        return parsed_hands

    def parse_hand(self, hand_text: str) -> Dict[str, Any]:
        """
        Parse a single hand from text

        Args:
            hand_text: Text of a single hand

        Returns:
            Parsed hand dictionary
        """
        lines = hand_text.strip().split('\n')

        # Initialize hand structure
        hand = {
            'site': self.site_name,
            'game_type': 'PLO',
            'players': [],
            'actions': {
                'preflop': []
            }
        }

        # Parse header (first line)
        header = lines[0]
        hand_id_match = self.hand_start_pattern.search(header)
        if not hand_id_match:
            raise ParsingError("Cannot find hand ID")
        hand['hand_id'] = hand_id_match.group(1)

        # Detect PLO5 vs PLO
        if 'Omaha-5' in header or '5 Card' in header:
            hand['game_type'] = 'PLO5'

        # Parse game info (stakes)
        game_match = self.game_info_pattern.search(header)
        if game_match:
            hand['stakes_sb'] = float(game_match.group(1))
            hand['stakes_bb'] = float(game_match.group(2))
        else:
            raise ParsingError("Cannot parse stakes")

        # Parse timestamp
        ts_match = self.timestamp_pattern.search(hand_text)
        if ts_match:
            ts_str = ts_match.group(1)
            hand['timestamp'] = datetime.strptime(ts_str, '%Y/%m/%d %H:%M:%S')
        else:
            hand['timestamp'] = datetime.now()

        # Parse table info
        table_match = self.table_pattern.search(hand_text)
        if table_match:
            hand['table_name'] = table_match.group(1)
            hand['button_seat'] = int(table_match.group(2))
        else:
            raise ParsingError("Cannot parse table info")

        # Parse seats/players
        for line in lines:
            seat_match = self.seat_pattern.search(line)
            if seat_match:
                seat_num = int(seat_match.group(1))
                player_name = seat_match.group(2).strip()
                stack = float(seat_match.group(3))

                hand['players'].append({
                    'seat': seat_num,
                    'name': player_name,
                    'stack': stack,
                    'position': None,  # Will be set later
                    'cards': None
                })

        if not hand['players']:
            raise ParsingError("No players found")

        # Detect positions
        total_players = len(hand['players'])
        button_seat = hand['button_seat']
        for player in hand['players']:
            player['position'] = self.detect_position(
                player['seat'], button_seat, total_players
            )

        # Find hero
        hero_cards_line = None
        for line in lines:
            if line.startswith('Dealt to '):
                hero_cards_line = line
                break

        if hero_cards_line:
            # Extract hero name and cards
            # Format: "Dealt to PlayerName [Ah Kh Qc Jd]"
            match = re.search(r'Dealt to ([^\[]+)\s*\[([^\]]+)\]', hero_cards_line)
            if match:
                hand['hero_name'] = match.group(1).strip()
                cards_str = match.group(2).strip()
                hand['hero_cards'] = [self.parse_card(c) for c in cards_str.split()]

                # Find hero in players and set position
                for player in hand['players']:
                    if player['name'] == hand['hero_name']:
                        hand['hero_seat'] = player['seat']
                        hand['hero_position'] = player['position']
                        player['cards'] = hand['hero_cards']
                        break
        else:
            # No hero found - this might be a hand from tracking software
            # Use first player as placeholder
            hand['hero_name'] = hand['players'][0]['name']
            hand['hero_seat'] = hand['players'][0]['seat']
            hand['hero_position'] = hand['players'][0]['position']
            hand['hero_cards'] = []

        # Parse actions
        current_street = None
        board_cards = []

        for line in lines:
            line = line.strip()

            # Detect street
            if line == '*** HOLE CARDS ***':
                current_street = 'preflop'
                if current_street not in hand['actions']:
                    hand['actions'][current_street] = []
            elif line.startswith('*** FLOP ***'):
                current_street = 'flop'
                # Extract board
                flop_match = re.search(r'\[([^\]]+)\]', line)
                if flop_match:
                    cards = flop_match.group(1).strip().split()
                    hand['board_flop'] = [self.parse_card(c) for c in cards]
                    hand['actions'][current_street] = {'board': hand['board_flop'], 'actions': []}
            elif line.startswith('*** TURN ***'):
                current_street = 'turn'
                # Extract turn card
                turn_match = re.search(r'\]\s+\[([^\]]+)\]', line)
                if turn_match:
                    turn_card = turn_match.group(1).strip()
                    hand['board_turn'] = self.parse_card(turn_card)
                    hand['actions'][current_street] = {'board': [hand['board_turn']], 'actions': []}
            elif line.startswith('*** RIVER ***'):
                current_street = 'river'
                # Extract river card
                river_match = re.search(r'\]\s+\[([^\]]+)\]', line)
                if river_match:
                    river_card = river_match.group(1).strip()
                    hand['board_river'] = self.parse_card(river_card)
                    hand['actions'][current_street] = {'board': [hand['board_river']], 'actions': []}
            elif line.startswith('*** SHOW DOWN ***'):
                current_street = 'showdown'
                hand['showdown'] = True
            elif line.startswith('*** SUMMARY ***'):
                break

            # Parse action if we're in a street
            if current_street and current_street != 'showdown':
                action = self._parse_action_line(line)
                if action:
                    if current_street == 'preflop':
                        hand['actions'][current_street].append(action)
                    elif current_street in ['flop', 'turn', 'river']:
                        hand['actions'][current_street]['actions'].append(action)

        # Parse results
        hand['showdown'] = 'SHOW DOWN' in hand_text

        # Find winner(s) and pot
        summary_start = hand_text.find('*** SUMMARY ***')
        if summary_start > 0:
            summary = hand_text[summary_start:]

            # Find total pot
            pot_match = re.search(r'Total pot \$?([\d.]+)', summary)
            if pot_match:
                hand['pot_total'] = float(pot_match.group(1))

            # Find rake
            rake_match = re.search(r'Rake \$?([\d.]+)', summary)
            if rake_match:
                hand['rake'] = float(rake_match.group(1))

            # Find winner(s)
            winners = re.findall(r'Seat \d+: ([^\(]+) (?:showed|collected)', summary)
            if winners:
                hand['winner'] = winners[0] if len(winners) == 1 else winners

        # Calculate hero result
        if hand.get('winner'):
            winners = hand['winner'] if isinstance(hand['winner'], list) else [hand['winner']]
            if hand['hero_name'] in winners:
                # Hero won - calculate profit
                hand['hero_result'] = hand.get('pot_total', 0)
            else:
                # Hero lost - calculate loss (negative)
                # Need to find how much hero invested
                hero_invested = self._calculate_hero_investment(hand)
                hand['hero_result'] = -hero_invested
        else:
            hand['hero_result'] = 0

        # Calculate result in BB
        if hand.get('hero_result') and hand.get('stakes_bb'):
            hand['hero_result_bb'] = hand['hero_result'] / hand['stakes_bb']

        # Detect pot type
        hand['pot_type'] = self.detect_pot_type(hand['actions'])

        # Detect preflop action
        hand['hero_action_preflop'] = self._detect_hero_preflop_action(hand)

        return hand

    def _parse_action_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse an action line

        Args:
            line: Action line

        Returns:
            Action dictionary or None
        """
        # Skip non-action lines
        if not line or line.startswith('***') or line.startswith('Dealt'):
            return None

        # Patterns for different actions
        patterns = {
            'fold': r'^([^:]+): folds',
            'check': r'^([^:]+): checks',
            'call': r'^([^:]+): calls \$?([\d.]+)',
            'bet': r'^([^:]+): bets \$?([\d.]+)',
            'raise': r'^([^:]+): raises \$?[\d.]+ to \$?([\d.]+)',
            'blind': r'^([^:]+): posts (?:small |big )?blind \$?([\d.]+)',
        }

        for action_type, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                action = {
                    'player': match.group(1).strip(),
                    'action': action_type
                }

                if action_type in ['call', 'bet', 'raise', 'blind']:
                    action['amount'] = float(match.group(2))

                return action

        return None

    def _calculate_hero_investment(self, hand: Dict[str, Any]) -> float:
        """
        Calculate how much hero invested in the hand

        Args:
            hand: Hand dictionary

        Returns:
            Total investment amount
        """
        total = 0.0
        hero_name = hand['hero_name']

        for street, actions_data in hand['actions'].items():
            if street == 'preflop':
                actions = actions_data
            else:
                actions = actions_data.get('actions', [])

            for action in actions:
                if action.get('player') == hero_name:
                    if 'amount' in action:
                        total += action['amount']

        return total

    def _detect_hero_preflop_action(self, hand: Dict[str, Any]) -> str:
        """
        Detect hero's preflop action type

        Args:
            hand: Hand dictionary

        Returns:
            Action type string
        """
        hero_name = hand['hero_name']
        preflop = hand['actions'].get('preflop', [])

        hero_actions = [a for a in preflop if a.get('player') == hero_name]

        if not hero_actions:
            return 'Fold'

        first_action = hero_actions[0]

        if first_action['action'] == 'raise':
            # Check if it's a 3-bet or open raise
            prior_raises = [a for a in preflop if a['action'] == 'raise']
            hero_raise_index = prior_raises.index(first_action)
            if hero_raise_index == 0:
                return 'PFR'  # Preflop raiser (open)
            elif hero_raise_index == 1:
                return '3-Bet'
            else:
                return '4-Bet+'
        elif first_action['action'] == 'call':
            return 'PFC'  # Preflop caller
        elif first_action['action'] in ['check', 'blind']:
            if hand['hero_position'] == 'BB':
                return 'BB'
            else:
                return 'SB'
        else:
            return 'Fold'
