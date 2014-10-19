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

import boto, boto.iam, boto.s3, boto.ec2
import json
import sys
from ucb_defaults import DEFAULT_REGION

#raise RuntimeError("DANGER! I warned you once... Don't run this script.")
def destroy(target):
    response = iam = boto.iam.connect_to_region(DEFAULT_REGION)
    try:
        response = alias = iam.get_account_alias().account_aliases
        if alias:
            iam.delete_account_alias(alias[0])
    except Exception:
        # if there was an exception, then the account didn't have an alias
        pass

    ec2 = boto.ec2.connect_to_region(DEFAULT_REGION)
    for k in ec2.get_all_key_pairs():
        response = ec2.delete_key_pair(k.name)

    response = s3 = boto.s3.connect_to_region(DEFAULT_REGION)
    ## only delete bucket names created with uniquify suffix
    ## Further details: https://github.com/ucberkeley/brc-experiments/issues/4
    try:
        for b in s3.get_all_buckets():
            if '-uq' in b.name:
                try:
                    b.delete_keys([k.name for k in b.get_all_keys()])
                except Exception, e:
                    pass
                try:
                    s3.delete_bucket(b.name)
                except Exception, e:
                    pass
    except Exception, e:
        print e
        pass
    for category in ['instructors','students']:
        group = target + '-' + category
        try:
            response = iam.get_group(group)
        except Exception:
            response = None
            pass
        if response:
            users = response.users
            for u in users:
                for k in iam.get_all_access_keys(u.user_name).access_key_metadata:
                    response = iam.delete_access_key(k.access_key_id, k.user_name)
                response = iam.create_access_key(u.user_name)
                for k in iam.get_all_access_keys(u.user_name).access_key_metadata:
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
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = 'cloud101-fall-2014'
    destroy(target)
