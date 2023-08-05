#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Backend for the create_edxapp_user that works under the open-release/juniper.master tag
"""
# pylint: disable=import-error
from __future__ import absolute_import, unicode_literals

import logging

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.user_api.accounts import USERNAME_MAX_LENGTH  # pylint: disable=unused-import
from openedx.core.djangoapps.user_api.accounts.serializers import UserReadOnlySerializer
from openedx.core.djangoapps.user_api.accounts.views import _set_unusable_password  # pylint: disable=unused-import
from openedx.core.djangoapps.user_api.models import UserRetirementStatus
from openedx.core.djangoapps.user_api.preferences import api as preferences_api
from openedx.core.djangoapps.user_authn.utils import generate_password  # pylint: disable=unused-import
from openedx.core.djangoapps.user_authn.views.registration_form import AccountCreationForm
from openedx.core.djangolib.oauth2_retirement_utils import retire_dot_oauth2_models  # pylint: disable=unused-import
from rest_framework import status
from rest_framework.exceptions import NotFound
from social_django.models import UserSocialAuth
from student.helpers import create_or_set_user_attribute_created_on_site, do_create_account
from student.models import (
    CourseEnrollment,
    LoginFailures,
    Registration,
    UserAttribute,
    UserProfile,
    UserSignupSource,
    create_comments_service_user,
    email_exists_or_retired,
    get_retired_email_by_email,
    username_exists_or_retired,
)

# pylint: disable=ungrouped-imports
try:
    from openedx.core.lib.triggers.v1 import post_register
except ImportError:
    # In case edx-platform -vanilla- Juniper release is used
    from openedx.core.djangoapps.user_authn.views.register import REGISTER_USER as post_register


LOG = logging.getLogger(__name__)
User = get_user_model()  # pylint: disable=invalid-name


def get_user_read_only_serializer():
    """
    Great serializer that fits our needs
    """
    return UserReadOnlySerializer


def check_edxapp_account_conflicts(email, username):
    """
    Exposed function to check conflicts
    """
    conflicts = []

    if username and username_exists_or_retired(username):
        conflicts.append("username")

    if email and email_exists_or_retired(email):
        conflicts.append("email")

    return conflicts


class EdnxAccountCreationForm(AccountCreationForm):
    """
    A form to extend the behaviour of the AccountCreationForm.
    For now the purpose of this form is to allow to make the
    password optional if the flag 'skip_password' is True.

    This form it's currently only used for validation, not rendering.
    """

    def __init__(  # pylint:disable=too-many-arguments
            self,
            data=None,
            extra_fields=None,
            extended_profile_fields=None,
            do_third_party_auth=True,
            tos_required=True,
    ):
        super().__init__(
            data=data,
            extra_fields=extra_fields,
            extended_profile_fields=extended_profile_fields,
            do_third_party_auth=do_third_party_auth,
            tos_required=tos_required,
        )

        if data.pop("skip_password", False):
            self.fields['password'] = forms.CharField(required=False)


def create_edxapp_user(*args, **kwargs):
    """
    Creates a user on the open edx django site using calls to
    functions defined in the edx-platform codebase

    Example call:

    data = {
        'email': "address@example.org",
        'username': "Username",
        'password': "P4ssW0rd",
        'fullname': "Full Name",
        'activate': True,
        'site': request.site,
        'language_preference': 'es-419',
    }
    user = create_edxapp_user(**data)

    """
    errors = []

    extra_fields = getattr(settings, "REGISTRATION_EXTRA_FIELDS", {})
    extended_profile_fields = getattr(settings, "extended_profile_fields", [])
    kwargs["name"] = kwargs.pop("fullname", None)
    email = kwargs.get("email")
    username = kwargs.get("username")
    conflicts = check_edxapp_account_conflicts(email=email, username=username)
    if conflicts:
        return None, ["Fatal: account collition with the provided: {}".format(", ".join(conflicts))]

    # Go ahead and create the new user
    with transaction.atomic():
        # In theory is possible to extend the registration form with a custom app
        # An example form app for this can be found at http://github.com/open-craft/custom-form-app
        # form = get_registration_extension_form(data=params)
        # if not form:
        form = EdnxAccountCreationForm(
            data=kwargs,
            tos_required=False,
            extra_fields=extra_fields,
            extended_profile_fields=extended_profile_fields,
            # enforce_password_policy=enforce_password_policy,
        )
        (user, profile, registration) = do_create_account(form)  # pylint: disable=unused-variable

    site = kwargs.pop("site", False)
    if site:
        create_or_set_user_attribute_created_on_site(user, site)
    else:
        errors.append("The user was not assigned to any site")

    try:
        create_comments_service_user(user)
    except Exception:  # pylint: disable=broad-except
        errors.append("No comments_service_user was created")

    # TODO: link account with third party auth

    # Announce registration through API call
    post_register.send_robust(sender=None, user=user)  # pylint: disable=no-member

    lang_pref = kwargs.pop("language_preference", False)
    if lang_pref:
        try:
            preferences_api.set_user_preference(user, LANGUAGE_KEY, lang_pref)
        except Exception:  # pylint: disable=broad-except
            errors.append("Could not set lang preference '{} for user '{}'".format(
                lang_pref,
                user.username,
            ))

    if kwargs.pop("activate_user", False):
        user.is_active = True
        user.save()

    # TODO: run conditional email sequence

    return user, errors


def get_edxapp_user(**kwargs):
    """
    Retrieve a user by username and/or email

    The user will be returned only if it belongs to the calling site

    Examples:
        >>> get_edxapp_user(
            {
                "username": "Bob",
                "site": request.site
            }
        )
        >>> get_edxapp_user(
            {
                "email": "Bob@mailserver.com",
                "site": request.site
            }
        )
    """
    params = {key: kwargs.get(key) for key in ['username', 'email'] if key in kwargs}
    site = kwargs.get('site')
    try:
        domain = site.domain
    except AttributeError:
        domain = None

    try:
        user = User.objects.get(**params)
        for source_method in FetchUserSiteSources.get_enabled_source_methods():
            if source_method(user, domain):
                break
        else:
            raise User.DoesNotExist
    except User.DoesNotExist:
        raise NotFound('No user found by {query} on site {site}.'.format(query=str(params), site=domain))
    return user


def delete_edxapp_user(*args, **kwargs):
    """
    Deletes a user from the platform.
    """
    msg = None

    user = kwargs.get("user")
    case_id = kwargs.get("case_id")
    site = kwargs.get("site")
    is_support_user = kwargs.get("is_support_user")

    user_response = "The user {username} <{email}> ".format(username=user.username, email=user.email)

    signup_sources = user.usersignupsource_set.all()
    sources = [signup_source.site for signup_source in signup_sources]

    if site and site.name.upper() in (source.upper() for source in sources):
        if len(sources) == 1:
            with transaction.atomic():
                support_label = "_support" if is_support_user else ""
                user.email = "{email}{case}.ednx{support}_retired".format(
                    email=user.email,
                    case=case_id,
                    support=support_label,
                )
                user.save()

                # Add user to retirement queue.
                UserRetirementStatus.create_retirement(user)

                # Unlink LMS social auth accounts
                UserSocialAuth.objects.filter(user_id=user.id).delete()

                # Change LMS password & email
                user.email = get_retired_email_by_email(user.email)
                user.save()
                _set_unusable_password(user)

                # Remove the activation keys sent by email to the user for account activation.
                Registration.objects.filter(user=user).delete()

                # Delete OAuth tokens associated with the user.
                retire_dot_oauth2_models(user)

                # Delete user signup source object
                signup_sources[0].delete()

                msg = "{user} has been removed".format(user=user_response)
        else:
            for signup_source in signup_sources:
                if signup_source.site.upper() == site.name.upper():
                    signup_source.delete()

                    msg = "{user} has more than one signup source. The signup source from the site {site} has been deleted".format(
                        user=user_response,
                        site=site,
                    )

        return msg, status.HTTP_200_OK

    raise NotFound("{user} does not have a signup source on the site {site}".format(user=user_response, site=site))


def get_course_team_user(*args, **kwargs):
    """
    Get _course_team_user function.
    We need to check if the SERVICE_VARIANT is equal to cms, since
    contentstore is a module registered in the INSTALLED_APPS
    of the cms only.
    """
    if settings.SERVICE_VARIANT == 'cms':
        from contentstore.views.user import _course_team_user  # pylint: disable=import-error,import-outside-toplevel
        return _course_team_user(*args, **kwargs)
    return None


class FetchUserSiteSources:
    """
    Methods to make the comparison to check if an user belongs to a site plus the
    get_enabled_source_methods that just brings an array of functions enabled to do so
    """

    @classmethod
    def get_enabled_source_methods(cls):
        """ Brings the array of methods to check if an user belongs to a site. """
        sources = configuration_helpers.get_value(
            'EOX_CORE_USER_ORIGIN_SITE_SOURCES',
            getattr(settings, 'EOX_CORE_USER_ORIGIN_SITE_SOURCES')
        )
        return [getattr(cls, source) for source in sources]

    @staticmethod
    def fetch_from_created_on_site_prop(user, domain):
        """ Fetch option. """
        if not domain:
            return False
        return UserAttribute.get_user_attribute(user, 'created_on_site') == domain

    @staticmethod
    def fetch_from_user_signup_source(user, domain):
        """ Read the signup source. """
        return len(UserSignupSource.objects.filter(user=user, site=domain)) > 0

    @staticmethod
    def fetch_from_unfiltered_table(user, site):
        """ Fetch option that does not take into account the multi-tentancy model of the installation. """
        return bool(user)


def get_course_enrollment():
    """ get CourseEnrollment model """
    return CourseEnrollment


def get_user_signup_source():
    """ get UserSignupSource model """
    return UserSignupSource


def get_login_failures():
    """ get LoginFailures model """
    return LoginFailures


def get_user_profile():
    """ Gets the UserProfile model """

    return UserProfile


def get_user_attribute():
    """ Gets the UserAttribute model """
    return UserAttribute
