#!/usr/bin/env python3

"""Active Directory Integration - Sense admin list change"""

import json

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

        self.members = {}

        for group in self.groups:
            self.members[group] = []

    def setup(self):
        pass

    def poll(self):

        for group in self.groups:

            members = self._get_members(group)
            self._logger.info(group)
            self._logger.info('members')
            self._logger.info(members)

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

            response_list = json.loads(response.__dict__['std_out'])

            self._logger.info(response_list)

            removed = []
            added = []
            added_names = []
            removed_names = []

            for new_item in response_list:
                if new_item not in members:
                    added.append(new_item)
                    added_names.append(new_item.get('SamAccountName'))
            for old_item in members:
                if old_item not in response_list:
                    removed.append(old_item)
                    removed_names.append(old_item.get('SamAccountName'))

            if added:
                self._logger.info('New member in AD group detected.')
                payload = {
                    'added': added,
                    'group': group,
                    'tenant': self.creds_name,
                    'SamAccountNames': added_names
                }

                self.sensor_service.dispatch(trigger='activedirectory.watched_group_member_added',
                                             payload=payload)

            if removed:
                self._logger.info('Member removal in AD group detected.')
                payload = {
                    'removed': removed,
                    'group': group,
                    'tenant': self.creds_name,
                    'SamAccountNames': removed_names
                }

                self.sensor_service.dispatch(trigger='activedirectory.watched_group_member_removed',
                                             payload=payload)

            if not removed and not added:
                self._logger.info('No change in AD group membership detected')

            self._set_members(members=response_list, group=group)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_members(self, group):
        if not self.members.get(group) and hasattr(self.sensor_service, 'get_value'):
            self.members[group] = self.sensor_service.get_value(group + '.members')

        return self.members[group]

    def _set_members(self, members, group):
        self.members[group] = members

        if hasattr(self.sensor_service, 'set_value'):
            self.sensor_service.set_value(name=group + '.members', value=members)
