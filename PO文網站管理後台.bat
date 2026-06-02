@echo off
title KC AI Education Blog Admin Dashboard Launcher
echo ===================================================
echo   KC AI Education Blog - Local Admin Dashboard
echo ===================================================
echo.
echo Preparing environment...
cd /d "%~dp0"

:: Disable TLS verification to prevent certificate errors
set NODE_TLS_REJECT_UNAUTHORIZED=0

echo Starting Astro dev server...
start /min "Astro Dev Server" cmd /c "npm run dev"

echo Waiting for server to start (3 seconds)...
ping -n 4 127.0.0.1 >nul

echo Opening browser to admin dashboard...
start http://localhost:4321/admin/

echo.
echo ---------------------------------------------------
echo Admin dashboard launched successfully!
echo You can now toggle FB checkboxes in the browser.
echo.
echo [NOTE] Keep this window open while using the dashboard.
echo When you are done, press any key here to shut down the server.
echo ---------------------------------------------------
echo.
pause

echo Shutting down background server...
taskkill /fi "windowtitle eq Astro Dev Server*" /f >nul 2>&1
echo Done! Thank you for using.
ping -n 3 127.0.0.1 >nul
