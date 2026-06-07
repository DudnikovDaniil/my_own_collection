#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
version_added: "1.0.0"
short_description: Create a text file on remote host
description:
    - This module creates a text file on the remote host with specified content.
    - If the file already exists and content matches, nothing is changed.
options:
    path:
        description:
            - The absolute path to the file to create.
        required: true
        type: str
    content:
        description:
            - The content to write to the file.
        required: true
        type: str
author:
    - DudnikovDaniil (@DudnikovDaniil)
'''

EXAMPLES = r'''
- name: Create a test file
  my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"

- name: Create a config file
  my_own_module:
    path: /etc/myapp/config.ini
    content: |
      [DEFAULT]
      debug = true
'''

RETURN = r'''
path:
    description: Path to the file that was created.
    type: str
    returned: always
    sample: "/tmp/test.txt"
content:
    description: Content that was written to the file.
    type: str
    returned: always
    sample: "Hello, World!"
'''

import os

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    result['path'] = path
    result['content'] = content

    # Проверяем, существует ли файл и совпадает ли содержимое
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                existing_content = f.read()
            if existing_content == content:
                module.exit_json(**result)
        except Exception as e:
            module.fail_json(msg="Failed to read existing file: {}".format(str(e)), **result)

    # Режим проверки (check mode)
    if module.check_mode:
        result['changed'] = True
        module.exit_json(**result)

    # Создаём директорию, если её нет
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            module.fail_json(msg="Failed to create directory {}: {}".format(directory, str(e)), **result)

    # Записываем файл
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg="Failed to write file: {}".format(str(e)), **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
