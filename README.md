# activedirectory Integration Pack

# Introduction
This pack provides an integration between StackStorm and Microsoft Active Directory.
It is designed to mimic the Active Directory Cmdlets for PowerShell:
Server 2012 Docs: https://technet.microsoft.com/en-us/library/ee617195.aspx
Server 2016 Docs: https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/activedirectory

## Prerequisites
This pack works by executing PowerShell commands on a remote Windows host that 
has the following things setup:

1. WinRM needs to be configured
   Execute the following script on all hosts that this pack will be running 
   commands on:
   https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1
   **TODO:** Distribute this script with our code
  
2. Install Remote Server Administration Tools (RSAT) tools for ActiveDirectory
   Install the "Active Directory Domain Services (AD DS) Tools and Active 
   Directory Lightweight Directory Services (AD LDS) Tools" component of
   RSAT tools on all hosts that this pack will be running commands on.
   **TODO:** Create action to install RSAT tools:
   ``` PowerShell
   Import-Module Servermanager
   Install-WindowsFeature -Name RSAT-AD-PowerShell
   ```

   


## Configuration
You will need to specificy Active Directory credentials that will be
using to connect to the remote Windows hosts in the 
`/opt/stackstorm/config/activedirectory.yaml` file. You can specificy multiple 
sets of credentials using nested values.


### Schema
---
activedirectory:
    port: <default port number to use for WinRM connections: default = '5986'>
    transport: <default transport to use for WinRM connections: default = 'ntlm'>
    <credentials1>:
        username: <username@domain.tld (preferred) or domain\username>
        password: <password for username>
    <credentials2>:
        username: <username@domain.tld (preferred) or domain\username>
        password: <password for username>
    ...
    

### Example
---
activedirectory:
  port: 5986
  transport: ntlm
  dev:
    username: username@dev.domain.tld
    password: xxx
  test:
      username: username@test.domain.tld
    password: xxx
  prod:
    username: produser@domain.tld
    password: xxx
  prod-svc:
    username: prodsvc@domain.tld
    password: xxx
    
    
**Note** : All actions allow you to specify a set of credentials as inputs
           to the action instead of requiring a configuration


# Actions




## example
TODO: Describe action



**TODO** 
Create action to install Active Directory? https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-#BKMK_PS
Active Directory Deployment Services (ADDS) cmdlets: https://technet.microsoft.com/en-us/itpro/powershell/windows/addsdeployment/addsdeployment
``` PowerShell
Import-Module ServerManager 
Install-WindowsFeature -IncludeManagementTools -Name AD-Domain-Services
Import-Module ADDSDeployment
Get-Command -Module ADDSDeployment
???
```


# Sensors

## Example Sensor
TODO: Describe sensor
