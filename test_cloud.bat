@echo off
echo Testing Cloud Monitor Script...
echo.

echo Setting test environment variables...
set TELEGRAM_BOT_TOKEN=test_token
set TELEGRAM_CHAT_ID=test_chat_id

echo.
echo Running single check (without Telegram)...
python monitor_cloud.py

pause