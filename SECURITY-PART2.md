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
