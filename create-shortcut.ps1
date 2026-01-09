# PowerShell script to create desktop shortcut for CEO Personal OS

$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "CEO Personal OS.lnk"
$targetPath = Join-Path $PSScriptRoot "start.bat"
$workingDirectory = $PSScriptRoot

Write-Host "Creating desktop shortcut..."
Write-Host "Target: $targetPath"
Write-Host "Working Directory: $workingDirectory"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = $workingDirectory
$shortcut.Description = "CEO Personal Operating System"
$shortcut.Save()

Write-Host "Shortcut created successfully at: $shortcutPath"
Write-Host "You can now double-click 'CEO Personal OS' on your desktop to launch the app."
