from winrm_connection import WinRmConnection
from st2actions.runners.pythonrunner import Action

# Note:  in order for this to work you need to run the following script on the host
#  https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

CREDENTIALS_ITEMS = ['username', 'password']
TRANSPORT_ITEMS = ['port', 'transpaort']

class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)

    def resolve_creds(self, **kwargs):
        creds_config = self.create_creds_spec(kwargs['credential_name'],
                                              kwargs['username'],
                                              kwargs['password'],
                                              kwargs['cmdlet_credential_name'],
                                              kwargs['cmdlet_username'],
                                              kwargs['cmdlet_password'])
        creds = {}
        for key, value in creds_config.items():
            creds[key] = self.resolve_creds_spec(value)
        return creds
    
    
    def create_creds_spec(self, 
                          credential_name,
                          username,
                          password,
                          cmdlet_credential_name,
                          cmdlet_username,
                          cmdlet_password):
        return { 'connect' : { 'credential_name' : credential_name,
                               'username' : username,
                               'password' : password,
                               'required' : True },
                 'cmdlet' : {'credential_name' : cmdlet_credential_name,
                             'username' : cmdlet_username,
                             'password' : cmdlet_password,
                             'required' : False } }
    

    def resolve_creds_spec(self, creds_spec):
        creds = {}

        # if the user specified the "credential_name" parameter
        # then grab the credentials from the pack's config.yaml
        credential_name = creds_spec['credential_name']
        if credential_name:
            creds = self.config['activedirectory'].get(credential_name)

        # Override the items in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for item in CREDENTIALS_ITEMS:
            if item in creds_spec and creds_spec[item]:
                creds[item] = creds_spec[item]
                
            # ensure that creds has all items (if this credential is required)
            if creds_spec['required'] and item not in creds:
                if credential_name:
                    raise KeyError("config.yaml mising: activedirectory:%s:%s"
                                   % (credential_name, item))
                else:
                    raise KeyError("missing action parameter %s" % item)
                
        return creds

    def resolve_transport(self, transport, port):
        if not port:
            if 'port' in self.config:
                port = self.config['port']
            else:
                port = 5986
                
        if not transport:
            if 'transport' in self.config:
                transport = self.config['transport']
            else:
                transport = 'ntlm'
        return { 'transport' : transport, 'port' : port }
    
    
    def connect(self, hostname, transport, creds):
        self.connection = WinRmConnection(hostname=hostname,
                                          port=transport['port'],
                                          transport=transport['transport'],
                                          username=creds['username'],
                                          password=creds['password'])
        
    def run_ps(self, cmd):
        """Run the PowerShell command/script in :param cmd:
        :param cmd: PowerShell command/script to execute on the windows host
        :returns: Dict containing 'stdout', 'stderr', and 'exit_status'
        :rtype: dict
        """
        result = self.connection.run_ps(cmd)
        return { 'stdout': result.std_out,
                 'stderr': result.std_err,
                 'exit_status': result.status_code }

    def run_cmd(self, cmd):
        """Run the Command Prompt command in :param cmd:
        :param cmd: Command Prompt command to execute on the windows host
        :returns: Dict containing 'stdout', 'stderr', and 'exit_status'
        :rtype: dict
        """
        result = self.connection.run_cmd(cmd)
        return { 'stdout': result.std_out,
                 'stderr': result.std_err,
                 'exit_status': result.status_code }


    def run_ad_cmdlet(self, cmdlet, **kwargs):
        creds = self.resolve_creds(**kwargs)
        tport = self.resolve_transport(kwargs['transport'], kwargs['port'])
        powershell  = ''
        cmdlet_args = kwargs['args']
        if 'username' in creds['cmdlet'] and 'passowrd' in creds['cmdlet']:
            powershell = '''
                $securepass = ConvertTo-SecureString "{3}" -AsPlainText -Force;
                $admincreds = New-Object System.Management.Automation.PSCredential("{3}", $securepass);
                {0} -Credential $admincreds {1}
                '''.format(cmdlet,
                           cmdlet_args,
                           creds['cmdlet']['username'],
                           creds['cmdlet']['password'])
        else:
            powershell = '{0} {1}'.format(cmdlet, cmdlet_args)
            
        self.connect(kwargs['hostname'], tport, creds['connect'])
        result = self.run_ps(powershell)
        
        if result['exit_status'] == 0:
            return (True, result)
        else:
            return (False, result)
