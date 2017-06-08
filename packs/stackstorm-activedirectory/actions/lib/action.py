from winrm_connection import WinRmConnection
from st2actions.runners.pythonrunner import Action

# Note:  in order for this to work you need to run the following script on the
# host
#  https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

CREDENTIALS_ITEMS = ['username', 'password']
TRANSPORT_ITEMS = ['port', 'transport']


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.connection = None

    def resolve_creds(self, **kwargs):
        creds_config = self.create_creds_spec(**kwargs)
        creds = {}
        for key, value in creds_config.items():
            creds[key] = self.resolve_creds_spec(value)
        return creds

    def get_arg(self, key, **kwargs):
        if key in kwargs:
            return kwargs[key]
        else:
            return None

    def create_creds_spec(self, **kwargs):
        return {'connect': {'credential_name': self.get_arg('credential_name', **kwargs),
                            'username': self.get_arg('username', **kwargs),
                            'password': self.get_arg('password', **kwargs),
                            'required': True},
                'cmdlet': {'credential_name': self.get_arg('cmdlet_credential_name', **kwargs),
                           'username': self.get_arg('cmdlet_username', **kwargs),
                           'password': self.get_arg('cmdlet_password', **kwargs),
                           'required': False}}

    def resolve_creds_spec(self, creds_spec):
        creds = {}

        # if the user specified the "credential_name" parameter
        # then grab the credentials from the pack's config.yaml
        credential_name = creds_spec['credential_name']
        config_creds = None
        if credential_name:
            config_creds = self.config['activedirectory'].get(credential_name)
            if not config_creds:
                raise KeyError("config.yaml missing credential: activedirectory:%s"
                               % credential_name)

        creds['credential_name'] = credential_name

        # Override the items in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for item in CREDENTIALS_ITEMS:
            if item in creds_spec and creds_spec[item]:
                # use creds from cmdline first (override)
                creds[item] = creds_spec[item]
            elif config_creds and item in config_creds and config_creds[item]:
                # fallback to creds in config
                creds[item] = config_creds[item]

            # ensure that creds has all items (if this credential is required)
            if ('required' in creds_spec and creds_spec['required'] and item not in creds):
                if credential_name:
                    raise KeyError("config.yaml mising: activedirectory:%s:%s"
                                   % (credential_name, item))
                else:
                    raise KeyError("missing action parameter %s" % item)

        # copy in all transport items into the credentials spec
        for item in TRANSPORT_ITEMS:
            if config_creds and item in config_creds and config_creds[item]:
                creds[item] = config_creds[item]

        return creds

    @staticmethod
    def default_transport():
        return 'ntlm'

    @staticmethod
    def default_port():
        return 5986

    def resolve_transport(self, connect_creds, **kwargs):
        """ Resolves the transport and port to use for the connection
        based on the following priorities:
        1) if port/transport specified as action params, use this
        2) if port/transport specified as params on the credentials in config
        3) if port/transport specified at root level in the config
        4) else, use the default port/transport (5986/ntlm)
        :param connect_creds: the connection credentials read in from the
        config.
        :returns: dictionary with 'transport' and 'port' set the resolved
        values
        :rtype: dictionary
        """
        resolved_transport = None
        resolved_port = None

        if 'port' in kwargs:
            resolved_port = kwargs['port']
        elif 'port' in connect_creds:
            resolved_port = connect_creds['port']
        elif 'port' in self.config:
            resolved_port = self.config['port']
        else:
            resolved_port = BaseAction.default_port()

        if 'transport' in kwargs:
            resolved_transport = kwargs['transport']
        elif 'transport' in connect_creds:
            resolved_transport = connect_creds['transport']
        elif 'transport' in self.config:
            resolved_transport = self.config['transport']
        else:
            resolved_transport = BaseAction.default_transport()

        return {'transport': resolved_transport, 'port': resolved_port}

    def connect(self, hostname, transport, creds):
        if not self.connection:
            self.connection = WinRmConnection(hostname=hostname,
                                              port=transport['port'],
                                              transport=transport['transport'],
                                              username=creds['username'],
                                              password=creds['password'])

    def run_ad_cmdlet(self, cmdlet, **kwargs):
        creds = self.resolve_creds(**kwargs)
        tport = self.resolve_transport(creds['connect'], **kwargs)
        powershell = ''
        cmdlet_args = kwargs['args'] if 'args' in kwargs else ''
        if 'username' in creds['cmdlet'] and 'password' in creds['cmdlet']:
            powershell = ("$securepass = ConvertTo-SecureString \"{3}\" -AsPlainText -Force;\n"
                          "$admincreds = New-Object System.Management.Automation.PSCredential(\"{2}\", $securepass);\n"  # noqa
                          "{0} -Credential $admincreds {1}"
                          "").format(cmdlet,
                                     cmdlet_args,
                                     creds['cmdlet']['username'],
                                     creds['cmdlet']['password'])
        else:
            powershell = '{0} {1}'.format(cmdlet, cmdlet_args)

        # connect to server
        self.connect(kwargs['hostname'], tport, creds['connect'])

        # run powershell command
        ps_result = self.connection.run_ps(powershell)
        result = {'stdout': ps_result.std_out,
                  'stderr': ps_result.std_err,
                  'exit_status': ps_result.status_code}

        if result['exit_status'] == 0:
            return (True, result)
        else:
            return (False, result)
