#!/usr/bin/python

# Requires students.csv, instructors.csv, email.template

import os.path
import boto.iam
import csv
import smtplib
import argparse
import string

from ucb_defaults import DEFAULT_REGION

# main
SMTP_SERVER = 'scf.berkeley.edu'

parser = argparse.ArgumentParser()
parser.add_argument('target', nargs='?', default='cloud101-fall-2014',
    metavar='course')
parser.add_argument('-s', '--sender', default='manager@stat.berkeley.edu',
    metavar='address', help='Email address to send credentials from.')
parser.add_argument('-u', '--users',
    help='Comma-delimited list of users. Default is all users.')
args = parser.parse_args()

# Connect to smtp server
connected = False 
while not connected:
    try:
        server = smtplib.SMTP(SMTP_SERVER)
        connected = True
        print 'Connect to ' + SMTP_SERVER
    except socket.error:
        print 'Could not connect to ' + SMTP_SERVER + '. Sleeping...'
        time.sleep(60)

template_buf = open(os.path.join(args.target, 'email.template')).read()
template = string.Template(template_buf)

creds_file = args.target + '-credentials.boto'
ssh_key_file = args.target + '-ssh_key.pem'

for category in ['instructors', 'students']:
    f = open(os.path.join(args.target, category + '.csv'), 'rb')
    users = csv.DictReader(f, delimiter='\t')
    for user in users:
        # Skip if we specify a fixed set of users and this isn't one of them.
        if args.users and user['username'] not in args.users:
            print 'skipping', user['username']
            continue
        msg = template.substitute(
            username=user['username'],
            target=args.target,
            url=user['signin_url'],
            password=user['password'],
            home_path=user['home_path'],
            creds_file=creds_file,
            ssh_key=ssh_key_file)

        try:
            print "Sending email to: " + user['username'] + '\n'
            server.sendmail(args.sender, user['username'], msg)
        except smtplib.SMTPRecipientsRefused:
            pass
