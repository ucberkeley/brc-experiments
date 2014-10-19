#!/usr/bin/env python

# FIXME: Missing feature in current version (2.33) of boto means we
# need to monkeypatch from upstream until this is merged and available
# in a standard system release.
# See: https://github.com/ucberkeley/brc-experiments/pull/1
# And: https://github.com/boto/boto/pull/2578
def create_login_profile(self, user_name, password, password_reset_required=False):
	"""
	Creates a login profile for the specified user, give the user the
	ability to access AWS services and the AWS Management Console.

	:type user_name: string
	:param user_name: The name of the user

	:type password: string
	:param password: The new password for the user

	:type password_reset_required: bool
	:param password_reset_required: Require user to create a new password
	    at next sign-in (Optional).  Defaults to False.
	"""
	params = {'UserName': user_name,
		  'Password': password}
	if password_reset_required:
	    params['PasswordResetRequired'] = 'true'
	else:
	    params['PasswordResetRequired'] = 'false'
	return self.get_response('CreateLoginProfile', params)
