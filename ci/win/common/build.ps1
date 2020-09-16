 param (
    [string]$sourceFolder,
    [string]$script,
    [string]$destinationFolder = (Join-Path -ChildPath "\dist" -Path (Resolve-Path ".")) ,
    [string]$workFolder = (Join-Path -ChildPath "\build" -Path (Resolve-Path ".")) ,
    [string]$specFolder = (Resolve-Path ".")
 )
$ErrorActionPreference = "Stop"
pyinstaller `
    --noconfirm `
    --onefile `
	--nowindow `
    --clean `
    --workpath ($workFolder) `
    --distpath ($destinationFolder) `
    --specpath ($specFolder) `
    (Join-Path -ChildPath $script -Path $sourceFolder)

# copy config file
"Copying config files......"
cp (Join-Path -ChildPath "config" -Path $sourceFolder) $destinationFolder -Recurse -Force

# create batch files for the fast run
"Creating batch files......."
"game.exe 2&PAUSE" | Out-File -FilePath (Join-Path -ChildPath "run-game-for-2.bat" -Path $destinationFolder) -Encoding ascii
"game.exe 3&PAUSE" | Out-File -FilePath (Join-Path -ChildPath "run-game-for-3.bat" -Path $destinationFolder) -Encoding ascii
"game.exe 4&PAUSE" | Out-File -FilePath (Join-Path -ChildPath "run-game-for-4.bat" -Path $destinationFolder) -Encoding ascii

# Edit readme file
"Composing readme file for Windows......"
$patternRequirements = "## Requirements"
$patternUsage = "## Usage"
$skipBlock = $false
$patternRun = "$ python game.py <number of players>"
$readmeStrList = Get-Content -Path (Join-Path -ChildPath "README.md" -Path $sourceFolder)
$i = 0
$readmeOutput = New-Object System.Collections.Generic.List[string]
While ($i -le $readmeStrList.GetUpperBound(0)) {
    if ($readmeStrList[$i] -like $patternUsage) {
        $skipBlock = $false
    }
    if ($skipBlock -eq $false) {
        $_ = $readmeOutput.Add($readmeStrList[$i])
    }
    if ($readmeStrList[$i] -like $patternRequirements) {
        $skipBlock = $true
        $_ = $readmeOutput.Add("* Windows 10")
    }
    $i++
}
$readmeOutput[$readmeOutput.IndexOf($patternRun)] = "> game.exe <number of players>"
$readmeOutput | Out-File -FilePath (Join-Path -ChildPath "readme.md" -Path $destinationFolder) -Encoding unicode
"Compilation completed successfully"
