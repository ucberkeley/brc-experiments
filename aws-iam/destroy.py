#!/usr/bin/python

# DANGER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Do *NOT* run this script in a production AWS IAM environment or you
# risk deleting important resources that cannot be recovered.
#
# Do you know for certain which AWS credentials you are using right now?
# EXTRA DANGER: you might delete something by accident if you run this script at all
#
# The purpose of this script is to conveniently and quickly
# deprovision an IAM environment for experimenting with building a
# safe way to provision and deprovision IAM accounts.

import boto
import json

raise RuntimeError("DANGER! I warned you once... Don't run this script.")
def destroy(target):
    response = iam = boto.connect_iam()
    for category in ['instructors','students']:
        group = target + '-' + category
        response = iam.get_group(group)
        users = response.users
        for u in users:
            response = iam.get_all_access_keys(u.user_name)
            access_keys = response.access_key_metadata
            for k in access_keys:
                response = iam.delete_access_key(k.access_key_id, k.user_name)
                iam.remove_user_from_group(group, u.user_name)
                iam.delete_login_profile(u.user_name)
                iam.delete_user(u.user_name)
        response = iam.get_all_group_policies(group)
        policies = response.policy_names
        for p in policies:
            response = iam.delete_group_policy(group, p)
        response = iam.delete_group(group)

if __name__ == '__main__':
    target = 'cloud101-fall-2014'
    destroy(target)
