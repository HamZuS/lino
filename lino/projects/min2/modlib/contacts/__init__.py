# Copyright 2014-2015 Luc Saffre
# License: BSD, see LICENSE for more details.

"""
An extension of :mod:`lino.modlib.contacts`
"""

from lino.modlib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']
