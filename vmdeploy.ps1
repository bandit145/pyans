#!/usr/bin/env powershell
param(
    [parameter(Mandatory=$true)]
    [string]$server,
    [parameter(Mandatory=$true)]
    [string]$template,
    [parameter(Mandatory=$true)]
    [string]$vmname

    )
$ram = New-Object System.Collections.ArrayList 
$vmhost = @{}
Import-Module VMWare.VimAutomation.Core
$credential = Get-Credential
Connect-VIServer -Server $server -Credential $credential
$hosts = Get-VMHost

foreach($box in $hosts){
    $sub = $box.MemoryTotalGB - $box.MemoryUsageGB
    $vmhost.Add($sub, $box.Name)
    $ram.Add($sub)
}
$ram = $ram | Sort-Object -Descending

foreach($num in $ram){
    try{
        New-VM -VMHost $vmhost.$num -Template $template -Name $vmname | Wait-Task
        Start-VM -VM $vmname
        Start-Sleep -s 20
        $data = Get-VMGuest -VM $vmname
        Write-Host $vmname ip address is $data.IPAddress
        exit

    }
    catch [VMware.VimAutomation.ViCore.Types.V1.ErrorHandling.NoDiskSpace]{
        continue
    }

}
