"""
Class: CSC648-848 SW Engineering SU21
Team: Team 4
Name: Kiara Gil, Ostyn Sy, Joshua Stone, Cong Le, Miho Shimizu, Vernon Xie, Melinda Yee
GitHub Name: KiaraGil, OstynSy, JoshLikesToCode, CleGuren, simicity, vxie123, melinda15

File Name: validators.py

Description: Validation checks for Registration.
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 number."),
                code='password_no_number',
            )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least 1 symbol."),
                code='password_no_symbol',
            )