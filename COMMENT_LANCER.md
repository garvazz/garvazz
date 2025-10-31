# 🚀 Comment Lancer l'Outil - PLO Mastery Suite

Guide ultra-rapide pour commencer immédiatement.

---

## 📁 Fichiers Disponibles

| Fichier | Description |
|---------|-------------|
| `scripts/demo_analysis.py` | Démo complète avec données d'exemple |
| `analyser_mes_stats.py` | **Script à utiliser avec VOS stats** |
| `GUIDE_UTILISATION.md` | Documentation complète en français |
| `EXEMPLES_UTILISATION.md` | Exemples concrets et FAQ |
| `output_demo_analysis.txt` | Exemple de rapport généré |

---

## ⚡ Démarrage Rapide - 3 Méthodes

### MÉTHODE 1: Voir la Démo (Recommandé pour débuter)

**La plus simple pour comprendre l'outil:**

```bash
cd /home/user/garvazz
python3 scripts/demo_analysis.py
```

✅ Durée: 30 secondes
✅ Montre toutes les fonctionnalités
✅ Aucune configuration requise

---

### MÉTHODE 2: Analyser VOS Stats (Le plus utile!)

**Pour analyser vos propres statistiques:**

#### Étape 1: Éditer le fichier

```bash
nano analyser_mes_stats.py
# ou utilisez votre éditeur préféré
```

#### Étape 2: Modifier vos stats (ligne 19)

```python
MES_STATS = {
    'vpip': 28.0,      # ← Mettez VOS valeurs ici
    'pfr': 20.0,       # ←
    'three_bet': 8.5,  # ←
    'cbet_freq_flop': 58.0,
    'fold_vs_cbet_flop': 43.0,
    'wtsd': 26.0,
    'w_sd': 50.0,
}

NOMBRE_DE_MAINS = 500  # Nombre de mains analysées
```

#### Étape 3: Lancer l'analyse

```bash
python3 analyser_mes_stats.py
```

#### Étape 4 (Optionnel): Sauvegarder le rapport

```bash
python3 analyser_mes_stats.py > mon_rapport.txt
```

---

### MÉTHODE 3: Mode One-Liner Express

**Pour une analyse ultra-rapide:**

```bash
python3 << 'EOF'
from src.analysis import GTOComparator

# VOS STATS
stats = {'vpip': 30, 'pfr': 18, 'three_bet': 7, 'cbet_freq_flop': 55}

# ANALYSE
comp = GTOComparator()
leaks = comp.get_leaks(stats)

# RÉSULTATS
print(f"\n{len(leaks)} leaks détectés:")
for leak in leaks:
    print(f"- {leak['stat_display_name']}: {leak['delta']:+.1f}% [{leak['severity']}]")
EOF
```

---

## 📊 Statistiques Supportées

### Preflop (8 stats)
- `vpip` - Voluntarily Put In Pot
- `pfr` - Preflop Raise
- `three_bet` - 3-Bet %
- `fold_vs_3bet` - Fold vs 3-Bet
- `fold_vs_3bet_ip` - Fold vs 3-Bet In Position
- `fold_vs_3bet_oop` - Fold vs 3-Bet Out of Position
- `four_bet` - 4-Bet %
- `fold_vs_4bet` - Fold vs 4-Bet

### Postflop Aggression (6 stats)
- `cbet_freq` - C-Bet Overall
- `cbet_freq_flop` - C-Bet Flop
- `cbet_freq_turn` - C-Bet Turn
- `cbet_freq_river` - C-Bet River
- `double_barrel` - Double Barrel
- `triple_barrel` - Triple Barrel

### Postflop Defense (4 stats)
- `fold_vs_cbet` - Fold vs C-Bet Overall
- `fold_vs_cbet_flop` - Fold vs Flop C-Bet
- `fold_vs_cbet_turn` - Fold vs Turn C-Bet
- `fold_vs_cbet_river` - Fold vs River C-Bet

### River (2 stats)
- `wtsd` - Went to Showdown
- `w_sd` - Won at Showdown

**TOTAL: 20+ stats essentielles avec baselines GTO**

---

## ✨ Ce Que l'Outil Fait

✅ **Compare** vos stats avec les baselines GTO
✅ **Identifie** et priorise vos leaks
✅ **Calcule** la perte EV en BB/100
✅ **Génère** un plan d'étude personnalisé
✅ **Track** votre progression dans le temps
✅ **Identifie** les leaks persistants
✅ **Produit** des rapports formatés professionnels

---

## 📝 Exemple de Résultat

```
ÉTAPE 1/4: COMPARAISON AVEC GTO
════════════════════════════════

⚠️  5 LEAKS DÉTECTÉS

🔴 1. VPIP [HIGH]
   Votre valeur:     35.0%
   GTO baseline:     25.0%
   Déviation:       +10.0%
   Perte EV estimée:  1.50 BB/100
   Sur 10h de jeu:   ~15 BB perdus

🟡 2. C-Bet Flop [MEDIUM]
   Votre valeur:     52.0%
   GTO baseline:     60.0%
   Déviation:        -8.0%
   Perte EV estimée:  1.20 BB/100

📈 SCORE GLOBAL
Score d'optimisation: 60.0%
Stats optimales:      3/8

ÉTAPE 4/4: PLAN D'ÉTUDE PERSONNALISÉ
═════════════════════════════════════

📚 Plan d'étude avec 2 zones de focus
⏱️  Temps total estimé: 5.0 heures

🔴 FOCUS #1: VPIP
Sévérité:      HIGH
Priorité:      2.17/4.0
Temps estimé:  180 minutes (3.0h)

Tâches à accomplir:
  ⭐ 1. PRIORITY: Schedule coaching session to review this leak
     2. Review VPIP ranges in GTO trainer
     3. Study hand charts for 6-max PLO
     4. Review 10 hands where you deviated from optimal range
```

---

## 💡 Conseils Importants

| Aspect | Recommandation |
|--------|----------------|
| **Minimum de mains** | 100 mains (fiable à partir de 500+) |
| **Stats requises** | Minimum 5-6 stats, pas besoin de toutes |
| **Focus** | Concentrez-vous sur 2-3 leaks à la fois |
| **Réanalyse** | Tous les 500-1000 mains |
| **Priorisation** | Corrigez d'abord les leaks HIGH et CRITICAL |

---

## 🎯 Commandes Essentielles

```bash
# Voir la démo complète
python3 scripts/demo_analysis.py

# Analyser vos stats (après édition du fichier)
python3 analyser_mes_stats.py

# Sauvegarder un rapport avec date
python3 analyser_mes_stats.py > rapport_$(date +%Y%m%d).txt

# Voir l'exemple de rapport
cat output_demo_analysis.txt

# Lire le guide complet
cat GUIDE_UTILISATION.md

# Voir les exemples
cat EXEMPLES_UTILISATION.md

# Lister toutes les stats disponibles
python3 -c "from src.stats.definitions import STAT_DEFINITIONS; print('\n'.join(STAT_DEFINITIONS.keys()))"
```

---

## 📚 Documentation Complète

Pour aller plus loin:

- **`GUIDE_UTILISATION.md`** - Documentation complète et détaillée
- **`EXEMPLES_UTILISATION.md`** - Exemples pratiques et FAQ
- **`output_demo_analysis.txt`** - Exemple de rapport complet

---

## 🎓 Workflow Recommandé

### Pour Débutants

```bash
# 1. Voir la démo pour comprendre
python3 scripts/demo_analysis.py

# 2. Éditer vos stats
nano analyser_mes_stats.py

# 3. Lancer votre première analyse
python3 analyser_mes_stats.py

# 4. Suivre le plan d'étude généré
```

### Pour Utilisateurs Réguliers

```bash
# 1. Exporter vos stats depuis PT4/HM3
# 2. Mettre à jour analyser_mes_stats.py
# 3. Lancer l'analyse
python3 analyser_mes_stats.py > rapport_hebdo_$(date +%Y%m%d).txt

# 4. Comparer avec le rapport précédent
# 5. Ajuster votre stratégie
```

---

## ❓ Questions Fréquentes

**Q: Combien de mains minimum?**
R: Minimum 100 mains, idéal 500+, très fiable 1000+

**Q: Je n'ai pas toutes les stats, c'est grave?**
R: Non! Minimum 5-6 stats de base suffisent (VPIP, PFR, 3bet, cbet, fold vs cbet)

**Q: Où trouver mes stats?**
R: PokerTracker 4, Hold'em Manager, ou export manuel depuis votre site de poker

**Q: Les baselines GTO sont-elles fiables?**
R: Oui, basées sur PioSOLVER et GTO+ pour PLO 6-max

**Q: Dois-je corriger tous les leaks?**
R: Non! Focus sur 2-3 leaks max simultanément, priorisez HIGH/CRITICAL

---

## 🔧 Dépannage Rapide

**Problème: Module not found**
```bash
# Vérifier que vous êtes dans le bon dossier
cd /home/user/garvazz
pwd

# Tester l'import
python3 -c "from src.analysis import GTOComparator; print('OK')"
```

**Problème: Aucun leak détecté mais vous en avez**
```bash
# Vérifier les noms des stats
python3 -c "from src.stats.definitions import STAT_DEFINITIONS; print(list(STAT_DEFINITIONS.keys()))"
```

---

## 📞 Support

Besoin d'aide? Consultez dans l'ordre:
1. Ce fichier (`COMMENT_LANCER.md`)
2. `GUIDE_UTILISATION.md` - Guide complet
3. `EXEMPLES_UTILISATION.md` - Exemples pratiques
4. Le code source (bien documenté)

---

**🎯 Bon courage pour corriger vos leaks et crusher le PLO! 🚀**

Contact: pekinio13@hotmail.fr
