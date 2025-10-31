#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Page d'Analyse des Statistiques PLO
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.analysis import GTOComparator, LeakDetector
from src.stats.definitions import STAT_DEFINITIONS

# Configuration de la page
st.set_page_config(
    page_title="Analyse Stats - PLO Mastery Suite",
    page_icon="📊",
    layout="wide"
)

# Style CSS
st.markdown("""
<style>
    .leak-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .leak-critical {
        background-color: #ffe6e6;
        border-color: #dc3545;
    }
    .leak-high {
        background-color: #fff3e6;
        border-color: #fd7e14;
    }
    .leak-medium {
        background-color: #fffbe6;
        border-color: #ffc107;
    }
    .leak-low {
        background-color: #e6f7ff;
        border-color: #17a2b8;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def create_comparison_chart(leaks, comparator):
    """Crée un graphique de comparaison GTO vs Joueur"""
    if not leaks:
        return None

    # Prendre les 10 premiers leaks
    top_leaks = leaks[:10]

    stat_names = [leak['stat_display_name'] for leak in top_leaks]
    player_values = [leak['player_value'] for leak in top_leaks]
    gto_values = [leak['gto_value'] for leak in top_leaks]

    fig = go.Figure()

    # Barres pour les valeurs du joueur
    fig.add_trace(go.Bar(
        name='Vos Stats',
        x=stat_names,
        y=player_values,
        marker_color='rgb(255, 127, 14)',
        text=[f"{v:.1f}%" for v in player_values],
        textposition='outside'
    ))

    # Barres pour les valeurs GTO
    fig.add_trace(go.Bar(
        name='GTO Baseline',
        x=stat_names,
        y=gto_values,
        marker_color='rgb(31, 119, 180)',
        text=[f"{v:.1f}%" for v in gto_values],
        textposition='outside'
    ))

    fig.update_layout(
        title='Comparaison de vos Stats avec les Baselines GTO',
        xaxis_title='Statistique',
        yaxis_title='Valeur (%)',
        barmode='group',
        height=500,
        hovermode='x unified'
    )

    return fig


def create_leak_severity_pie(leaks):
    """Crée un graphique circulaire de la sévérité des leaks"""
    if not leaks:
        return None

    severity_counts = {}
    for leak in leaks:
        sev = leak['severity']
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    colors = {
        'CRITICAL': '#dc3545',
        'HIGH': '#fd7e14',
        'MEDIUM': '#ffc107',
        'LOW': '#17a2b8'
    }

    fig = go.Figure(data=[go.Pie(
        labels=list(severity_counts.keys()),
        values=list(severity_counts.values()),
        marker=dict(colors=[colors.get(sev, '#ccc') for sev in severity_counts.keys()]),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value} leaks<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title='Répartition des Leaks par Sévérité',
        height=400
    )

    return fig


def create_ev_loss_chart(leaks, comparator):
    """Crée un graphique de perte EV"""
    if not leaks:
        return None

    top_leaks = leaks[:10]

    stat_names = [leak['stat_display_name'] for leak in top_leaks]
    ev_losses = [comparator.calculate_ev_loss(leak)['ev_loss_bb100'] for leak in top_leaks]

    fig = go.Figure(data=[
        go.Bar(
            x=stat_names,
            y=ev_losses,
            marker_color='rgb(220, 53, 69)',
            text=[f"{ev:.2f} BB/100" for ev in ev_losses],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title='Perte EV Estimée par Leak (BB/100)',
        xaxis_title='Statistique',
        yaxis_title='Perte EV (BB/100)',
        height=400
    )

    return fig


def main():
    st.title("📊 Analyse de vos Statistiques PLO")
    st.markdown("---")

    # Initialiser la session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        stakes = st.selectbox(
            "Stakes",
            ["PLO50", "PLO100", "PLO200"],
            index=1
        )

        sample_size = st.number_input(
            "Nombre de mains",
            min_value=50,
            max_value=100000,
            value=500,
            step=50,
            help="Recommandé: 500+ mains pour une analyse fiable"
        )

        min_severity = st.selectbox(
            "Sévérité minimale",
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            index=1,
            help="Afficher uniquement les leaks au-dessus de cette sévérité"
        )

        st.markdown("---")

        # Charger stats d'exemple
        if st.button("📋 Charger des stats d'exemple"):
            st.session_state.example_stats = {
                'vpip': 35.0,
                'pfr': 22.0,
                'three_bet': 12.5,
                'fold_vs_3bet': 58.0,
                'cbet_freq_flop': 52.0,
                'cbet_freq_turn': 38.0,
                'fold_vs_cbet_flop': 48.0,
                'wtsd': 28.0,
                'w_sd': 48.0,
            }
            st.success("Stats d'exemple chargées!")

    # Tabs pour les différentes méthodes d'input
    tab1, tab2 = st.tabs(["📝 Saisie Manuelle", "📁 Import Fichier"])

    with tab1:
        st.markdown("### Entrez vos statistiques")

        # Organiser par catégories
        categories = {
            'Preflop': ['vpip', 'pfr', 'three_bet', 'fold_vs_3bet', 'four_bet', 'fold_vs_4bet'],
            'Postflop - Agression': ['cbet_freq_flop', 'cbet_freq_turn', 'cbet_freq_river', 'double_barrel', 'triple_barrel'],
            'Postflop - Défense': ['fold_vs_cbet_flop', 'fold_vs_cbet_turn', 'fold_vs_cbet_river'],
            'River': ['wtsd', 'w_sd']
        }

        user_stats = {}

        # Vérifier si on a des stats d'exemple
        example_stats = st.session_state.get('example_stats', {})

        for category, stats in categories.items():
            with st.expander(f"📊 {category}", expanded=(category == 'Preflop')):
                cols = st.columns(2)
                for idx, stat_key in enumerate(stats):
                    if stat_key in STAT_DEFINITIONS:
                        stat_info = STAT_DEFINITIONS[stat_key]
                        display_name = stat_info.get('display_name', stat_key)

                        with cols[idx % 2]:
                            default_value = example_stats.get(stat_key, 0.0)
                            value = st.number_input(
                                display_name,
                                min_value=0.0,
                                max_value=100.0,
                                value=float(default_value),
                                step=0.1,
                                key=f"input_{stat_key}",
                                help=stat_info.get('description', '')
                            )
                            if value > 0:
                                user_stats[stat_key] = value

    with tab2:
        st.markdown("### Import depuis un fichier")
        st.info("Fonctionnalité d'import à venir - Support PT4/HM3 CSV")

        uploaded_file = st.file_uploader(
            "Choisissez un fichier CSV",
            type=['csv'],
            help="Export depuis PokerTracker 4 ou Hold'em Manager 3"
        )

        if uploaded_file is not None:
            st.warning("⚠️ Parsing CSV à implémenter")

    # Bouton d'analyse
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 LANCER L'ANALYSE",
            type="primary",
            use_container_width=True
        )

    # Lancer l'analyse
    if analyze_button:
        if len(user_stats) < 3:
            st.error("❌ Veuillez entrer au moins 3 statistiques pour lancer l'analyse")
        else:
            with st.spinner("🔄 Analyse en cours..."):
                # Créer les analyseurs
                comparator = GTOComparator(stakes=stakes)
                detector = LeakDetector(stakes=stakes)

                # Obtenir les leaks
                leaks = comparator.get_leaks(user_stats, min_severity=min_severity)

                # Analyse détaillée
                analysis = detector.detect_leaks(user_stats, sample_size=sample_size)

                # Résumé
                summary = comparator.generate_comparison_summary(user_stats, sample_size=sample_size)

                # Plan d'étude
                study_plan = detector.get_study_plan(user_stats, sample_size=sample_size, focus_areas=3)

                # Stocker dans session state
                st.session_state.analysis_results = {
                    'user_stats': user_stats,
                    'leaks': leaks,
                    'analysis': analysis,
                    'summary': summary,
                    'study_plan': study_plan,
                    'comparator': comparator,
                    'detector': detector,
                    'stakes': stakes,
                    'sample_size': sample_size
                }

            st.success("✅ Analyse terminée!")
            st.rerun()

    # Afficher les résultats
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results

        st.markdown("---")
        st.markdown("## 📈 Résultats de l'Analyse")

        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Score d'Optimisation",
                f"{results['summary']['overall_score']:.1f}%",
                help="% de stats dans la plage GTO optimale"
            )

        with col2:
            st.metric(
                "Leaks Détectés",
                results['summary']['total_leaks'],
                delta=f"-{results['summary']['total_leaks']}" if results['summary']['total_leaks'] > 0 else "0",
                delta_color="inverse"
            )

        with col3:
            st.metric(
                "Stats Analysées",
                f"{results['summary']['stats_within_threshold']}/{results['summary']['total_stats_analyzed']}"
            )

        with col4:
            if results['leaks']:
                total_ev_loss = sum(
                    results['comparator'].calculate_ev_loss(leak)['ev_loss_bb100']
                    for leak in results['leaks'][:5]
                )
                st.metric(
                    "Perte EV (Top 5)",
                    f"{total_ev_loss:.2f} BB/100",
                    delta=f"-{total_ev_loss:.2f}",
                    delta_color="inverse"
                )

        st.markdown("---")

        # Tabs pour les différentes vues
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Leaks Détectés", "📊 Visualisations", "📚 Plan d'Étude", "📋 Détails"])

        with tab1:
            if results['leaks']:
                st.markdown(f"### ⚠️ {len(results['leaks'])} Leaks Détectés")

                for idx, leak in enumerate(results['leaks'], 1):
                    ev_loss = results['comparator'].calculate_ev_loss(leak, hours_played=10)

                    # Emoji et couleur selon sévérité
                    severity_config = {
                        'CRITICAL': ('🔴', 'leak-critical'),
                        'HIGH': ('🟠', 'leak-high'),
                        'MEDIUM': ('🟡', 'leak-medium'),
                        'LOW': ('🟢', 'leak-low')
                    }
                    emoji, css_class = severity_config.get(leak['severity'], ('⚪', 'leak-low'))

                    st.markdown(f"""
                    <div class="leak-card {css_class}">
                        <h4>{emoji} #{idx} - {leak['stat_display_name']} [{leak['severity']}]</h4>
                        <p>
                            <b>Votre valeur:</b> {leak['player_value']:.1f}% |
                            <b>GTO baseline:</b> {leak['gto_value']:.1f}% |
                            <b>Déviation:</b> {leak['delta']:+.1f}% ({leak['direction']})
                        </p>
                        <p>
                            <b>Perte EV estimée:</b> {ev_loss['ev_loss_bb100']:.2f} BB/100
                            (~{ev_loss['total_ev_loss_bb']:.0f} BB sur 10h de jeu)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.success("🎉 Aucun leak détecté! Toutes vos stats sont dans la plage GTO optimale.")

        with tab2:
            st.markdown("### 📊 Visualisations Graphiques")

            if results['leaks']:
                # Graphique de comparaison
                fig_comparison = create_comparison_chart(results['leaks'], results['comparator'])
                if fig_comparison:
                    st.plotly_chart(fig_comparison, use_container_width=True)

                col1, col2 = st.columns(2)

                with col1:
                    # Graphique de sévérité
                    fig_severity = create_leak_severity_pie(results['leaks'])
                    if fig_severity:
                        st.plotly_chart(fig_severity, use_container_width=True)

                with col2:
                    # Graphique de perte EV
                    fig_ev = create_ev_loss_chart(results['leaks'], results['comparator'])
                    if fig_ev:
                        st.plotly_chart(fig_ev, use_container_width=True)

            else:
                st.info("Aucun graphique à afficher - pas de leaks détectés")

        with tab3:
            st.markdown("### 📚 Votre Plan d'Étude Personnalisé")

            if results['study_plan'] and results['study_plan']['study_tasks']:
                st.info(f"⏱️ Temps total estimé: **{results['study_plan']['total_estimated_hours']:.1f} heures**")

                for idx, task_group in enumerate(results['study_plan']['study_tasks'], 1):
                    leak = task_group['leak']
                    tasks = task_group['tasks']
                    time_min = task_group['estimated_study_time']

                    severity_emoji = {
                        'CRITICAL': '🔴',
                        'HIGH': '🟠',
                        'MEDIUM': '🟡',
                        'LOW': '🟢'
                    }.get(leak['severity'], '⚪')

                    with st.expander(
                        f"{severity_emoji} Focus #{idx}: {leak['stat_display_name']} - {time_min} min",
                        expanded=(idx == 1)
                    ):
                        st.markdown(f"""
                        **Sévérité:** {leak['severity']}
                        **Score de priorité:** {leak['priority_score']:.2f}/4.0
                        **Temps estimé:** {time_min} minutes ({time_min/60:.1f}h)
                        """)

                        st.markdown("**Tâches à accomplir:**")
                        for task_idx, task in enumerate(tasks, 1):
                            if 'PRIORITY' in task:
                                st.markdown(f"⭐ {task_idx}. {task}")
                            else:
                                st.markdown(f"{task_idx}. {task}")

            else:
                st.success("✅ Pas de plan d'étude nécessaire - vos stats sont optimales!")

        with tab4:
            st.markdown("### 📋 Détails de l'Analyse")

            # Breakdown par catégorie
            st.markdown("#### Leaks par Catégorie")

            categories_fr = {
                'preflop': 'Preflop',
                'postflop_aggression': 'Postflop - Agression',
                'postflop_defense': 'Postflop - Défense',
                'river': 'River',
                'positional': 'Positionnelles',
                'pot_type': 'Type de pot',
                'advanced': 'Avancées'
            }

            category_data = []
            for category, leaks_list in results['analysis']['leaks_by_category'].items():
                category_data.append({
                    'Catégorie': categories_fr.get(category, category),
                    'Nombre de Leaks': len(leaks_list)
                })

            if category_data:
                df_categories = pd.DataFrame(category_data)
                st.dataframe(df_categories, use_container_width=True, hide_index=True)

            # Breakdown par sévérité
            st.markdown("#### Breakdown par Sévérité")

            severity_data = []
            for sev, count in results['summary']['severity_breakdown'].items():
                if count > 0:
                    severity_data.append({
                        'Sévérité': sev,
                        'Nombre': count
                    })

            if severity_data:
                df_severity = pd.DataFrame(severity_data)
                st.dataframe(df_severity, use_container_width=True, hide_index=True)

            # Stats analysées
            st.markdown("#### Statistiques Analysées")
            st.json(results['user_stats'])


if __name__ == "__main__":
    main()
