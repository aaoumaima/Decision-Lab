@echo off
setlocal EnableDelayedExpansion
title Ollama Model Installer / Pack
color 0A

:check_ollama
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo =======================================================
    echo [ERREUR] Ollama n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Ollama depuis https://ollama.com/
    echo =======================================================
    pause
    exit /b
)

:menu
cls
color 0B
echo ==============================================================================
echo                           OLLAMA MODEL PACK
echo ==============================================================================
echo Choisissez le modele a installer. Assurez-vous d'avoir assez de RAM/VRAM !
echo.
echo --- MODELES GENERALISTES (Recommandes pour usage standard) ---
echo  [1] Llama 3.1 (8B)      - ~4.7 GB (Meta) - Le standard actuel, tres intelligent
echo  [2] Mistral (7B)        - ~4.1 GB (Mistral AI) - Tres rapide et performant
echo  [3] Gemma 2 (9B)        - ~5.5 GB (Google) - Excellent pour le raisonnement
echo.
echo --- MODELES LEGERS (Pour petits PCs / Laptops) ---
echo  [4] Phi 3 Mini (3.8B)   - ~2.3 GB (Microsoft) - Impressionnant pour sa taille
echo  [5] Qwen 2.5 (1.5B)     - ~1.0 GB (Alibaba) - Ultra leger, parfait pour tester
echo  [6] Gemma 2 (2B)        - ~1.6 GB (Google) - Tres bonne alternative legere
echo.
echo --- MODELES LOURDS (Pour PCs Puissants - 16GB+ RAM requis) ---
echo  [7] Mixtral (8x7B)      - ~26 GB (Mistral AI) - Modele expert tres puissant
echo  [8] Llama 3.1 (70B)     - ~40 GB (Meta) - Niveau GPT-4, necessite gros PC
echo  [9] Command R (35B)     - ~20 GB (Cohere) - Excellent pour le RAG
echo.
echo --- MODELES SPECIALISES (Code / Vision) ---
echo  [10] LLaVA (7B)         - ~4.5 GB - Modele Vision (analyse et decrit les images)
echo  [11] DeepSeek Coder (6.7B)- ~3.8 GB - Excellent pour la programmation
echo  [12] Qwen 2.5 Coder (7B)- ~4.4 GB - Nouvelle generation experte pour le code
echo.
echo  [13] Saisir un nom de modele manuel...
echo.
echo  [0] Quitter
echo ==============================================================================
echo.

set /p choix="> Entrez votre choix (0-13) : "

if "%choix%"=="1" set nom_modele=llama3.1
if "%choix%"=="2" set nom_modele=mistral
if "%choix%"=="3" set nom_modele=gemma2
if "%choix%"=="4" set nom_modele=phi3
if "%choix%"=="5" set nom_modele=qwen2.5:1.5b
if "%choix%"=="6" set nom_modele=gemma2:2b
if "%choix%"=="7" set nom_modele=mixtral
if "%choix%"=="8" set nom_modele=llama3.1:70b
if "%choix%"=="9" set nom_modele=command-r
if "%choix%"=="10" set nom_modele=llava
if "%choix%"=="11" set nom_modele=deepseek-coder:6.7b
if "%choix%"=="12" set nom_modele=qwen2.5-coder:7b
if "%choix%"=="13" goto custom_model
if "%choix%"=="0" goto fin

:: Si le choix n'est pas reconnu, on retourne au menu
if not defined nom_modele goto menu

goto install

:custom_model
echo.
set /p nom_modele="> Entrez le nom exact du modele (voir https://ollama.com/library) : "
if "%nom_modele%"=="" goto menu
goto install

:install
cls
color 0E
echo =================================================================
echo [*] Preparation de l'installation de : !nom_modele!
echo [*] Cela peut prendre du temps en fonction de votre connexion...
echo =================================================================
echo.

ollama pull !nom_modele!

if %errorlevel% equ 0 (
    color 0A
    echo.
    echo =================================================================
    echo [SUCCES] Le modele !nom_modele! a ete installe avec succes !
    echo Vous pouvez maintenant l'utiliser dans votre terminal avec :
    echo -^> ollama run !nom_modele!
    echo =================================================================
) else (
    color 0C
    echo.
    echo =================================================================
    echo [ERREUR] Une erreur s'est produite lors du telechargement.
    echo =================================================================
)

echo.
pause
set nom_modele=
goto menu

:fin
color 07
cls
echo Merci d'avoir utilise le script !
timeout /t 2 >nul
exit /b
