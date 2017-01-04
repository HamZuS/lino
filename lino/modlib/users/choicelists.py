# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the choicelists for :mod:`lino.modlib.users`.

"""

from __future__ import unicode_literals
from builtins import str

from django.conf import settings

from lino.core.choicelists import ChoiceList, Choice
from lino.core.roles import SiteAdmin

from lino.api import dd, _


class UserType(Choice):
    """Base class for all user profiles.

    .. attribute:: role

        The role of users having this type. This is an instance of
        :class:`<lino.core.roles.UserRole>` or some subclass thereof.

    .. attribute:: readonly

        Whether users of this type get only write-proteced access.

    .. attribute:: hidden_languages

        A subset of :attr:`languages<lino.core.site.Site.languages>`
        which should be hidden for users of this type.  Default value
        is :attr:`hidden_languages<UserTypes.hidden_languages>`.  This
        is used on multilingual sites with more than 4 or 5 languages.

    """

    role = None
    hidden_languages = None
    readonly = False

    # authenticated = True
    # """Whether users with this profile should be considered authenticated."""

    def __init__(self, value, text, role_class,
                 name=None,  # authenticated=True,
                 readonly=False,
                 **kw):
        # if value is None:
        #     value = self.__module__.split('.')[-2] + '.' \
        #         + self.__class__.__name__
        super(UserType, self).__init__(value, text, name)
        self.role = role_class()
        self.readonly = readonly
        self.kw = kw

    def attach(self, cls):
        super(UserType, self).attach(cls)
        self.kw.setdefault('hidden_languages', cls.hidden_languages)

        for k, vf in list(cls.virtual_fields.items()):
            if vf.has_default():
                self.kw.setdefault(k, vf.get_default())
            elif vf.return_type.blank:
                self.kw.setdefault(k, None)

        for k, v in list(self.kw.items()):
            setattr(self, k, v)

        if self.hidden_languages is not None:
            self.hidden_languages = set(
                settings.SITE.resolve_languages(self.hidden_languages))

        del self.kw

    def __repr__(self):
        #~ s = self.__class__.__name__
        s = str(self.choicelist)
        if self.name:
            s += "." + self.name
        s += ":" + self.value
        return s

    def has_required_roles(self, required_roles):
        """Return `True` if this user profile's :attr:`role` satisfies the
        specified requirements.  See
        :meth:`lino.core.roles.UserRole.has_required_roles`.

        """
        return self.role.has_required_roles(required_roles)
        # try:
        #     return self.role.has_required_roles(required_roles)
        # except TypeError:
        #     raise Exception("Invalid roles specified: {0}".format(
        #         required_roles))


##


class UserTypes(ChoiceList):
    """The list of user profiles available on this site.
    
    You can see the user profiles available in your application via
    :menuselection:`Explorer --> System --> User Profiles`.

    Every site should define at least three named user types:

    .. attribute:: anonymous

    .. attribute:: user

    .. attribute:: admin

    """
    required_roles = dd.login_required(SiteAdmin)
    item_class = UserType
    verbose_name = _("User type")
    verbose_name_plural = _("User types")
    show_values = True
    max_length = 20
    # column_names = "value name text readonly"

    preferred_foreignkey_width = 20

    # readonly = models.BooleanField(_("Read-only"), default=False)
    
    hidden_languages = settings.SITE.hidden_languages
    """Default value for the
    :attr:`hidden_languages<UserType.hidden_languages>` of newly
    attached choice item.

    """

# add = UserTypes.add_item
# add('000', _("Anonymous"), UserRole, 'anonymous', readonly=True)
# add('100', _("User"), SiteUser, 'user')
# add('900', _("Administrator"), SiteAdmin, 'admin')



