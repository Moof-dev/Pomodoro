@echo off
set HOST=127.0.0.1
set PORT=8000

:: --- Командный роутер ---
IF "%1"=="dev" (
    set ENV_FILE=.dev.env
    goto start
) ELSE IF "%1"=="prod" (
    set ENV_FILE=.prod.env
    goto start
) ELSE IF "%1"=="local" (
    set ENV_FILE=.local.env
    goto start
) ELSE IF "%1"=="db" (
    goto sqlite
) ELSE IF "%1"=="uninstall" (
    goto uninstall
) ELSE IF "%1"=="install" (
    goto add
) ELSE IF "%1"=="migrate" (
    goto migrate
) ELSE IF "%1"=="migrate-apply" (
    goto migrate-apply
) ELSE IF "%1"=="migrate-history" (
    goto migrate-history
) ELSE IF "%1"=="migrate-rollback" (
    goto migrate-rollback
)ELSE IF "%1"=="worker" (
    goto worker
) ELSE IF "%1"=="worker-solo" (
    goto worker-solo
)ELSE IF "%1"=="flower" (
    goto flower
)ELSE (
    goto help
)

:start
if not exist %ENV_FILE% (
    echo Error: %ENV_FILE% not found!
    exit /b 1
)
echo Starting FastAPI in [%1] mode...
set ENVIRONMENT=%1
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --env-file .%1.env
pause
exit

:worker
poetry run celery -A worker.celery worker --loglevel=info -P eventlet -c 10
exit /b

:flower
poetry run celery -A worker.celery flower --address=127.0.0.1 --port=5555
exit /b

:worker-solo
poetry run celery -A worker.celery:celery worker --loglevel=info -P solo
exit /b


:migrate
set "M_ENV=.%2.env"
if "%2"=="" set "M_ENV=.local.env"
if not exist %M_ENV% (echo Error: %M_ENV% not found & exit /b 1)

set "MSG=%~3"
if "%MSG%"=="" set "MSG=auto_rev"

echo [ALEMBIC] Creating migration using %M_ENV%...
set "ENV_FILE=%M_ENV%"
poetry run alembic revision --autogenerate -m "%MSG%"
exit /b

:migrate-apply
set "M_ENV=.%2.env"
if "%2"=="" set "M_ENV=.local.env"
if not exist %M_ENV% (echo Error: %M_ENV% not found & exit /b 1)

echo [ALEMBIC] Upgrading database to HEAD using %M_ENV%...
set "ENV_FILE=%M_ENV%"
poetry run alembic upgrade head
exit /b

:migrate-history
set "M_ENV=.%2.env"
if "%2"=="" set "M_ENV=.local.env"
if not exist %M_ENV% (echo Error: %M_ENV% not found & exit /b 1)

echo [ALEMBIC] Showing migration history (-v for verbose)...
set "ENV_FILE=%M_ENV%"
:: Флаг -v выводит подробности, включая даты
poetry run alembic history -v
exit /b

:migrate-rollback
set "M_ENV=.%2.env"
if "%2"=="" set "M_ENV=.local.env"
if not exist %M_ENV% (echo Error: %M_ENV% not found & exit /b 1)

:: По умолчанию откатываемся на 1 шаг (-1)
set "STEP=%~3"
if "%STEP%"=="" set "STEP=-1"

echo [ALEMBIC] Rolling back database to %STEP% using %M_ENV%...
set "ENV_FILE=%M_ENV%"
poetry run alembic downgrade %STEP%
exit /b

:sqlite
:: ... (ваш существующий код без изменений) ...
set DB_MODE=%2
if "%DB_MODE%"=="" set DB_MODE=local
set SEARCH_ENV=.%DB_MODE%.env

if not exist %SEARCH_ENV% (
    echo Error: %SEARCH_ENV% not found!
    exit /b 1
)

echo Extracting database path from %SEARCH_ENV%...
for /f "tokens=2 delims==" %%a in ('findstr /i ".db" %SEARCH_ENV%') do set DB_PATH=%%a

if defined DB_PATH (
    set DB_PATH=%DB_PATH:"=%
    echo Opening SQLite3 shell [%DB_MODE%]: %DB_PATH%
    sqlite3 %DB_PATH%
) else (
    echo Error: Could not find .db path in %SEARCH_ENV% (Only for SQLite)
)
exit /b

:uninstall
:: ... (без изменений) ...
if "%2"=="" (
    echo Error: Specify library name. Example: %0 uninstall requests
) ELSE (
    echo Removing %2...
    poetry remove %2
)
exit /b

:add
:: ... (без изменений) ...
if "%2"=="" (
    echo Error: Specify library name.
    exit /b 1
)
set "IS_DEV=0"
if "%3"=="--dev" set "IS_DEV=1"
if "%3"=="-D" set "IS_DEV=1"

if "%IS_DEV%"=="1" (
    echo Adding library %2 to development group...
    poetry add %2 --group dev
) else (
    echo Adding library %2 to main dependencies...
    poetry add %2
)
exit /b

:help
echo ===============================================================================
echo Project Management Script Help
echo ===============================================================================
echo.
echo RUNNING THE APP:
echo   %0 local              - Start FastAPI with .local.env
echo   %0 dev                - Start FastAPI with .dev.env
echo   %0 prod               - Start FastAPI with .prod.env
echo.
echo DATABASE MIGRATIONS (ALEMBIC):
echo   %0 migrate [env] "msg"  - Create new migration (default env: local)
echo   %0 migrate-apply [env]  - Apply all migrations (to HEAD)
echo   %0 migrate-history [env]- View migration history
echo   %0 migrate-rollback [env] [step] - Rollback (default step: -1)
echo                             Example: %0 migrate-rollback dev -2
echo                             Example: %0 migrate-rollback local base (to initial)
echo.
echo DEPENDENCY MANAGEMENT (POETRY):
echo   %0 install [lib]        - Add production library
echo   %0 install [lib] -D     - Add development library
echo   %0 uninstall [lib]      - Remove library
echo.
echo UTILITIES:
echo   %0 db [env]             - Open SQLite3 shell
echo.
echo ===============================================================================
exit /b