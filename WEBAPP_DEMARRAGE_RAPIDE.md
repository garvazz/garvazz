# Guide de Demarrage Rapide - Application Web PLO Mastery Suite

## Lancement de l'Application

### Methode Simple (Recommandee)

```bash
cd /home/user/garvazz
./lancer_webapp.sh
```

L'application sera accessible a l'adresse: **http://localhost:8501**

---

## Depannage Rapide

### Probleme: "Port 8501 is already in use"

**Solution:**
```bash
# Arreter tous les processus Streamlit
pkill -f "streamlit run"

# Attendre 2 secondes
sleep 2

# Relancer l'application
./lancer_webapp.sh
```

---

### Probleme: "Module not found"

**Solution:**
```bash
# Verifier que vous etes dans le bon repertoire
cd /home/user/garvazz
pwd
# Doit afficher: /home/user/garvazz

# Verifier les modules
python3 -c "from src.analysis import GTOComparator; print('OK')"
```

---

### Probleme: "Streamlit n'est pas installe"

**Solution:**
```bash
# Installer Streamlit et les dependances
pip install -r requirements.txt

# Ou installation manuelle
pip install streamlit plotly streamlit-aggrid
```

---

## Utilisation de l'Application

### 1. Page d'Accueil
- Vue d'ensemble de l'application
- Navigation vers les differentes sections

### 2. Analyse Stats
- Entrez vos statistiques manuellement
- Ou chargez des stats d'exemple pour tester
- Cliquez sur "LANCER L'ANALYSE"
- Consultez les resultats dans les differents onglets

### 3. Dashboard
- Vue graphique de vos performances
- Comparaison avec les baselines GTO

### 4. Plan d'Etude
- Plan personnalise base sur vos leaks
- Temps estime pour chaque tache
- Priorites detaillees

### 5. Progression
- Suivez votre evolution dans le temps
- Comparez vos sessions
- Identifiez les tendances

---

## Commandes Utiles

### Lancer l'application
```bash
./lancer_webapp.sh
```

### Arreter l'application
- Methode 1: Appuyez sur `Ctrl+C` dans le terminal
- Methode 2: `pkill -f "streamlit run"`

### Verifier si l'application tourne
```bash
lsof -i :8501
# Si une ligne s'affiche, l'application tourne
```

### Changer le port (si 8501 est occupe)
```bash
streamlit run webapp/app.py --server.port 8502
# L'application sera sur http://localhost:8502
```

---

## Configuration Avancee

### Fichier de configuration
Le fichier `.streamlit/config.toml` contient la configuration de l'application:

- **Port**: 8501 (modifiable)
- **Theme**: Bleu et blanc (personnalisable)
- **CORS**: Active pour permettre l'acces local

### Logs de debug
Pour voir les logs detailles:
```bash
streamlit run webapp/app.py --logger.level=debug
```

---

## Fonctionnalites Principales

### Analyse de Stats
- Entree manuelle de 20+ statistiques
- Stats d'exemple pre-chargees
- Detection automatique des leaks
- Calcul de perte EV

### Visualisations
- Graphiques de comparaison GTO vs Joueur
- Diagramme circulaire de severite des leaks
- Graphique de perte EV
- Tableaux interactifs

### Plan d'Etude
- Generation automatique basee sur vos leaks
- Priorite des taches
- Temps estime par tache
- Recommandations personnalisees

### Suivi de Progression
- Historique de vos sessions
- Graphiques d'evolution
- Detection des leaks persistants
- Export des donnees

---

## FAQ

**Q: L'application ne se charge pas dans le navigateur**
R: Verifiez que:
1. L'application est bien lancee (pas d'erreur dans le terminal)
2. Vous utilisez http://localhost:8501 (pas https)
3. Votre navigateur n'a pas de bloqueur de contenu actif

**Q: Les graphiques ne s'affichent pas**
R: Installez plotly:
```bash
pip install plotly
```

**Q: Comment sauvegarder mes analyses?**
R: L'application utilise la session Streamlit. Pour sauvegarder:
- Utilisez la page "Progression" pour ajouter une session
- Les donnees seront stockees dans `st.session_state`
- Pour une sauvegarde permanente, exportez en CSV (fonctionnalite a venir)

**Q: Puis-je utiliser l'application sur un autre port?**
R: Oui:
```bash
streamlit run webapp/app.py --server.port 8080
```

**Q: Comment mettre a jour l'application?**
R:
```bash
cd /home/user/garvazz
git pull
pip install -r requirements.txt --upgrade
```

---

## Support

Pour toute question ou probleme:
1. Consultez ce guide
2. Verifiez `WEBAPP_GUIDE.md` pour la documentation complete
3. Contactez: pekinio13@hotmail.fr

---

**Bon courage pour analyser vos stats et crusher le PLO!**
