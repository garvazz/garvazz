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

# Vérifier que Streamlit est installé
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit n'est pas installé. Installation en cours..."
    pip install streamlit plotly streamlit-aggrid -q
    echo "✅ Streamlit installé!"
fi

echo "🚀 Lancement de l'application web..."
echo ""
echo "📍 L'application sera accessible à l'adresse:"
echo "   👉 http://localhost:8501"
echo ""
echo "💡 Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Lancer Streamlit
cd webapp
streamlit run app.py
