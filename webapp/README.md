# 🌐 PLO Mastery Suite - Application Web

Application web interactive pour l'analyse de vos statistiques PLO 6-max.

## 🚀 Démarrage Rapide

### Depuis le répertoire racine:
```bash
cd /home/user/garvazz
./lancer_webapp.sh
```

### Depuis ce répertoire:
```bash
streamlit run app.py
```

L'application sera accessible à : **http://localhost:8501**

## 📱 Pages de l'Application

| Page | Description |
|------|-------------|
| 🏠 **Accueil** | Présentation et documentation |
| 📊 **Analyse Stats** | Analysez vos statistiques et détectez vos leaks |
| 📈 **Dashboard** | Visualisations graphiques avancées |
| 📚 **Plan d'Étude** | Plan d'étude personnalisé et interactif |
| 📊 **Progression** | Suivez votre évolution dans le temps |

## ✨ Fonctionnalités

### Analyse Stats
- ✅ Saisie manuelle ou import de stats
- ✅ Détection automatique des leaks
- ✅ Calcul de perte EV (BB/100)
- ✅ Score d'optimisation global
- ✅ Plan d'étude personnalisé

### Dashboard
- ✅ Radar charts comparatifs
- ✅ Heatmaps de leaks
- ✅ Matrices de priorités
- ✅ Export CSV/JSON

### Plan d'Étude
- ✅ Tâches interactives (checkboxes)
- ✅ Tracking de progression
- ✅ Estimation du temps
- ✅ Calendrier personnalisable

### Progression
- ✅ Historique de toutes vos analyses
- ✅ Graphiques d'évolution
- ✅ Comparaisons entre sessions
- ✅ Leaks récurrents

## 📖 Documentation

Consultez **WEBAPP_GUIDE.md** pour le guide complet d'utilisation.

## 🔧 Configuration

La configuration Streamlit se trouve dans `.streamlit/config.toml`:
- Thème et couleurs
- Port du serveur (8501)
- Options de sécurité

## 📦 Dépendances

```
streamlit>=1.28.0
plotly>=5.0.0
streamlit-aggrid>=0.3.4
pandas>=1.3.0
```

## 🎯 Workflow Recommandé

1. **Première visite** : Explorez la page d'accueil
2. **Test** : Chargez des stats d'exemple dans "Analyse Stats"
3. **Analyse réelle** : Entrez vos vraies stats
4. **Visualisations** : Consultez le Dashboard
5. **Action** : Suivez votre Plan d'Étude
6. **Tracking** : Sauvegardez dans Progression

## 💡 Conseils

- Analysez vos stats tous les 500-1000 mains
- Sauvegardez régulièrement dans la page Progression
- Exportez votre historique pour backup
- Concentrez-vous sur 2-3 leaks maximum

## 📞 Support

- Guide complet : `../WEBAPP_GUIDE.md`
- Guide CLI : `../GUIDE_UTILISATION.md`
- Contact : pekinio13@hotmail.fr

---

**Version 1.0** | PLO Mastery Suite Web Application
