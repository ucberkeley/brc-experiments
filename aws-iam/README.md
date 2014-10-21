# TODO
- [X] default student policy allowing limited EC2 access
- [X] default instructor policy allowing full account access
- [X] create groups with corresponding policy attached
- [X] provision users in instructor group
- [X] provision users in student group
- [X] save credentials for all users
- [X] create alias for login url - [Issue #2](https://github.com/ucberkeley/brc-experiments/issues/2)
- [X] set us-west-2 (Oregon) as default region for UC Berkeley - [Issue #5](https://github.com/ucberkeley/brc-experiments/issues/5)
- [X] distribute credentials via protected S3 bucket only available after password change at first login
- [X] force changing password at first login - [Issue #1](https://github.com/ucberkeley/brc-experiments/pull/1)
- [X] email template for temporary password and login instructions
- [ ] script for student to self-start EC2 instance with Spark AMI from laptop BCE VM
- [ ] stricter student policy allowing even more limited EC2 access -[Issue #8](https://github.com/ucberkeley/brc-experiments/issues/8)
  - [ ] Max instance runtime: 4 hours
  - [ ] At most 13 EC2 instances: 1 master, 12 slaves
  - [ ] default instance type for Spark: 8GB, 2 core
  - [ ] allow optional instance types up to a limit of: 16GB, 8 cores
- [ ] handle SES From address verification and requesting production access from Amazon - [Issue #9](https://github.com/ucberkeley/brc-experiments/issues/9)

# Use Case
Provision a set of users in AWS IAM with limited delegated access to
EC2 resources for use in courses, workshops, bootcamps, and hackathons.

# Instructions
**WARNING:** Do **NOT** run this code on a production system!

Set up your AWS credentials with boto by copying the example and
replacing with your own credentials:

    cp -i .boto.example ~/.boto
    chmod 400 ~/.boto

The first time, simply run the following on an Ubuntu (BCE) system:

    sudo pip install boto
    ./provision.py [name of directory (i.e., class name) containing student/instructor lists]

Note: a previous version suggested version of this document suggested
`sudo apt-get install -y python-boto` to install boto, however as of
this writing, the BCE 1.3 release that uses Ubuntu 14.04 LTS (Trusty)
only has boto `v2.20.1`, whereas I am now using boto `v2.32.1` which
is necessary due to
[differences in the earlier versions](https://github.com/ucberkeley/brc-experiments/issues/11).

And then check your [AWS console IAM
dashboard](https://console.aws.amazon.com/iam/home?#home) to see the
provisioned
[users](https://console.aws.amazon.com/iam/home?#users),
[groups](https://console.aws.amazon.com/iam/home?#groups),
and [policies](https://console.aws.amazon.com/iam/home?#groups/cloud101-fall-2014-students).

# Sign-in URL alias limitations

The script will also attempt to create a _unique_ sign-in alias based on the
course name with a random suffix that starts with `-uq.....`, with the following behavior:

- If your account already has an alias it will leave the existing
  alias in place, it will _not_ overwrite it.

- If the alias you chose is already in use, then it will use the
  default signin url.

[Limitations on IAM Entities](http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html) says:

- AWS account ID aliases must be unique across AWS products, and must
  be alphanumeric following DNS naming conventions. An alias must be
  lowercase, it must not start or end with a hyphen, it cannot contain
  two consecutive hyphens, and it cannot be a 12 digit number.

- AWS account ID alias: 3 to 63 characters.

- AWS account aliases per AWS account: 1

Currently in iterative testing mode on a non-production AWS instance

    clear; ./destroy.py [class dir name]  && ./provision.py [class dir name]  && ./sendcreds.py [class dir name]
