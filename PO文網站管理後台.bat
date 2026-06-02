@echo off
title  PO文網站管理後台啟動器
chcp 65001 >nul
echo ===================================================
echo        KC AI 教育手記 - 本地管理後台啟動器
echo ===================================================
echo.
echo 正在準備環境...
cd /d "C:\Users\ji3cp\OneDrive - Foxconn\01_Home\40_AI_folder\PO文網站"

:: 設定憑證安全繞過，避免本地與 API 通訊發生憑證錯誤
set NODE_TLS_REJECT_UNAUTHORIZED=0

:: 在背景最小化啟動 Astro 開發伺服器
echo 正在啟動 Astro 開發伺服器...
start /min "Astro Dev Server" cmd /c "npm run dev"

echo 正在等待伺服器啟動 (3秒)...
timeout /t 3 /nobreak >nul

echo 正在開啟瀏覽器進入管理後台介面...
start http://localhost:4321/admin/

echo.
echo ---------------------------------------------------
echo  後台已成功啟動！您可以在瀏覽器中點選 FB 標記並自動存檔。
echo.
echo [提醒] 結束使用後，請在此視窗按任意鍵，系統會自動關閉背景伺服器。
echo ---------------------------------------------------
echo.
pause

echo 正在關閉背景伺服器...
taskkill /fi "windowtitle eq Astro Dev Server*" /f >nul 2>&1
echo 關閉完成！感謝您的使用。
timeout /t 2 >nul
