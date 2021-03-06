#!/usr/bin/env powershell
param(
    [parameter(Mandatory=$true)]
    [string]$server,
    [parameter(Mandatory=$true)]
    [string]$template,
    [parameter(Mandatory=$true)]
    [string]$vmname,
    [parameter(Mandatory=$true)]
    [string]$user,
    [parameter(Mandatory=$true)]
    [string]$password,
    [string]$folder = "Unassigned"
    )
$paswd = ConvertTo-SecureString $password -AsPlainText -force
$credential = New-Object System.Management.Automation.PSCredential($user,$paswd)
#for hostname and loadvg
$hostname = New-Object System.Collections.Specialized.OrderedDictionary
#for the broken down cpu percentage and ram usage percentage
$hostinfo = @{}
Import-Module VMWare.VimAutomation.Core -ErrorAction "SilentlyContinue"
Import-Module PowerCLI.ViCore -ErrorAction "SilentlyContinue"
Connect-VIServer -Server $server -Credential $credential
$folders = Get-Folder -Type VM
$hosts = Get-VMHost
#make vmhost hash table correspond to open memeory and add open memeory to its own list
foreach($box in $hosts){
    $ramper = $box.MemoryUsageGB / $box.MemoryTotalGB
    $cpuper = $box.CpuUsageMhz / $box.CpuTotalMhz
    $loadavg = ($ramper + $cpuper) / 2
    #hostname = @{hostname = $loadavg}
    $hostname.Add($box.name,$loadavg)
    #hostinfo = {hostname = @{cpuper = .50; ramper = .40}; etc.}
    $hostinfo.Add($box.name,@{cpuper = $cpuper; ramper = $ramper})
}
$hostname = $hostname | Sort-Object -Property Value -Descending #sort hostname hash table by lowest load avg first
#loop through ram arraylist and try to deploy to hosts
foreach($vmhost in $hostname.Keys){
    if($hostinfo.$vmhost.cpuper -lt .80 -Or $hostinfo.$vmhost.ramper -lt .75){ 
        New-VM -VMHost $vmhost -Template $template -Name $vmname  | Out-Null
        if($folders.name -Contains $folder){
            Move-VM -VM $vmname -Destination $folder | Out-Null
        }
        #do until stopgap since it seems wait-task is broken in newest powercli 6.5
        do{
            Write-Host "Creating "$vmname"...."
             Start-Sleep -sec 5}
        until(Get-VMGuest -VM $vmname)
        #Out-Null so esxi host ip address is not picked up by regex
        #Start-VM spits out info about the machine it started
        Start-VM -VM $vmname | Out-Null
        do{
            Write-Host "Wating for "$vmname"s ip ...."
            Start-Sleep -sec 5
            $data = Get-VMGuest -VM $vmname
        }
        until($data.IPAddress -like "192.168.*")#ip address to wait for (or this or that etc.)
        Write-Host $vmname ip address is $data.IPAddress
        exit
    }

}