"""
Leak Detection and Pattern Analysis Module
Identifies persistent leaks, tracks improvement, and prioritizes fixes
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from ..stats.definitions import STAT_DEFINITIONS, STAT_CATEGORIES
from .gto_comparison import GTOComparator

logger = logging.getLogger(__name__)


class LeakDetector:
    """
    Detects and tracks leaks across multiple sessions
    Provides prioritization and improvement tracking
    """

    def __init__(self, stakes: str = 'PLO100'):
        """
        Initialize leak detector

        Args:
            stakes: Stakes level for analysis (e.g., 'PLO50', 'PLO100')
        """
        self.stakes = stakes
        self.comparator = GTOComparator(stakes=stakes)
        self.leak_history: List[Dict[str, Any]] = []

    def detect_leaks(self, player_stats: Dict[str, float],
                    sample_size: int,
                    session_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Detect leaks in current session

        Args:
            player_stats: Dictionary of stat_name: value
            sample_size: Number of hands in sample
            session_date: Date of session (defaults to now)

        Returns:
            Dictionary with leak analysis and recommendations
        """
        if session_date is None:
            session_date = datetime.now()

        # Get all leaks from GTO comparison
        leaks = self.comparator.get_leaks(player_stats, min_severity='MEDIUM')

        # Categorize leaks
        categorized = self._categorize_leaks(leaks)

        # Calculate priority scores
        prioritized = self._prioritize_leaks(leaks, sample_size)

        # Generate recommendations
        recommendations = self._generate_recommendations(prioritized[:5])

        # Store in history for tracking
        self._add_to_history(leaks, session_date, sample_size)

        return {
            'session_date': session_date.isoformat(),
            'sample_size': sample_size,
            'total_leaks': len(leaks),
            'leaks_by_category': categorized,
            'prioritized_leaks': prioritized,
            'top_5_priorities': prioritized[:5],
            'recommendations': recommendations,
            'reliable': sample_size >= 100
        }

    def track_improvement(self, days: int = 30) -> Dict[str, Any]:
        """
        Track leak improvement over time

        Args:
            days: Number of days to look back

        Returns:
            Dictionary with improvement metrics
        """
        if not self.leak_history:
            return {
                'status': 'insufficient_data',
                'message': 'No historical data available'
            }

        cutoff_date = datetime.now() - timedelta(days=days)

        # Filter history to time window
        recent_history = [
            entry for entry in self.leak_history
            if entry['date'] >= cutoff_date
        ]

        if len(recent_history) < 2:
            return {
                'status': 'insufficient_data',
                'message': f'Need at least 2 sessions in past {days} days'
            }

        # Compare first vs last session
        first_session = recent_history[0]
        last_session = recent_history[-1]

        improvements = self._compare_sessions(first_session, last_session)

        # Calculate overall improvement score
        improvement_score = self._calculate_improvement_score(improvements)

        return {
            'status': 'success',
            'time_period_days': days,
            'sessions_analyzed': len(recent_history),
            'first_session_date': first_session['date'].isoformat(),
            'last_session_date': last_session['date'].isoformat(),
            'improvements': improvements,
            'overall_improvement_score': improvement_score,
            'trending': 'improving' if improvement_score > 0 else 'declining'
        }

    def identify_persistent_leaks(self, min_occurrences: int = 3) -> List[Dict[str, Any]]:
        """
        Identify leaks that appear consistently across sessions

        Args:
            min_occurrences: Minimum number of times leak must appear

        Returns:
            List of persistent leaks with occurrence count
        """
        if len(self.leak_history) < min_occurrences:
            return []

        # Track leak occurrences
        leak_counts = defaultdict(int)
        leak_details = {}

        for session in self.leak_history:
            for leak in session['leaks']:
                stat_name = leak['stat_name']
                leak_counts[stat_name] += 1

                # Keep most recent details
                if stat_name not in leak_details:
                    leak_details[stat_name] = leak

        # Filter to persistent leaks
        persistent = []
        for stat_name, count in leak_counts.items():
            if count >= min_occurrences:
                leak = leak_details[stat_name].copy()
                leak['occurrences'] = count
                leak['persistence_rate'] = (count / len(self.leak_history)) * 100
                persistent.append(leak)

        # Sort by persistence rate
        persistent.sort(key=lambda x: x['persistence_rate'], reverse=True)

        return persistent

    def get_study_plan(self, player_stats: Dict[str, float],
                       sample_size: int,
                       focus_areas: int = 3) -> Dict[str, Any]:
        """
        Generate a study plan based on detected leaks

        Args:
            player_stats: Dictionary of stat_name: value
            sample_size: Number of hands in sample
            focus_areas: Number of focus areas to include

        Returns:
            Dictionary with structured study plan
        """
        # Detect current leaks
        leak_analysis = self.detect_leaks(player_stats, sample_size)

        # Get persistent leaks
        persistent = self.identify_persistent_leaks()

        # Combine and prioritize
        all_leaks = leak_analysis['prioritized_leaks']

        # Mark persistent leaks
        persistent_names = {leak['stat_name'] for leak in persistent}
        for leak in all_leaks:
            leak['is_persistent'] = leak['stat_name'] in persistent_names

        # Select top focus areas
        focus_leaks = all_leaks[:focus_areas]

        # Generate study tasks
        study_tasks = []
        for leak in focus_leaks:
            tasks = self._generate_study_tasks(leak)
            study_tasks.append({
                'leak': leak,
                'tasks': tasks,
                'estimated_study_time': len(tasks) * 30  # 30 min per task
            })

        return {
            'date_created': datetime.now().isoformat(),
            'sample_size': sample_size,
            'focus_areas': focus_areas,
            'study_tasks': study_tasks,
            'total_estimated_hours': sum(t['estimated_study_time'] for t in study_tasks) / 60,
            'persistent_leaks_count': len(persistent)
        }

    def _categorize_leaks(self, leaks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize leaks by stat category"""
        categorized = defaultdict(list)

        for leak in leaks:
            category = leak['category']
            categorized[category].append(leak)

        return dict(categorized)

    def _prioritize_leaks(self, leaks: List[Dict[str, Any]],
                         sample_size: int) -> List[Dict[str, Any]]:
        """
        Calculate priority scores for leaks

        Priority based on:
        - Severity (weight: 40%)
        - EV loss (weight: 30%)
        - Sample size reliability (weight: 20%)
        - Category importance (weight: 10%)
        """
        severity_scores = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}
        category_importance = {
            'preflop': 3,
            'postflop_aggression': 2,
            'postflop_defense': 2,
            'river': 1,
            'positional': 2,
            'pot_type': 1,
            'advanced': 1
        }

        prioritized = []
        for leak in leaks:
            # Severity score (0-4)
            severity_score = severity_scores.get(leak['severity'], 1)

            # EV loss (normalized 0-4)
            ev_loss = self.comparator.calculate_ev_loss(leak)
            ev_score = min(ev_loss['ev_loss_bb100'] / 2.0, 4.0)

            # Sample reliability (0-4)
            reliability_score = min(sample_size / 100.0, 4.0)

            # Category importance (1-3)
            category_score = category_importance.get(leak['category'], 1)

            # Calculate weighted priority
            priority = (
                severity_score * 0.40 +
                ev_score * 0.30 +
                reliability_score * 0.20 +
                category_score * 0.10
            )

            leak_copy = leak.copy()
            leak_copy['priority_score'] = round(priority, 2)
            leak_copy['ev_loss_bb100'] = ev_loss['ev_loss_bb100']
            prioritized.append(leak_copy)

        # Sort by priority score
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)

        return prioritized

    def _generate_recommendations(self, top_leaks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations for top leaks"""
        recommendations = []

        # Map stats to study recommendations
        study_map = {
            'vpip': 'Tighten starting hand ranges. Review hand selection charts for your position.',
            'pfr': 'Increase aggression with raising. Study optimal raise-first-in ranges.',
            'three_bet': 'Work on 3-bet ranges. Study when to 3-bet for value vs as a bluff.',
            'fold_vs_3bet': 'Review your 3-bet calling ranges. May be calling too wide or folding too much.',
            'fold_vs_3bet_ip': 'Optimize IP defense vs 3-bets. Can defend wider in position.',
            'fold_vs_3bet_oop': 'Tighten OOP defense vs 3-bets. Position disadvantage requires more discipline.',
            'cbet_freq': 'Review c-betting strategy. Study board textures and range advantage.',
            'cbet_freq_flop': 'Optimize flop c-bet frequency based on board texture and position.',
            'cbet_freq_turn': 'Work on turn barreling. Study when to continue vs give up.',
            'fold_vs_cbet': 'Review your defense vs c-bets. May be over-folding or over-calling.',
            'double_barrel': 'Study turn barreling spots. Work on recognizing good turn barrels.',
            'wtsd': 'Review river decisions. May be going to showdown too often or not enough.',
        }

        for leak in top_leaks:
            stat_name = leak['stat_name']
            recommendation = study_map.get(stat_name, 'Review this statistic and compare to GTO baseline.')

            recommendations.append({
                'stat_name': stat_name,
                'stat_display': leak['stat_display_name'],
                'severity': leak['severity'],
                'recommendation': recommendation,
                'priority': leak.get('priority_score', 0),
                'ev_impact': f"{leak.get('ev_loss_bb100', 0):.2f} BB/100"
            })

        return recommendations

    def _generate_study_tasks(self, leak: Dict[str, Any]) -> List[str]:
        """Generate specific study tasks for a leak"""
        stat_name = leak['stat_name']
        category = leak['category']

        tasks = []

        # Category-specific tasks
        if category == 'preflop':
            tasks.extend([
                f"Review {leak['stat_display_name']} ranges in GTO trainer",
                "Study hand charts for 6-max PLO",
                "Review 10 hands where you deviated from optimal range",
                "Practice range quiz for this situation"
            ])
        elif category == 'postflop_aggression':
            tasks.extend([
                f"Study optimal {leak['stat_display_name']} frequencies",
                "Review 5 hands where you checked instead of betting",
                "Analyze board textures where you should bet more/less",
                "Practice c-betting drills in solver"
            ])
        elif category == 'postflop_defense':
            tasks.extend([
                f"Review defense frequencies for {leak['stat_display_name']}",
                "Study calling ranges vs aggression",
                "Analyze 5 hands where you folded incorrectly",
                "Practice defense drills"
            ])

        # Add severity-based tasks
        if leak['severity'] in ['HIGH', 'CRITICAL']:
            tasks.append("PRIORITY: Schedule coaching session to review this leak")
            tasks.append("Add this spot to daily drill routine")

        return tasks

    def _add_to_history(self, leaks: List[Dict[str, Any]],
                       session_date: datetime,
                       sample_size: int) -> None:
        """Add session to history"""
        self.leak_history.append({
            'date': session_date,
            'leaks': leaks,
            'sample_size': sample_size
        })

        # Keep only last 30 sessions
        if len(self.leak_history) > 30:
            self.leak_history = self.leak_history[-30:]

    def _compare_sessions(self, first: Dict[str, Any],
                         last: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare two sessions to track improvement"""
        improvements = []

        # Create lookup for first session leaks
        first_leaks = {leak['stat_name']: leak for leak in first['leaks']}
        last_leaks = {leak['stat_name']: leak for leak in last['leaks']}

        # Check all stats from first session
        for stat_name, first_leak in first_leaks.items():
            if stat_name in last_leaks:
                last_leak = last_leaks[stat_name]
                delta_change = last_leak['abs_delta'] - first_leak['abs_delta']

                improvements.append({
                    'stat_name': stat_name,
                    'stat_display': first_leak['stat_display_name'],
                    'first_deviation': first_leak['abs_delta'],
                    'last_deviation': last_leak['abs_delta'],
                    'change': round(delta_change, 2),
                    'improved': delta_change < 0,
                    'still_leak': last_leak['is_leak']
                })
            else:
                # Leak was fixed!
                improvements.append({
                    'stat_name': stat_name,
                    'stat_display': first_leak['stat_display_name'],
                    'first_deviation': first_leak['abs_delta'],
                    'last_deviation': 0,
                    'change': -first_leak['abs_delta'],
                    'improved': True,
                    'still_leak': False,
                    'fixed': True
                })

        # Sort by improvement (most improved first)
        improvements.sort(key=lambda x: x['change'])

        return improvements

    def _calculate_improvement_score(self, improvements: List[Dict[str, Any]]) -> float:
        """
        Calculate overall improvement score

        Returns:
            Score from -100 to +100 (positive = improving)
        """
        if not improvements:
            return 0.0

        improved_count = sum(1 for imp in improvements if imp['improved'])
        total_count = len(improvements)

        # Calculate percentage improved
        improvement_rate = (improved_count / total_count) * 100

        # Calculate average change magnitude
        avg_change = sum(imp['change'] for imp in improvements) / total_count

        # Combine (negative change is good)
        score = (improvement_rate / 2) - (avg_change * 10)

        return round(max(-100, min(100, score)), 1)

    def format_leak_report(self, leak_analysis: Dict[str, Any]) -> str:
        """
        Format leak detection results as readable report

        Args:
            leak_analysis: Output from detect_leaks()

        Returns:
            Formatted string report
        """
        lines = []
        lines.append("=" * 70)
        lines.append("LEAK DETECTION REPORT")
        lines.append("=" * 70)
        lines.append(f"Session Date: {leak_analysis['session_date']}")
        lines.append(f"Sample Size: {leak_analysis['sample_size']} hands")
        lines.append(f"Reliability: {'RELIABLE' if leak_analysis['reliable'] else 'NEED MORE HANDS'}")
        lines.append(f"Total Leaks Detected: {leak_analysis['total_leaks']}")
        lines.append("")

        # Top priorities
        lines.append("TOP 5 PRIORITY LEAKS:")
        lines.append("-" * 70)
        for i, leak in enumerate(leak_analysis['top_5_priorities'], 1):
            lines.append(f"\n{i}. {leak['stat_display_name']} - {leak['severity']}")
            lines.append(f"   Your Value: {leak['player_value']:.1f}% | "
                        f"GTO: {leak['gto_value']:.1f}% | "
                        f"Deviation: {leak['delta']:+.1f}%")
            lines.append(f"   Priority Score: {leak['priority_score']:.2f} | "
                        f"EV Loss: {leak['ev_loss_bb100']:.2f} BB/100")

        # Recommendations
        lines.append("\n")
        lines.append("RECOMMENDATIONS:")
        lines.append("-" * 70)
        for i, rec in enumerate(leak_analysis['recommendations'], 1):
            lines.append(f"\n{i}. {rec['stat_display']} ({rec['severity']})")
            lines.append(f"   {rec['recommendation']}")
            lines.append(f"   EV Impact: {rec['ev_impact']}")

        lines.append("\n" + "=" * 70)

        return '\n'.join(lines)
