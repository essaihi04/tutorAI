@echo off
echo ============================================
echo Configuration de la base de donnees locale
echo ============================================
echo.

echo Etape 1: Demarrage de PostgreSQL et Redis avec Docker...
cd /d C:\Users\HP\Desktop\ai-tutor-bac
docker-compose up -d db redis

echo.
echo Etape 2: Attente du demarrage de PostgreSQL (10 secondes)...
timeout /t 10 /nobreak

echo.
echo Etape 3: Verification de l'etat des conteneurs...
docker-compose ps

echo.
echo ============================================
echo Configuration terminee!
echo ============================================
echo.
echo Prochaines etapes:
echo 1. Modifiez backend\.env pour utiliser localhost
echo 2. Executez: cd backend
echo 3. Executez: alembic upgrade head
echo 4. Demarrez le backend: python -m uvicorn app.main:app --reload
echo.
pause
