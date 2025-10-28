# 🌐 Guide d'Utilisation - Application Web PLO Mastery Suite

Guide complet pour utiliser l'application web interactive.

---

## 🚀 Lancement de l'Application

### Méthode Simple (Recommandée)

```bash
cd /home/user/garvazz
./lancer_webapp.sh
```

### Méthode Manuelle

```bash
cd /home/user/garvazz/webapp
streamlit run app.py
```

L'application sera accessible à : **http://localhost:8501**

---

## 📱 Navigation dans l'Application

L'application web est organisée en **5 pages principales** :

### 1. 🏠 Accueil (`app.py`)
**Page d'accueil et présentation**

✅ Vue d'ensemble de l'outil
✅ Liste des fonctionnalités
✅ Statistiques supportées
✅ FAQ et aide

**Actions :**
- Découvrir l'application
- Consulter la documentation
- Voir les stats disponibles

---

### 2. 📊 Analyse Stats
**Analysez vos statistiques PLO**

✅ Saisie manuelle ou import de stats
✅ Analyse en temps réel
✅ Détection des leaks avec sévérité
✅ Calcul de perte EV (BB/100)
✅ Plan d'étude personnalisé

**Workflow :**

1. **Configurez les paramètres** (sidebar)
   - Stakes (PLO50/PLO100/PLO200)
   - Nombre de mains
   - Sévérité minimale

2. **Entrez vos statistiques**
   - Onglet "Saisie Manuelle" : Formulaire interactif
   - Onglet "Import Fichier" : Upload CSV (à venir)
   - Bouton "Charger stats d'exemple" pour tester

3. **Lancez l'analyse**
   - Cliquez sur "🔍 LANCER L'ANALYSE"
   - Attendez le traitement (quelques secondes)

4. **Consultez les résultats** (4 onglets)
   - **Leaks Détectés** : Liste complète avec détails
   - **Visualisations** : Graphiques interactifs
   - **Plan d'Étude** : Tâches personnalisées
   - **Détails** : Breakdown par catégorie

**Stats Minimales Recommandées :**
- VPIP (essentiel)
- PFR (essentiel)
- 3-Bet (essentiel)
- C-Bet Flop (essentiel)
- Fold vs C-Bet (recommandé)
- WTSD (optionnel)

---

### 3. 📈 Dashboard
**Visualisations avancées de vos leaks**

✅ Vue d'ensemble graphique
✅ Radar charts comparatifs
✅ Heatmaps de leaks
✅ Matrices de priorités
✅ Export de données (CSV/JSON)

**4 Vues Principales :**

#### 🎯 Vue Globale
- Radar chart (Vous vs GTO)
- Distribution des leaks par catégorie
- Vue d'ensemble

#### 📊 Comparaisons
- Graphique de déviation GTO
- Tableau comparatif détaillé
- Analyse par statistique

#### 🔥 Heatmaps
- Heatmap par catégorie/sévérité
- Matrice de perte EV
- Visualisation de l'impact

#### ⚡ Priorités
- Matrice Sévérité vs EV Loss
- Top 5 priorités
- Guide de lecture

**Options d'Export :**
- 📄 CSV (compatible Excel)
- 📊 JSON (format brut)
- 📄 PDF (à venir)

---

### 4. 📚 Plan d'Étude
**Votre plan d'étude personnalisé et interactif**

✅ Plan optimisé par priorité
✅ Tâches checkables
✅ Tracking de progression
✅ Estimation du temps
✅ Calendrier personnalisable

**3 Vues Principales :**

#### 📋 Plan Complet
- Liste détaillée des focus areas
- Tâches à accomplir par leak
- Checkboxes interactives
- Progression par focus
- Recommandations spécifiques

**Comment utiliser :**
1. Consultez les focus areas (triés par priorité)
2. Commencez par le Focus #1
3. Cochez les tâches au fur et à mesure
4. Suivez les recommandations
5. Travaillez focus par focus

#### 📊 Vue Résumée
- Tableau récapitulatif
- Statistiques globales
- Temps total/restant
- Vue d'ensemble

#### 📈 Progression
- Graphique par focus
- % de complétion
- Conseils motivationnels
- Étapes suivantes

**Options Sidebar :**
- Filtrer par sévérité
- Afficher/masquer tâches terminées
- Planification calendrier
- Réinitialiser progression

**Export du Plan :**
- 📄 TXT (format texte)
- 📄 PDF (à venir)
- 📧 Email (à venir)

---

### 5. 📊 Progression
**Trackez votre évolution dans le temps**

✅ Historique de toutes vos analyses
✅ Graphiques d'évolution
✅ Comparaisons entre sessions
✅ Statistiques globales
✅ Leaks récurrents

**4 Vues Principales :**

#### 📈 Graphiques
- Évolution du score d'optimisation
- Évolution du nombre de leaks
- Taille des échantillons
- Tendances

#### 📋 Historique
- Timeline de toutes les analyses
- Détails de chaque session
- Breakdown par sévérité
- Comparaison rapide

#### 🎯 Comparaison
- Sélecteur d'analyses
- Radar chart comparatif
- Tableau de différences
- Évolution par stat

#### 📊 Statistiques
- Résumé de progression
- Score moyen/min/max
- Leaks récurrents
- Mains totales jouées

**Gestion de l'Historique (Sidebar) :**
- 💾 Sauvegarder l'analyse actuelle
- 📥 Exporter l'historique (JSON)
- 📤 Importer un historique
- 🗑️ Effacer l'historique

**Workflow Recommandé :**
1. Analysez vos stats (page Analyse)
2. Sauvegardez l'analyse (sidebar Progression)
3. Consultez votre progression
4. Comparez avec analyses précédentes
5. Identifiez les leaks récurrents

---

## 💡 Workflows Recommandés

### 🆕 Première Utilisation

```
1. Accueil → Lire la présentation
2. Analyse Stats → Charger stats d'exemple
3. Lancer l'analyse (test)
4. Dashboard → Explorer les visualisations
5. Plan d'Étude → Voir le plan généré
6. Progression → Sauvegarder pour commencer le tracking
```

### 🎯 Analyse Régulière (tous les 500-1000 mains)

```
1. Exporter vos stats depuis PT4/HM3
2. Analyse Stats → Entrer vos vraies stats
3. Lancer l'analyse
4. Dashboard → Identifier les leaks prioritaires
5. Plan d'Étude → Suivre le plan
6. Progression → Sauvegarder + Comparer
```

### 📚 Suivi d'un Plan d'Étude

```
1. Plan d'Étude → Consulter vos focus areas
2. Travailler sur Focus #1
3. Cocher les tâches complétées
4. Suivre la progression
5. Réanalyser après correction (500+ mains)
6. Progression → Mesurer l'amélioration
```

---

## ⚙️ Personnalisation

### Configuration Sidebar

Chaque page a une sidebar avec des options :

**Analyse Stats :**
- Stakes (PLO50/100/200)
- Nombre de mains
- Sévérité minimale
- Stats d'exemple

**Dashboard :**
- (Aucune config spécifique)

**Plan d'Étude :**
- Filtres de sévérité
- Affichage des tâches terminées
- Date de début
- Heures/semaine

**Progression :**
- Sauvegarde d'analyse
- Import/Export
- Effacement historique

---

## 📊 Interprétation des Résultats

### Score d'Optimisation

| Score | Signification | Action |
|-------|---------------|--------|
| 90-100% | Excellent | Continuez ainsi |
| 70-89% | Bon | Quelques ajustements mineurs |
| 50-69% | Moyen | Travail nécessaire sur leaks majeurs |
| 30-49% | Faible | Révision importante requise |
| < 30% | Critique | Coaching fortement recommandé |

### Sévérité des Leaks

| Sévérité | Emoji | Signification | Priorité |
|----------|-------|---------------|----------|
| CRITICAL | 🔴 | Perte EV majeure | Corriger IMMÉDIATEMENT |
| HIGH | 🟠 | Impact significatif | Très prioritaire |
| MEDIUM | 🟡 | Impact modéré | À corriger |
| LOW | 🟢 | Impact mineur | Optionnel |

### Perte EV (BB/100)

- **< 0.5 BB/100** : Impact négligeable
- **0.5-1.0 BB/100** : Impact modéré
- **1.0-2.0 BB/100** : Impact sérieux
- **> 2.0 BB/100** : Impact majeur (critique!)

---

## 🔧 Fonctionnalités Avancées

### Export de Données

**Format CSV :**
- Compatible Excel
- Import dans d'autres outils
- Analyse statistique externe

**Format JSON :**
- Format brut complet
- Intégration API
- Backup structuré

### Persistence des Données

L'application utilise `st.session_state` pour :
- Conserver les résultats d'analyse
- Tracker les tâches complétées
- Sauvegarder l'historique
- Maintenir les préférences

**Important :** Les données sont conservées pendant la session.
Pour sauvegarder définitivement :
1. Utilisez l'export JSON (Progression)
2. Réimportez lors de la prochaine session

---

## 📱 Raccourcis Clavier

Dans Streamlit :
- **R** : Rerun l'application
- **Ctrl+C** (terminal) : Arrêter l'app
- **F5** : Rafraîchir la page

---

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier l'installation de Streamlit
pip list | grep streamlit

# Réinstaller si nécessaire
pip install streamlit plotly streamlit-aggrid

# Relancer
./lancer_webapp.sh
```

### "Module not found"

```bash
# Assurez-vous d'être dans le bon dossier
cd /home/user/garvazz

# Vérifier la structure
ls -la webapp/

# Relancer
./lancer_webapp.sh
```

### Les graphiques ne s'affichent pas

```bash
# Réinstaller plotly
pip install plotly --upgrade

# Vider le cache Streamlit
rm -rf webapp/.streamlit/cache
```

### Les données ne se sauvegardent pas

- Les données sont en session
- Utilisez l'export JSON pour sauvegarder
- Réimportez à chaque nouvelle session

---

## 💾 Sauvegarde et Backup

### Exporter votre Historique

1. Page **Progression** → Sidebar
2. Cliquez sur **"📥 Exporter Historique"**
3. Sauvegardez le fichier JSON
4. Conservez-le précieusement

### Restaurer votre Historique

1. Page **Progression** → Sidebar
2. **"📤 Importer Historique"**
3. Sélectionnez votre fichier JSON
4. Vos données sont restaurées

---

## 🎯 Bonnes Pratiques

### Fréquence d'Analyse

- **Débutant** : Tous les 500 mains
- **Intermédiaire** : Tous les 1000 mains
- **Avancé** : Tous les 2000-5000 mains
- **Après session d'étude** : Immédiatement

### Nombre de Focus

- Concentrez-vous sur **2-3 leaks max**
- Ne dispersez pas vos efforts
- Corrigez complètement avant de passer au suivant
- Réanalysez régulièrement

### Utilisation du Plan d'Étude

- Cochez les tâches honnêtement
- Travaillez 30-60 min par session
- Soyez régulier (3-5h/semaine)
- Appliquez en jeu rapidement

---

## 🚀 Prochaines Fonctionnalités

✅ Actuellement disponible
🔄 En développement
📋 Planifié

- ✅ Analyse complète des stats
- ✅ Visualisations interactives
- ✅ Plan d'étude personnalisé
- ✅ Tracking de progression
- 🔄 Export PDF des rapports
- 🔄 Import CSV PT4/HM3
- 📋 Authentification utilisateur
- 📋 Base de données persistante
- 📋 Recommandations IA
- 📋 Intégration coaching vidéo

---

## 📞 Support et Contact

**Besoin d'aide ?**

1. Consultez ce guide
2. Lisez la FAQ (page Accueil)
3. Vérifiez `GUIDE_UTILISATION.md`
4. Contactez : pekinio13@hotmail.fr

---

## 🎓 Ressources Complémentaires

- `GUIDE_UTILISATION.md` - Guide CLI complet
- `EXEMPLES_UTILISATION.md` - Exemples pratiques
- `COMMENT_LANCER.md` - Quick start
- `README.md` - Présentation

---

**🎯 Bon courage pour crusher le PLO avec l'application web! 🚀**

Version: 1.0 | PLO Mastery Suite Web App
