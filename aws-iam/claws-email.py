#!/usr/bin/python

# Requires students.csv, instructors.csv, email.template

import os.path
import boto.iam
import csv
import smtplib
import argparse
import string.Template

from ucb_defaults import DEFAULT_REGION

# main
SMTP_SERVER = 'scf.berkeley.edu'

parser = argparse.ArgumentParser()
parser.add_argument('target', nargs='?', default='cloud101-fall-2014',
    metavar='course')
parser.add_argument('-s', '--sender', default='manager@stat.berkeley.edu',
    metavar='address', help='Email address to send credentials from.')
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

template_buf = open(os.path.join(args.target, 'email.template').read()

for category in ['instructors', 'students']:
    f = open(os.path.join(args.target, category + '.csv'), rb)
    users = csv.DictReader(f, delimiter='\t')
    for user in users:
        msg = template.substitute(
            username=user['username'],
            target=args.target,
            url=user['signin_url'],
            password=user['password'],
            home_path=user['home_path'],
            creds_file=user['credentials_filename'],
            ssh_key=user['ssh_key_filename'])

        try:
            server.sendmail(args.sender, student['username'], msg)
            print "Sending email to: " + user_creds['username'] + '\n'
        except smtplib.SMTPRecipientsRefused:
            pass
