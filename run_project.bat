@echo off
title LLM Cognitive Bias Lab
color 0B

echo ========================================================
echo        Lancement de l'interface d'experimentation
echo ========================================================
echo.

:: Rediriger les dossiers temporaires vers E: pour eviter le disque C: plein
set "TMP=E:\IA PFE\temp"
set "TEMP=E:\IA PFE\temp"
set "PIP_CACHE_DIR=E:\IA PFE\temp"

cd /d "E:\IA PFE"

:: Verification de l'environnement virtuel
if not exist ".venv\Scripts\activate.bat" (
    echo [ERREUR] L'environnement virtuel est introuvable.
    pause
    exit /b
)

:: Activation et lancement
call ".venv\Scripts\activate.bat"
echo Demarrage du serveur Streamlit...
streamlit run app.py

pause
