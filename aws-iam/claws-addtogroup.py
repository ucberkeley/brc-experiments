#!/usr/bin/python

# Example:
# class-addtogroup.py s157-students user1@berkeley.edu user2@berkeley.edu ...

import sys
import boto.iam

from ucb_defaults import DEFAULT_REGION

iam = boto.iam.connect_to_region(DEFAULT_REGION)

if len(sys.argv) < 3:
    print 'Usage: %s GROUP USER [ USER ... ]' % sys.argv[0]
    sys.exit(1)

group = sys.argv[1]
users = sys.argv[2:]

all_groups = iam.get_all_groups()
groups = all_groups['list_groups_response']['list_groups_result']['groups']

if group not in map(lambda x: x.group_name, groups):
    print 'Error: group does not exist: ' + group
    sys.exit(1)

for user in users:
    response = iam.add_user_to_group(group, user)
