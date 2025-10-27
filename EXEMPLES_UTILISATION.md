# 📖 Exemples d'Utilisation - PLO Mastery Suite

Guide pratique avec exemples concrets pour lancer l'outil.

---

## 🚀 MÉTHODE 1: Lancer la Démo Complète (Recommandé)

La manière la plus simple pour voir toutes les fonctionnalités:

```bash
cd /home/user/garvazz
python3 scripts/demo_analysis.py
```

**Ce que vous verrez:**
- Comparaison GTO complète
- Détection de 14 leaks
- Plan d'étude personnalisé
- Suivi de progression sur 3 sessions
- Rapports formatés

**Durée:** ~30 secondes

---

## 🎯 MÉTHODE 2: Analyser VOS Stats (Le plus utile!)

### Option A: Modifier le Script Quick Start

1. **Ouvrir le fichier:**
   ```bash
   nano analyser_mes_stats.py
   # ou avec votre éditeur préféré
   ```

2. **Modifier la section MES_STATS** (ligne 19):
   ```python
   MES_STATS = {
       'vpip': 30.5,      # VOS vraies valeurs ici
       'pfr': 22.0,       #
       'three_bet': 9.0,
       'cbet_freq_flop': 58.0,
       'fold_vs_cbet_flop': 45.0,
       'wtsd': 26.0,
       'w_sd': 50.0,
   }

   NOMBRE_DE_MAINS = 750  # Nombre de mains analysées
   ```

3. **Lancer l'analyse:**
   ```bash
   python3 analyser_mes_stats.py
   ```

4. **Sauvegarder le rapport (optionnel):**
   ```bash
   python3 analyser_mes_stats.py > mon_rapport_$(date +%Y%m%d).txt
   ```

### Option B: Script One-Liner Rapide

Pour une analyse ultra-rapide en ligne de commande:

```bash
python3 << 'EOF'
from src.analysis import GTOComparator

# VOS STATS ICI
stats = {'vpip': 32, 'pfr': 18, 'three_bet': 6, 'cbet_freq_flop': 52}

comp = GTOComparator()
leaks = comp.get_leaks(stats)

print(f"\n🔍 {len(leaks)} leaks détectés:\n")
for i, leak in enumerate(leaks, 1):
    print(f"{i}. {leak['stat_display_name']}: {leak['delta']:+.1f}% [{leak['severity']}]")
EOF
```

### Option C: Mode Interactif Python

```bash
python3
```

Puis:
```python
>>> from src.analysis import GTOComparator, LeakDetector
>>>
>>> # Vos stats
>>> mes_stats = {
...     'vpip': 28.0,
...     'pfr': 20.0,
...     'three_bet': 8.0,
...     'cbet_freq_flop': 60.0,
...     'fold_vs_cbet_flop': 42.0,
...     'wtsd': 25.0,
...     'w_sd': 50.0
... }
>>>
>>> # Analyser
>>> comp = GTOComparator()
>>> leaks = comp.get_leaks(mes_stats)
>>>
>>> # Résultats
>>> print(f"{len(leaks)} leaks détectés")
>>>
>>> # Détails du premier leak
>>> if leaks:
...     leak = leaks[0]
...     print(f"\nTop leak: {leak['stat_display_name']}")
...     print(f"Votre valeur: {leak['player_value']:.1f}%")
...     print(f"GTO: {leak['gto_value']:.1f}%")
...     print(f"Déviation: {leak['delta']:+.1f}%")
...
>>> # Plan d'étude
>>> detector = LeakDetector()
>>> plan = detector.get_study_plan(mes_stats, sample_size=500, focus_areas=2)
>>> print(f"\nTemps d'étude: {plan['total_estimated_hours']:.1f}h")
>>>
>>> # Quitter
>>> exit()
```

---

## 📊 EXEMPLES DE STATS À ANALYSER

### Exemple 1: Joueur Trop Loose/Passif

```python
stats_loose_passive = {
    'vpip': 35.0,       # Trop loose (GTO: 25%)
    'pfr': 15.0,        # Trop passif (GTO: 20%)
    'three_bet': 5.0,   # Pas assez de 3-bets (GTO: 8%)
    'cbet_freq_flop': 45.0,  # Pas assez de c-bets (GTO: 60%)
    'fold_vs_cbet_flop': 55.0,  # Fold trop (GTO: 42%)
}

# Analyser
from src.analysis import GTOComparator
comp = GTOComparator()
leaks = comp.get_leaks(stats_loose_passive)

for leak in leaks:
    print(f"- {leak['stat_display_name']}: {leak['delta']:+.1f}% [{leak['severity']}]")
```

**Résultat attendu:**
- VPIP trop élevé (leak HIGH)
- PFR trop bas (leak MEDIUM)
- 3-bet trop bas (leak MEDIUM)
- C-bet flop trop bas (leak MEDIUM)
- Fold vs c-bet trop haut (leak MEDIUM)

### Exemple 2: Joueur Trop Tight/Agressif

```python
stats_tight_aggressive = {
    'vpip': 18.0,       # Trop tight (GTO: 25%)
    'pfr': 16.0,        # Trop tight (GTO: 20%)
    'three_bet': 12.0,  # Trop de 3-bets (GTO: 8%)
    'cbet_freq_flop': 75.0,  # Trop de c-bets (GTO: 60%)
    'fold_vs_3bet': 70.0,    # Fold trop vs 3-bet (GTO: 55%)
}
```

### Exemple 3: Joueur avec Stats Partielles

Si vous n'avez que quelques stats:

```python
stats_partielles = {
    'vpip': 26.0,
    'pfr': 19.0,
    'wtsd': 24.0,
    'w_sd': 52.0
}

# Ça fonctionne quand même!
from src.analysis import LeakDetector
detector = LeakDetector()
analyse = detector.detect_leaks(stats_partielles, sample_size=300)

print(f"Leaks: {analyse['total_leaks']}")
for rec in analyse['recommendations']:
    print(f"- {rec['stat_display']}: {rec['recommendation']}")
```

---

## 🔄 SUIVI DE PROGRESSION

Pour tracker vos améliorations sur plusieurs sessions:

```python
from src.analysis import LeakDetector
from datetime import datetime, timedelta

detector = LeakDetector()

# Session 1 - Il y a 2 semaines (avec leaks)
stats_s1 = {
    'vpip': 35.0, 'pfr': 16.0, 'three_bet': 5.5,
    'cbet_freq_flop': 48.0, 'fold_vs_cbet_flop': 52.0
}
detector.detect_leaks(
    stats_s1,
    sample_size=400,
    session_date=datetime.now() - timedelta(days=14)
)
print("✓ Session 1 enregistrée")

# Session 2 - Il y a 1 semaine (amélioration)
stats_s2 = {
    'vpip': 29.0, 'pfr': 18.0, 'three_bet': 7.0,
    'cbet_freq_flop': 55.0, 'fold_vs_cbet_flop': 46.0
}
detector.detect_leaks(
    stats_s2,
    sample_size=500,
    session_date=datetime.now() - timedelta(days=7)
)
print("✓ Session 2 enregistrée")

# Session 3 - Aujourd'hui (encore mieux!)
stats_s3 = {
    'vpip': 26.0, 'pfr': 20.0, 'three_bet': 8.5,
    'cbet_freq_flop': 59.0, 'fold_vs_cbet_flop': 43.0
}
detector.detect_leaks(
    stats_s3,
    sample_size=600,
    session_date=datetime.now()
)
print("✓ Session 3 enregistrée")

# Analyser la progression
progress = detector.track_improvement(days=30)

print(f"\n📈 PROGRESSION:")
print(f"Trend: {progress['trending']}")
print(f"Score: {progress['overall_improvement_score']}")
print(f"\nAméliorations par stat:")
for imp in progress['improvements']:
    if imp['improved']:
        symbole = "✅ FIXÉ" if imp.get('fixed') else "📈 AMÉLIORÉ"
        print(f"{symbole} {imp['stat_display']}: {imp['change']:+.1f}%")

# Identifier leaks persistants
persistants = detector.identify_persistent_leaks(min_occurrences=2)
if persistants:
    print(f"\n⚠️  LEAKS PERSISTANTS:")
    for leak in persistants:
        print(f"- {leak['stat_display_name']}: {leak['persistence_rate']:.0f}% des sessions")
```

---

## 💾 SAUVEGARDER LES RAPPORTS

### Méthode 1: Redirection de sortie

```bash
# Rapport simple
python3 analyser_mes_stats.py > rapport_$(date +%Y%m%d).txt

# Voir le rapport
cat rapport_20251027.txt
```

### Méthode 2: Dans le script Python

```python
from src.analysis import LeakDetector

mes_stats = {'vpip': 30, 'pfr': 18, 'three_bet': 6}

detector = LeakDetector()
analyse = detector.detect_leaks(mes_stats, sample_size=500)

# Générer le rapport formaté
rapport = detector.format_leak_report(analyse)

# Sauvegarder
with open('mon_rapport_leaks.txt', 'w', encoding='utf-8') as f:
    f.write(rapport)

print("✓ Rapport sauvegardé dans mon_rapport_leaks.txt")
```

### Méthode 3: Avec horodatage

```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"rapport_leaks_{timestamp}.txt"

with open(filename, 'w', encoding='utf-8') as f:
    f.write(rapport)

print(f"✓ Rapport: {filename}")
```

---

## 📈 CALCULER LA PERTE EV

Pour estimer combien vos leaks vous coûtent:

```python
from src.analysis import GTOComparator

mes_stats = {
    'vpip': 35.0,  # Trop loose
    'cbet_freq_flop': 45.0,  # Pas assez de c-bets
}

comp = GTOComparator()
leaks = comp.get_leaks(mes_stats)

print("\n💸 ESTIMATION DES PERTES EV:\n")

total_loss = 0
for leak in leaks:
    # Sur 100 heures de jeu à 100 mains/heure
    ev = comp.calculate_ev_loss(
        leak,
        hands_per_hour=100,
        hours_played=100
    )

    print(f"{leak['stat_display_name']}:")
    print(f"  Perte: {ev['ev_loss_bb100']:.2f} BB/100")
    print(f"  Sur 100h: {ev['total_ev_loss_bb']:.0f} BB")
    print()

    total_loss += ev['total_ev_loss_bb']

print(f"TOTAL ESTIMÉ: ~{total_loss:.0f} BB perdus sur 100h de jeu")
print(f"(soit ~{total_loss/100:.0f} buy-ins à PLO100)")
```

---

## 🎓 WORKFLOW RECOMMANDÉ

### Pour débutants:

```bash
# 1. Voir la démo
python3 scripts/demo_analysis.py

# 2. Éditer vos stats
nano analyser_mes_stats.py

# 3. Analyser
python3 analyser_mes_stats.py

# 4. Sauvegarder
python3 analyser_mes_stats.py > mon_premier_rapport.txt
```

### Pour utilisateurs réguliers:

```bash
# Workflow hebdomadaire:

# 1. Exporter vos stats depuis votre tracker (ex: PT4, HM3)
#    → Copier VPIP, PFR, 3bet, etc.

# 2. Créer un script de session
cat > session_$(date +%Y%m%d).py << 'EOF'
from src.analysis import LeakDetector
from datetime import datetime

stats_today = {
    'vpip': 27.5,
    'pfr': 19.5,
    'three_bet': 8.2,
    'cbet_freq_flop': 58.0,
    # ... autres stats
}

detector = LeakDetector()
analyse = detector.detect_leaks(stats_today, sample_size=850)
rapport = detector.format_leak_report(analyse)

# Sauvegarder
filename = f"rapport_{datetime.now().strftime('%Y%m%d')}.txt"
with open(filename, 'w') as f:
    f.write(rapport)

print(f"✓ Rapport: {filename}")
print(f"✓ Leaks: {analyse['total_leaks']}")
EOF

# 3. Exécuter
python3 session_$(date +%Y%m%d).py

# 4. Consulter
cat rapport_*.txt | tail -50
```

---

## 🔧 ASTUCES & TIPS

### Astuce 1: Analyse Rapide en Une Ligne

```bash
python3 -c "from src.analysis import GTOComparator; leaks = GTOComparator().get_leaks({'vpip': 32, 'pfr': 16}); print(f'{len(leaks)} leaks'); [print(f\"- {l['stat_display_name']}: {l['delta']:+.1f}%\") for l in leaks]"
```

### Astuce 2: Vérifier Quelles Stats Sont Disponibles

```python
from src.stats.definitions import STAT_DEFINITIONS

print("Stats disponibles:")
for stat_name, definition in STAT_DEFINITIONS.items():
    print(f"- {stat_name:20s}: {definition['name']} (GTO: {definition['gto_baseline']:.1f}%)")
```

### Astuce 3: Comparer Deux Sessions

```python
from src.analysis import GTOComparator

session1 = {'vpip': 35, 'pfr': 15, 'three_bet': 5}
session2 = {'vpip': 28, 'pfr': 19, 'three_bet': 8}

comp = GTOComparator()

print("SESSION 1:")
leaks1 = comp.get_leaks(session1)
print(f"Leaks: {len(leaks1)}")

print("\nSESSION 2:")
leaks2 = comp.get_leaks(session2)
print(f"Leaks: {len(leaks2)}")

print(f"\nAmélioration: {len(leaks1) - len(leaks2)} leaks corrigés!")
```

---

## ❓ FAQ

**Q: Combien de mains minimum pour une analyse fiable?**
- Minimum absolu: 50 mains (peu fiable)
- Minimum recommandé: 100 mains
- Bon: 500 mains
- Très fiable: 1000+ mains

**Q: Je n'ai pas toutes les stats, ça pose problème?**
- Non! L'outil analyse seulement les stats que vous fournissez
- Minimum conseillé: 5-6 stats de base (VPIP, PFR, 3bet, cbet, fold vs cbet)

**Q: Comment obtenir mes stats?**
- PokerTracker 4 ou Hold'em Manager
- Export manuel depuis votre room de poker
- Calculateur de stats custom

**Q: Les baselines GTO sont-elles fiables?**
- Basées sur les solvers modernes (PioSOLVER, GTO+)
- Adaptées pour PLO 6-max
- Peuvent varier légèrement selon pool de joueurs

**Q: Dois-je corriger tous les leaks?**
- Non! Concentrez-vous sur 2-3 leaks max en même temps
- Priorisez les leaks HIGH et CRITICAL
- Suivez le plan d'étude généré

---

## 📞 BESOIN D'AIDE?

1. Relire `GUIDE_UTILISATION.md`
2. Vérifier `README.md`
3. Examiner `scripts/demo_analysis.py`
4. Consulter le code source (bien documenté)

**Bon courage dans votre quête PLO! 🚀**
