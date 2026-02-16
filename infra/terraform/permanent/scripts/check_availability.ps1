[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string]$Suffix,

    [Parameter(Mandatory = $true)]
    [string]$Env,

    [Parameter(Mandatory = $true)]
    [string]$Location
)

$ErrorActionPreference = "Stop"

Write-Host "[INFO] checking availability for suffix: $Suffix in $Location..."

# Define Resource Names
$keyVaultName = "kv-rag-$Env-$Suffix"
$acrName = "acrrag$Env$Suffix"
$storageName = "strag$Env$Suffix"
$postgresName = "psql-rag-$Env-$Suffix"

$jobs = @()

# 1. Key Vault
$jobs += Start-Job -ScriptBlock {
    param($n)
    try {
        $result = az keyvault check-name --name $n | ConvertFrom-Json
        if (-not $result.nameAvailable) {
            return "[FAIL] KeyVault '$n' is NOT available: $($result.message)"
        }
        return "[PASS] KeyVault '$n' is available."
    }
    catch {
        return "[WARN] Failed to check KeyVault '$n': $_"
    }
} -ArgumentList $keyVaultName

# 2. ACR
$jobs += Start-Job -ScriptBlock {
    param($n)
    try {
        $result = az acr check-name --name $n | ConvertFrom-Json
        if (-not $result.nameAvailable) {
            return "[FAIL] ACR '$n' is NOT available: $($result.message)"
        }
        return "[PASS] ACR '$n' is available."
    }
    catch {
        return "[WARN] Failed to check ACR '$n': $_"
    }
} -ArgumentList $acrName

# 3. Storage Account
$jobs += Start-Job -ScriptBlock {
    param($n)
    try {
        $result = az storage account check-name --name $n | ConvertFrom-Json
        if (-not $result.nameAvailable) {
            return "[FAIL] Storage '$n' is NOT available: $($result.message)"
        }
        return "[PASS] Storage '$n' is available."
    }
    catch {
        return "[WARN] Failed to check Storage '$n': $_"
    }
} -ArgumentList $storageName

# 4. Postgres Flexible Server
$jobs += Start-Job -ScriptBlock {
    param($n, $loc)
    try {
        $result = az postgres flexible-server check-name-availability --name $n --location $loc 2>&1
        if ($LASTEXITCODE -eq 0) {
            $json = $result | ConvertFrom-Json
            if (-not $json.nameAvailable) {
                return "[FAIL] Postgres '$n' is NOT available: $($json.message)"
            }
            return "[PASS] Postgres '$n' is available."
        }
        else {
            return "[WARN] Postgres check failed execution."
        }
    }
    catch {
        return "[WARN] Failed to check Postgres '$n': $_"
    }
} -ArgumentList $postgresName, $Location

# Wait for all checks
$results = $jobs | Receive-Job -Wait -AutoRemoveJob

# Process Results
$failed = $false
foreach ($res in $results) {
    Write-Host $res
    if ($res -like "[FAIL]*") {
        $failed = $true
    }
}

if ($failed) {
    Write-Error "[STOP] Pre-flight checks FAILED. Some names are already taken globally or conflict with soft-deleted resources."
    exit 1
}

Write-Host "[DONE] All names are available! Proceeding with Terraform..."
exit 0
