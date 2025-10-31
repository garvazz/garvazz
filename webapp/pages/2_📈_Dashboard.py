#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📈 Dashboard de Visualisation
"""

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.stats.definitions import STAT_DEFINITIONS

# Configuration de la page
st.set_page_config(
    page_title="Dashboard - PLO Mastery Suite",
    page_icon="📈",
    layout="wide"
)


def create_radar_chart(user_stats, gto_baselines):
    """Crée un radar chart comparant le joueur avec GTO"""
    categories = list(user_stats.keys())[:8]  # Limiter à 8 stats pour lisibilité

    player_values = [user_stats[cat] for cat in categories]
    gto_values = [gto_baselines.get(cat, {}).get('optimal', 50) for cat in categories]

    # Normaliser les valeurs (0-100)
    player_norm = [(v / 100) * 100 for v in player_values]
    gto_norm = [(v / 100) * 100 for v in gto_values]

    fig = go.Figure()

    # Trace pour le joueur
    fig.add_trace(go.Scatterpolar(
        r=player_norm,
        theta=[STAT_DEFINITIONS.get(cat, {}).get('display_name', cat) for cat in categories],
        fill='toself',
        name='Vos Stats',
        line_color='rgb(255, 127, 14)'
    ))

    # Trace pour GTO
    fig.add_trace(go.Scatterpolar(
        r=gto_norm,
        theta=[STAT_DEFINITIONS.get(cat, {}).get('display_name', cat) for cat in categories],
        fill='toself',
        name='GTO Baseline',
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
        title="Comparaison Radar - Vous vs GTO",
        height=600
    )

    return fig


def create_heatmap(leaks):
    """Crée une heatmap des leaks par catégorie et sévérité"""
    if not leaks:
        return None

    # Organiser par catégorie
    categories = {}
    for leak in leaks:
        stat_name = leak['stat_display_name']
        severity = leak['severity']

        # Déterminer la catégorie
        for stat_key, stat_info in STAT_DEFINITIONS.items():
            if stat_info.get('display_name') == stat_name:
                category = stat_info.get('category', 'Autres')
                break
        else:
            category = 'Autres'

        if category not in categories:
            categories[category] = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

        categories[category][severity] += 1

    # Créer le DataFrame
    df = pd.DataFrame(categories).T
    df = df.fillna(0)

    fig = px.imshow(
        df,
        labels=dict(x="Sévérité", y="Catégorie", color="Nombre de Leaks"),
        x=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
        color_continuous_scale='Reds',
        aspect='auto'
    )

    fig.update_layout(
        title="Heatmap des Leaks par Catégorie et Sévérité",
        height=400
    )

    return fig


def create_deviation_chart(leaks):
    """Crée un graphique de déviation par rapport à GTO"""
    if not leaks:
        return None

    stat_names = [leak['stat_display_name'] for leak in leaks[:15]]
    deviations = [leak['delta'] for leak in leaks[:15]]

    # Couleurs selon la direction
    colors = ['rgb(220, 53, 69)' if d > 0 else 'rgb(40, 167, 69)' for d in deviations]

    fig = go.Figure(data=[
        go.Bar(
            x=deviations,
            y=stat_names,
            orientation='h',
            marker_color=colors,
            text=[f"{d:+.1f}%" for d in deviations],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title="Déviation par rapport à GTO (+ = trop élevé, - = trop faible)",
        xaxis_title="Déviation (%)",
        yaxis_title="Statistique",
        height=600,
        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )

    return fig


def create_priority_matrix(leaks, comparator):
    """Crée une matrice de priorité (Sévérité vs Perte EV)"""
    if not leaks:
        return None

    severity_score = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}

    data = []
    for leak in leaks:
        ev_loss = comparator.calculate_ev_loss(leak)['ev_loss_bb100']
        data.append({
            'stat': leak['stat_display_name'],
            'severity_num': severity_score[leak['severity']],
            'ev_loss': ev_loss,
            'severity': leak['severity']
        })

    df = pd.DataFrame(data)

    # Créer le scatter plot
    fig = px.scatter(
        df,
        x='ev_loss',
        y='severity_num',
        size='ev_loss',
        color='severity',
        hover_data=['stat'],
        labels={'ev_loss': 'Perte EV (BB/100)', 'severity_num': 'Sévérité'},
        title="Matrice de Priorité des Leaks",
        color_discrete_map={
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#17a2b8'
        }
    )

    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4],
            ticktext=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        ),
        height=500
    )

    return fig


def main():
    st.title("📈 Dashboard de Visualisation")
    st.markdown("Visualisations avancées de vos statistiques et leaks")
    st.markdown("---")

    # Vérifier si on a des résultats d'analyse
    if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
        st.warning("⚠️ Aucune analyse disponible. Veuillez d'abord analyser vos stats dans la page **📊 Analyse Stats**.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Aller à l'Analyse Stats", use_container_width=True):
                st.switch_page("pages/1_📊_Analyse_Stats.py")

        return

    results = st.session_state.analysis_results

    # Métriques en haut
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Score Global",
            f"{results['summary']['overall_score']:.1f}%"
        )

    with col2:
        st.metric(
            "Total Leaks",
            results['summary']['total_leaks']
        )

    with col3:
        critical_count = results['summary']['severity_breakdown'].get('CRITICAL', 0)
        st.metric(
            "🔴 Critical",
            critical_count
        )

    with col4:
        high_count = results['summary']['severity_breakdown'].get('HIGH', 0)
        st.metric(
            "🟠 High",
            high_count
        )

    with col5:
        medium_count = results['summary']['severity_breakdown'].get('MEDIUM', 0)
        st.metric(
            "🟡 Medium",
            medium_count
        )

    st.markdown("---")

    # Tabs pour différentes visualisations
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Vue Globale",
        "📊 Comparaisons",
        "🔥 Heatmaps",
        "⚡ Priorités"
    ])

    with tab1:
        st.markdown("### 🎯 Vue d'Ensemble")

        col1, col2 = st.columns(2)

        with col1:
            # Radar Chart
            if results['user_stats']:
                from src.analysis import GTOComparator
                comparator = GTOComparator(stakes=results.get('stakes', 'PLO100'))

                # Obtenir les baselines GTO pour les stats du joueur
                gto_baselines = {}
                for stat_key in results['user_stats'].keys():
                    if stat_key in STAT_DEFINITIONS:
                        stat_info = STAT_DEFINITIONS[stat_key]
                        gto_baselines[stat_key] = {
                            'optimal': stat_info.get('gto_baseline', {}).get('optimal', 50)
                        }

                fig_radar = create_radar_chart(results['user_stats'], gto_baselines)
                st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            # Distribution des leaks par catégorie
            if results['analysis']['leaks_by_category']:
                categories_fr = {
                    'preflop': 'Preflop',
                    'postflop_aggression': 'Agression',
                    'postflop_defense': 'Défense',
                    'river': 'River',
                    'positional': 'Positionnelles',
                    'pot_type': 'Type de pot',
                    'advanced': 'Avancées'
                }

                cat_counts = {
                    categories_fr.get(cat, cat): len(leaks)
                    for cat, leaks in results['analysis']['leaks_by_category'].items()
                    if len(leaks) > 0
                }

                if cat_counts:
                    fig_cat = go.Figure(data=[
                        go.Pie(
                            labels=list(cat_counts.keys()),
                            values=list(cat_counts.values()),
                            hole=0.3
                        )
                    ])

                    fig_cat.update_layout(
                        title="Distribution des Leaks par Catégorie",
                        height=500
                    )

                    st.plotly_chart(fig_cat, use_container_width=True)

    with tab2:
        st.markdown("### 📊 Comparaisons Détaillées")

        # Graphique de déviation
        if results['leaks']:
            fig_dev = create_deviation_chart(results['leaks'])
            if fig_dev:
                st.plotly_chart(fig_dev, use_container_width=True)

            # Tableau comparatif
            st.markdown("#### Tableau Comparatif")

            comparison_data = []
            for leak in results['leaks']:
                comparison_data.append({
                    'Statistique': leak['stat_display_name'],
                    'Votre Valeur': f"{leak['player_value']:.1f}%",
                    'GTO Baseline': f"{leak['gto_value']:.1f}%",
                    'Déviation': f"{leak['delta']:+.1f}%",
                    'Direction': leak['direction'],
                    'Sévérité': leak['severity']
                })

            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)

        else:
            st.success("🎉 Aucun leak détecté!")

    with tab3:
        st.markdown("### 🔥 Heatmaps et Matrices")

        if results['leaks']:
            # Heatmap
            fig_heatmap = create_heatmap(results['leaks'])
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)

            # Matrice EV Loss
            st.markdown("#### Perte EV par Leak")

            ev_data = []
            for leak in results['leaks'][:20]:
                ev_loss = results['comparator'].calculate_ev_loss(leak)
                ev_data.append({
                    'Statistique': leak['stat_display_name'],
                    'Sévérité': leak['severity'],
                    'EV Loss (BB/100)': ev_loss['ev_loss_bb100'],
                    'EV Loss (10h)': ev_loss['total_ev_loss_bb']
                })

            df_ev = pd.DataFrame(ev_data)

            fig_ev_heatmap = px.density_heatmap(
                df_ev,
                x='Sévérité',
                y='Statistique',
                z='EV Loss (BB/100)',
                color_continuous_scale='Reds',
                title="Heatmap Perte EV"
            )

            fig_ev_heatmap.update_layout(height=600)
            st.plotly_chart(fig_ev_heatmap, use_container_width=True)

        else:
            st.info("Aucune heatmap à afficher - pas de leaks détectés")

    with tab4:
        st.markdown("### ⚡ Matrice de Priorités")

        if results['leaks']:
            # Matrice de priorité
            fig_priority = create_priority_matrix(results['leaks'], results['comparator'])
            if fig_priority:
                st.plotly_chart(fig_priority, use_container_width=True)

            st.info("""
            **Comment lire cette matrice :**
            - **Axe X (horizontal)** : Perte EV en BB/100
            - **Axe Y (vertical)** : Sévérité du leak
            - **Taille des bulles** : Impact relatif
            - **Priorité élevée** : En haut à droite (sévérité haute + perte EV élevée)
            - **Priorité faible** : En bas à gauche
            """)

            # Top priorités
            st.markdown("#### 🎯 Top 5 Priorités")

            if results['analysis']['top_5_priorities']:
                for idx, leak in enumerate(results['analysis']['top_5_priorities'], 1):
                    severity_emoji = {
                        'CRITICAL': '🔴',
                        'HIGH': '🟠',
                        'MEDIUM': '🟡',
                        'LOW': '🟢'
                    }.get(leak['severity'], '⚪')

                    st.markdown(f"""
                    {severity_emoji} **#{idx} - {leak['stat_display_name']}**
                    - Score de priorité: {leak['priority_score']:.2f}/4.0
                    - Perte EV: {leak['ev_loss_bb100']:.2f} BB/100
                    - Sévérité: {leak['severity']}
                    """)

        else:
            st.success("✅ Pas de leaks à prioriser!")

    st.markdown("---")

    # Options d'export
    st.markdown("### 💾 Export des Données")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Exporter en CSV", use_container_width=True):
            if results['leaks']:
                csv_data = []
                for leak in results['leaks']:
                    ev_loss = results['comparator'].calculate_ev_loss(leak)
                    csv_data.append({
                        'Statistique': leak['stat_display_name'],
                        'Valeur Joueur': leak['player_value'],
                        'GTO Baseline': leak['gto_value'],
                        'Déviation': leak['delta'],
                        'Sévérité': leak['severity'],
                        'EV Loss BB/100': ev_loss['ev_loss_bb100']
                    })

                df_export = pd.DataFrame(csv_data)
                csv = df_export.to_csv(index=False)

                st.download_button(
                    label="⬇️ Télécharger CSV",
                    data=csv,
                    file_name="plo_analysis_export.csv",
                    mime="text/csv"
                )

    with col2:
        if st.button("📊 Exporter en JSON", use_container_width=True):
            import json
            json_data = {
                'summary': results['summary'],
                'leaks': results['leaks'][:10],  # Top 10
                'user_stats': results['user_stats']
            }

            st.download_button(
                label="⬇️ Télécharger JSON",
                data=json.dumps(json_data, indent=2),
                file_name="plo_analysis_export.json",
                mime="application/json"
            )

    with col3:
        st.info("📄 Export PDF disponible prochainement")


if __name__ == "__main__":
    main()
