#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_delay_profile_info

short_description: Get information about Sonarr delay profile.

version_added: "0.5.0"

description: Get information about Sonarr delay profile.

options:
    tag:
        description: Tag.
        type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all delay profiles.
- name: Gather information about all delay profiles
  devopsarr.sonarr.sonarr_delay_profile_info:

# Gather information about a single delay profile.
- name: Gather information about a single delay profile
  devopsarr.sonarr.sonarr_delay_profile_info:
    tag: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
delay_profiles:
    description: A list of delay profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Delay Profile ID.
            type: int
            returned: always
            sample: 1
        preferred_protocol:
            description: Preferred protocol.
            returned: always
            type: str
            sample: 'torrent'
        usenet_delay:
            description: Usenet delay.
            returned: always
            type: int
            sample: 0
        torrent_delay:
            description: Torrent delay.
            returned: always
            type: int
            sample: 0
        minimum_custom_format_score:
            description: Minimum cutoff format score.
            type: int
            returned: always
            sample: 0
        order:
            description: Order.
            returned: always
            type: int
            sample: 10
        enable_usenet:
            description: Enable Usenet.
            returned: always
            type: bool
            sample: true
        enable_torrent:
            description: Enable Torrent.
            returned: always
            type: bool
            sample: true
        bypass_if_highest_quality:
            description: Bypass if highest quality flag.
            returned: always
            type: bool
            sample: true
        bypass_if_above_custom_format_score:
            description: Bypass if above custom format score flag.
            returned: always
            type: bool
            sample: true
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        tag=dict(type='int'),
    )

    result = dict(
        changed=False,
        delay_profiles=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    client = sonarr.DelayProfileApi(module.api)

    # List resources.
    try:
        response = client.list_delay_profile()
    except Exception as e:
        module.fail_json('Error listing delay profiles: %s' % to_native(e.reason), **result)

    profiles = []
    # Check if a resource is present already.
    for profile in response:
        if module.params['tag']:
            if module.params['tag'] in profile['tags']:
                profiles = [profile.dict(by_alias=False)]
        else:
            profiles.append(profile.dict(by_alias=False))

    result.update(delay_profiles=profiles)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
