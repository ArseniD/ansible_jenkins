# -*- coding: utf-8 -*-

import subprocess
import vagrant

from fabric.state import output
from fabric.api import env, execute, run
from ansible.module_utils.basic import AnsibleModule
output['everything'] = False


class Vagrant(object):

    def __init__(self, vagrant_path, state):

        self.v = vagrant.Vagrant(root=vagrant_path,
                                 quiet_stdout=True,
                                 quiet_stderr=True,
                                 )

        if self.v.status() != 'running':
            self.switch_case(state)

        env.hosts = [self.v.user_hostname_port()]
        env.key_filename = self.v.keyfile()
        env.disable_known_hosts = True

    def switch_case(self, state):
        return {
            'started': lambda: self.v.up(),
            'stopped': lambda: self.v.halt(),
            'destroyed': lambda: self.v.destroy()
        }[state]()

    def get_ram(self):
        return run("echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE) / (1024 * 1024)))")

    def get_os(self):
        return run("cat /etc/*-release | head -1 | awk {'print $1'}")

    def os_name(self):
        return execute(self.get_os).values()[0]

    def ram_size(self):
        return execute(self.get_ram).values()[0]

    def get_info(self):
        data = dict()
        data['state'] = self.v.status()[0][1]
        data['ip'] = self.v.hostname()
        data['port'] = int(self.v.port())
        data['ssh_key'] = self.v.keyfile()
        data['username'] = self.v.user()
        data['os_name'] = self.os_name()
        data['ram_size_mb'] = int(self.ram_size())
        return data


if __name__ == "__main__":

    try:
        global module
        module = AnsibleModule(
            argument_spec={
                'vagrant_path': {'required': True, 'type': 'str'},
                'state': {'required': True, 'type': 'str'}
            },
            supports_check_mode=True,
        )

        args = module.params
        output_data =  Vagrant(args['vagrant_path'], args['state']).get_info()

        result = {'result': output_data}
        module.exit_json(**result)

    except subprocess.CalledProcessError:
        print('Something is going wrong, vm is already stopped/destroyed \n'
              'or vagrantfile have mistakes.')
    except OSError:
        print('No such file or directory')
