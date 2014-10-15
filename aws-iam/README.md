# Use Case
Provision a set of users in AWS IAM with limited delegated access to
EC2 resources for use in courses, workshops, bootcamps, and hackathons.

# Instructions
**WARNING:** Do **NOT** run this code on a production system!

The first time, simply run the following on an Ubuntu (BCE) system:

    sudo apt-get install -y python-boto
    ./provision.py

And then check your [AWS console IAM
dashboard](https://console.aws.amazon.com/iam/home?#home) to see the
provisioned
[users](https://console.aws.amazon.com/iam/home?#users),
[groups](https://console.aws.amazon.com/iam/home?#groups),
and [policies](https://console.aws.amazon.com/iam/home?#groups/cloud101-fall-2014-students).

Currently in iterative testing mode on a non-production AWS instance

    clear; ./destroy.py && ./provision.py

# TODO
- [X] default student policy allowing limited EC2 access
- [X] default instructor policy allowing full account access
- [X] create groups with corresponding policy attached
- [X] provision users in instructor group
- [X] provision users in student group
- [ ] save credentials for all users
- [ ] script for student to self-start EC2 instance with Spark AMI from laptop BCE VM
- [ ] stricter student policy allowing even more limited EC2 access
