#!/home/student/.pyenv/versions/3.5.4/bin/python
# -*- coding: utf-8 -*-

import tomcatmanager as tm
from ansible.module_utils.basic import AnsibleModule

class Tomcat(object):
    def __init__(self, url, war, username, password):

        self.url = url
        self.war = war
        self.username = username
        self.password = password

    def deploy(self):
        tomcat = tm.TomcatManager()
        try:
            r = tomcat.connect(url=self.url, user=self.username, password=self.password)
            if r.ok:
                tomcat.deploy(path='/sample', localwar=self.war)
            else:
                print('not connected')
        except Exception as err:
            # handle exception
            print('not connected')


if __name__ == "__main__":

    try:
        global module
        module = AnsibleModule(
            argument_spec={
                'url': {'required': True, 'type': 'str'},
                'war': {'required': True, 'type': 'str'},
                'username': {'required': True, 'type': 'str'},
                'password': {'required': True, 'type': 'str'}
            },
            supports_check_mode=True,
        )

        args = module.params
        output_data =  Tomcat(args['url'],
                              args['war'],
                              args['username'],
                              args['password']).deploy()

        result = {'result': output_data}
        module.exit_json(**result)
    except:
        print('Something went wrong, please check tomcat and input data')

    # Tomcat('http://10.0.0.10/manager',
    #        '/home/juzo/cm/ansible/day-4/hello-war/target/mnt-lab.war',
    #        'arsen', 'arsen').deploy()
