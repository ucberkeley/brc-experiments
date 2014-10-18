#!/usr/bin/env python

# Variable interpolation syntax for policy templates use %var% as the
# variable name to replace in the template formatting due to JSON
# syntax requiring escaping of {} as {{}} prior to the variable
# interpolation occuring.
import re
def formatstring_json_escape(s):
    escape_s = re.sub(r'([{}])', r'\1\1', s)
    return re.sub(r'%(.+?)%', r'{\1}', escape_s)

policy_template = {
'students-ec2': '''
{
    "Version": "2012-10-17",
    "Statement": [
	{
	    "Effect": "Allow",
	    "Action": "ec2:RunInstances",
	    "Resource": "arn:aws:ec2:us-west-2::image/ami-3d50120d"
	},
	{
	    "Effect": "Allow",
	    "Action": [
		"ec2:Describe*",
		"ec2:StartInstances",
		"ec2:StopInstances",
		"ec2:TerminateInstances"
	    ],
	    "Resource": "*"
	}
    ]
}
''',
'students-home': '''
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGroupToSeeBucketListInTheConsole",
      "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
      "Effect": "Allow",
      "Resource": ["arn:aws:s3:::*"]
    },
    {
      "Sid": "AllowRootAndHomeListingOfCompanyBucket",
      "Action": ["s3:ListBucket"],
      "Effect": "Allow",
      "Resource": ["arn:aws:s3:::%bucket%"],
      "Condition":{"StringEquals":{"s3:prefix":["","home/"],"s3:delimiter":["/"]}}
    },
    {
      "Sid": "AllowListingOfUserFolder",
      "Action": ["s3:ListBucket"],
      "Effect": "Allow",
      "Resource": ["arn:aws:s3:::%bucket%"],
      "Condition":{"StringLike":{"s3:prefix":["home/${aws:username}/*"]}}
    },
    {
       "Sid": "AllowAllS3ActionsInUserFolder",
       "Action":["s3:*"],
       "Effect":"Allow",
       "Resource": ["arn:aws:s3:::%bucket%/home/${aws:username}/*"]
    }
  ]
}
''',
'instructors-ec2' : '''
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
''',
'instructors-home' : '''
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
'''
}


import boto
import json
import logging

def apply_policy(group, policy_name):
    logging.debug(policy_template[policy_name])
    iam = boto.connect_iam()
    policy = json.dumps(json.loads(formatstring_json_escape(policy_template[policy_name]).format(bucket=group)))
    response = iam.put_group_policy(group, policy_name, policy)
    return response
