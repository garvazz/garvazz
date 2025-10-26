"""
Base parser class for hand history parsing
All site-specific parsers inherit from this base
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class ParsingError(Exception):
    """Custom exception for parsing errors"""
    pass


class BaseParser(ABC):
    """
    Abstract base class for hand history parsers
    """

    def __init__(self):
        """Initialize parser"""
        self.supported_game_types = ['PLO', 'PLO5']

    @abstractmethod
    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Parse a hand history file

        Args:
            filepath: Path to hand history file

        Returns:
            List of parsed hand dictionaries

        Raises:
            ParsingError: If parsing fails
        """
        pass

    @abstractmethod
    def parse_hand(self, hand_text: str) -> Dict[str, Any]:
        """
        Parse a single hand from text

        Args:
            hand_text: Text of a single hand

        Returns:
            Parsed hand dictionary

        Raises:
            ParsingError: If parsing fails
        """
        pass

    def validate_hand(self, hand: Dict[str, Any]) -> bool:
        """
        Validate a parsed hand

        Args:
            hand: Parsed hand dictionary

        Returns:
            True if valid

        Raises:
            ParsingError: If validation fails
        """
        required_fields = [
            'hand_id', 'timestamp', 'game_type', 'stakes_sb', 'stakes_bb',
            'hero_name', 'players'
        ]

        for field in required_fields:
            if field not in hand or hand[field] is None:
                raise ParsingError(f"Missing required field: {field}")

        # Validate game type
        if hand['game_type'] not in self.supported_game_types:
            raise ParsingError(f"Unsupported game type: {hand['game_type']}")

        # Validate player count (PLO: 2-9 players)
        if not (2 <= len(hand['players']) <= 9):
            raise ParsingError(f"Invalid player count: {len(hand['players'])}")

        # Validate hero exists in players
        hero_found = any(p['name'] == hand['hero_name'] for p in hand['players'])
        if not hero_found:
            raise ParsingError("Hero not found in players list")

        return True

    @staticmethod
    def parse_card(card_str: str) -> str:
        """
        Parse a card string to standardized format

        Args:
            card_str: Card string (e.g., 'Ah', 'Kd')

        Returns:
            Standardized card string
        """
        if len(card_str) != 2:
            raise ParsingError(f"Invalid card format: {card_str}")

        rank = card_str[0].upper()
        suit = card_str[1].lower()

        valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        valid_suits = ['h', 'd', 'c', 's']

        if rank not in valid_ranks or suit not in valid_suits:
            raise ParsingError(f"Invalid card: {card_str}")

        return rank + suit

    @staticmethod
    def parse_amount(amount_str: str) -> float:
        """
        Parse a monetary amount from string

        Args:
            amount_str: Amount string (e.g., '$10.50', '€5.00')

        Returns:
            Float amount
        """
        # Remove currency symbols and parse
        cleaned = re.sub(r'[^\d.]', '', amount_str)
        try:
            return float(cleaned)
        except ValueError:
            raise ParsingError(f"Invalid amount: {amount_str}")

    @staticmethod
    def detect_position(seat: int, button_seat: int, total_players: int) -> str:
        """
        Detect player position based on seat and button

        Args:
            seat: Player's seat number (1-9)
            button_seat: Button seat number
            total_players: Total number of players

        Returns:
            Position string
        """
        if total_players == 2:
            # Heads-up
            return 'BTN' if seat == button_seat else 'BB'

        # Calculate seats after button
        seats_after_button = (seat - button_seat) % total_players

        if seats_after_button == 1:
            return 'SB'
        elif seats_after_button == 2:
            return 'BB'
        elif seats_after_button == 0:
            return 'BTN'
        elif seats_after_button == total_players - 1:
            return 'CO'
        elif seats_after_button == total_players - 2:
            if total_players >= 6:
                return 'MP'
            else:
                return 'EP'
        else:
            return 'EP'

    @staticmethod
    def detect_pot_type(actions: Dict[str, Any]) -> str:
        """
        Detect pot type from preflop actions

        Args:
            actions: Actions dictionary

        Returns:
            Pot type: 'SRP', '3BP', '4BP', or 'MW'
        """
        if 'preflop' not in actions:
            return 'SRP'

        preflop = actions['preflop']
        raise_count = sum(1 for a in preflop if a.get('action') == 'raise')
        players_involved = len(set(a.get('player') for a in preflop if a.get('action') in ['call', 'raise']))

        # Multiway (3+ players)
        if players_involved >= 3:
            return 'MW'
        # 4-bet pot
        elif raise_count >= 3:
            return '4BP'
        # 3-bet pot
        elif raise_count == 2:
            return '3BP'
        # Single raised pot
        else:
            return 'SRP'
