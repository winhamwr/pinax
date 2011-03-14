from django.utils.functional import LazyObject
from django.utils.translation import ugettext_lazy as _

class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = AccountSettings()


class AccountSettings(object):
    def __init__(self):
        from django.conf import settings

        self.ERROR_MSG = {}
        self.ERROR_MSG['ResetPassword'] = {}
        self.ERROR_MSG['ResetPassword']['unverified_email'] = getattr(
            settings,
            'ACCOUNT_ERRORMSG_RESETPASSWORD_UNVERIFIEDEMAIL',
            _("E-mail address not verified for any user account"))

settings = AccountSettings()