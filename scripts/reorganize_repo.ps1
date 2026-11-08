$ErrorActionPreference = 'Stop'
$root = 'C:\laragon\www\app-ios-astonCamera'
$docs = Join-Path $root 'docs'
$phase1 = Join-Path $docs 'phases\phase1'
$phase2 = Join-Path $docs 'phases\phase2'
$phase3 = Join-Path $docs 'phases\phase3'
$phase4 = Join-Path $docs 'phases\phase4'

New-Item -ItemType Directory -Force -Path $docs, $phase1, $phase2, $phase3, $phase4 | Out-Null

$phaseMappings = @(
    @{ Pattern = 'phase1*'; Dest = $phase1 },
    @{ Pattern = 'phase2*'; Dest = $phase2 },
    @{ Pattern = 'phase3*'; Dest = $phase3 },
    @{ Pattern = 'phase4*'; Dest = $phase4 },
    @{ Pattern = 'PROJECT_HANDOFF.md'; Dest = $docs }
)

Get-ChildItem -Path $root -File | Where-Object { $_.Name -match '^(phase[0-9].*|PROJECT_HANDOFF\.md)$' } | ForEach-Object {
    $match = $phaseMappings | Where-Object { $_.Pattern -eq 'PROJECT_HANDOFF.md' -and $_.Name -eq 'PROJECT_HANDOFF.md' }
    foreach ($entry in $phaseMappings) {
        if ($_.Name -like $entry.Pattern) {
            $target = Join-Path $entry.Dest $_.Name
            if (Test-Path $target) { Remove-Item $target -Force }
            Move-Item -Path $_.FullName -Destination $entry.Dest -Force
            break
        }
    }
}

Write-Output 'Repository reorganization complete.'
