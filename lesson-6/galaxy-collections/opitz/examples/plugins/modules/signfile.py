#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import os
import datetime

DOCUMENTATION = r'''
---
module: signfile

short_description: Sign a file with name and date

version_added: "0.0.2"

description: Module inserts user and date in the first line of the file.

options:
    name:
        description: Name of a user who wants to sign file.
        required: true
        type: str
    path:
        description: Path to file
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
#extends_documentation_fragment:
#    - opitz.samples.my_doc_fragment_name

author:
    - Fabian Hardt
'''

EXAMPLES = r'''
# Pass in a message
- name: Insert user and date to file
  opitz.samples.signfile:
    name: Ingo Brauckhoff
    file: /tmp/testfile.txt
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
stat:
    description: Status of the file (true if the file exists, false if not).
    type: boolean
    returned: always
    sample: 'true'
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        path=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=True,
        path="",
        stat=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # the body of the module
    result['path'] = module.params['path']

    # check if the file exists
    if(os.path.exists(module.params['path'])):
        result['stat'] = True
        # check if a sign is already in the file
        with open(module.params['path']) as fp:
            all_lines = fp.readlines()
        if(all_lines[0][0:5] == "SIGNATURE:"):
            result['changed'] = False
    else:
        all_lines = []

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if(module.check_mode or not result['changed']):
        module.exit_json(**result)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # sign the file
    ft = datetime.datetime.now()
    sign_line = "SIGNATURE: " + module.params['name'] + "  " + ft.strftime("%c") + "\n"
    all_lines.insert(0, sign_line)
    with open(module.params['path'], "wt") as fp:
        fp.writelines(all_lines)
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
