#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Page de Suivi de Progression
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Configuration de la page
st.set_page_config(
    page_title="Progression - PLO Mastery Suite",
    page_icon="📊",
    layout="wide"
)

# Style CSS
st.markdown("""
<style>
    .timeline-item {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    .improvement {
        color: #28a745;
        font-weight: bold;
    }
    .regression {
        color: #dc3545;
        font-weight: bold;
    }
    .stable {
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)


def save_analysis_to_history(results):
    """Sauvegarde l'analyse actuelle dans l'historique"""
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'summary': results['summary'],
        'user_stats': results['user_stats'],
        'leaks_count': len(results['leaks']),
        'top_leaks': results['leaks'][:5] if results['leaks'] else [],
        'stakes': results.get('stakes', 'PLO100'),
        'sample_size': results.get('sample_size', 0)
    }

    st.session_state.analysis_history.append(history_entry)

    # Limiter l'historique à 50 entrées
    if len(st.session_state.analysis_history) > 50:
        st.session_state.analysis_history = st.session_state.analysis_history[-50:]


def create_progression_line_chart(history):
    """Crée un graphique de progression du score d'optimisation"""
    if not history:
        return None

    dates = [entry['date'] for entry in history]
    scores = [entry['summary']['overall_score'] for entry in history]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Score d\'Optimisation',
        line=dict(color='rgb(31, 119, 180)', width=3),
        marker=dict(size=10)
    ))

    # Ligne de référence à 70%
    fig.add_hline(y=70, line_dash="dash", line_color="green",
                  annotation_text="Objectif: 70%")

    fig.update_layout(
        title='Évolution du Score d\'Optimisation',
        xaxis_title='Date',
        yaxis_title='Score (%)',
        height=400,
        hovermode='x unified'
    )

    return fig


def create_leaks_evolution_chart(history):
    """Crée un graphique de l'évolution du nombre de leaks"""
    if not history:
        return None

    dates = [entry['date'] for entry in history]
    leaks_counts = [entry['leaks_count'] for entry in history]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=leaks_counts,
        name='Nombre de Leaks',
        marker_color='rgb(220, 53, 69)',
        text=leaks_counts,
        textposition='outside'
    ))

    fig.update_layout(
        title='Évolution du Nombre de Leaks',
        xaxis_title='Date',
        yaxis_title='Nombre de Leaks',
        height=400
    )

    return fig


def create_stats_comparison_radar(history):
    """Crée un radar chart comparant la première et dernière analyse"""
    if len(history) < 2:
        return None

    first_stats = history[0]['user_stats']
    last_stats = history[-1]['user_stats']

    # Prendre les stats communes
    common_stats = set(first_stats.keys()) & set(last_stats.keys())
    common_stats = list(common_stats)[:8]  # Limiter à 8

    if not common_stats:
        return None

    from src.stats.definitions import STAT_DEFINITIONS

    categories = [STAT_DEFINITIONS.get(stat, {}).get('display_name', stat) for stat in common_stats]
    first_values = [first_stats[stat] for stat in common_stats]
    last_values = [last_stats[stat] for stat in common_stats]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=first_values,
        theta=categories,
        fill='toself',
        name=f'Première Analyse ({history[0]["date"]})',
        line_color='rgb(255, 127, 14)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=last_values,
        theta=categories,
        fill='toself',
        name=f'Dernière Analyse ({history[-1]["date"]})',
        line_color='rgb(31, 119, 180)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Comparaison Première vs Dernière Analyse",
        height=500
    )

    return fig


def analyze_improvement(history):
    """Analyse l'amélioration entre la première et dernière analyse"""
    if len(history) < 2:
        return None

    first = history[0]
    last = history[-1]

    improvements = {
        'score_delta': last['summary']['overall_score'] - first['summary']['overall_score'],
        'leaks_delta': first['leaks_count'] - last['leaks_count'],
        'first_date': first['date'],
        'last_date': last['date'],
        'analyses_count': len(history)
    }

    return improvements


def main():
    st.title("📊 Suivi de Progression")
    st.markdown("Trackez votre évolution et mesurez vos progrès au fil du temps")
    st.markdown("---")

    # Initialiser l'historique
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Gestion de l'Historique")

        # Sauvegarder l'analyse actuelle
        if st.session_state.get('analysis_results'):
            if st.button("💾 Sauvegarder l'Analyse Actuelle"):
                save_analysis_to_history(st.session_state.analysis_results)
                st.success("✅ Analyse sauvegardée!")
                st.rerun()

        st.markdown("---")

        # Nombre d'analyses
        st.metric(
            "Analyses Sauvegardées",
            len(st.session_state.analysis_history)
        )

        # Import/Export
        st.markdown("---")
        st.markdown("### 💾 Import/Export")

        # Export
        if st.session_state.analysis_history:
            export_data = json.dumps(st.session_state.analysis_history, indent=2)

            st.download_button(
                label="📥 Exporter Historique",
                data=export_data,
                file_name=f"plo_history_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        # Import
        uploaded_file = st.file_uploader(
            "📤 Importer Historique",
            type=['json'],
            help="Importez un fichier d'historique précédemment exporté"
        )

        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                st.session_state.analysis_history = imported_data
                st.success(f"✅ {len(imported_data)} analyses importées!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur d'import: {e}")

        st.markdown("---")

        # Réinitialiser
        if st.button("🗑️ Effacer l'Historique", type="secondary"):
            if st.button("⚠️ Confirmer la suppression"):
                st.session_state.analysis_history = []
                st.success("Historique effacé")
                st.rerun()

    # Vérifier s'il y a des données
    if not st.session_state.analysis_history:
        st.info("""
        📊 **Commencez à tracker votre progression**

        Pour utiliser cette page :
        1. Analysez vos stats dans la page **📊 Analyse Stats**
        2. Revenez ici et cliquez sur **💾 Sauvegarder l'Analyse Actuelle** (sidebar)
        3. Répétez régulièrement (tous les 500-1000 mains)
        4. Visualisez votre évolution!

        **Recommandé :** Sauvegardez vos analyses :
        - Après chaque session d'étude
        - Tous les 500-1000 mains jouées
        - Après avoir corrigé un leak majeur
        """)

        # Bouton pour aller à l'analyse
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Aller à l'Analyse Stats", use_container_width=True):
                st.switch_page("pages/1_📊_Analyse_Stats.py")

        return

    history = st.session_state.analysis_history

    # Métriques principales
    if len(history) >= 2:
        improvements = analyze_improvement(history)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Score Actuel",
                f"{history[-1]['summary']['overall_score']:.1f}%",
                f"{improvements['score_delta']:+.1f}%"
            )

        with col2:
            st.metric(
                "Leaks Actuels",
                history[-1]['leaks_count'],
                f"{-improvements['leaks_delta']}" if improvements['leaks_delta'] != 0 else "0"
            )

        with col3:
            st.metric(
                "Analyses",
                improvements['analyses_count']
            )

        with col4:
            # Calculer la tendance
            if len(history) >= 3:
                recent_scores = [h['summary']['overall_score'] for h in history[-3:]]
                trend = "📈" if recent_scores[-1] > recent_scores[0] else "📉" if recent_scores[-1] < recent_scores[0] else "➡️"
            else:
                trend = "➡️"

            st.metric(
                "Tendance",
                trend,
                help="Basé sur les 3 dernières analyses"
            )

        st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Graphiques",
        "📋 Historique",
        "🎯 Comparaison",
        "📊 Statistiques"
    ])

    with tab1:
        st.markdown("### 📈 Évolution dans le Temps")

        # Graphique de score
        fig_score = create_progression_line_chart(history)
        if fig_score:
            st.plotly_chart(fig_score, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Graphique de leaks
            fig_leaks = create_leaks_evolution_chart(history)
            if fig_leaks:
                st.plotly_chart(fig_leaks, use_container_width=True)

        with col2:
            # Graphique de sample size
            if history:
                dates = [entry['date'] for entry in history]
                samples = [entry['sample_size'] for entry in history]

                fig_samples = go.Figure()
                fig_samples.add_trace(go.Scatter(
                    x=dates,
                    y=samples,
                    mode='lines+markers',
                    name='Sample Size',
                    fill='tozeroy',
                    line=dict(color='rgb(107, 174, 214)')
                ))

                fig_samples.update_layout(
                    title='Taille des Échantillons',
                    xaxis_title='Date',
                    yaxis_title='Nombre de Mains',
                    height=400
                )

                st.plotly_chart(fig_samples, use_container_width=True)

    with tab2:
        st.markdown("### 📋 Historique des Analyses")

        # Timeline inversée (plus récent en premier)
        for idx, entry in enumerate(reversed(history)):
            real_idx = len(history) - idx - 1

            with st.expander(
                f"📅 {entry['date']} - Score: {entry['summary']['overall_score']:.1f}% - {entry['leaks_count']} leaks",
                expanded=(idx == 0)
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"""
                    **Date :** {entry['date']}
                    **Score d'optimisation :** {entry['summary']['overall_score']:.1f}%
                    **Nombre de leaks :** {entry['leaks_count']}
                    **Stakes :** {entry['stakes']}
                    **Sample size :** {entry['sample_size']} mains
                    """)

                    # Breakdown par sévérité
                    st.markdown("**Breakdown des leaks :**")
                    for sev, count in entry['summary']['severity_breakdown'].items():
                        if count > 0:
                            emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(sev, '⚪')
                            st.markdown(f"{emoji} {sev}: {count}")

                with col2:
                    # Stats analysées
                    st.markdown("**Stats analysées :**")
                    st.markdown(f"{entry['summary']['stats_within_threshold']}/{entry['summary']['total_stats_analyzed']}")

                    # Top leaks
                    if entry['top_leaks']:
                        st.markdown("**Top Leaks:**")
                        for leak in entry['top_leaks'][:3]:
                            st.markdown(f"- {leak['stat_display_name']}")

                # Bouton pour comparer
                if idx > 0:
                    if st.button(f"🔍 Comparer avec analyse précédente", key=f"compare_{real_idx}"):
                        st.session_state.compare_indices = (real_idx - 1, real_idx)
                        st.rerun()

    with tab3:
        st.markdown("### 🎯 Comparaison Détaillée")

        if len(history) >= 2:
            # Sélection des analyses à comparer
            col1, col2 = st.columns(2)

            with col1:
                first_idx = st.selectbox(
                    "Première analyse",
                    range(len(history)),
                    format_func=lambda x: f"{history[x]['date']} ({history[x]['summary']['overall_score']:.1f}%)"
                )

            with col2:
                second_idx = st.selectbox(
                    "Deuxième analyse",
                    range(len(history)),
                    index=len(history) - 1,
                    format_func=lambda x: f"{history[x]['date']} ({history[x]['summary']['overall_score']:.1f}%)"
                )

            if first_idx != second_idx:
                first = history[first_idx]
                second = history[second_idx]

                # Métriques de comparaison
                col1, col2, col3 = st.columns(3)

                with col1:
                    score_diff = second['summary']['overall_score'] - first['summary']['overall_score']
                    st.metric(
                        "Évolution du Score",
                        f"{second['summary']['overall_score']:.1f}%",
                        f"{score_diff:+.1f}%"
                    )

                with col2:
                    leaks_diff = first['leaks_count'] - second['leaks_count']
                    st.metric(
                        "Évolution des Leaks",
                        second['leaks_count'],
                        f"{-leaks_diff:+d}"
                    )

                with col3:
                    sample_diff = second['sample_size'] - first['sample_size']
                    st.metric(
                        "Sample Size",
                        second['sample_size'],
                        f"{sample_diff:+d}"
                    )

                # Radar chart de comparaison
                fig_radar = create_stats_comparison_radar([first, second])
                if fig_radar:
                    st.plotly_chart(fig_radar, use_container_width=True)

                # Tableau de comparaison des stats
                st.markdown("#### Comparaison des Statistiques")

                common_stats = set(first['user_stats'].keys()) & set(second['user_stats'].keys())

                if common_stats:
                    from src.stats.definitions import STAT_DEFINITIONS

                    comparison_data = []
                    for stat_key in common_stats:
                        first_val = first['user_stats'][stat_key]
                        second_val = second['user_stats'][stat_key]
                        diff = second_val - first_val

                        comparison_data.append({
                            'Statistique': STAT_DEFINITIONS.get(stat_key, {}).get('display_name', stat_key),
                            f'Analyse 1': f"{first_val:.1f}%",
                            f'Analyse 2': f"{second_val:.1f}%",
                            'Évolution': f"{diff:+.1f}%",
                            'Tendance': '📈' if diff > 1 else '📉' if diff < -1 else '➡️'
                        })

                    df_comparison = pd.DataFrame(comparison_data)
                    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

        else:
            st.info("Vous avez besoin d'au moins 2 analyses pour faire une comparaison")

    with tab4:
        st.markdown("### 📊 Statistiques Globales")

        if len(history) >= 2:
            improvements = analyze_improvement(history)

            # Résumé de progression
            st.markdown("#### 🎯 Résumé de Progression")

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"""
                **📅 Période**
                - Première analyse : {improvements['first_date']}
                - Dernière analyse : {improvements['last_date']}
                - Nombre d'analyses : {improvements['analyses_count']}
                """)

            with col2:
                if improvements['score_delta'] > 0:
                    st.success(f"""
                    **📈 Amélioration**
                    - Score : +{improvements['score_delta']:.1f}%
                    - Leaks corrigés : {improvements['leaks_delta']}
                    - Tendance : Positive 🎉
                    """)
                elif improvements['score_delta'] < 0:
                    st.warning(f"""
                    **📉 Régression**
                    - Score : {improvements['score_delta']:.1f}%
                    - Nouveaux leaks : {-improvements['leaks_delta']}
                    - Tendance : À surveiller ⚠️
                    """)
                else:
                    st.info("""
                    **➡️ Stable**
                    - Pas de changement significatif
                    - Continuez vos efforts
                    """)

            # Statistiques détaillées
            st.markdown("#### 📈 Statistiques Détaillées")

            scores = [h['summary']['overall_score'] for h in history]
            leaks_counts = [h['leaks_count'] for h in history]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Score Moyen", f"{sum(scores) / len(scores):.1f}%")
                st.metric("Score Max", f"{max(scores):.1f}%")
                st.metric("Score Min", f"{min(scores):.1f}%")

            with col2:
                st.metric("Leaks Moyen", f"{sum(leaks_counts) / len(leaks_counts):.1f}")
                st.metric("Leaks Max", max(leaks_counts))
                st.metric("Leaks Min", min(leaks_counts))

            with col3:
                samples = [h['sample_size'] for h in history]
                st.metric("Mains Totales", f"{sum(samples):,}")
                st.metric("Moyenne/Analyse", f"{sum(samples) // len(samples):,}")

            # Leaks récurrents
            st.markdown("#### 🔄 Leaks Récurrents")

            leak_frequency = {}
            for entry in history:
                for leak in entry['top_leaks']:
                    stat_name = leak['stat_display_name']
                    leak_frequency[stat_name] = leak_frequency.get(stat_name, 0) + 1

            if leak_frequency:
                # Trier par fréquence
                sorted_leaks = sorted(leak_frequency.items(), key=lambda x: x[1], reverse=True)

                st.markdown("**Leaks apparaissant le plus souvent:**")
                for leak_name, count in sorted_leaks[:10]:
                    pct = (count / len(history)) * 100
                    st.markdown(f"- **{leak_name}** : {count} fois ({pct:.0f}%)")

                st.warning("""
                💡 **Conseil :** Les leaks récurrents nécessitent un travail approfondi.
                Concentrez-vous sur ces points faibles persistants.
                """)

        else:
            st.info("Vous avez besoin de plus d'analyses pour afficher des statistiques globales")


if __name__ == "__main__":
    main()
