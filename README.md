[![Build Status](https://circleci.com/gh/EncoreTechnologies/stackstorm-activedirectory.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/EncoreTechnologies/stackstorm-activedirectory) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


# Microsoft Active Directory Integration Pack

# <a name="Introduction"></a> Introduction
This pack provides an integration between StackStorm and Microsoft Active Directory.
It is designed to mimic the Active Directory Cmdlets for PowerShell:

- [Server 2012 Docs](https://technet.microsoft.com/en-us/library/ee617195.aspx)
- [Server 2016 Docs](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/activedirectory)

This pack works by executing Active Driectory PowerShell commands on a remote
windows hosts.


# <a name="QuickStart"></a> Quick Start


**Steps**

1. Install the pack

    ``` shell
    st2 pack install activedirectory
    ```

2. Configure WinRM on a remote Windows host by running the [setup PowerShell
   script](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)

   ``` PowerShell
   Invoke-WebRequest https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 -OutFile "ConfigureRemotingForAnsible.ps1"
   .\ConfigureRemotingForAnsible.ps1
   ```

3. Install Remote Server Administration Tools (RSAT):

    ``` shell
    st2 run activedirectory.install_rsat_ad_powershell hostname='remotehost.domain.com' username='Administrator' password='xxx'
    ```

4. Execute an action (example: check if HOSTTOGET is a member of AD)

    ``` shell
    st2 run activedirectory.get_ad_computer hostname='remotehost.domain.com' username='Administrator' password='xxx' args='HOSTTOGET'
    ```



# <a name="Prerequisites"></a> Prerequisites
This pack works by executing PowerShell commands on a remote Windows host that
has the following setup:

1. WinRM needs to be configured
   Execute the following script on all hosts that this pack will be running
   commands on:
   https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

2. Install Remote Server Administration Tools (RSAT) tools for ActiveDirectory
   Install the "Active Directory Domain Services (AD DS) Tools and Active
   Directory Lightweight Directory Services (AD LDS) Tools" component of
   RSAT on all hosts that this pack will be running commands on.
   **Note** : This only works on Windows Server OSes.

## Manual Install
``` PowerShell
Import-Module Servermanager
Install-WindowsFeature -Name RSAT-AD-PowerShell
```

## Install using st2 action (from this pack)
``` shell
st2 run activedirectory.install_rsat_ad_powershell hostname='remotehost.domain.com' username='xxx' password='xxx'
```

# <a name="Installation"></a> Installation
Currently this pack is in incubation, so installation must be performed from the
github page.

``` shell
st2 pack install https://github.com/EncoreTechnologies/stackstorm-activedirectory
```

Once it is added to the exchange you can install it like so:

``` shell
st2 pack install activedirectory
```

# <a name="Configuration"></a> Configuration
You will need to specificy Active Directory credentials that will be
using to connect to the remote Windows hosts in the
`/opt/stackstorm/config/activedirectory.yaml` file. You can specificy multiple
sets of credentials using nested values.

**Note** : `st2 pack config` doesn't handle nested schemas very well (known bug)
    so it's best to create the configuraiton file yourself and copy it into
    `/opt/stackstorm/configs/activedirectory.yaml` then run `st2ctl reload --register-configs`


## <a name="Schema"></a> Schema

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

## <a name="SchemaExample"></a> Schema Example
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
           to the action instead of requiring a configuration. See the [Actions](#Actions)
           section for more information.

# <a name="Actions"></a> Actions

Actions in this pack are based off of the PowerShell cmdlets in ActiveDirectory module [link](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/activedirectory).

The actions from these cmdlets are auto-generated based on a the file `etc/cmdlets.txt`
using the generation script `etc/cmdlets_generate.py`

Below is a list of the currently implemented actions based on cmdlets.

| Action | PowerShell Cmdlet | Description |
|--------|-------------------|-------------|
| add_ad_computer_service_account | [Add-ADComputerServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/add-adcomputerserviceaccount)  | Adds one or more service accounts to an Active Directory computer. |
| add_ad_domain_controller_password_replication_policy | [Add-ADDomainControllerPasswordReplicationPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/add-addomaincontrollerpasswordreplicationpolicy)  | Adds users, computers, and groups to the Allowed List or the Denied List of the read-only domain controller (RODC) Password Replication Policy (PRP). |
| add_ad_fine_grained_password_policy_subject | [Add-ADFineGrainedPasswordPolicySubject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/add-adfinegrainedpasswordpolicysubject)  | Applies a fine-grained password policy to one more users and groups. |
| add_ad_group_member | [Add-ADGroupMember](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/add-adgroupmember)  | Adds one or more members to an Active Directory group. |
| add_ad_principal_group_membership | [Add-ADPrincipalGroupMembership](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/add-adprincipalgroupmembership)  | Adds a member to one or more Active Directory groups. |
| clear_ad_account_expiration | [Clear-ADAccountExpiration](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/clear-adaccountexpiration)  | Clears the expiration date for an Active Directory account. |
| disable_ad_account | [Disable-ADAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/disable-adaccount)  | Disables an Active Directory account. |
| disable_ad_optional_feature | [Disable-ADOptionalFeature](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/disable-adoptionalfeature)  | Disables an Active Directory optional feature. |
| enable_ad_account | [Enable-ADAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/enable-adaccount)  | Enables an Active Directory account. |
| enable_ad_optional_feature | [Enable-ADOptionalFeature](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/enable-adoptionalfeature)  | Enables an Active Directory optional feature. |
| get_ad_account_authorization_group | [Get-ADAccountAuthorizationGroup](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adaccountauthorizationgroup)  | Gets the Active Directory security groups that contain an account. |
| get_ad_account_resultant_password_replication_policy | [Get-ADAccountResultantPasswordReplicationPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adaccountresultantpasswordreplicationpolicy)  | Gets the resultant password replication policy for an Active Directory account. |
| get_ad_computer | [Get-ADComputer](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adcomputer)  | Gets one or more Active Directory computers. |
| get_ad_computer_service_account | [Get-ADComputerServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adcomputerserviceaccount)  | Gets the service accounts that are hosted by an Active Directory computer. |
| get_ad_default_domain_password_policy | [Get-ADDefaultDomainPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-addefaultdomainpasswordpolicy)  | Gets the default password policy for an Active Directory domain. |
| get_ad_domain | [Get-ADDomain](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-addomain)  | Gets an Active Directory domain. |
| get_ad_domain_controller | [Get-ADDomainController](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-addomaincontroller)  | Gets one or more Active Directory domain controllers, based on discoverable services criteria, search parameters, or by providing a domain controller identifier, such as the NetBIOS name. |
| get_ad_domain_controller_password_replication_policy | [Get-ADDomainControllerPasswordReplicationPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-addomaincontrollerpasswordreplicationpolicy)  | Gets the members of the Allowed List or the Denied List of the RODC PRP. |
| get_ad_domain_controller_password_replication_policy_usage | [Get-ADDomainControllerPasswordReplicationPolicyUsage](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-addomaincontrollerpasswordreplicationpolicyusage)  | Gets the resultant password policy of the specified ADAccount on the specified RODC. |
| get_ad_fine_grained_password_policy | [Get-ADFineGrainedPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adfinegrainedpasswordpolicy)  | Gets one or more Active Directory fine-grained password policies. |
| get_ad_fine_grained_password_policy_subject | [Get-ADFineGrainedPasswordPolicySubject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adfinegrainedpasswordpolicysubject)  | Gets the users and groups to which a fine-grained password policy is applied. |
| get_ad_forest | [Get-ADForest](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adforest)  | Gets an Active Directory forest. |
| get_ad_group | [Get-ADGroup](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adgroup)  | Gets one or more Active Directory groups. |
| get_ad_group_member | [Get-ADGroupMember](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adgroupmember)  | Gets the members of an Active Directory group. |
| get_ad_object | [Get-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adobject)  | Gets one or more Active Directory objects. |
| get_ad_optional_feature | [Get-ADOptionalFeature](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adoptionalfeature)  | Gets one or more Active Directory optional features. |
| get_ad_organizational_unit | [Get-ADOrganizationalUnit](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adorganizationalunit)  | Gets one or more Active Directory OUs. |
| get_ad_principal_group_membership | [Get-ADPrincipalGroupMembership](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adprincipalgroupmembership)  | Gets the Active Directory groups that have a specified user, computer, or group. |
| get_ad_root_dse | [Get-ADRootDSE](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adrootdse)  | Gets the root of a domain controller information tree. |
| get_ad_service_account | [Get-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-adserviceaccount)  | Gets one or more Active Directory service accounts. |
| get_ad_user | [Get-ADUser](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-aduser)  | Gets one or more Active Directory users. |
| get_ad_user_resultant_password_policy | [Get-ADUserResultantPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/get-aduserresultantpasswordpolicy)  | Gets the resultant password policy for a user. |
| install_ad_service_account | [Install-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/install-adserviceaccount)  | Installs an Active Directory service account on a computer. |
| move_ad_directory_server | [Move-ADDirectoryServer](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/move-addirectoryserver)  | Moves a domain controller in AD DS to a new site. |
| move_ad_directory_server_operation_master_role | [Move-ADDirectoryServerOperationMasterRole](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/move-addirectoryserveroperationmasterrole)  | Moves operation master (also known as flexible single master operations or FSMO) roles to an Active Directory domain controller. |
| move_ad_object | [Move-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/move-adobject)  | Moves an Active Directory object or a container of objects to a different container or domain. |
| new_ad_computer | [New-ADComputer](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adcomputer)  | Creates a new Active Directory computer. |
| new_ad_fine_grained_password_policy | [New-ADFineGrainedPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adfinegrainedpasswordpolicy)  | Creates a new Active Directory fine-grained password policy. |
| new_ad_group | [New-ADGroup](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adgroup)  | Creates an Active Directory group. |
| new_ad_object | [New-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adobject)  | Creates an Active Directory object. |
| new_ad_organizational_unit | [New-ADOrganizationalUnit](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adorganizationalunit)  | Creates a new Active Directory OU. |
| new_ad_service_account | [New-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-adserviceaccount)  | Creates a new Active Directory service account. |
| new_ad_user | [New-ADUser](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/new-aduser)  | Creates a new Active Directory user. |
| remove_ad_computer | [Remove-ADComputer](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adcomputer)  | Removes an Active Directory computer. |
| remove_ad_computer_service_account | [Remove-ADComputerServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adcomputerserviceaccount)  | Removes one or more service accounts from a computer. |
| remove_ad_domain_controller_password_replication_policy | [Remove-ADDomainControllerPasswordReplicationPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-addomaincontrollerpasswordreplicationpolicy)  | Removes users, computers, and groups from the Allowed List or the Denied List of the RODC PRP. |
| remove_ad_fine_grained_password_policy | [Remove-ADFineGrainedPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adfinegrainedpasswordpolicy)  | Removes an Active Directory fine-grained password policy. |
| remove_ad_fine_grained_password_policy_subject | [Remove-ADFineGrainedPasswordPolicySubject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adfinegrainedpasswordpolicysubject)  | Removes one or more users from a fine-grained password policy. |
| remove_ad_group | [Remove-ADGroup](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adgroup)  | Removes an Active Directory group. |
| remove_ad_group_member | [Remove-ADGroupMember](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adgroupmember)  | Removes one or more members from an Active Directory group. |
| remove_ad_object | [Remove-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adobject)  | Removes an Active Directory object. |
| remove_ad_organizational_unit | [Remove-ADOrganizationalUnit](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adorganizationalunit)  | Removes an Active Directory OU. |
| remove_ad_principal_group_membership | [Remove-ADPrincipalGroupMembership](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adprincipalgroupmembership)  | Removes a member from one or more Active Directory groups. |
| remove_ad_service_account | [Remove-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-adserviceaccount)  | Removes an Active Directory service account. |
| remove_ad_user | [Remove-ADUser](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/remove-aduser)  | Removes an Active Directory user. |
| rename_ad_object | [Rename-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/rename-adobject)  | Changes the name of an Active Directory object. |
| reset_ad_service_account_password | [Reset-ADServiceAccountPassword](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/reset-adserviceaccountpassword)  | Resets the service account password for a computer. |
| restore_ad_object | [Restore-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/restore-adobject)  | Restores an Active Directory object. |
| search_ad_account | [Search-ADAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/search-adaccount)  | Gets Active Directory user, computer, and service accounts. |
| set_ad_account_control | [Set-ADAccountControl](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adaccountcontrol)  | Modifies user account control (UAC) values for an Active Directory account. |
| set_ad_account_expiration | [Set-ADAccountExpiration](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adaccountexpiration)  | Sets the expiration date for an Active Directory account. |
| set_ad_account_password | [Set-ADAccountPassword](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adaccountpassword)  | Modifies the password of an Active Directory account. |
| set_ad_computer | [Set-ADComputer](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adcomputer)  | Modifies an Active Directory computer. |
| set_ad_default_domain_password_policy | [Set-ADDefaultDomainPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-addefaultdomainpasswordpolicy)  | Modifies the default password policy for an Active Directory domain. |
| set_ad_domain | [Set-ADDomain](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-addomain)  | Modifies an Active Directory domain. |
| set_ad_domain_mode | [Set-ADDomainMode](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-addomainmode)  | Sets the domain functional level for an Active Directory domain. |
| set_ad_fine_grained_password_policy | [Set-ADFineGrainedPasswordPolicy](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adfinegrainedpasswordpolicy)  | Modifies an Active Directory fine-grained password policy. |
| set_ad_forest | [Set-ADForest](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adforest)  | Modifies an Active Directory forest. |
| set_ad_forest_mode | [Set-ADForestMode](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adforestmode)  | Sets the forest mode for an Active Directory forest. |
| set_ad_group | [Set-ADGroup](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adgroup)  | Modifies an Active Directory group. |
| set_ad_object | [Set-ADObject](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adobject)  | Modifies an Active Directory object. |
| set_ad_organizational_unit | [Set-ADOrganizationalUnit](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adorganizationalunit)  | Modifies an Active Directory OU. |
| set_ad_service_account | [Set-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-adserviceaccount)  | Modifies an Active Directory service account. |
| set_ad_user | [Set-ADUser](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/set-aduser)  | Modifies an Active Directory user. |
| uninstall_ad_service_account | [Uninstall-ADServiceAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/uninstall-adserviceaccount)  | Uninstalls an Active Directory service account from a computer. |
| unlock_ad_account | [Unlock-ADAccount](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/unlock-adaccount)  | Unlocks an Active Directory account. |
| install_rsat_ad_powershell | [Install-WindowsFeature -Name RSAT-AD-PowerShell](https://technet.microsoft.com/en-us/itpro/powershell/windows/servermanager/install-windowsfeature)  | Installs RSAT Tools Active Directory PowerShell module. |


## <a name="Usage"></a> Usage

### <a name="BasicUsage"></a> Basic Usage

The actions that are created are fairly simplistic, simply executing the PowerShell
cmdlet that they represent along with any arguments that are passed in via the `args`
parameter on the action.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld'
st2 run activedirectory.new_ad_computer args='NEWCOMPUTER' hostname='windowshost.domain.tld'
```

Every cmdlet action has a required `hostname` parameter that is the hostname of
the remote windows box that we will execute the cmdlet on. Please ensure that
hosts have the [Prerequisites](#Prerequisites) installed properly (WinRM and RSAT tools)

### <a name="Authentication"></a> Authentication

When logging in to a system and invoking commands you will need to authenticate
to login to the host, and maybe need to pass in a different set of credentials
to the cmdlet. When logging in to the remote system there are two ways to pass
in authentication credentials to the action.

#### Options:
- username/password parameters passed directly to the action
- credential_name parameter passed to the action

#### username/password parameters
In this case the username/password are specified where the action is invoked,
thus allowing you to pass in credentials on the commandline for easy testing.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld' username='user@domain.com' password='Password1'
```

#### credential_name parameter
In this case the name of the credential to used is passed in where the action
is invoked, and the actual credentials themselves are stored in the pack's
configuration file `/opt/stackstorm/configs/activedirectory.yaml`.

Let's say we had a configuration file with the contents:

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
```

We could invoke an action using the `dev` credentials to login to `hostname` like so:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev'
```

Similarly if we wanted to invoke the same action using the `test` credentials:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='testhost.domain.tld' credential_name='test'
```

### <a name="CmdletAuthentication"></a> Cmdlet Authentication

When executing a PowerShell cmdlet the it normally uses the credentials of
the currently logged in user. In our case this would either be `username/password`
or the username/password associated with the `credential_name` in the config.
Alternativey, the cmdlets in the ActiveDirectory PowerShell module can take an
optional `-Credential` parameter that is used to provide different credentials
for the executin of the command itself (example, maybe a specific command requires
an elevated set of priveleges). The PowerShell for a normal command looks like:

``` PowerShell
Get-ADUser someuser
```

To execute this with a different set of credentials it would look like:

``` PowerShell
$securepass = ConvertTo-SecureString "Password!" -AsPlainText -Force
$admincreds = New-Object System.Management.Automation.PSCredential("username@domain.com", $securepass)
Get-ADUser -Credential $admincreds someuser
```

Because it is a fairly common scenario this use-case has been baked into the actions
within this pack. To execute a command with an elevated set of credentials there
are two options, just like host authentication.

#### Options:
- cmdlet_username/cmdlet_password parameters passed directly to the action
- cmdlet_credential_name parameter passed to the action


#### cmdlet_username/cmdlet_password parameters
In this case the cmdlet_username/cmdlet_password are specified where the action
is invoked, thus allowing you to pass in credentials on the commandline for easy
testing.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld' username='user@domain.com' password='Password1' cmdlet_username='elevated@domain.com' cmdlet_password='SuperSecurePassword'
```

#### cmdlet_credential_name parameter
In this case the name of the credential to used is passed in where the action
is invoked, and the actual credentials themselves are stored in the pack's
configuration file `/opt/stackstorm/configs/activedirectory.yaml`.

Let's say we had a configuration file with the contents:

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
  elevated:
    username: username@test.domain.tld
    password: xxx
    port: 5522
```

We could invoke an action using the `dev` credentials to login to `hostname` and
then using the `elevated` set of credentials for the cmdlet execution like so:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev' cmdlet_credential_name='elevated'
```

### <a name="TransportPort"></a> Transport/Port

We provide the ability to specialize _how_ we connect to a host using WinRM by
allowing the `transport` and `port` to be overridden. The `transport` is the connection
protocol used to perform WinRM authentication. The `port` is the network port to
use to make the connection to the remote host.

The default, and recommended `transport` and `port` is: `transport='ntlm' port='5986'`

This pack supports all transports that are supported by the [pywinrm](https://github.com/diyan/pywinrm/)
python module. As of the time of writing the valid transports are:

- `basic`
- `plaintext`
- `certificate`
- `ssl`
- `kerberos`
- `ntlm`
- `credssp`

For more info on how to use and setup your Windows host for these various transports
please refer to the [pywinrm](https://github.com/diyan/pywinrm/) documentation.


#### Transport/Port Overrides

We provide the following options for specifying what `transport` and `port` to use
for the connection (ordered in terms of highest priority):

1. if transport/port specified as action params, use this
2. if transport/port specified as params on the credentials in config
3. if transport/port specified at root level in the config
4. else, use the default transport/port (5986/ntlm)


#### Transport/Port as Action Params

The most specific case is passing in the `transport`/`port` as parameters to
the action when you invoke it:

``` shell
# will use transport='basic' and port='1234' from the invokation
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev' port='1234' transport='basic'
```

#### Transport/Port as From Credentials in Config

Alternatively, if you pass in a `credential_name` to the action invokation
and that credential has the `transport` and `port` options set in the config, then
we'll automatically look up and utilize those values.

Example config:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
    transport: basic
```

``` shell
# will use transport='basic' and port=5522 from the 'test' credential in the config
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


#### Transport/Port as From Config Root

If the credential doesn't have `transport`/`port` defined then we'll use the "global"
settings for `transport` and `port` at the root level of the config

Example config:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
```

``` shell
# will use transport='ntlm' and port=5986 from the root of the config
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


#### Transport/Port default

Finally if there are no `transport`/`port` specified as params, or in the config
we'll use our packs built-in default of `transport='ntlm' port='5986'`.

Example config:

``` yaml
---
activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
```

``` shell
# will use transport='ntlm' and port=5986 from the pack's built-in defaults
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


## <a name="Output"></a> Output

In an effort to be flexible and play well with StackStorm we have coded up this
pack to allow for the output of the actions to be in one of the following formats:

- json (default)
- raw

### <a name="JSON"></a> JSON

JSON output works by appending `| ConvertTo-Json` to the end of the powershell
cmdlet being run and converts any exceptions that are thrown into JSON. The
exact code that gets executed is:

``` PowerShell
Try
{
  <cmdlet> | ConvertTo-Json
}
Catch
{
  $formatted_output = ConvertTo-Json -InputObject $_
  $host.ui.WriteErrorLine($formatted_output)
  exit 1
}
```

This takes the resulting PowerShell object and converts it to
JSON representation. The benefit of this is that by using JSON it allows us
to parse it into a python `dict` and then return it from the action. This allows
the end-user to utilize the output in a meaningful way within workflows. To utilize
this dictionary parsed output there are two variables `stdout_dict` and `stderr_dict`
that are populated. If no output is present an empty dictionary is returned.

**Example Mistral workflow usage:**

``` yaml
version: '2.0'

activedirectory.json-example:
    description: Workflow demoing the json parsed output
    type: direct
    input:
        - hostname
        - username
        - password
        - computer
    output:
        dns_hostname: <% $.dns_hostname %>
    tasks:
        task1:
            action: activedirectory.get_ad_computer hostname=<% $.hostname %> args="<% $.computer %>" username=<% $.username %> password=<% $.password %> cmdlet_username=<% $.username %> cmdlet_password=<% $.password %>
            publish:
                dns_hostname: <% task(task1).result.result.stdout_dict.DNSHostName %>
                stderr_dict: <% task(task1).result.result.stderr_dict %>
```

### <a name="Raw"></a> Raw

Raw output is simply the stdout/stderr strings returned to you. In this case
the output variables `stdout` and `stderr` would be your interaction point.
The variables `stdout_dict` and `stderr_dict` will be set to empty dictionaries.



# <a name="FutureIdeas"></a> Future Ideas
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
- Create sensors that monitor events in AD
  - Users added/removed
  - Computers added/removed
  - Groups added/removed
  - Users added/removed from groups
