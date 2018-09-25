import winrm

# Note:  in order for this to work you need to run the following script on the
#  host
#  https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1


class WinRmConnection(object):

    def __init__(self, hostname,
                 port=5986,
                 transport='ntlm',
                 username=None,
                 password=None):
        # default to https (usualy port 5986)
        scheme = 'https'

        # if connect to 5985 then we need to use http
        if port == 5985:
            scheme = "http"

        winrm_url = '{}://{}:{}/wsman'.format(scheme, hostname, port)
        self.session = winrm.Session(winrm_url,
                                     auth=(username, password),
                                     transport=transport,
                                     server_cert_validation='ignore')

    def run_ps(self, cmd):
        """Run the PowerShell command/script in :param cmd:
        :param cmd: PowerShell command/script to execute on the windows host
        """
        return self.session.run_ps(cmd)

    def run_cmd(self, cmd):
        """Run the Command Prompt command in :param cmd:
        :param cmd: Command Prompt command to execute on the windows host
        """
        return self.session.run_cmd(cmd)
