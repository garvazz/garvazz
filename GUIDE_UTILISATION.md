# 📖 Guide d'Utilisation - PLO Mastery Suite

Guide complet pour utiliser l'outil d'analyse de leaks PLO.

---

## 🚀 Démarrage Rapide

### Option 1: Lancer la Démonstration (Recommandé pour débuter)

```bash
cd /home/user/garvazz
python3 scripts/demo_analysis.py
```

Cette démo montre **toutes les fonctionnalités** avec des données d'exemple.

**Ce que vous verrez:**
- ✅ Comparaison de 20 stats avec les baselines GTO
- ✅ Détection et priorisation des leaks
- ✅ Plan d'étude personnalisé
- ✅ Suivi des progrès sur plusieurs sessions
- ✅ Rapports formatés professionnels

---

## 📊 Utiliser l'Outil avec Vos Propres Stats

### Méthode 1: Script Python Simple

Créez un fichier `analyze_my_stats.py`:

```python
#!/usr/bin/env python3
from src.analysis import GTOComparator, LeakDetector

# VOS STATS (remplacez par vos vraies valeurs)
mes_stats = {
    'vpip': 28.0,          # % de mains jouées
    'pfr': 22.0,           # % de raises preflop
    'three_bet': 9.0,      # % de 3-bets
    'fold_vs_3bet': 57.0,  # % de fold vs 3-bet
    'cbet_freq_flop': 62.0,  # % de c-bet au flop
    'fold_vs_cbet_flop': 45.0,  # % de fold vs c-bet flop
    'wtsd': 26.0,          # % went to showdown
    'w_sd': 51.0,          # % won at showdown
}

taille_echantillon = 500  # Nombre de mains analysées

# === ÉTAPE 1: COMPARAISON GTO ===
print("=" * 70)
print("ANALYSE DE VOS STATS")
print("=" * 70)

comparator = GTOComparator(stakes='PLO100')

# Obtenir tous les leaks
leaks = comparator.get_leaks(mes_stats, min_severity='MEDIUM')

print(f"\n🔍 {len(leaks)} leaks détectés\n")

# Afficher les top 3 leaks
for i, leak in enumerate(leaks[:3], 1):
    print(f"{i}. {leak['stat_display_name']} - {leak['severity']}")
    print(f"   Votre valeur: {leak['player_value']:.1f}%")
    print(f"   GTO baseline: {leak['gto_value']:.1f}%")
    print(f"   Déviation: {leak['delta']:+.1f}%")
    print(f"   Perte EV: {comparator.calculate_ev_loss(leak)['ev_loss_bb100']:.2f} BB/100\n")


# === ÉTAPE 2: DÉTECTION DE LEAKS ===
detector = LeakDetector(stakes='PLO100')
analyse = detector.detect_leaks(mes_stats, sample_size=taille_echantillon)

print("=" * 70)
print("TOP RECOMMANDATIONS")
print("=" * 70)

for i, rec in enumerate(analyse['recommendations'][:3], 1):
    print(f"\n{i}. {rec['stat_display']} [{rec['severity']}]")
    print(f"   → {rec['recommendation']}")
    print(f"   Impact EV: {rec['ev_impact']}")


# === ÉTAPE 3: PLAN D'ÉTUDE ===
study_plan = detector.get_study_plan(mes_stats, taille_echantillon, focus_areas=2)

print("\n" + "=" * 70)
print("VOTRE PLAN D'ÉTUDE")
print("=" * 70)
print(f"Temps total estimé: {study_plan['total_estimated_hours']:.1f} heures\n")

for i, task in enumerate(study_plan['study_tasks'], 1):
    leak = task['leak']
    print(f"\n📚 FOCUS #{i}: {leak['stat_display_name']}")
    print(f"   Sévérité: {leak['severity']}")
    print(f"   Temps: {task['estimated_study_time']} minutes")
    print(f"   Tâches:")
    for j, t in enumerate(task['tasks'][:3], 1):
        print(f"      {j}. {t}")
```

**Lancer votre analyse:**
```bash
python3 analyze_my_stats.py
```

---

### Méthode 2: Mode Interactif Python

```bash
python3
```

Puis dans l'interpréteur Python:

```python
from src.analysis import GTOComparator, LeakDetector

# Vos stats
stats = {
    'vpip': 30.0,
    'pfr': 18.0,
    'three_bet': 7.0,
    'cbet_freq_flop': 55.0,
}

# Analyser
comparator = GTOComparator()
leaks = comparator.get_leaks(stats)

# Afficher les résultats
for leak in leaks[:5]:
    print(f"{leak['stat_display_name']}: {leak['delta']:+.1f}% ({leak['severity']})")

# Rapport complet
summary = comparator.generate_comparison_summary(stats, sample_size=200)
print(f"Score global: {summary['overall_score']:.1f}%")

# Plan d'étude
detector = LeakDetector()
plan = detector.get_study_plan(stats, sample_size=200)
print(f"Heures d'étude: {plan['total_estimated_hours']:.1f}h")
```

---

## 🎯 Utilisation Complète avec Hand History

### Workflow Complet

```
Hand History → Parser → Calculateur Stats → Analyseur → Rapports
```

### Script Complet

```python
#!/usr/bin/env python3
"""
Analyse complète depuis les hand histories
"""
from src.parsers import PokerStarsParser
from src.stats import StatsCalculator
from src.analysis import LeakDetector
from src.database import DatabaseManager

# === 1. PARSER LES HAND HISTORIES ===
print("📁 Parsing des hand histories...")
parser = PokerStarsParser()
hands = parser.parse_file('mes_mains.txt')
print(f"✓ {len(hands)} mains parsées")

# === 2. SAUVEGARDER EN BASE ===
print("💾 Sauvegarde en base de données...")
db = DatabaseManager('poker_data.db')
for hand in hands:
    db.save_hand(hand)
print(f"✓ Données sauvegardées")

# === 3. CALCULER LES STATS ===
print("📊 Calcul des statistiques...")
calculator = StatsCalculator()
mes_stats = calculator.calculate_player_stats('VotreNom', hands)
print(f"✓ {len(mes_stats)} stats calculées")

# === 4. ANALYSER LES LEAKS ===
print("🔍 Détection des leaks...")
detector = LeakDetector(stakes='PLO100')
analyse = detector.detect_leaks(mes_stats, sample_size=len(hands))

# === 5. GÉNÉRER LE RAPPORT ===
rapport = detector.format_leak_report(analyse)
print(rapport)

# Sauvegarder le rapport
with open('mon_rapport_leaks.txt', 'w') as f:
    f.write(rapport)
print("\n✓ Rapport sauvegardé dans mon_rapport_leaks.txt")
```

---

## 📋 Statistiques Supportées

### 20+ Stats Essentielles

#### Preflop (8 stats)
- `vpip` - Voluntarily Put In Pot
- `pfr` - Preflop Raise
- `three_bet` - 3-Bet %
- `fold_vs_3bet` - Fold vs 3-Bet
- `fold_vs_3bet_ip` - Fold vs 3-Bet In Position
- `fold_vs_3bet_oop` - Fold vs 3-Bet Out of Position
- `four_bet` - 4-Bet %
- `fold_vs_4bet` - Fold vs 4-Bet

#### Postflop Aggression (6 stats)
- `cbet_freq` - C-Bet Overall
- `cbet_freq_flop` - C-Bet Flop
- `cbet_freq_turn` - C-Bet Turn
- `cbet_freq_river` - C-Bet River
- `double_barrel` - Double Barrel %
- `triple_barrel` - Triple Barrel %

#### Postflop Defense (4 stats)
- `fold_vs_cbet` - Fold vs C-Bet Overall
- `fold_vs_cbet_flop` - Fold vs Flop C-Bet
- `fold_vs_cbet_turn` - Fold vs Turn C-Bet
- `fold_vs_cbet_river` - Fold vs River C-Bet

#### River (2 stats)
- `wtsd` - Went to Showdown
- `w_sd` - Won at Showdown

---

## ⚙️ Configuration

### Changer les Stakes

```python
# Pour PLO50
comparator = GTOComparator(stakes='PLO50')
detector = LeakDetector(stakes='PLO50')

# Pour PLO100 (défaut)
comparator = GTOComparator(stakes='PLO100')

# Pour PLO200
comparator = GTOComparator(stakes='PLO200')
```

### Ajuster la Sévérité Minimum

```python
# Tous les leaks (même LOW)
leaks = comparator.get_leaks(stats, min_severity='LOW')

# Seulement MEDIUM et plus (défaut)
leaks = comparator.get_leaks(stats, min_severity='MEDIUM')

# Seulement HIGH et CRITICAL
leaks = comparator.get_leaks(stats, min_severity='HIGH')
```

### Personnaliser le Plan d'Étude

```python
# 5 zones de focus au lieu de 3
plan = detector.get_study_plan(stats, sample_size=500, focus_areas=5)

# 2 zones seulement (plus concentré)
plan = detector.get_study_plan(stats, sample_size=500, focus_areas=2)
```

---

## 📈 Suivi de Progression

### Tracker vos Améliorations

```python
from src.analysis import LeakDetector
from datetime import datetime, timedelta

detector = LeakDetector()

# Session 1 (il y a 2 semaines)
stats_s1 = {'vpip': 35.0, 'pfr': 15.0, 'three_bet': 5.0}
detector.detect_leaks(
    stats_s1,
    sample_size=200,
    session_date=datetime.now() - timedelta(days=14)
)

# Session 2 (il y a 1 semaine)
stats_s2 = {'vpip': 30.0, 'pfr': 18.0, 'three_bet': 6.5}
detector.detect_leaks(
    stats_s2,
    sample_size=250,
    session_date=datetime.now() - timedelta(days=7)
)

# Session 3 (aujourd'hui)
stats_s3 = {'vpip': 26.0, 'pfr': 20.0, 'three_bet': 8.0}
detector.detect_leaks(
    stats_s3,
    sample_size=300,
    session_date=datetime.now()
)

# Analyser la progression
progression = detector.track_improvement(days=30)

print(f"Trend: {progression['trending']}")
print(f"Score: {progression['overall_improvement_score']}")

for imp in progression['improvements']:
    if imp['improved']:
        print(f"✅ {imp['stat_display']}: amélioration de {abs(imp['change']):.1f}%")
```

### Identifier les Leaks Persistants

```python
# Leaks qui apparaissent dans au moins 3 sessions
persistants = detector.identify_persistent_leaks(min_occurrences=3)

for leak in persistants:
    print(f"⚠️ {leak['stat_display_name']}")
    print(f"   Apparaît dans {leak['occurrences']} sessions")
    print(f"   Persistance: {leak['persistence_rate']:.0f}%")
```

---

## 💡 Exemples d'Utilisation

### Exemple 1: Analyse Rapide

```bash
python3 -c "
from src.analysis import GTOComparator

stats = {'vpip': 28, 'pfr': 20, 'three_bet': 8}
comp = GTOComparator()
leaks = comp.get_leaks(stats)

print(f'{len(leaks)} leaks trouvés:')
for l in leaks:
    print(f'- {l[\"stat_display_name\"]}: {l[\"delta\"]:+.1f}%')
"
```

### Exemple 2: Rapport Formaté

```python
from src.analysis import LeakDetector

stats = {
    'vpip': 30.0, 'pfr': 18.0, 'three_bet': 6.0,
    'cbet_freq_flop': 52.0, 'fold_vs_cbet_flop': 48.0
}

detector = LeakDetector()
analyse = detector.detect_leaks(stats, sample_size=300)
rapport = detector.format_leak_report(analyse)

# Afficher
print(rapport)

# Sauvegarder
with open('rapport.txt', 'w') as f:
    f.write(rapport)
```

### Exemple 3: Calcul EV Loss

```python
from src.analysis import GTOComparator

stats = {'vpip': 35.0}  # Trop loose!
comp = GTOComparator()
leaks = comp.get_leaks(stats)

for leak in leaks:
    ev = comp.calculate_ev_loss(
        leak,
        hands_per_hour=100,
        hours_played=50  # 50 heures de jeu
    )
    print(f"{leak['stat_display_name']}:")
    print(f"  Perte: {ev['ev_loss_bb100']:.2f} BB/100")
    print(f"  Total: {ev['total_ev_loss_bb']:.0f} BB sur {ev['total_hands']} mains")
```

---

## 🔧 Dépannage

### Problème: "Module not found"

**Solution:**
```bash
# Assurez-vous d'être dans le bon répertoire
cd /home/user/garvazz

# Vérifier que Python trouve les modules
python3 -c "import sys; print(sys.path)"

# Tester l'import
python3 -c "from src.analysis import GTOComparator; print('OK')"
```

### Problème: "No leaks detected" mais vous savez qu'il y en a

**Solution:** Vérifiez que vos stats ont les bons noms:
```python
from src.stats.definitions import STAT_DEFINITIONS

# Lister toutes les stats disponibles
print("Stats disponibles:")
for stat_name in STAT_DEFINITIONS.keys():
    print(f"- {stat_name}")
```

### Problème: Résultats peu fiables

**Solution:** Augmentez la taille d'échantillon
```python
# Minimum recommandé: 100 mains
# Idéal: 500+ mains
# Très fiable: 1000+ mains

analyse = detector.detect_leaks(stats, sample_size=1000)
print(f"Fiable: {analyse['reliable']}")  # Doit être True
```

---

## 📚 Ressources

### Fichiers Importants

- `src/analysis/gto_comparison.py` - Module de comparaison GTO
- `src/analysis/leak_detector.py` - Détecteur de leaks
- `src/stats/definitions.py` - Définitions des stats et baselines GTO
- `scripts/demo_analysis.py` - Script de démonstration
- `output_demo_analysis.txt` - Exemple de sortie

### Commandes Utiles

```bash
# Lancer la démo complète
python3 scripts/demo_analysis.py

# Afficher le rapport d'exemple
cat output_demo_analysis.txt

# Tester les imports
python3 -c "from src.analysis import GTOComparator, LeakDetector; print('✓')"

# Lister toutes les stats
python3 -c "from src.stats.definitions import get_essential_stats; print(get_essential_stats())"
```

---

## 🎓 Workflow Recommandé

### Pour Débutants

1. **Lancer la démo** pour comprendre les fonctionnalités
   ```bash
   python3 scripts/demo_analysis.py
   ```

2. **Créer un fichier avec vos stats** (depuis votre tracker)
   ```python
   mes_stats = {'vpip': ..., 'pfr': ..., ...}
   ```

3. **Analyser vos leaks**
   ```python
   from src.analysis import LeakDetector
   detector = LeakDetector()
   analyse = detector.detect_leaks(mes_stats, sample_size=500)
   ```

4. **Suivre le plan d'étude généré**

### Pour Utilisateurs Avancés

1. Parser vos hand histories
2. Calculer les stats automatiquement
3. Analyser sur plusieurs sessions
4. Tracker la progression
5. Identifier les leaks persistants
6. Ajuster votre stratégie

---

## 📞 Support

Pour plus d'aide:
- Consulter `README.md`
- Examiner les exemples dans `scripts/`
- Lire le code source documenté

**Bon courage pour corriger vos leaks et améliorer votre jeu! 🚀**
