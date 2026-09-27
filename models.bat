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
echo =================================================================
echo    ____  _      _       _      __  __      _   __  __           
echo   / __ \^| ^|    ^| ^|     / \    ^|  \/  ^|    / \  \ \/ /           
echo  ^| ^|  ^| ^| ^|    ^| ^|    / _ \   ^| ^|\/^| ^|   / _ \  \  /            
echo  ^| ^|__^| ^| ^|____^| ^|___/ ___ \  ^| ^|  ^| ^|  / ___ \ /  \            
echo   \____/^|______^|____/_/   \_\ ^|_^|  ^|_^| /_/   \_\_/\_\           
echo.
echo                 OLLAMA MODEL INSTALLER PACK                     
echo =================================================================
echo.
echo Choisissez le modele a installer (telechargement local) :
echo.
echo  [1] Llama 3 (8B)      - Excellent pour usage general (Meta)
echo  [2] Mistral (7B)      - Performant et tres utilise (Mistral AI)
echo  [3] Gemma 2 (9B)      - Modele open-source puissant (Google)
echo  [4] Phi 3 (3.8B)      - Rapide, leger, ideal pour petits PCs (Microsoft)
echo  [5] Qwen 2 (7B)       - Tres bon en logique et programmation (Alibaba)
echo  [6] LLaVA (7B)        - Modele de vision (comprend et decrit les images)
echo  [7] DeepSeek Coder    - Specialise dans le code et le developpement
echo  [8] Saisir un nom de modele manuel (ex: mixtral, codellama, etc.)
echo.
echo  [0] Quitter
echo =================================================================
echo.

set /p choix="> Entrez votre choix (0-8) : "

if "%choix%"=="1" set nom_modele=llama3
if "%choix%"=="2" set nom_modele=mistral
if "%choix%"=="3" set nom_modele=gemma2
if "%choix%"=="4" set nom_modele=phi3
if "%choix%"=="5" set nom_modele=qwen2
if "%choix%"=="6" set nom_modele=llava
if "%choix%"=="7" set nom_modele=deepseek-coder
if "%choix%"=="8" goto custom_model
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

:: La commande pull télécharge le modèle localement
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
    echo Veuillez verifier votre connexion internet ou le nom du modele.
    echo =================================================================
)

echo.
pause
set nom_modele=
goto menu

:fin
color 07
cls
echo Merci d'avoir utilise le script d'installation de modeles Ollama !
timeout /t 2 >nul
exit /b
