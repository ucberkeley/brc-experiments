# Security Best Practices For EVERYONE

## Your Responsibility

You are responsible for keeping your AWS credentials **Safe & Secure**.

## Bad Guys

If you do not keep your credentials **Safe & Secure**, for example if you upload them to your GitHub account, then Bad Guys will find them.

In fact, the Bad Guys are continuously scanning for credentials everywhere and will find them almost immediately as soon as they are exposed.

Then the Bad Guys will take over all available resources and drain them until they are discovered. They might even destroy your homework.

## Oops!

If you think your credentials have been exposed, please tell us right away at [aws-support@stat.berkeley.edu](mailto:aws-support@stat.berkeley.edu) so that we can immediately revoke the credentials to keep the bad guys out of the system.

## What are my credentials?

Your credentials come in two files with the following suffixes in their name:

- *-credentials.boto*
- *-ssh_key.pem*

## How to keep credentials Safe & Secure

- Only download your credential files to your local machine
- Do not send your credentials via email
- Do **NOT** upload your credentials (even in encrypted form) to GitHub, Bitbucket, Dropbox, Google Drive, or any other remote location.
- Don't share your credentials with anybody else, even temporarily.
- Do not make a copy or snapshot of your VM (Virtual Machine) to share with others because your credentials will also be copied along with the rest of the VM image.

## More about Credentials

### AWS Access Keys

The *-credentials.boto* file contains the credentials that allow you to use an automated script to start, access, read, write, stop, and destroy AWS resources such as Elastic MapReduce clusters and S3 Storage buckets.

There are two parts to an access key, the *access key ID* and the *secret access key*. Both of these items are sensitive information that you should not share with anyone nor upload anywhere.

- An *access key ID* looks like **AKIAIOSFODNN7EXAMPLE**
- A *secret access key* is longer and looks like **wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY**

### SSH Key pairs

The *-ssh_key.pem* file contains the credentials that allow you to log into your EC2 compute or EMR (Elastic MapReduce) instance using the ssh program (e.g. ssh, PuTTY, Terminal, etc).

# Security Best Practices For Service Providers

You fall under this heading if you are configuring or providing access to any of the following to users that you delegate access to cloud resources for which you are the owner.

## AWS Shared Responsibility Model

Under the [AWS Shared Responsibility Model](http://media.amazonwebservices.com/AWS_Security_Best_Practices.pdf) we as the customers are responsible for the security of the following:

- Amazon Machine Images (AMIs)
- Operating systems
- Applications
- Data in transit
- Data at rest
- Data stores
- Credentials
- Policies and configuration

### AWS Checklists

- [AWS Auditing Security Checklist](http://d0.awsstatic.com/whitepapers/compliance/AWS_Auditing_Security_Checklist.pdf)
- [AWS Operational Checklists](http://media.amazonwebservices.com/AWS_Operational_Checklists.pdf#page%3D5)

## Credentials

# Distributing Credentials

# AWS Security Incident Response
