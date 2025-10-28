#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 Page du Plan d'Étude Personnalisé
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Configuration de la page
st.set_page_config(
    page_title="Plan d'Étude - PLO Mastery Suite",
    page_icon="📚",
    layout="wide"
)

# Style CSS
st.markdown("""
<style>
    .study-task {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    .priority-task {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .completed-task {
        background-color: #d4edda;
        border-left-color: #28a745;
        opacity: 0.7;
    }
    .focus-area {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .time-estimate {
        background-color: #e7f3ff;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def format_time(minutes):
    """Formate le temps en heures et minutes"""
    hours = minutes // 60
    mins = minutes % 60

    if hours > 0:
        return f"{hours}h {mins}min" if mins > 0 else f"{hours}h"
    else:
        return f"{mins}min"


def main():
    st.title("📚 Votre Plan d'Étude Personnalisé")
    st.markdown("Plan d'étude optimisé basé sur vos leaks prioritaires")
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
    study_plan = results.get('study_plan')

    if not study_plan or not study_plan.get('study_tasks'):
        st.success("🎉 Félicitations! Vos stats sont optimales, aucun plan d'étude nécessaire.")
        return

    # Initialiser le tracking des tâches si nécessaire
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = set()

    # En-tête du plan
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⏱️ Temps Total",
            f"{study_plan['total_estimated_hours']:.1f}h"
        )

    with col2:
        st.metric(
            "🎯 Zones de Focus",
            len(study_plan['study_tasks'])
        )

    with col3:
        total_tasks = sum(len(task_group['tasks']) for task_group in study_plan['study_tasks'])
        completed = len(st.session_state.completed_tasks)
        progress = (completed / total_tasks * 100) if total_tasks > 0 else 0
        st.metric(
            "✅ Progression",
            f"{completed}/{total_tasks}",
            f"{progress:.0f}%"
        )

    st.markdown("---")

    # Sidebar pour les options
    with st.sidebar:
        st.header("⚙️ Options du Plan")

        # Filtre par sévérité
        show_severity = st.multiselect(
            "Afficher les sévérités",
            ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            default=['CRITICAL', 'HIGH', 'MEDIUM']
        )

        # Afficher les tâches complétées
        show_completed = st.checkbox("Afficher les tâches terminées", value=True)

        # Calendrier d'étude
        st.markdown("---")
        st.markdown("### 📅 Planification")

        start_date = st.date_input(
            "Date de début",
            value=datetime.now()
        )

        hours_per_week = st.slider(
            "Heures d'étude par semaine",
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )

        # Calculer la date de fin estimée
        total_hours = study_plan['total_estimated_hours']
        weeks_needed = total_hours / hours_per_week
        end_date = start_date + timedelta(weeks=weeks_needed)

        st.info(f"""
        **Estimation :**
        - Début : {start_date.strftime('%d/%m/%Y')}
        - Fin estimée : {end_date.strftime('%d/%m/%Y')}
        - Durée : {weeks_needed:.1f} semaines
        """)

        # Reset progression
        st.markdown("---")
        if st.button("🔄 Réinitialiser Progression"):
            st.session_state.completed_tasks = set()
            st.rerun()

    # Tabs pour différentes vues
    tab1, tab2, tab3 = st.tabs(["📋 Plan Complet", "📊 Vue Résumée", "📈 Progression"])

    with tab1:
        st.markdown("### 📋 Plan d'Étude Détaillé")

        # Afficher chaque zone de focus
        for idx, task_group in enumerate(study_plan['study_tasks'], 1):
            leak = task_group['leak']
            tasks = task_group['tasks']
            time_min = task_group['estimated_study_time']

            # Vérifier le filtre de sévérité
            if leak['severity'] not in show_severity:
                continue

            # Emoji selon la sévérité
            severity_config = {
                'CRITICAL': ('🔴', '#dc3545'),
                'HIGH': ('🟠', '#fd7e14'),
                'MEDIUM': ('🟡', '#ffc107'),
                'LOW': ('🟢', '#17a2b8')
            }
            emoji, color = severity_config.get(leak['severity'], ('⚪', '#6c757d'))

            # Calculer le nombre de tâches complétées pour ce focus
            task_keys = [f"{idx}_{task_idx}" for task_idx in range(len(tasks))]
            completed_count = sum(1 for key in task_keys if key in st.session_state.completed_tasks)
            focus_progress = (completed_count / len(tasks) * 100) if tasks else 0

            with st.expander(
                f"{emoji} Focus #{idx}: {leak['stat_display_name']} - {format_time(time_min)}",
                expanded=(idx == 1)
            ):
                # En-tête du focus
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"""
                    **Statistique :** {leak['stat_display_name']}
                    **Sévérité :** {leak['severity']}
                    **Priorité :** {leak['priority_score']:.2f}/4.0
                    **Perte EV :** {leak['ev_loss_bb100']:.2f} BB/100
                    """)

                with col2:
                    st.markdown(f"""
                    <div class="time-estimate">
                        ⏱️ <b>{format_time(time_min)}</b><br>
                        ✅ <b>{completed_count}/{len(tasks)} tâches</b><br>
                        📊 <b>{focus_progress:.0f}%</b>
                    </div>
                    """, unsafe_allow_html=True)

                # Barre de progression pour ce focus
                st.progress(focus_progress / 100)

                st.markdown("---")

                # Afficher les tâches
                st.markdown("**📝 Tâches à Accomplir :**")

                for task_idx, task in enumerate(tasks, 1):
                    task_key = f"{idx}_{task_idx-1}"
                    is_completed = task_key in st.session_state.completed_tasks
                    is_priority = 'PRIORITY' in task

                    # Afficher seulement si pas complété ou si on affiche les complétés
                    if is_completed and not show_completed:
                        continue

                    col1, col2 = st.columns([0.1, 0.9])

                    with col1:
                        # Checkbox pour marquer comme complété
                        completed = st.checkbox(
                            "",
                            value=is_completed,
                            key=f"task_{task_key}",
                            label_visibility="collapsed"
                        )

                        # Mettre à jour le set des tâches complétées
                        if completed:
                            st.session_state.completed_tasks.add(task_key)
                        else:
                            st.session_state.completed_tasks.discard(task_key)

                    with col2:
                        # Afficher la tâche
                        task_class = "completed-task" if is_completed else "priority-task" if is_priority else "study-task"

                        task_prefix = "⭐" if is_priority else f"{task_idx}."
                        task_text = task.replace("PRIORITY: ", "")

                        st.markdown(f"""
                        <div class="{task_class}">
                            <b>{task_prefix}</b> {task_text}
                        </div>
                        """, unsafe_allow_html=True)

                # Recommandations supplémentaires
                st.markdown("---")
                st.markdown("**💡 Recommandations :**")

                recommendations = {
                    'VPIP': [
                        "Utilisez des range charts spécifiques au PLO",
                        "Pratiquez avec un GTO trainer (GTO+, PioSOLVER)",
                        "Reviewez vos mains hors range"
                    ],
                    'PFR': [
                        "Identifiez vos situations de limp",
                        "Travaillez vos ranges de raise par position",
                        "Analysez vos fréquences dans le HUD"
                    ],
                    '3-Bet': [
                        "Étudiez les ranges de 3-bet optimales",
                        "Identifiez les spots de 3-bet light",
                        "Travaillez l'équilibre entre value et bluff"
                    ],
                    'C-Bet': [
                        "Analysez les textures de board favorables",
                        "Travaillez vos ranges de c-bet merged",
                        "Étudiez les fréquences par position"
                    ]
                }

                # Chercher des recommandations pertinentes
                stat_name = leak['stat_display_name']
                for key, recs in recommendations.items():
                    if key.lower() in stat_name.lower():
                        for rec in recs:
                            st.markdown(f"- {rec}")
                        break
                else:
                    st.info("Consultez votre coach pour des recommandations spécifiques")

    with tab2:
        st.markdown("### 📊 Vue Résumée du Plan")

        # Tableau récapitulatif
        summary_data = []

        for idx, task_group in enumerate(study_plan['study_tasks'], 1):
            leak = task_group['leak']
            tasks = task_group['tasks']
            time_min = task_group['estimated_study_time']

            # Compter les tâches complétées
            task_keys = [f"{idx}_{task_idx}" for task_idx in range(len(tasks))]
            completed_count = sum(1 for key in task_keys if key in st.session_state.completed_tasks)

            summary_data.append({
                'Focus': f"#{idx} - {leak['stat_display_name']}",
                'Sévérité': leak['severity'],
                'Priorité': f"{leak['priority_score']:.2f}",
                'Temps': format_time(time_min),
                'Tâches': f"{completed_count}/{len(tasks)}",
                'Progression': f"{(completed_count/len(tasks)*100):.0f}%"
            })

        import pandas as pd
        df_summary = pd.DataFrame(summary_data)

        st.dataframe(
            df_summary,
            use_container_width=True,
            hide_index=True
        )

        # Statistiques globales
        st.markdown("---")
        st.markdown("### 📈 Statistiques Globales")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"""
            **⏱️ Temps d'Étude**
            - Total : {study_plan['total_estimated_hours']:.1f}h
            - Par zone : {study_plan['total_estimated_hours'] / len(study_plan['study_tasks']):.1f}h
            - Par semaine : {hours_per_week}h
            """)

        with col2:
            total_tasks_all = sum(len(tg['tasks']) for tg in study_plan['study_tasks'])
            completed_all = len(st.session_state.completed_tasks)

            st.success(f"""
            **✅ Progression**
            - Complétées : {completed_all}
            - Restantes : {total_tasks_all - completed_all}
            - Total : {total_tasks_all}
            """)

        with col3:
            # Calculer le temps restant
            remaining_tasks = total_tasks_all - completed_all
            avg_time_per_task = (study_plan['total_estimated_hours'] * 60) / total_tasks_all
            remaining_time = (remaining_tasks * avg_time_per_task) / 60

            st.warning(f"""
            **⏳ Temps Restant**
            - Estimé : {remaining_time:.1f}h
            - Semaines : {remaining_time / hours_per_week:.1f}
            - Fin : {(start_date + timedelta(weeks=remaining_time / hours_per_week)).strftime('%d/%m/%Y')}
            """)

    with tab3:
        st.markdown("### 📈 Suivi de Progression")

        # Graphique de progression
        import plotly.graph_objects as go

        progress_data = []
        for idx, task_group in enumerate(study_plan['study_tasks'], 1):
            tasks = task_group['tasks']
            task_keys = [f"{idx}_{task_idx}" for task_idx in range(len(tasks))]
            completed_count = sum(1 for key in task_keys if key in st.session_state.completed_tasks)

            progress_data.append({
                'focus': f"Focus #{idx}",
                'completed': completed_count,
                'remaining': len(tasks) - completed_count
            })

        import pandas as pd
        df_progress = pd.DataFrame(progress_data)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Complétées',
            x=df_progress['focus'],
            y=df_progress['completed'],
            marker_color='rgb(40, 167, 69)'
        ))

        fig.add_trace(go.Bar(
            name='Restantes',
            x=df_progress['focus'],
            y=df_progress['remaining'],
            marker_color='rgb(108, 117, 125)'
        ))

        fig.update_layout(
            title='Progression par Zone de Focus',
            xaxis_title='Zone',
            yaxis_title='Nombre de Tâches',
            barmode='stack',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Motivation et conseils
        st.markdown("---")
        st.markdown("### 💪 Conseils de Progression")

        total_tasks_all = sum(len(tg['tasks']) for tg in study_plan['study_tasks'])
        completed_all = len(st.session_state.completed_tasks)
        progress_pct = (completed_all / total_tasks_all * 100) if total_tasks_all > 0 else 0

        if progress_pct == 0:
            st.info("""
            🎯 **Démarrez votre parcours !**
            - Commencez par le Focus #1 (plus haute priorité)
            - Cochez les tâches au fur et à mesure
            - Travaillez 30-60 min par session minimum
            - Soyez régulier plutôt qu'intensif
            """)
        elif progress_pct < 25:
            st.success("""
            🌱 **Bon début !**
            - Continuez à travailler méthodiquement
            - Ne sautez pas d'étapes
            - Documentez vos learnings
            - Appliquez en jeu régulièrement
            """)
        elif progress_pct < 50:
            st.success("""
            📈 **Progression solide !**
            - Vous êtes sur la bonne voie
            - Commencez à réanalyser vos stats
            - Mesurez l'impact de votre travail
            - Ajustez le plan si nécessaire
            """)
        elif progress_pct < 75:
            st.success("""
            🚀 **Excellent travail !**
            - Vous approchez de la fin
            - Consolidez vos acquis
            - Préparez la prochaine analyse
            - Restez discipliné
            """)
        elif progress_pct < 100:
            st.success("""
            🏆 **Presque fini !**
            - Dernière ligne droite
            - Terminez toutes les tâches
            - Préparez votre réanalyse
            - Célébrez vos progrès
            """)
        else:
            st.balloons()
            st.success("""
            🎉 **FÉLICITATIONS !**
            - Plan d'étude terminé !
            - Réanalysez vos stats maintenant
            - Mesurez votre progression
            - Créez un nouveau plan si nécessaire
            """)

            if st.button("🔄 Relancer une Analyse", use_container_width=True):
                st.switch_page("pages/1_📊_Analyse_Stats.py")

    st.markdown("---")

    # Export du plan
    st.markdown("### 💾 Exporter le Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Exporter en TXT", use_container_width=True):
            # Générer le texte
            txt_content = "PLAN D'ÉTUDE PLO MASTERY SUITE\n"
            txt_content += "=" * 50 + "\n\n"

            for idx, task_group in enumerate(study_plan['study_tasks'], 1):
                leak = task_group['leak']
                tasks = task_group['tasks']
                time_min = task_group['estimated_study_time']

                txt_content += f"FOCUS #{idx}: {leak['stat_display_name']}\n"
                txt_content += f"Sévérité: {leak['severity']}\n"
                txt_content += f"Temps estimé: {format_time(time_min)}\n\n"
                txt_content += "Tâches:\n"

                for task_idx, task in enumerate(tasks, 1):
                    txt_content += f"  {task_idx}. {task}\n"

                txt_content += "\n" + "-" * 50 + "\n\n"

            st.download_button(
                label="⬇️ Télécharger TXT",
                data=txt_content,
                file_name=f"plan_etude_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

    with col2:
        st.info("📄 Export PDF disponible prochainement")

    with col3:
        st.info("📧 Envoi par email disponible prochainement")


if __name__ == "__main__":
    main()
