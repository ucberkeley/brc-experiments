#!/usr/bin/python

import os.path
import json
import boto
import csv

def create_iam_users(target, category):
    email_file = os.path.join(target, category + '.list')
    email_addresses = [r[0] for r in csv.reader(open(email_file))]
    policy_file = os.path.join(target, category + '-policy.json')
    policy = json.dumps(json.load(open(policy_file)))

    iam = boto.connect_iam()
    group = target + '-' + category
    response = iam.create_group(group)
    response = iam.put_group_policy(group, category + '-policy', policy)

    for e in email_addresses:
        response = iam.create_user(e)
        user = response.user
        response = iam.add_user_to_group(group, e)
        response = iam.create_access_key(e)
        access_key = response.access_key_id
        secret_key = response.secret_access_key

def save_credentials(target, category, creds):
    pass

def provision(target):
    for category in ['instructors','students']:
        creds = create_iam_users(target, category)
        save_credentials(target, category, creds)

if __name__ == '__main__':
    target = 'cloud101-fall-2014'
    provision(target)
