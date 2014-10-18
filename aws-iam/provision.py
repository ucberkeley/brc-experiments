#!/usr/bin/python

import os.path
import json
import boto
import csv
import string
import random
import logging
import re
import uuid

from iampolicies import apply_policy
from ucb_defaults import DEFAULT_REGION

def random_string(size=10, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_signin_url(target):
    # The script will also attempt to create a sign-in alias based on the
    # course name, with the following behavior:
    #
    # - If your account already has an alias it will leave the existing
    #   alias in place, it will _not_ overwrite it.
    #
    # - If the alias you chose is already in use, then it will use the
    #   default signin url.
    #
    # [Limitations on IAM Entities](http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html) says:
    #
    # - AWS account ID aliases must be unique across AWS products, and must
    #   be alphanumeric following DNS naming conventions. An alias must be
    #   lowercase, it must not start or end with a hyphen, it cannot contain
    #   two consecutive hyphens, and it cannot be a 12 digit number.
    #
    # - AWS account ID alias: 3 to 63 characters.
    #
    # - AWS account aliases per AWS account: 1

    iam = boto.iam.connect_to_region(DEFAULT_REGION)
    signin_url = "https://{}.signin.aws.amazon.com/console/".format(iam.get_user().user.user_id)
    try:
        response = iam.create_account_alias(target)
        signin_url = iam.get_signin_url()
        signin_url = re.sub(r'/console/.*', '/console', signin_url) # trim to just the essential part
    except boto.exception.BotoServerError, response:
        logging.warn(response.body)

    logging.info('Using default sign-in url: {}'.format(signin_url))

def create_iam_users(target, category):
    email_file = os.path.join(target, category + '.list')
    email_addresses = [r[0] for r in csv.reader(open(email_file))]

    iam = boto.iam.connect_to_region(DEFAULT_REGION)
    group = target + '-' + category
    response = iam.create_group(group)
    resources = ['ec2', 'home']
    for r in resources:
        response = apply_policy(group, category + '-' + r)

    s3 = boto.s3.connect_to_region(DEFAULT_REGION)
    bucket = s3.get_bucket(target)

    data = []
    for e in email_addresses:
        response = iam.create_user(e)
        user = response.user
        response = iam.add_user_to_group(group, e)
        response = iam.create_access_key(e)
        access_key = response.access_key_id
        secret_key = response.secret_access_key
        password = random_string()
        response = iam.create_login_profile(e, password)
        # response = iam.create_login_profile(e, password, password_reset_required=True)
        ### The password_reset_required is a new feature in a pull
        ### request waiting to be merged:
        ### https://github.com/boto/boto/pull/2578

        data.append({
            'username' : e,
            'access_key' : access_key,
            'secret_key' : secret_key,
            'password' : password,
        })
    return data

def save_credentials(target, category, creds):
    keys = ['username', 'access_key', 'secret_key', 'password']
    f = open(os.path.join(target, category + '.csv'), 'wb')
    dict_writer = csv.DictWriter(f, keys, delimiter='\t')
    dict_writer.writer.writerow(keys)
    dict_writer.writerows(creds)

def provision(target):
    create_signin_url(target)
    s3 = boto.connect_s3()
    ## create bucket names with uniquify suffix
    ## Further details: https://github.com/ucberkeley/brc-experiments/issues/4
    uniquify = 'uq' + str(uuid.uuid4())[:5]
    bucket_name = target + '-' + uniquify
    bucket = s3.create_bucket(bucket_name)
    for category in ['instructors','students']:
        creds = create_iam_users(target, category)
        save_credentials(target, category, creds)

if __name__ == '__main__':
    target = 'cloud101-fall-2014'
    provision(target)
