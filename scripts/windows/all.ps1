param(
    [switch]$r
)

.\scripts\windows\removemigrations.ps1
.\scripts\windows\removedata.ps1
.\scripts\windows\makemigrations.ps1
.\scripts\windows\migrate.ps1
.\scripts\windows\collectstatic.ps1
if (!$r) {
  .\scripts\windows\runserver.ps1
}