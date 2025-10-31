#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 PLO Mastery Suite - Application Web
Page d'accueil et navigation principale
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis import GTOComparator, LeakDetector
from src.stats.definitions import STAT_DEFINITIONS

# Configuration de la page
st.set_page_config(
    page_title="PLO Mastery Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown('<div class="main-header">🎯 PLO Mastery Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analysez, Optimisez, Dominez le PLO 6-max</div>', unsafe_allow_html=True)

    # Barre de séparation
    st.markdown("---")

    # Introduction
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Analyse GTO")
        st.info("""
        Comparez vos statistiques avec les baselines GTO et identifiez vos leaks automatiquement.
        """)

    with col2:
        st.markdown("### 🎓 Plan d'Étude")
        st.success("""
        Recevez un plan d'étude personnalisé basé sur vos leaks prioritaires.
        """)

    with col3:
        st.markdown("### 📈 Suivi Progression")
        st.warning("""
        Trackez votre progression et visualisez l'évolution de vos statistiques.
        """)

    st.markdown("---")

    # Section "Démarrage Rapide"
    st.markdown("## 🚀 Démarrage Rapide")

    st.markdown("""
    Bienvenue dans la **PLO Mastery Suite** ! Cette application vous aide à :

    ✅ **Identifier vos leaks** en comparant vos stats avec les baselines GTO
    ✅ **Prioriser votre travail** grâce au calcul de perte EV
    ✅ **Créer un plan d'étude** personnalisé et optimisé
    ✅ **Suivre votre progression** dans le temps

    ### 📍 Comment utiliser l'application ?

    1. **Rendez-vous sur la page "📊 Analyse Stats"** dans la barre latérale
    2. **Entrez vos statistiques** (manuellement ou importez-les)
    3. **Consultez votre analyse** complète avec visualisations
    4. **Suivez votre plan d'étude** personnalisé
    5. **Trackez votre progression** au fil du temps
    """)

    st.markdown("---")

    # Statistiques supportées
    st.markdown("## 📋 Statistiques Supportées")

    # Grouper les stats par catégorie
    categories = {}
    for stat_name, stat_info in STAT_DEFINITIONS.items():
        category = stat_info.get('category', 'Autres')
        if category not in categories:
            categories[category] = []
        categories[category].append(stat_info.get('display_name', stat_name))

    # Mapper les noms de catégories en français
    category_names = {
        'preflop': '🃏 Preflop',
        'postflop_aggression': '💪 Postflop - Agression',
        'postflop_defense': '🛡️ Postflop - Défense',
        'river': '🌊 River',
        'positional': '📍 Positionnelles',
        'pot_type': '🎲 Type de Pot',
        'advanced': '⚡ Avancées'
    }

    cols = st.columns(2)
    for idx, (category, stats) in enumerate(categories.items()):
        with cols[idx % 2]:
            cat_name = category_names.get(category, category)
            with st.expander(f"{cat_name} ({len(stats)} stats)", expanded=False):
                for stat in stats:
                    st.markdown(f"✓ {stat}")

    st.markdown("---")

    # Fonctionnalités
    st.markdown("## ✨ Fonctionnalités Principales")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Analyse Approfondie")
        st.markdown("""
        - Comparaison avec GTO baselines
        - Détection automatique des leaks
        - Calcul de perte EV (BB/100)
        - Score d'optimisation global
        - Breakdown par catégorie
        """)

        st.markdown("### 📚 Plan d'Étude")
        st.markdown("""
        - Priorisation intelligente des leaks
        - Tâches d'étude personnalisées
        - Estimation du temps requis
        - Ressources d'apprentissage
        """)

    with col2:
        st.markdown("### 📊 Visualisations")
        st.markdown("""
        - Graphiques interactifs
        - Comparaison GTO vs Vous
        - Evolution dans le temps
        - Heatmaps de leaks
        """)

        st.markdown("### 💾 Tracking & Export")
        st.markdown("""
        - Historique de vos analyses
        - Tracking de progression
        - Export PDF des rapports
        - Sauvegarde des sessions
        """)

    st.markdown("---")

    # Section FAQ rapide
    st.markdown("## ❓ Questions Fréquentes")

    with st.expander("Combien de mains minimum pour une analyse fiable ?"):
        st.markdown("""
        - **100 mains** : Minimum absolu (peu fiable)
        - **500 mains** : Résultats relativement fiables
        - **1000+ mains** : Excellente fiabilité
        - **5000+ mains** : Fiabilité optimale
        """)

    with st.expander("Je n'ai pas toutes les stats, est-ce grave ?"):
        st.markdown("""
        Non ! Vous pouvez analyser vos stats même si vous n'en avez que quelques-unes.

        **Stats minimales recommandées** (5-6) :
        - VPIP
        - PFR
        - 3-Bet
        - C-Bet Flop
        - Fold vs C-Bet
        - WTSD (optionnel)
        """)

    with st.expander("Les baselines GTO sont-elles fiables ?"):
        st.markdown("""
        Oui ! Nos baselines sont basées sur :
        - **PioSOLVER** pour les ranges optimales
        - **GTO+** pour les stratégies postflop
        - **Données de players high-stakes** (25k+ mains)
        - **Calibration PLO 6-max** spécifique
        """)

    with st.expander("Comment interpréter le score d'optimisation ?"):
        st.markdown("""
        Le score d'optimisation représente le % de stats dans la plage GTO :

        - **90-100%** : Excellent, jeu très optimal
        - **70-89%** : Bon, quelques leaks mineurs
        - **50-69%** : Moyen, plusieurs leaks à corriger
        - **30-49%** : Faible, travail important requis
        - **< 30%** : Critique, révision complète nécessaire
        """)

    st.markdown("---")

    # Call to action
    st.markdown("## 🎯 Prêt à Commencer ?")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        👈 **Utilisez la barre latérale** pour naviguer vers :
        - **📊 Analyse Stats** : Analysez vos statistiques
        - **📈 Dashboard** : Visualisez vos résultats
        - **📚 Plan d'Étude** : Consultez votre plan personnalisé
        - **📊 Progression** : Suivez votre évolution
        """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>PLO Mastery Suite v1.0 | Développé pour les joueurs de PLO 6-max</p>
        <p>Contact: pekinio13@hotmail.fr</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
