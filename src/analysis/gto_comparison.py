"""
GTO Baseline Comparison Module
Compares player statistics against GTO baselines to identify deviations
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from ..stats.definitions import STAT_DEFINITIONS

logger = logging.getLogger(__name__)


class GTOComparator:
    """
    Compares player statistics against GTO baselines
    """

    def __init__(self, stakes: str = 'PLO100'):
        """
        Initialize GTO comparator

        Args:
            stakes: Stakes level for GTO baselines (e.g., 'PLO50', 'PLO100')
        """
        self.stakes = stakes

    def compare_stats(self, player_stats: Dict[str, float],
                     stat_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Compare player stats against GTO baselines

        Args:
            player_stats: Dictionary of stat_name: value
            stat_names: Optional list of stats to compare (default: all)

        Returns:
            List of deviation dictionaries with analysis
        """
        if stat_names is None:
            stat_names = list(STAT_DEFINITIONS.keys())

        deviations = []

        for stat_name in stat_names:
            if stat_name not in STAT_DEFINITIONS:
                continue

            # Get player value
            player_value = player_stats.get(stat_name)
            if player_value is None:
                continue

            # Get GTO baseline
            definition = STAT_DEFINITIONS[stat_name]
            gto_value = definition.get('gto_baseline')
            threshold = definition.get('threshold', 3.0)

            if gto_value is None:
                continue

            # Calculate deviation
            delta = player_value - gto_value
            abs_delta = abs(delta)

            # Classify deviation
            severity = self._classify_severity(abs_delta, threshold)
            direction = 'over' if delta > 0 else 'under' if delta < 0 else 'optimal'

            # Determine if this is a potential leak
            is_leak = abs_delta > threshold

            deviation = {
                'stat_name': stat_name,
                'stat_display_name': definition['name'],
                'category': definition['category'],
                'player_value': round(player_value, 2),
                'gto_value': round(gto_value, 2),
                'delta': round(delta, 2),
                'abs_delta': round(abs_delta, 2),
                'threshold': threshold,
                'severity': severity,
                'direction': direction,
                'is_leak': is_leak,
                'description': definition.get('description', '')
            }

            deviations.append(deviation)

        # Sort by absolute delta (largest deviations first)
        deviations.sort(key=lambda x: x['abs_delta'], reverse=True)

        return deviations

    def get_leaks(self, player_stats: Dict[str, float],
                  min_severity: str = 'MEDIUM') -> List[Dict[str, Any]]:
        """
        Get only the leaks (deviations exceeding threshold)

        Args:
            player_stats: Dictionary of stat_name: value
            min_severity: Minimum severity to include ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')

        Returns:
            List of leak dictionaries
        """
        all_deviations = self.compare_stats(player_stats)

        # Filter to only leaks
        leaks = [d for d in all_deviations if d['is_leak']]

        # Filter by minimum severity
        severity_levels = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2, 'CRITICAL': 3}
        min_level = severity_levels.get(min_severity, 1)

        leaks = [leak for leak in leaks
                if severity_levels.get(leak['severity'], 0) >= min_level]

        return leaks

    def get_strengths(self, player_stats: Dict[str, float],
                     top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get player's statistical strengths (stats within optimal range)

        Args:
            player_stats: Dictionary of stat_name: value
            top_n: Number of top strengths to return

        Returns:
            List of strength dictionaries
        """
        all_deviations = self.compare_stats(player_stats)

        # Filter to non-leaks only
        strengths = [d for d in all_deviations if not d['is_leak']]

        # Sort by how close to GTO (smallest abs_delta)
        strengths.sort(key=lambda x: x['abs_delta'])

        return strengths[:top_n]

    def _classify_severity(self, abs_delta: float, threshold: float) -> str:
        """
        Classify the severity of a deviation

        Args:
            abs_delta: Absolute deviation from GTO
            threshold: Acceptable threshold for this stat

        Returns:
            Severity level: 'CRITICAL', 'HIGH', 'MEDIUM', or 'LOW'
        """
        if abs_delta < threshold:
            return 'LOW'  # Within acceptable range

        # Calculate how many thresholds exceeded
        multiplier = abs_delta / threshold

        if multiplier >= 3.0:
            return 'CRITICAL'  # 3x+ threshold
        elif multiplier >= 2.0:
            return 'HIGH'  # 2-3x threshold
        else:
            return 'MEDIUM'  # 1-2x threshold

    def generate_comparison_summary(self, player_stats: Dict[str, float],
                                   sample_size: int) -> Dict[str, Any]:
        """
        Generate a comprehensive comparison summary

        Args:
            player_stats: Dictionary of stat_name: value
            sample_size: Number of hands in sample

        Returns:
            Summary dictionary with overall analysis
        """
        deviations = self.compare_stats(player_stats)

        leaks = [d for d in deviations if d['is_leak']]
        strengths = [d for d in deviations if not d['is_leak']]

        # Count by severity
        severity_counts = {
            'CRITICAL': len([l for l in leaks if l['severity'] == 'CRITICAL']),
            'HIGH': len([l for l in leaks if l['severity'] == 'HIGH']),
            'MEDIUM': len([l for l in leaks if l['severity'] == 'MEDIUM']),
            'LOW': len([l for l in leaks if l['severity'] == 'LOW'])
        }

        # Count by category
        category_leaks = {}
        for leak in leaks:
            category = leak['category']
            if category not in category_leaks:
                category_leaks[category] = 0
            category_leaks[category] += 1

        # Top 5 leaks
        top_leaks = sorted(leaks, key=lambda x: x['abs_delta'], reverse=True)[:5]

        # Calculate overall score (percentage of stats within threshold)
        total_stats = len(deviations)
        optimal_stats = len(strengths)
        overall_score = (optimal_stats / total_stats * 100) if total_stats > 0 else 0

        summary = {
            'sample_size': sample_size,
            'stakes': self.stakes,
            'total_stats_analyzed': total_stats,
            'stats_within_threshold': optimal_stats,
            'total_leaks': len(leaks),
            'severity_breakdown': severity_counts,
            'category_breakdown': category_leaks,
            'overall_score': round(overall_score, 1),
            'top_leaks': top_leaks,
            'top_strengths': self.get_strengths(player_stats, top_n=3),
            'analysis_date': datetime.now().isoformat(),
            'reliable': sample_size >= 100
        }

        return summary

    def calculate_ev_loss(self, leak: Dict[str, Any],
                         hands_per_hour: int = 100,
                         hours_played: int = 100) -> Dict[str, float]:
        """
        Estimate EV loss from a specific leak

        Args:
            leak: Leak dictionary from compare_stats
            hands_per_hour: Hands played per hour
            hours_played: Hours played in analysis period

        Returns:
            Dictionary with EV loss estimates
        """
        stat_name = leak['stat_name']
        definition = STAT_DEFINITIONS.get(stat_name, {})

        # Get EV loss coefficient (BB/100 per % deviation)
        # This is a simplified estimate - real values would come from solver analysis
        ev_coefficient = definition.get('ev_loss_coefficient', 0.15)

        abs_delta = leak['abs_delta']

        # Calculate EV loss in BB/100
        ev_loss_bb100 = abs_delta * ev_coefficient

        # Calculate total hands
        total_hands = hands_per_hour * hours_played

        # Calculate total EV loss in BB
        total_ev_loss_bb = (ev_loss_bb100 / 100) * total_hands

        return {
            'ev_loss_bb100': round(ev_loss_bb100, 2),
            'total_ev_loss_bb': round(total_ev_loss_bb, 2),
            'total_hands': total_hands,
            'stat_name': stat_name,
            'severity': leak['severity']
        }

    def format_deviation_report(self, deviation: Dict[str, Any]) -> str:
        """
        Format a single deviation as a readable report

        Args:
            deviation: Deviation dictionary

        Returns:
            Formatted string report
        """
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"{deviation['stat_display_name']} ({deviation['stat_name']})")
        lines.append(f"{'='*60}")
        lines.append(f"Your Value:    {deviation['player_value']:6.1f}%")
        lines.append(f"GTO Baseline:  {deviation['gto_value']:6.1f}%")
        lines.append(f"Deviation:     {deviation['delta']:+6.1f}% ({deviation['direction']})")
        lines.append(f"Threshold:     ±{deviation['threshold']:.1f}%")
        lines.append(f"Severity:      {deviation['severity']}")
        lines.append(f"Category:      {deviation['category']}")

        if deviation['is_leak']:
            lines.append(f"\n⚠ LEAK DETECTED")
            ev_loss = self.calculate_ev_loss(deviation)
            lines.append(f"Estimated EV Loss: {ev_loss['ev_loss_bb100']:.2f} BB/100")

        lines.append(f"\nDescription: {deviation['description']}")
        lines.append(f"{'='*60}\n")

        return '\n'.join(lines)
