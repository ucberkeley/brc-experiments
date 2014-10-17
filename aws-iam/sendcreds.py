#!/usr/bin/env python

import boto

ses = boto.connect_ses()
ses.send_email(
    source='aculich@berkeley.edu',
    subject='Subject',
    body='Body.',
    to_addresses='aculich@berkeley.edu',
    cc_addresses='aculich@berkeley.edu',
    bcc_addresses='aculich@berkeley.edu',
    format='text',
    reply_addresses=None,
    return_path=None)
