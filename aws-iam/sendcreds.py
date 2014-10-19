#!/usr/bin/env python

import boto
import os.path
import csv

def send_emails(target):
    content = open(os.path.join(target, 'email.template')).readlines()
    subject = content[2]
    template = ''.join(content)
    ses = boto.connect_ses()
    people = csv.DictReader(open(os.path.join(target, 'students.csv')), delimiter='\t')
    for data in people:
        data['course'] = target
        recipient = data['username']
        body = template.format(**data)
        subject = subject.format(**data)
        try:
            ses.send_email(
                source='aculich@berkeley.edu',
                subject=subject,
                body=body,
                to_addresses=recipient,
                cc_addresses=None,
                bcc_addresses='aculich@berkeley.edu',
                format='text',
                reply_addresses=None,
                return_path=None)
        except boto.ses.exceptions.SESAddressNotVerifiedError:
            print "-------------------------------------------------------"
            print "****ATTENTION: Email *NOT* sent to unverified recipient: {}".format(recipient)
            print "see Issue #9: https://github.com/ucberkeley/brc-experiments/issues/9"
            print "Below is the message that would have been sent."
            print; print
            print body
            pass
if __name__ == '__main__':
    target = 'cloud101-fall-2014'
    send_emails(target)
