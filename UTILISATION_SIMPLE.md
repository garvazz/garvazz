# Guide d'Utilisation Simple - PLO Mastery Suite

**L'interface web n'est pas accessible dans cet environnement.**
**Utilisez les scripts Python directement - c'est tout aussi simple!**

---

## METHODE 1: Voir une Demo (30 secondes)

```bash
cd /home/user/garvazz
python3 scripts/demo_analysis.py
```

Vous verrez:
- Comparaison avec GTO
- Detection de leaks
- Calcul de perte EV
- Plan d'etude personnalise

---

## METHODE 2: Analyser VOS Stats (Le plus utile!)

### Etape 1: Editer vos stats

```bash
nano analyser_mes_stats.py
```

### Etape 2: Modifier la section MES_STATS (ligne 27)

Remplacez par VOS valeurs:

```python
MES_STATS = {
    'vpip': 28.0,              # <-- Changez ca
    'pfr': 20.0,               # <-- Et ca
    'three_bet': 8.5,          # <-- Et ca
    'cbet_freq_flop': 58.0,    # <-- Etc...
    'fold_vs_cbet_flop': 43.0,
    'wtsd': 26.0,
    'w_sd': 50.0,
}

NOMBRE_DE_MAINS = 500  # Nombre de mains analysees
```

**Vous n'avez pas besoin de toutes les stats!**
Minimum 5-6 stats suffisent (VPIP, PFR, 3bet, cbet, fold vs cbet)

### Etape 3: Sauvegarder et lancer

```bash
# Sauvegarder: Ctrl+O puis Enter
# Quitter: Ctrl+X

# Lancer l'analyse
python3 analyser_mes_stats.py
```

### Etape 4 (Optionnel): Sauvegarder le rapport

```bash
python3 analyser_mes_stats.py > mon_rapport_$(date +%Y%m%d).txt
```

---

## METHODE 3: Mode One-Liner (Ultra-rapide)

```bash
python3 << 'EOF'
from src.analysis import GTOComparator

# VOS STATS ICI
stats = {
    'vpip': 30,
    'pfr': 18,
    'three_bet': 7,
    'cbet_freq_flop': 55
}

# ANALYSE
comp = GTOComparator()
leaks = comp.get_leaks(stats)

# RESULTATS
print(f"\n{len(leaks)} leaks detectes:")
for leak in leaks:
    print(f"- {leak['stat_display_name']}: {leak['delta']:+.1f}% [{leak['severity']}]")
EOF
```

---

## Stats Disponibles (20+)

Vous pouvez analyser ces stats (copiez les noms exacts):

### Preflop:
- `vpip` - Voluntarily Put In Pot
- `pfr` - Preflop Raise
- `three_bet` - 3-Bet %
- `fold_vs_3bet` - Fold vs 3-Bet
- `fold_vs_3bet_ip` - Fold vs 3-Bet In Position
- `fold_vs_3bet_oop` - Fold vs 3-Bet Out of Position
- `four_bet` - 4-Bet %
- `fold_vs_4bet` - Fold vs 4-Bet

### Postflop Aggression:
- `cbet_freq` - C-Bet Overall
- `cbet_freq_flop` - C-Bet Flop
- `cbet_freq_turn` - C-Bet Turn
- `cbet_freq_river` - C-Bet River
- `double_barrel` - Double Barrel
- `triple_barrel` - Triple Barrel

### Postflop Defense:
- `fold_vs_cbet` - Fold vs C-Bet Overall
- `fold_vs_cbet_flop` - Fold vs Flop C-Bet
- `fold_vs_cbet_turn` - Fold vs Turn C-Bet
- `fold_vs_cbet_river` - Fold vs River C-Bet

### River:
- `wtsd` - Went to Showdown
- `w_sd` - Won at Showdown

---

## Exemple de Resultat

```
ETAPE 1/4: COMPARAISON AVEC GTO
================================

5 LEAKS DETECTES

1. VPIP [HIGH]
   Votre valeur:     35.0%
   GTO baseline:     25.0%
   Deviation:       +10.0%
   Perte EV estimee:  1.50 BB/100
   Sur 10h de jeu:   ~15 BB perdus

2. C-Bet Flop [MEDIUM]
   Votre valeur:     52.0%
   GTO baseline:     60.0%
   Deviation:        -8.0%
   Perte EV estimee:  1.20 BB/100

ETAPE 4/4: PLAN D'ETUDE PERSONNALISE
=====================================

FOCUS #1: VPIP
Severite:      HIGH
Temps estime:  180 minutes (3.0h)

Taches a accomplir:
  1. PRIORITY: Schedule coaching session
  2. Review VPIP ranges in GTO trainer
  3. Study hand charts for 6-max PLO
  4. Review 10 hands where you deviated
```

---

## Commandes Utiles

```bash
# Voir la demo complete
python3 scripts/demo_analysis.py

# Analyser vos stats
python3 analyser_mes_stats.py

# Sauvegarder un rapport
python3 analyser_mes_stats.py > rapport_$(date +%Y%m%d).txt

# Lister toutes les stats disponibles
python3 -c "from src.stats.definitions import STAT_DEFINITIONS; print('\n'.join(STAT_DEFINITIONS.keys()))"

# Voir un rapport d'exemple
cat output_demo_analysis.txt
```

---

## Questions Frequentes

**Q: Combien de mains minimum?**
R: Minimum 100 mains, ideal 500+, tres fiable 1000+

**Q: Je n'ai pas toutes les stats, c'est grave?**
R: Non! Minimum 5-6 stats de base suffisent (VPIP, PFR, 3bet, cbet, fold vs cbet)

**Q: Ou trouver mes stats?**
R: PokerTracker 4, Hold'em Manager, ou export manuel depuis votre site de poker

**Q: Les baselines GTO sont-elles fiables?**
R: Oui, basees sur PioSOLVER et GTO+ pour PLO 6-max

**Q: Dois-je corriger tous les leaks?**
R: Non! Focus sur 2-3 leaks max simultanement, priorisez HIGH/CRITICAL

---

## Depannage

**Probleme: Module not found**
```bash
cd /home/user/garvazz
python3 -c "from src.analysis import GTOComparator; print('OK')"
```

**Probleme: Aucun leak detecte mais vous en avez**
```bash
# Verifier les noms des stats
python3 -c "from src.stats.definitions import STAT_DEFINITIONS; print(list(STAT_DEFINITIONS.keys()))"
```

---

## Workflow Recommande

### Pour Debutants:
```bash
# 1. Voir la demo pour comprendre
python3 scripts/demo_analysis.py

# 2. Editer vos stats
nano analyser_mes_stats.py

# 3. Lancer votre premiere analyse
python3 analyser_mes_stats.py

# 4. Suivre le plan d'etude genere
```

### Pour Utilisateurs Reguliers:
```bash
# 1. Exporter vos stats depuis PT4/HM3
# 2. Mettre a jour analyser_mes_stats.py
# 3. Lancer l'analyse
python3 analyser_mes_stats.py > rapport_hebdo_$(date +%Y%m%d).txt

# 4. Comparer avec le rapport precedent
# 5. Ajuster votre strategie
```

---

**Bon courage pour corriger vos leaks et crusher le PLO!**

Contact: pekinio13@hotmail.fr
