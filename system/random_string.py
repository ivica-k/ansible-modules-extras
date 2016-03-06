#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import *
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
import random

DOCUMENTATION = '''
---
module: random_string
author:
    - "Ivica Kolenkaš (ivica.kolenkas@gmail.com)"
version_added: "2.0.1.0"
description:
    - Generate random strings.
short_description: Generate random strings.
options:
  length:
    description:
      - Length of a generated string, defaults to 12.
    required: false
    default: 12
    aliases: [ "characters" ]
  digits:
    description:
      - Include digits 0-9 in generated string.
    required: false
    default: no
    aliases: [ "numbers" ]
  lowercase:
    description:
      - Include lowercase a-z in generated string..
    required: false
    default: no
    aliases: [ "lower" ]
  uppercase:
    description:
      - Include uppercase A-Z in generated string..
    required: false
    default: "yes"
    aliases: [ "upper", "caps" ]
  special:
    description:
      - Include !, #, $, %, &, =, ?, _  in generated string..
    required: false
    default: "no"
'''

EXAMPLES = '''
- name: generate 15 character uppercase string
  randomize:
    length=15
    uppercase=yes
- name: generate 12 character password
  randomize: >
    uppercase=yes
    digits=yes
    special=yes
    lowercase=yes
'''

RETURN = '''
rand_string:
    description: random string
    returned: success
    type: string
    sample: "GWaIq9qGyVaS"
'''

SPECIAL_CHARACTERS = ['!', '#', '$', '%', '&', '=', '?', '_']


def _generate(input_range, uppercase, lowercase, use_digits, special_chars):
    choices = []

    if uppercase:
        choices += ascii_uppercase
    if lowercase:
        choices += ascii_lowercase
    if use_digits:
        choices += digits
    if special_chars:
        choices += SPECIAL_CHARACTERS

    return ''.join(random.SystemRandom().choice(choices) for _ in range(input_range))


def main():
    module = AnsibleModule(
        argument_spec={
            'length': {'required': False, 'default': 12, 'type': 'int', 'aliases': ['characters']},
            'lowercase': {'required': False, 'default': False, 'type': 'bool', 'aliases': ['lower']},
            'uppercase': {'required': False, 'default': True, 'type': 'bool', 'aliases': ['upper', 'caps']},
            'digits': {'required': False, 'default': False, 'type': 'bool', 'aliases': ['numbers']},
            'special': {'required': False, 'default': False, 'type': 'bool'},
        },
        supports_check_mode=False
    )

    length = int(module.params['length'])
    lowercase = module.params['lowercase']
    uppercase = module.params['uppercase']
    use_digits = module.params['digits']
    special_chars = module.params['special']

    rand_string = _generate(length, uppercase, lowercase, use_digits, special_chars)

    module.exit_json(rand_string=rand_string)


if __name__ == '__main__':
    main()
