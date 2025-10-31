#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ANALYSE RAPIDE DE VOS STATS PLO

Instructions:
1. Remplacez les valeurs dans la section MES_STATS ci-dessous
2. Lancez le script: python3 analyser_mes_stats.py
3. Consultez les résultats et suivez le plan d'étude

"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.analysis import GTOComparator, LeakDetector

# ============================================================================
# 📊 VOS STATS - MODIFIEZ ICI
# ============================================================================

# Entrez vos statistiques ici (valeurs en pourcentage)
# Si vous n'avez pas une stat, commentez la ligne avec # ou supprimez-la

MES_STATS = {
    # === PREFLOP ===
    'vpip': 28.0,           # % de mains où vous mettez de l'argent volontairement
    'pfr': 20.0,            # % de mains où vous raisez preflop
    'three_bet': 8.5,       # % de 3-bets face à une raise
    'fold_vs_3bet': 56.0,   # % de fold face à un 3-bet
    # 'fold_vs_3bet_ip': 53.0,   # % fold vs 3-bet en position
    # 'fold_vs_3bet_oop': 60.0,  # % fold vs 3-bet hors position
    # 'four_bet': 11.0,          # % de 4-bets
    # 'fold_vs_4bet': 66.0,      # % fold vs 4-bet

    # === POSTFLOP AGGRESSION ===
    'cbet_freq_flop': 58.0,    # % de c-bet au flop
    'cbet_freq_turn': 44.0,    # % de c-bet à la turn
    # 'cbet_freq_river': 39.0,   # % de c-bet à la river
    # 'double_barrel': 48.0,     # % de double barrel
    # 'triple_barrel': 43.0,     # % de triple barrel

    # === POSTFLOP DEFENSE ===
    'fold_vs_cbet_flop': 43.0,  # % fold vs c-bet flop
    # 'fold_vs_cbet_turn': 49.0,  # % fold vs c-bet turn
    # 'fold_vs_cbet_river': 53.0, # % fold vs c-bet river

    # === RIVER ===
    'wtsd': 26.0,    # % went to showdown
    'w_sd': 50.0,    # % won at showdown
}

# Nombre de mains analysées (plus c'est grand, plus c'est fiable)
# Minimum: 100 | Recommandé: 500+ | Idéal: 1000+
NOMBRE_DE_MAINS = 500

# Vos stakes (pour les baselines GTO adaptées)
# Options: 'PLO50', 'PLO100', 'PLO200'
MES_STAKES = 'PLO100'

# Nombre de zones de focus dans le plan d'étude
# Recommandé: 2-3 pour rester concentré
ZONES_FOCUS = 3

# ============================================================================
# 🔍 ANALYSE - NE MODIFIEZ PAS CETTE SECTION
# ============================================================================

def afficher_header(titre):
    """Affiche un header formaté"""
    print("\n" + "=" * 80)
    print(f"  {titre}")
    print("=" * 80)


def main():
    # Validation
    if not MES_STATS:
        print("❌ ERREUR: Aucune statistique entrée!")
        print("→ Éditez ce fichier et remplissez la section MES_STATS")
        return

    if NOMBRE_DE_MAINS < 50:
        print("⚠️  ATTENTION: Échantillon très petit (< 50 mains)")
        print("→ Les résultats seront peu fiables")
        print()

    # Bannière
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "ANALYSE DE VOS STATS PLO" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")

    print(f"\n📊 Statistiques fournies: {len(MES_STATS)}")
    print(f"🎲 Taille d'échantillon: {NOMBRE_DE_MAINS} mains")
    print(f"💰 Stakes: {MES_STAKES}")
    print(f"✅ Fiabilité: {'OUI' if NOMBRE_DE_MAINS >= 100 else 'NON - augmentez à 100+ mains'}")

    # ========================================================================
    # ÉTAPE 1: COMPARAISON GTO
    # ========================================================================
    afficher_header("ÉTAPE 1/4: COMPARAISON AVEC GTO")

    comparator = GTOComparator(stakes=MES_STAKES)

    # Obtenir tous les leaks
    leaks = comparator.get_leaks(MES_STATS, min_severity='MEDIUM')

    if not leaks:
        print("\n🎉 EXCELLENT! Aucun leak détecté!")
        print("→ Toutes vos stats sont dans la plage GTO optimale")
    else:
        print(f"\n⚠️  {len(leaks)} LEAKS DÉTECTÉS\n")

        # Afficher top 5
        print("TOP 5 LEAKS:")
        print("-" * 80)
        for i, leak in enumerate(leaks[:5], 1):
            ev_loss = comparator.calculate_ev_loss(leak, hands_per_hour=100, hours_played=10)

            # Emoji selon sévérité
            emoji = "🔴" if leak['severity'] == 'CRITICAL' else \
                    "🟠" if leak['severity'] == 'HIGH' else \
                    "🟡" if leak['severity'] == 'MEDIUM' else "🟢"

            print(f"\n{emoji} {i}. {leak['stat_display_name']} [{leak['severity']}]")
            print(f"   Votre valeur:     {leak['player_value']:6.1f}%")
            print(f"   GTO baseline:     {leak['gto_value']:6.1f}%")
            print(f"   Déviation:        {leak['delta']:+6.1f}% ({leak['direction']})")
            print(f"   Perte EV estimée: {ev_loss['ev_loss_bb100']:.2f} BB/100")
            print(f"   Sur 10h de jeu:   ~{ev_loss['total_ev_loss_bb']:.0f} BB perdus")

    # Score global
    summary = comparator.generate_comparison_summary(MES_STATS, sample_size=NOMBRE_DE_MAINS)

    print("\n" + "-" * 80)
    print("📈 SCORE GLOBAL")
    print("-" * 80)
    print(f"Score d'optimisation: {summary['overall_score']:.1f}%")
    print(f"Stats optimales:      {summary['stats_within_threshold']}/{summary['total_stats_analyzed']}")

    # Breakdown par sévérité
    if summary['total_leaks'] > 0:
        print(f"\nBreakdown des leaks:")
        if summary['severity_breakdown']['CRITICAL'] > 0:
            print(f"  🔴 CRITICAL: {summary['severity_breakdown']['CRITICAL']}")
        if summary['severity_breakdown']['HIGH'] > 0:
            print(f"  🟠 HIGH:     {summary['severity_breakdown']['HIGH']}")
        if summary['severity_breakdown']['MEDIUM'] > 0:
            print(f"  🟡 MEDIUM:   {summary['severity_breakdown']['MEDIUM']}")

    # ========================================================================
    # ÉTAPE 2: DÉTECTION AVANCÉE
    # ========================================================================
    afficher_header("ÉTAPE 2/4: ANALYSE DÉTAILLÉE DES LEAKS")

    detector = LeakDetector(stakes=MES_STAKES)
    analyse = detector.detect_leaks(MES_STATS, sample_size=NOMBRE_DE_MAINS)

    # Breakdown par catégorie
    print("\n📊 LEAKS PAR CATÉGORIE:")
    print("-" * 80)
    categories_fr = {
        'preflop': 'Preflop',
        'postflop_aggression': 'Postflop - Agression',
        'postflop_defense': 'Postflop - Défense',
        'river': 'River',
        'positional': 'Positionnelles',
        'pot_type': 'Type de pot',
        'advanced': 'Avancées'
    }

    for category, leaks_list in analyse['leaks_by_category'].items():
        nom_cat = categories_fr.get(category, category)
        print(f"{nom_cat:30s}: {len(leaks_list)} leak(s)")

    # Top priorités
    if analyse['top_5_priorities']:
        print("\n🎯 TOP PRIORITÉS (par score):")
        print("-" * 80)
        for i, leak in enumerate(analyse['top_5_priorities'], 1):
            emoji = "🔴" if leak['severity'] == 'CRITICAL' else \
                    "🟠" if leak['severity'] == 'HIGH' else \
                    "🟡" if leak['severity'] == 'MEDIUM' else "🟢"

            print(f"{emoji} {i}. {leak['stat_display_name']}")
            print(f"     Score priorité: {leak['priority_score']:.2f}/4.0 | "
                  f"Perte EV: {leak['ev_loss_bb100']:.2f} BB/100")

    # ========================================================================
    # ÉTAPE 3: RECOMMANDATIONS
    # ========================================================================
    afficher_header("ÉTAPE 3/4: RECOMMANDATIONS D'ACTION")

    if analyse['recommendations']:
        for i, rec in enumerate(analyse['recommendations'], 1):
            emoji = "🔴" if rec['severity'] == 'CRITICAL' else \
                    "🟠" if rec['severity'] == 'HIGH' else \
                    "🟡" if rec['severity'] == 'MEDIUM' else "🟢"

            print(f"\n{emoji} {i}. {rec['stat_display']} [{rec['severity']}]")
            print(f"   → {rec['recommendation']}")
            print(f"   💸 Impact EV: {rec['ev_impact']}")
    else:
        print("\n✅ Aucune recommandation - continuez votre bon jeu!")

    # ========================================================================
    # ÉTAPE 4: PLAN D'ÉTUDE
    # ========================================================================
    afficher_header("ÉTAPE 4/4: VOTRE PLAN D'ÉTUDE PERSONNALISÉ")

    if leaks:
        study_plan = detector.get_study_plan(
            MES_STATS,
            sample_size=NOMBRE_DE_MAINS,
            focus_areas=min(ZONES_FOCUS, len(leaks))
        )

        print(f"\n📚 Plan d'étude avec {len(study_plan['study_tasks'])} zone(s) de focus")
        print(f"⏱️  Temps total estimé: {study_plan['total_estimated_hours']:.1f} heures")

        for i, task_group in enumerate(study_plan['study_tasks'], 1):
            leak = task_group['leak']
            tasks = task_group['tasks']
            temps = task_group['estimated_study_time']

            emoji = "🔴" if leak['severity'] == 'CRITICAL' else \
                    "🟠" if leak['severity'] == 'HIGH' else \
                    "🟡" if leak['severity'] == 'MEDIUM' else "🟢"

            print("\n" + "-" * 80)
            print(f"{emoji} FOCUS #{i}: {leak['stat_display_name']}")
            print("-" * 80)
            print(f"Sévérité:      {leak['severity']}")
            print(f"Priorité:      {leak['priority_score']:.2f}/4.0")
            print(f"Temps estimé:  {temps} minutes ({temps/60:.1f}h)")
            print(f"\nTâches à accomplir:")

            for j, task in enumerate(tasks, 1):
                # Vérifier si c'est une tâche prioritaire
                if 'PRIORITY' in task:
                    print(f"  ⭐ {j}. {task}")
                else:
                    print(f"     {j}. {task}")
    else:
        print("\n✅ Pas de plan d'étude nécessaire - vos stats sont optimales!")

    # ========================================================================
    # CONCLUSION
    # ========================================================================
    afficher_header("📊 RÉSUMÉ DE L'ANALYSE")

    print(f"\n✓ Stats analysées:        {len(MES_STATS)}")
    print(f"✓ Taille échantillon:     {NOMBRE_DE_MAINS} mains")
    print(f"✓ Leaks détectés:         {len(leaks)}")
    print(f"✓ Score d'optimisation:   {summary['overall_score']:.1f}%")

    if leaks:
        total_ev_loss = sum(
            comparator.calculate_ev_loss(leak)['ev_loss_bb100']
            for leak in leaks[:5]
        )
        print(f"✓ Perte EV totale (top5):  ~{total_ev_loss:.2f} BB/100")
        print(f"✓ Temps d'étude suggéré:   {study_plan['total_estimated_hours']:.1f} heures")

    print("\n" + "=" * 80)

    if leaks:
        print("\n🎯 PROCHAINES ÉTAPES:")
        print(f"   1. Concentrez-vous sur le leak #{1}: {leaks[0]['stat_display_name']}")
        print("   2. Suivez les tâches du plan d'étude ci-dessus")
        print("   3. Réanalysez vos stats après 500-1000 mains")
        print("   4. Trackez votre progression!")
    else:
        print("\n🎉 FÉLICITATIONS!")
        print("   Vos stats sont toutes dans la plage GTO optimale!")
        print("   Continuez ainsi et n'oubliez pas de réanalyser régulièrement.")

    print("\n💾 Pour sauvegarder ce rapport:")
    print("   python3 analyser_mes_stats.py > mon_rapport.txt")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analyse interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ ERREUR: {e}")
        print("\n💡 Vérifiez que:")
        print("   - Vous êtes dans le bon répertoire (/home/user/garvazz)")
        print("   - Les modules sont correctement installés")
        print("   - Vos stats sont au bon format (dictionnaire Python)")
        import traceback
        print("\nDétails de l'erreur:")
        traceback.print_exc()
