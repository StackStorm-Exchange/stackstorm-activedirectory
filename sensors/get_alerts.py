#!/usr/bin/env python3

"""Active Directory Integration - Sense admin list change"""

import winrm
from st2reactor.sensor.base import PollingSensor


class ADAdminSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):

        interval = config.get('poll_interval', 120)
        if interval:
            poll_interval = interval
        super(ADAdminSensor, self).__init__(sensor_service=sensor_service,
                                            config=config,
                                            poll_interval=poll_interval)
        self._trigger_ref = 'activedirectory.watched_group_changed'

        self._logger = self._sensor_service.get_logger(__name__)

        self.groups = config.get('groups')

        hostname = config.get('hostname')
        port = config.get('port', 5986)
        transport = config.get('transport', 'ntlm')

        self.creds_name = config.get('sensor_credential_name')
        creds = config.get('activedirectory').get(self.creds_name)

        username = creds.get('username')
        password = creds.get('password')

        scheme = 'http' if port == 5985 else 'https'

        winrm_url = '{}://{}:{}/wsman'.format(scheme, hostname, port)
        self.session = winrm.Session(winrm_url,
                                     auth=(username, password),
                                     transport=transport,
                                     server_cert_validation='ignore')

        self.members = ['first_run_place_holder']

    def setup(self):
        pass

    def poll(self):

        for group in self.groups:

            members = self._get_members()

            output_ps = ("Try\n"
                         "{{\n"
                         "  {0} | ConvertTo-Json\n"
                         "}}\n"
                         "Catch\n"
                         "{{\n"
                         "  $formatted_output = ConvertTo-Json -InputObject $_\n"
                         "  $host.ui.WriteErrorLine($formatted_output)\n"
                         "  exit 1\n"
                         "}}")

            powershell = "$ProgressPreference = 'SilentlyContinue';\n"
            powershell += 'Get-ADGroupMember -Identity "' + group + '"'

            # add output formatters to the powershell code
            powershell = output_ps.format(powershell)

            self._logger.debug(powershell)

            # run powershell command
            response = self.session.run_ps(powershell)

            self._logger.info(response)
            self._logger.info(response.json())

            response_output = response.__dict__['std_out']

            self._logger.debug(response_output)

            response_list = response_output.split('\r\n\r\n')

            removed = list(set(members) - set(response_list))
            added = list(set(response_list) - set(members))

            if removed or added:
                self._logger.info('Change in AD group membership detected.')
                payload = {
                    'old_list': members,
                    'new_list': response_list,
                    'removed': removed,
                    'added': added,
                    'group': group,
                    'tenant': self.creds_name
                }

                self.sensor_service.dispatch(trigger=self._trigger_ref,
                                             payload=payload)

                self._set_members(members=response_list)
            else:
                self._logger.info('No change in AD group membership detected')

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_members(self):
        if not self.members and hasattr(self.sensor_service, 'get_value'):
            self.members = self.sensor_service.get_value('members')

        return self.members

    def _set_members(self, members):
        self.members = members

        if hasattr(self.sensor_service, 'set_value'):
            self.sensor_service.set_value(name='members', value=members)
