# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This started as a copy of :mod:`lino.modlib.plain` and moved to the
version 3 of `Bootstrap <http://twitter.github.com/bootstrap>`_ CSS
toolkit.

.. autosummary::
   :toctree:

    views
    renderer
    models


"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    # ui_label = _("Bootstrap")
    ui_handle_attr_name = 'openui5_handle'

    # site_js_snippets = ['snippets/plain.js']

    needs_plugins = ['lino.modlib.jinja']

    url_prefix = 'ui5'

    media_name = 'openui5'
    # media_root = None
    # media_base_url = "http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/"

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer

    def get_patterns(self):
        from django.conf.urls import url
        from . import views

        rx = '^'

        urls = [
            # url(rx + r'/?$', views.Index.as_view()),

            ## original views from bs3 commented out
            # url(rx + r'$', views.Index.as_view()),
            url(rx + r'auth$', views.Authenticate.as_view()),
            # url(rx + r'(?P<app_label>\w+)/(?P<actor>\w+)$',
            #     views.List.as_view()),
            # url(rx + r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
            #     views.Element.as_view()),
            url(rx + r'api/main_html$', views.MainHtml.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.Restful.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.Restful.as_view()),

            url(rx + r'ui/(?P<name>.*)$',
                views.Connector.as_view()),

            url(rx + r'$', views.Tickets.as_view()),

        ]
        return urls

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("Openui5", '1.50.8', "http://openui5.org")
            # yield ("jQuery", '?', "http://...")

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

