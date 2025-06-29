@echo off
echo 🚀 LUCIQ GITHUB PUSH FIX
echo =========================
echo.

echo 🔍 Checking current branch...
git branch

echo.
echo 🔄 Switching to main branch (GitHub default)...
git branch -M main

echo.
echo 📡 Checking remote connection...
git remote -v

echo.
echo ☁️ Pushing to GitHub...
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ✅ SUCCESS! Your Palantir-competing platform is backed up!
    echo 🎉 Repository: https://github.com/virrpe/luciq-platform
) else (
    echo ❌ Push failed. Common fixes:
    echo.
    echo 1. Make sure repository exists on GitHub
    echo 2. Check your GitHub credentials
    echo 3. Try: git pull origin main --allow-unrelated-histories
    echo 4. Then: git push -u origin main
)

echo.
pause 