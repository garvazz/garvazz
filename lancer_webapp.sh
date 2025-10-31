#!/bin/bash
# Script de lancement de l'application web PLO Mastery Suite

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         PLO Mastery Suite - Application Web               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "lancer_webapp.sh" ]; then
    echo "❌ Erreur: Ce script doit être lancé depuis le répertoire racine du projet"
    echo "   cd /home/user/garvazz && ./lancer_webapp.sh"
    exit 1
fi

# Vérifier Python
echo "🔍 Vérification des prérequis..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python 3 n'est pas installé"
    exit 1
fi

# Vérifier que Streamlit est installé
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit n'est pas installé. Installation en cours..."
    pip install streamlit plotly streamlit-aggrid -q
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation de Streamlit"
        exit 1
    fi
    echo "✅ Streamlit installé!"
fi

# Vérifier les modules Python
echo "🔍 Vérification des modules Python..."
python3 -c "from src.analysis import GTOComparator" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Les modules du projet ne sont pas accessibles"
    echo "   Assurez-vous d'être dans le répertoire racine du projet"
    exit 1
fi
echo "✅ Modules Python OK"

# Vérifier si le port est disponible
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo ""
    echo "⚠️  Le port 8501 est déjà utilisé!"
    echo "   Une application Streamlit est peut-être déjà en cours d'exécution."
    echo ""
    echo "   Pour arrêter l'application en cours, tapez:"
    echo "   pkill -f 'streamlit run'"
    echo ""
    read -p "Voulez-vous arrêter l'application en cours et continuer? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        pkill -f "streamlit run"
        sleep 2
        echo "✅ Application arrêtée"
    else
        echo "❌ Lancement annulé"
        exit 1
    fi
fi

echo ""
echo "🚀 Lancement de l'application web..."
echo ""
echo "📍 L'application sera accessible à l'adresse:"
echo "   👉 http://localhost:8501"
echo ""
echo "💡 Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Lancer Streamlit depuis le répertoire racine
streamlit run webapp/app.py
