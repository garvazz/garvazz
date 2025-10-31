#!/usr/bin/env python3
"""
Demo script for PLO Mastery Suite Analysis Tools
Demonstrates leak detection and GTO comparison features
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis import GTOComparator, LeakDetector
from src.stats.definitions import get_essential_stats, STAT_DEFINITIONS
from datetime import datetime, timedelta


def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_gto_comparison():
    """Demonstrate GTO comparison features"""
    print_header("DEMO 1: GTO COMPARISON")

    # Sample player stats (with intentional leaks)
    player_stats = {
        'vpip': 32.5,           # Too loose
        'pfr': 17.0,            # Too passive
        'three_bet': 5.5,       # Too low
        'fold_vs_3bet': 62.0,   # Folding too much
        'fold_vs_3bet_ip': 58.0,
        'fold_vs_3bet_oop': 66.0,
        'four_bet': 10.0,
        'fold_vs_4bet': 68.0,
        'cbet_freq': 48.0,      # Too low
        'cbet_freq_flop': 52.0, # Too low
        'cbet_freq_turn': 38.0, # Too low
        'cbet_freq_river': 35.0,
        'double_barrel': 42.0,  # Too low
        'triple_barrel': 38.0,
        'fold_vs_cbet': 52.0,   # Too high
        'fold_vs_cbet_flop': 50.0,  # Too high
        'fold_vs_cbet_turn': 55.0,  # Too high
        'fold_vs_cbet_river': 58.0, # Too high
        'wtsd': 22.0,
        'w_sd': 49.0,
    }

    print(f"\nAnalyzing player with {len(player_stats)} stats...")
    print(f"Sample size: 250 hands")

    # Create comparator
    comparator = GTOComparator(stakes='PLO100')

    # Get all deviations
    deviations = comparator.compare_stats(player_stats)
    print(f"\n✓ Compared {len(deviations)} statistics")

    # Get leaks only
    leaks = comparator.get_leaks(player_stats, min_severity='MEDIUM')
    print(f"✓ Found {len(leaks)} medium+ severity leaks")

    # Show top 5 leaks
    print("\n" + "-" * 80)
    print("TOP 5 LEAKS:")
    print("-" * 80)
    for i, leak in enumerate(leaks[:5], 1):
        ev_loss = comparator.calculate_ev_loss(leak, hands_per_hour=100, hours_played=10)
        print(f"\n{i}. {leak['stat_display_name']} [{leak['severity']}]")
        print(f"   Your Value:   {leak['player_value']:6.1f}%")
        print(f"   GTO Baseline: {leak['gto_value']:6.1f}%")
        print(f"   Deviation:    {leak['delta']:+6.1f}% ({leak['direction']})")
        print(f"   EV Loss:      {ev_loss['ev_loss_bb100']:.2f} BB/100")
        print(f"   Total Loss:   {ev_loss['total_ev_loss_bb']:.1f} BB over {ev_loss['total_hands']} hands")

    # Get strengths
    strengths = comparator.get_strengths(player_stats, top_n=3)
    print("\n" + "-" * 80)
    print("TOP 3 STRENGTHS (Stats closest to GTO):")
    print("-" * 80)
    for i, strength in enumerate(strengths, 1):
        print(f"\n{i}. {strength['stat_display_name']}")
        print(f"   Your Value:   {strength['player_value']:6.1f}%")
        print(f"   GTO Baseline: {strength['gto_value']:6.1f}%")
        print(f"   Deviation:    {strength['delta']:+6.1f}%")

    # Generate summary
    summary = comparator.generate_comparison_summary(player_stats, sample_size=250)
    print("\n" + "-" * 80)
    print("OVERALL SUMMARY:")
    print("-" * 80)
    print(f"Overall Score:        {summary['overall_score']:.1f}%")
    print(f"Stats within range:   {summary['stats_within_threshold']}/{summary['total_stats_analyzed']}")
    print(f"Total leaks:          {summary['total_leaks']}")
    print(f"Critical leaks:       {summary['severity_breakdown']['CRITICAL']}")
    print(f"High leaks:           {summary['severity_breakdown']['HIGH']}")
    print(f"Medium leaks:         {summary['severity_breakdown']['MEDIUM']}")
    print(f"Reliable sample:      {'YES' if summary['reliable'] else 'NO - Need 100+ hands'}")

    return player_stats


def demo_leak_detector(player_stats):
    """Demonstrate leak detection features"""
    print_header("DEMO 2: LEAK DETECTION & TRACKING")

    detector = LeakDetector(stakes='PLO100')

    # Detect current leaks
    print("\nDetecting leaks in current session...")
    leak_analysis = detector.detect_leaks(player_stats, sample_size=250)

    print(f"✓ Total leaks detected: {leak_analysis['total_leaks']}")
    print(f"✓ Categorized by: {len(leak_analysis['leaks_by_category'])} categories")
    print(f"✓ Generated {len(leak_analysis['recommendations'])} recommendations")

    # Show category breakdown
    print("\n" + "-" * 80)
    print("LEAKS BY CATEGORY:")
    print("-" * 80)
    for category, leaks in leak_analysis['leaks_by_category'].items():
        print(f"{category:25s}: {len(leaks)} leaks")

    # Show top priorities
    print("\n" + "-" * 80)
    print("TOP 5 PRIORITY LEAKS (by priority score):")
    print("-" * 80)
    for i, leak in enumerate(leak_analysis['top_5_priorities'], 1):
        print(f"\n{i}. {leak['stat_display_name']} - {leak['severity']}")
        print(f"   Priority Score:   {leak['priority_score']:.2f}/4.0")
        print(f"   Your Value:       {leak['player_value']:6.1f}%")
        print(f"   GTO Baseline:     {leak['gto_value']:6.1f}%")
        print(f"   Deviation:        {leak['delta']:+6.1f}%")
        print(f"   EV Loss:          {leak['ev_loss_bb100']:.2f} BB/100")

    # Show recommendations
    print("\n" + "-" * 80)
    print("ACTION RECOMMENDATIONS:")
    print("-" * 80)
    for i, rec in enumerate(leak_analysis['recommendations'], 1):
        print(f"\n{i}. {rec['stat_display']} [{rec['severity']}]")
        print(f"   {rec['recommendation']}")
        print(f"   EV Impact: {rec['ev_impact']}")

    return detector


def demo_study_plan(detector, player_stats):
    """Demonstrate study plan generation"""
    print_header("DEMO 3: PERSONALIZED STUDY PLAN")

    print("\nGenerating study plan with 3 focus areas...")
    study_plan = detector.get_study_plan(player_stats, sample_size=250, focus_areas=3)

    print(f"✓ Created study plan")
    print(f"✓ Focus areas: {study_plan['focus_areas']}")
    print(f"✓ Total estimated time: {study_plan['total_estimated_hours']:.1f} hours")

    print("\n" + "-" * 80)
    print("STUDY PLAN:")
    print("-" * 80)

    for i, task_group in enumerate(study_plan['study_tasks'], 1):
        leak = task_group['leak']
        tasks = task_group['tasks']
        time = task_group['estimated_study_time']

        print(f"\nFOCUS AREA #{i}: {leak['stat_display_name']}")
        print(f"Severity: {leak['severity']} | Priority: {leak['priority_score']:.2f}")
        print(f"Estimated Study Time: {time} minutes ({time/60:.1f} hours)")
        print(f"\nTasks:")
        for j, task in enumerate(tasks, 1):
            print(f"  {j}. {task}")

    print("\n" + "-" * 80)
    print(f"TOTAL STUDY TIME: {study_plan['total_estimated_hours']:.1f} hours")
    print("-" * 80)


def demo_improvement_tracking(detector):
    """Demonstrate improvement tracking over time"""
    print_header("DEMO 4: IMPROVEMENT TRACKING")

    print("\nSimulating 3 sessions over 2 weeks...")

    # Session 1 (2 weeks ago) - Many leaks
    session1_stats = {
        'vpip': 35.0, 'pfr': 15.0, 'three_bet': 5.0,
        'cbet_freq_flop': 45.0, 'fold_vs_cbet_flop': 55.0,
        'wtsd': 30.0, 'w_sd': 45.0
    }
    detector.detect_leaks(
        session1_stats,
        sample_size=200,
        session_date=datetime.now() - timedelta(days=14)
    )
    print("✓ Session 1 recorded (14 days ago)")

    # Session 2 (1 week ago) - Some improvement
    session2_stats = {
        'vpip': 30.0, 'pfr': 17.0, 'three_bet': 6.5,
        'cbet_freq_flop': 52.0, 'fold_vs_cbet_flop': 48.0,
        'wtsd': 27.0, 'w_sd': 47.0
    }
    detector.detect_leaks(
        session2_stats,
        sample_size=250,
        session_date=datetime.now() - timedelta(days=7)
    )
    print("✓ Session 2 recorded (7 days ago)")

    # Session 3 (today) - More improvement
    session3_stats = {
        'vpip': 27.0, 'pfr': 19.0, 'three_bet': 7.5,
        'cbet_freq_flop': 58.0, 'fold_vs_cbet_flop': 44.0,
        'wtsd': 25.5, 'w_sd': 49.0
    }
    detector.detect_leaks(
        session3_stats,
        sample_size=300,
        session_date=datetime.now()
    )
    print("✓ Session 3 recorded (today)")

    # Track improvement
    print("\n" + "-" * 80)
    print("IMPROVEMENT ANALYSIS:")
    print("-" * 80)

    improvement = detector.track_improvement(days=30)

    if improvement['status'] == 'success':
        print(f"\nTime Period:          {improvement['time_period_days']} days")
        print(f"Sessions Analyzed:    {improvement['sessions_analyzed']}")
        print(f"Overall Score:        {improvement['overall_improvement_score']:.1f}")
        print(f"Trend:                {improvement['trending'].upper()}")

        print("\n" + "-" * 80)
        print("STAT-BY-STAT IMPROVEMENTS:")
        print("-" * 80)

        for imp in improvement['improvements'][:5]:
            status = "✓ FIXED" if imp.get('fixed') else ("✓ IMPROVED" if imp['improved'] else "✗ WORSE")
            print(f"\n{imp['stat_display']}: {status}")
            print(f"  First session:  {imp['first_deviation']:.2f}% deviation")
            print(f"  Last session:   {imp['last_deviation']:.2f}% deviation")
            print(f"  Change:         {imp['change']:+.2f}% ({'better' if imp['improved'] else 'worse'})")

    # Persistent leaks
    print("\n" + "-" * 80)
    print("PERSISTENT LEAKS (appear in multiple sessions):")
    print("-" * 80)

    persistent = detector.identify_persistent_leaks(min_occurrences=2)
    if persistent:
        for i, leak in enumerate(persistent[:3], 1):
            print(f"\n{i}. {leak['stat_display_name']}")
            print(f"   Appeared in {leak['occurrences']}/{len(detector.leak_history)} sessions")
            print(f"   Persistence Rate: {leak['persistence_rate']:.0f}%")
            print(f"   Current Deviation: {leak['delta']:+.1f}%")
    else:
        print("\nNo persistent leaks found (great job!)")


def demo_formatted_report(detector, player_stats):
    """Demonstrate formatted leak report"""
    print_header("DEMO 5: FORMATTED LEAK REPORT")

    leak_analysis = detector.detect_leaks(player_stats, sample_size=250)
    report = detector.format_leak_report(leak_analysis)

    print(report)


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PLO MASTERY SUITE - ANALYSIS DEMO" + " " * 25 + "║")
    print("║" + " " * 20 + "Leak Detection & GTO Comparison" + " " * 27 + "║")
    print("╚" + "=" * 78 + "╝")

    # Run demos
    player_stats = demo_gto_comparison()
    detector = demo_leak_detector(player_stats)
    demo_study_plan(detector, player_stats)
    demo_improvement_tracking(detector)
    demo_formatted_report(detector, player_stats)

    # Final summary
    print_header("DEMO COMPLETE")
    print("\n✅ All analysis features demonstrated successfully!")
    print("\nFeatures shown:")
    print("  1. GTO Comparison - Compare stats against optimal baselines")
    print("  2. Leak Detection - Identify and prioritize leaks")
    print("  3. Study Plans - Generate personalized study tasks")
    print("  4. Improvement Tracking - Monitor progress over time")
    print("  5. Formatted Reports - Professional leak reports")
    print("\nNext steps:")
    print("  - Parse your hand history files")
    print("  - Calculate your actual stats")
    print("  - Run leak detection on your data")
    print("  - Follow the study plan to improve!")
    print()


if __name__ == '__main__':
    main()
