[![Build Status](https://circleci.com/gh/EncoreTechnologies/stackstorm-activedirectory.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/EncoreTechnologies/stackstorm-activedirectory) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


# Microsoft Active Directory Integration Pack

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

**Note** : `st2 pack config` doesn't handle nested schemas very well (known bug)
    so it's best to create the configuraiton file yourself and copy it into
    `/opt/stackstorm/configs/activedirectory.yaml` then run `st2ctl reload --register-configs`


### Schema
``` yaml
---
port: <default port number to use for WinRM connections: default = '5986'>
transport: <default transport to use for WinRM connections: default = 'ntlm'>

activedirectory:
  <credential-name-1>:
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
  <credential-name-2>:
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
    port: <port number override to use for WinRM connections: default = '5986'>
    transport: <transport override to use for WinRM connections: default = 'ntlm'>
  ...
```
    
### Example
``` yaml
---
port: 5986
transport: ntlm
  
activedirectory:
  dev:
    username: username@dev.domain.tld
    password: xxx
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
  prod:
    username: produser@domain.tld
    password: xxx
    port: 6611
    transport: kerberos
  prod-svc:
    username: prodsvc@domain.tld
    password: xxx
    port: 1234
    transport: basic
```
    
**Note** : All actions allow you to specify a set of credentials as inputs
           to the action instead of requiring a configuration

# Actions




## Examples
**TODO** Describe action


# Sensors

## Example Sensor
TODO: Describe sensor


# TODOs
- Tests (mock) for WinRM connection and cmdlets
- Complete this readme file with comprehensive documentation
- Workflow to install RSAT toos
- Include ps1 script to setup Windows machines

# Future Ideas
-  Create action to install Active Directory
   https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-#BKMK_PS
   Active Directory Deployment Services (ADDS) cmdlets: https://technet.microsoft.com/en-us/itpro/powershell/windows/addsdeployment/addsdeployment
   ``` PowerShell
   Import-Module ServerManager 
   Install-WindowsFeature -IncludeManagementTools -Name AD-Domain-Services
   Import-Module ADDSDeployment
   Get-Command -Module ADDSDeployment
   ???
   ```

