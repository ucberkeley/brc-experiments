#!/usr/bin/python

import os.path
import json
import boto
import csv
import string
import random
import logging
import re

def random_string(size=10, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_signin_url(target):
    iam = boto.connect_iam()
    # Note: account aliases must be GLOBALLY unique across the entire
    # AWS sign-in alias namespace and there is nothing that prevents
    # someone from registering the same alias.
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
    policy_file = os.path.join(target, category + '-policy.json')
    policy = json.dumps(json.load(open(policy_file)))

    iam = boto.connect_iam()
    group = target + '-' + category
    response = iam.create_group(group)
    response = iam.put_group_policy(group, category + '-policy', policy)

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
    for category in ['instructors','students']:
        creds = create_iam_users(target, category)
        save_credentials(target, category, creds)

if __name__ == '__main__':
    target = 'cloud101-fall-2014'
    provision(target)
