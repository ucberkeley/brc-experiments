#!/usr/bin/python

import os.path
import boto, boto.iam, boto.s3, boto.ec2
import csv
import string
import random
import logging
import re
import uuid
import sys
import smtplib

from custom_policies import apply_policy
from ucb_defaults import DEFAULT_REGION

# FIXME: Missing feature in current version (2.33) of boto means we
# need to monkeypatch from upstream until this is merged and available
# in a standard system release.
# See: https://github.com/ucberkeley/brc-experiments/pull/1
# And: https://github.com/boto/boto/pull/2578
import monkeypatch
boto.iam.IAMConnection.create_login_profile=monkeypatch.create_login_profile

def random_string(size=10, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_signin_url(iam, target, uq):
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

    signin_url = "https://{}.signin.aws.amazon.com/console/".format(iam.get_user().user.user_id)

    try:
        response = iam.create_account_alias(uq)
        signin_url = iam.get_signin_url()
        signin_url = re.sub(r'/console/.*', '/console', signin_url) # trim to just the essential part
    except boto.exception.BotoServerError, response:
        logging.warn(response.body)

    print 'Sign-in url: {}'.format(signin_url)
    with open(os.path.join(target, 'signin.url'), 'w') as f:
        f.writelines(signin_url + '\n')
    print "URL: " + signin_url
    return signin_url

credentials_template = """
[Credentials]
aws_access_key_id = {}
aws_secret_access_key = {}
ssh_key_filename = {}
ssh_key_fingerprint = {}
"""

def create_iam_users(target, category, bucket_name, signin_url):
    email_file = os.path.join(target, category + '.list')
    email_addresses = [r[0] for r in csv.reader(open(email_file))]

    iam = boto.iam.connect_to_region(DEFAULT_REGION)
    group = target + '-' + category
    try:
        response = iam.create_group(group)
    except boto.exception.BotoServerError, x:
        print 'Warning: Skipping error on create_group:', group

    resources = ['ec2', 'home']
    for r in resources:
        response = apply_policy(group, category + '-' + r, bucket_name)

    s3 = boto.s3.connect_to_region(DEFAULT_REGION)
    bucket = s3.get_bucket(bucket_name)

    data = []
    for e in email_addresses:
        try:
            response = iam.create_user(e)
        except boto.exception.BotoServerError, x:
            print 'Warning: Skipping error on create_user:', e
            continue
        response = iam.add_user_to_group(group, e)
        response = iam.create_access_key(e)
        access_key = response.access_key_id
        secret_key = response.secret_access_key
        ec2 = boto.ec2.connect_to_region(DEFAULT_REGION)
        ssh_key_name = e + ':' + target
        ssh_key_filename = target + '-ssh_key.pem'
        credentials_filename = target + '-credentials.boto'
        try:
            ssh_key = ec2.create_key_pair(ssh_key_name)
        except boto.exception.BotoServerError, x:
            print 'Warning: Skipping error on create_key_pair:', ssh_key_name
            continue
        credentials = credentials_template.format(access_key, secret_key, ssh_key_filename, ssh_key.fingerprint)
        home = "home/{}/".format(e)
        home_path = bucket_name + "/" + home
        key = bucket.new_key(home)
        prefix = home + credentials_filename
        key = bucket.new_key(prefix)
        key.set_contents_from_string(credentials)
        prefix = home + ssh_key_filename
        key = bucket.new_key(prefix)
        key.set_contents_from_string(ssh_key.material)
        password = random_string()
        response = iam.create_login_profile(e, password, password_reset_required=True)
        ### The password_reset_required is a new feature in a pull
        ### request waiting to be merged:
        ### https://github.com/boto/boto/pull/2578

        data.append(dict(
            username=e,
            access_key=access_key,
            secret_key=secret_key,
            password=password,
            signin_url = signin_url,
            home_path = home_path,
            credentials_filename = credentials_filename,
            ssh_key_filename = ssh_key_filename,
        ))
    return data

def save_credentials(target, category, creds):
    keys = ['username', 'password', 'access_key', 'secret_key',
            'credentials_filename', 'ssh_key_filename', 'home_path',
            'signin_url']
    f = open(os.path.join(target, category + '.csv'), 'ab')
    dict_writer = csv.DictWriter(f, keys, delimiter='\t')
    dict_writer.writer.writerow(keys)
    dict_writer.writerows(creds)

def email_user_passwords(creds, target, from_email):  
    SMTP_FROM = from_email
    SMTP_SERVER = 'scf.berkeley.edu'
    subject = 'Subject: Amazon class account'
    for user_creds in creds:
        to = 'To: ' + user_creds['username'] + '\n'
        fromInfo ='From: ' + SMTP_FROM + '\n'
        msg = fromInfo + to + subject + '\n\n' + 'Your Amazon class account for ' + target + \
        ' has been set up.\n' + \
        'Your username is ' + user_creds['username'] + '.\n' + \
        'Your one-time password is ' + user_creds['password'] + '.\n' + \
        'Please log in to ' + user_creds['signin_url'] + ' using the above information.\n' + \
        'Then change your password as prompted and navigate to the S3 service to' + \
        ' download your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and private SSH key.\n'
        connected = False 
        while not connected:
            try:
                server = smtplib.SMTP(SMTP_SERVER)
                connected = True
            except socket.error:
                time.sleep(60)
            try:
                server.sendmail(SMTP_FROM, user_creds['username'], msg)
                print "Sending notification to: " + user_creds['username'] + '\n'
            except smtplib.SMTPRecipientsRefused:
                pass


def provision(args):
    iam = boto.iam.connect_to_region(DEFAULT_REGION)
    try:
        response = iam.get_account_alias()
        uq = response['list_account_aliases_response']['list_account_aliases_result']['account_aliases'][0]
        print 'UQ (exists): ' + uq
        signin_url = "https://%s.signin.aws.amazon.com/console/" % uq
    except Exception, e:
        uniquify = '-uq' + str(uuid.uuid4())[:5]
        uq = args.target + uniquify
        print 'UQ (new): ' + uq
        signin_url = create_signin_url(iam, args.target, uq)

    bucket_name = uq

    s3 = boto.s3.connect_to_region(DEFAULT_REGION)
    ## create bucket names with uniquify suffix
    ## Further details: https://github.com/ucberkeley/brc-experiments/issues/4
    try:
        s3.create_bucket(bucket_name, location=DEFAULT_REGION)
    except:
        pass

#    for category in ['instructors','students']:
    for category in ['instructors']:
        creds = create_iam_users(args.target, category, bucket_name, signin_url)
        save_credentials(args.target, category, creds)
        if args.email: email_user_passwords(creds, args.target, args.sender)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('target', nargs='?', default='cloud101-fall-2014',
        metavar='course')
    parser.add_argument('-e', '--email', action='store_true',
        help='Email credentials.')
    parser.add_argument('-s', '--sender', default='manager@stat.berkeley.edu',
        metavar='address', help='Email address to send credentials from.')
    args = parser.parse_args()

    provision(args)
