import threading
from rest_framework import serializers
from django.core.exceptions import ValidationError
import magic
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.mail import EmailMessage
from .constants import FACULTY_DOMAINS, STUDENT_DOMAINS
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def institute_email_validator(value):
    email = value.lower()
    if not email.endswith('.nitdgp.ac.in'):
        raise ValidationError('Please use Institute email only.')
    domain = email.split('@')[1].lower()
    parts = domain.split('.')
    if len(parts) != 4:
        raise ValidationError('Not a valid Institute email ID.')
    sub_domain = parts[0]
    if (sub_domain not in FACULTY_DOMAINS) and (sub_domain not in STUDENT_DOMAINS):
        raise ValidationError('Institute email not valid. If you feel it is right, please contact the administrator.')
    return email


def get_group_name(email):
    try:
        domain = email.split('@')[1].lower()
        parts = domain.split('.')
        if len(parts) != 4:
            raise Exception('Email ID not valid')
    except IndexError:
        return 'teacher'

    if parts[0] in STUDENT_DOMAINS:
        return 'student'
    return 'teacher'


class LowerEmailField(serializers.EmailField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).lower()
        return value.strip() if self.trim_whitespace else value


@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': ("Ensure this file size is not greater than %(max_size)s."
                     " Your file size is %(size)s."),
        'min_size': ("Ensure this file size is not less than %(min_size)s. "
                     "Your file size is %(size)s."),
        'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=1024 * 10, min_size=1024, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                  'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)

    def __eq__(self, other):
        return (
                isinstance(other, FileValidator) and
                self.max_size == other.max_size and
                self.min_size == other.min_size and
                self.content_types == other.content_types
        )


class ThreadedMailing(threading.Thread):
    def __init__(self, email: EmailMessage, fail_silently=True):
        self.email_msg = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        self.email_msg.send(fail_silently=self.fail_silently)


def sendVerificationEmail(domain, user, *args, **kwargs):
    if domain is None or user is None:
        raise ValidationError('Domain/User instance not provided')
    mail_subject = 'Activate your IEEE Research Portal account.'
    message = render_to_string('usr_val/acc_active_email.html', {
        'first_name': user.first_name,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(
        mail_subject,
        message,
        to=[to_email, ]
    )
    threaded_mail = ThreadedMailing(mail)
    threaded_mail.start()
    return message
