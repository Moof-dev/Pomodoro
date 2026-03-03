@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:menu
cls
echo ==========================================
echo    УПРАВЛЕНИЕ DOCKER-COMPOSE (POMODORO)
echo ==========================================
echo 1.1 Запустить (в фоновом режиме)
echo 1.2 Запустить тестовый DOCKER-COMPOSE
echo 2.1 Остановить все (stop)
echo 2.2 Остановить все TEST (stop)
echo 3. Удалить контейнеры и сети (down)
echo 4.1 Статус контейнеров (ps)
echo 4.2 Статус test контейнеров (ps)
echo 5. Просмотр логов (в реальном времени)
echo 6. Войти в терминал DB (Postgres)
echo 7. Войти в терминал CACHE (Redis)
echo 8. пересобрать и запустить
echo 0. Выход
echo ==========================================
set /p choice="Выберите опцию (0-8): "

if "%choice%"=="1.1" goto up
if "%choice%"=="1.2" goto up-test
if "%choice%"=="2.1" goto stop
if "%choice%"=="2.2" goto stop-test
if "%choice%"=="3" goto exit
if "%choice%"=="4.1" goto status
if "%choice%"=="4.2" goto status-test
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto shell_db
if "%choice%"=="7" goto shell_cache
if "%choice%"=="8" goto rebuild
if "%choice%"=="0" exit
goto menu

:up
echo Запуск сервисов...
docker-compose -p pomodoro up -d
pause
goto menu

:up-test
echo Запуск сервисов...
docker-compose -f docker-compose-test.yml -p pomodoro-test up -d
pause
goto menu

:stop
echo Остановка сервисов...
docker-compose -p pomodoro stop
pause
goto menu

:stop-test
echo Остановка сервисов...
docker-compose -p pomodoro-test stop
pause
goto menu

:down
echo Удаление контейнеров...
docker-compose down
pause
goto menu

:status
echo Текущее состояние:
docker-compose -p pomodoro ps
pause
goto menu

:status-test
echo Текущее состояние:
docker-compose -p pomodoro-test ps
pause
goto menu

:logs
echo Нажмите Ctrl+C для выхода из логов
docker-compose logs -f
goto menu

:shell_db
echo Вход в контейнер базы данных...
docker-compose exec db bash
goto menu

:shell_cache
echo Вход в контейнер Redis...
docker-compose exec cache redis-cli
goto menu

:rebuild
echo Пересборка и запуск...
docker-compose -p pomodoro up -d --build
pause
goto menu