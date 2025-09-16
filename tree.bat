@echo off
REM ==========================================
REM Proper ASCII tree with live progress
REM Excludes: .venv, __pycache__
REM Save as: tree.bat (put inside the target folder and run)
REM ==========================================

REM 1) Ensure we're in the script's directory
cd /d "%~dp0" || (
  echo [!] Can't access the script's folder: %~dp0
  pause
  exit /b 1
)

set "ROOT=%CD%"
set "OUT=%ROOT%\folder_tree.txt"
set "TMP=%TEMP%\folder_tree_%RANDOM%_%RANDOM%.tmp"

echo.
echo Generating folder and file tree for:
echo   %ROOT%
echo Output file (when done):
echo   %OUT%
echo.

REM 2) Header to TEMP file first (avoid self-lock/scan)
(
  echo Folder and file tree for: %ROOT%
  echo ========================================
  echo.
) > "%TMP%"

REM 3) Build the tree with PowerShell (stdout -> file, progress -> console)
echo Working... you should see "scanning:" lines as it progresses.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$r = [IO.Path]::GetFullPath('%ROOT%');" ^
  "$exclude = @('.venv','__pycache__');" ^
  "$sw = [Diagnostics.Stopwatch]::StartNew();" ^
  "[Console]::Error.WriteLine('> Building tree (excluding: ' + ($exclude -join ', ') + ')...');" ^
  "function Show-Tree([string]$p,[string]$prefix) {" ^
  "  $dirs  = Get-ChildItem -LiteralPath $p -Force -Directory | Where-Object { $exclude -notcontains $_.Name } | Sort-Object Name;" ^
  "  $files = Get-ChildItem -LiteralPath $p -Force -File      | Sort-Object Name;" ^
  "  $items = @() + $dirs + $files;" ^
  "  for ($i=0; $i -lt $items.Count; $i++) {" ^
  "    $it = $items[$i]; $isLast = ($i -eq $items.Count - 1);" ^
  "    $connector = if ($isLast) { '\-- ' } else { '+-- ' };" ^
  "    Write-Output ($prefix + $connector + $it.Name);" ^
  "    if ($it.PSIsContainer) {" ^
  "      $rel = $it.FullName.Substring($r.Length).TrimStart('\'); if ($rel -eq '') { $rel='.' }" ^
  "      [Console]::Error.WriteLine('  scanning: ' + $rel);" ^
  "      if ($isLast) { $tail = '    ' } else { $tail = '|   ' }" ^
  "      $newPrefix = $prefix + $tail;" ^
  "      Show-Tree -p $it.FullName -prefix $newPrefix;" ^
  "    }" ^
  "  }" ^
  "}" ^
  "Write-Output ('+-- ' + (Split-Path -Leaf $r));" ^
  "Show-Tree -p $r -prefix '';" ^
  "[Console]::Error.WriteLine(('> Done in {0:N1}s' -f $sw.Elapsed.TotalSeconds));" >> "%TMP%"

if errorlevel 1 (
  echo.
  echo [!] PowerShell reported an error. Partial output is at:
  echo     %TMP%
  pause
  exit /b 1
)

REM 4) Move finished file into the folder
move /Y "%TMP%" "%OUT%" >nul

echo.
echo Done! Saved to:
echo   %OUT%
echo.
pause
