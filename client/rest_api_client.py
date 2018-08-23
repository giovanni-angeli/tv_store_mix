# -*- coding: UTF-8 -*-

import os
import sys
import time
import traceback
import pprint
import json
import random
import requests


DEFAULT_BASE_SERVER_URL = 'http://localhost:8007'
# ~ DEFAULT_BASE_SERVER_URL = 'http://metusco.pythonanywhere.com'


class RestApiClient(object):

    def __init__(self, base_server_url, auth, verbose=False):

        self.base_server_url = base_server_url
        self.auth_credentials = auth # (usr, pwd)
        self.verbose = verbose

    def _print_result(self, r):

        print(" **** : {} {}".format(r.url, r.request), "r.status_code:{}".format(r.status_code))
        
        if self.verbose:
            try:
                r_json = r.json()
                print("r_json:{}".format(r_json))
                if isinstance(r_json, list):
                    print("js_attributes:")
                    pprint.pprint(json.loads(r_json[0]['js_attributes']))
            except:
                traceback.print_exc()
                print(r.text)
            print(".")

    def get_units(self, filter=None):

        r = requests.get('{}/api-auth/units/'.format(self.base_server_url), auth=self.auth_credentials, params=filter)
        self._print_result(r)

    def get_contacts(self, filter=None):

        r = requests.get('{}/api-auth/contacts/'.format(self.base_server_url), auth=self.auth_credentials, params=filter)
        self._print_result(r)

    def create_contact(self, type, status, unit_serial_nr, js_attributes):

        pars_ = {
            'type': type,
            'status': status,
            'unit_serial_nr': unit_serial_nr,
            'js_attributes': js_attributes,
        }
        r = requests.post('{}/api-auth/contacts/'.format(self.base_server_url), auth=self.auth_credentials, data=pars_)
        self._print_result(r)

    def create_unit(self, name, serial_nr, ftp_url, user, js_attributes, group='generic'):

        pars_ = {
            'name': name,
            'ftp_url': ftp_url,
            'serial_nr': serial_nr,
            'user': user,
            'group': group,
            'js_attributes': js_attributes,
        }
        r = requests.post('{}/api-auth/units/'.format(self.base_server_url), auth=self.auth_credentials, data=pars_)
        self._print_result(r)

    def test_call_sequence(self, unit_nr, n_of_contacts=5):

        self.get_units()
        self.get_contacts()

        pars_ = {
            'name': "unit_{}".format(unit_nr),
            'ftp_url': "ftp://1.1.1.1/metusco",
            'serial_nr': "0000-000{}".format(unit_nr),
            'user': 'generic',
            'group': 'generic',
            'js_attributes': json.dumps({'time': time.asctime()}),
        }
        self.create_unit(**pars_)

        pars_ = {
            'type': 0,
            'status': 1,
            'unit_serial_nr': "0000-000{}".format(unit_nr),
            'js_attributes': json.dumps({'time': time.asctime()}),
        }
        for i in range(n_of_contacts):
            pars_['type'] = random.randint(0, 3)
            pars_['status'] = random.randint(0, 3)
            self.create_contact(**pars_)
            time.sleep(.1)

        filter = {'serial_nr': "0000-000{}".format(unit_nr)}
        self.get_units(filter)


def load_api_auth_credentials():

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '..', 'web_app', 'conf', 'API_AUTH')) as f:
        auths = [tuple(l.strip().split(' ')) for l in f.readlines()]

    return auths

def main():

    base_server_url = DEFAULT_BASE_SERVER_URL
    if len(sys.argv) > 1:
        base_server_url = sys.argv[1]
    print("\n   {}   base_server_url:<{}>\n".format(__file__, base_server_url))

    auths = load_api_auth_credentials()
    
    RestApiClient(base_server_url, auths[0]).test_call_sequence(4)

    RestApiClient(base_server_url, auths[1]).test_call_sequence(5)

    RestApiClient(base_server_url, auths[1]).get_contacts({'type': 1})


if __name__ == '__main__':

    main()
