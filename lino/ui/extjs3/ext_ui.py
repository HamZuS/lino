# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import time
#import traceback
import cPickle as pickle
from urllib import urlencode
import codecs

#~ import Cheetah
from Cheetah.Template import Template as CheetahTemplate

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, Http404
from django import http
from django.core import exceptions
from django.utils import functional
from django.utils.encoding import force_unicode
#~ from django.utils.functional import Promise

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.utils import translation

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url, include


import lino
from lino.ui.extjs3 import ext_elems
from lino.ui.extjs3 import ext_store
from lino.ui.extjs3 import ext_windows
#~ from . import ext_viewport
#~ from . import ext_requests
from lino.ui import requests as ext_requests

#~ from lino.ui import store as ext_store
from lino import dd
from lino.core import actions #, layouts #, commands
from lino.core import table
from lino.utils import tables
from lino.utils import xhtml as xhg
from lino.core import fields
from lino.ui import base
from lino.core import actors
from lino.tools import makedirs_if_missing
from lino.tools import full_model_name
from lino.utils import dblogger
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import babel
from lino.utils import choicelists
from lino.utils import menus
from lino.utils import jsgen
from lino.utils import isiterable
from lino.utils import codetime
from lino.utils.config import find_config_file
from lino.utils.jsgen import py2js, js_code, id2js

from lino.utils.jscompressor import JSCompressor
if False:
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      
from lino.mixins import printable

from lino.core.coretools import app_labels

from lino.utils.babel import LANGUAGE_CHOICES

from lino.utils.choicelists import DoYouLike, HowWell
STRENGTH_CHOICES = DoYouLike.get_choices()
KNOWLEDGE_CHOICES = HowWell.get_choices()

from lino.tools import resolve_model, obj2str, obj2unicode
#~ from lino.ui.extjs.ext_windows import WindowConfig # 20100316 backwards-compat window_confics.pck 

User = resolve_model(settings.LINO.user_model)

def is_devserver():
    """
    Returns True if we are running a development server.
    
    Thanks to Aryeh Leib Taurog in 
    `How can I tell whether my Django application is running on development server or not?
    <http://stackoverflow.com/questions/1291755>`_
    
    Added the `len(sys.argv) > 1` test because under 
    mod_wsgi the process is called without arguments.
    """
    return len(sys.argv) > 1 and sys.argv[1] == 'runserver'
    


class HttpResponseDeleted(HttpResponse):
    status_code = 204
    
def prepare_label(mi):
    return mi.label
    """
    The original idea doesn't work any more with lazy translation.
    See :doc:`/blog/2011/1112`
    """
    #~ label = unicode(mi.label) # trigger translation
    #~ n = label.find(mi.HOTKEY_MARKER)
    #~ if n != -1:
        #~ label = label.replace(mi.HOTKEY_MARKER,'')
        #~ #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    #~ return label
    
        
#~ def element_name(elem):
    #~ return u"%s (#%s in %s.%s)" % (elem,elem.pk,elem._meta.app_label,elem.__class__.__name__)


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

def json_response_kw(msg=None,**kw):
    if msg:
        kw.update(message=msg)
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #~ logger.debug("json_response() -> %r", s)
    # http://dev.sencha.com/deploy/dev/docs/source/BasicForm.html#cfg-Ext.form.BasicForm-fileUpload
    return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='text/json')
    #~ r = HttpResponse(s, content_type='application/json')
    # see also http://stackoverflow.com/questions/477816/the-right-json-content-type
    #~ return r
    #~ return HttpResponse(s, mimetype='text/html')
    
def error_response(e=None,message=None,**kw):
    kw.update(success=False)
    if e is not None:
        if hasattr(e,'message_dict'):
            kw.update(errors=e.message_dict)
    #~ kw.update(alert_msg=cgi.escape(message_prefix+unicode(e)))
    kw.update(alert=True)
    kw.update(message=message)
    if message is None:
        message = unicode(e)
    kw.update(message=cgi.escape(message))
    #~ kw.update(message=message_prefix+unicode(e))
    dblogger.debug('error_response %s',kw)
    return json_response(kw)
    

def elem2rec1(ar,rh,elem,**rec):
    rec.update(data=rh.store.row2dict(ar,elem))
    return rec

#~ def elem2rec_empty(ar,ah,**rec):
    #~ rec.update(data=dict())
    #~ rec.update(title='Empty detail')
    #~ return rec
    
def elem2rec_insert(ar,ah,elem):
    """
    Returns a dict of this record, designed for usage by an InsertWindow.
    """
    rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(phantom=True)
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_empty(ar,ah,elem,**rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    #~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    #~ rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_detailed(ar,rh,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relativ to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See :doc:`/blog/2010/0716`,
    :doc:`/blog/2010/0721`,
    :doc:`/blog/2010/1116`,
    :doc:`/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rec = elem2rec1(ar,rh,elem,**rec)
    rec.update(title=ar.get_title() + u" » " + unicode(elem))
    #~ rec.update(title=rh.report.model._meta.verbose_name + u"«%s»" % unicode(elem))
    #~ rec.update(title=unicode(elem))
    rec.update(id=elem.pk)
    #~ if rh.report.disable_delete:
    rec.update(disabled_actions=rh.report.disabled_actions(elem,ar.request))
    rec.update(disable_delete=rh.report.disable_delete(elem,ar.request))
    if rh.report.show_detail_navigator:
        first = None
        prev = None
        next = None
        last = None
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
        recno = 0
        if len(ar.data_iterator) > 0:
            if True:
                # this algorithm is clearly quicker on reports with a few thousand Persons
                id_list = list(ar.data_iterator.values_list('pk',flat=True))
                """
                Uncommented the following assert because it failed in certain circumstances 
                (see :doc:`/blog/2011/1220`)
                """
                #~ assert len(id_list) == ar.total_count, \
                    #~ "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
                #~ print 20111220, id_list
                first = id_list[0]
                last = id_list[-1]
                try:
                    i = id_list.index(elem.pk)
                except ValueError:
                    pass
                else:
                    recno = i + 1
                    if i > 0:
                        #~ prev = ar.queryset[i-1]
                        prev = id_list[i-1]
                    if i < len(ar.data_iterator) - 1:
                        #~ next = ar.queryset[i+1]
                        next = id_list[i+1]
            else:
                first = ar.queryset[0]
                last = ar.queryset.reverse()[0]
                if len(ar.data_iterator) > 200:
                    #~ TODO: check performance
                    pass
                g = enumerate(ar.queryset) # a generator
                try:
                    while True:
                        index, item = g.next()
                        if item == elem:
                            if index > 0:
                                prev = ar.queryset[index-1]
                            recno = index + 1
                            index,next = g.next()
                            break
                except StopIteration:
                    pass
                if first is not None: first = first.pk
                if last is not None: last = last.pk
                if prev is not None: prev = prev.pk
                if next is not None: next = next.pk
        rec.update(navinfo=dict(
            first=first,prev=prev,next=next,last=last,recno=recno,
            message=_("Row %(rowid)d of %(rowcount)d") % dict(rowid=recno,rowcount=len(ar.data_iterator))))
    return rec
            
    
#~ class ViewReportRequest(table.ReportActionRequest):
    
    #~ sort_column = None
    #~ sort_direction = None
    
    #~ def __init__(self,request,rh,action,*args,**kw):
        #~ table.ReportActionRequest.__init__(self,rh.ui,rh.report,action)
        #~ self.ah = rh
        #~ self.request = request
        #~ self.store = rh.store
        #~ if request is None:
            #~ self.user = None
        #~ else:
            #~ kw = self.parse_req(request,rh,**kw)
        #~ self.setup(*args,**kw)
        
        
    #~ def get_user(self):
        #~ return self.user

    #~ def row2list(self,row):
        #~ return self.store.row2list(self,row)
      
    #~ def row2dict(self,row):
        #~ return self.store.row2dict(self,row)
 


class ExtUI(base.UI):
    """The central instance of Lino's ExtJS3 User Interface.
    """
    #~ _response = None
    name = 'extjs3'
    verbose_name = "ExtJS with Windows"
    Panel = ext_elems.Panel
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    def __init__(self,*args,**kw):
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
        jsgen.register_converter(self.py2js_converter)
        #~ self.window_configs = {}
        #~ if os.path.exists(self.window_configs_file):
            #~ logger.info("Loading %s...",self.window_configs_file)
            #~ wc = pickle.load(open(self.window_configs_file,"rU"))
            #~ #logger.debug("  -> %r",wc)
            #~ if type(wc) is dict:
                #~ self.window_configs = wc
        #~ else:
            #~ logger.warning("window_configs_file %s not found",self.window_configs_file)
            
        base.UI.__init__(self,*args,**kw) # will create a.window_wrapper for all actions
        
        #~ self.welcome_template = get_template('welcome.html')
        
        #~ from django.template.loader import find_template
        #~ source, origin = find_template('welcome.html')
        #~ print source, origin
        
        fn = find_config_file('welcome.html')
        logger.info("Using welcome template %s",fn)
        self.welcome_template = CheetahTemplate(file(fn).read())
        self.build_lino_js()
        #~ self.generate_linolib_messages()
        
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        try:
            de = lh.get_data_elem(name)
        except Exception, e:
            de = None
            name += " (" + str(e) + ")"
            
        if isinstance(de,table.RemoteField):
            dummy = ext_elems.field2elem(lh,de.field,**kw)
            dummy.editable = False
            #~ dummy = self.create_field_element(lh,de.field,**kw)
            lh.add_store_field(de)
            return dummy
            #~ kw.setdefault('preferred_width',dummy.preferred_width)
            #~ kw.setdefault('height',dummy.height)
            #~ kw.setdefault('width',dummy.width)
            #~ kw.setdefault('label',dummy.label)
            #~ # logger.info("%s : %s", name,kw)
            #~ return ext_elems.DisplayElement(lh,de,**kw)
            
            
        #~ if isinstance(de,table.ComputedColumn):
            #~ lh.add_store_field(de)
            #~ kw.setdefault('width',de.width)
            #~ return ext_elems.DisplayElement(lh,de,**kw)
            
        if isinstance(de,fields.FieldSet):
            return lh.desc2elem(ext_elems.FieldSetPanel,name,de.desc)
            
        if isinstance(de,models.Field):
            if isinstance(de,(babel.BabelCharField,babel.BabelTextField)):
                if len(babel.BABEL_LANGS) > 0:
                    elems = [ self.create_field_element(lh,de,**kw) ]
                    for lang in babel.BABEL_LANGS:
                        bf = lh.get_data_elem(name+'_'+lang)
                        elems.append(self.create_field_element(lh,bf,**kw))
                    return elems
            return self.create_field_element(lh,de,**kw)
            
        if isinstance(de,fields.LinkedForeignKey):
            de.primary_key = False # for ext_store.Store()
            lh.add_store_field(de)
            return ext_elems.LinkedForeignKeyElement(lh,de,**kw)
            
        if isinstance(de,generic.GenericForeignKey):
            # create a horizontal panel with 2 comboboxes
            #~ print 20111123, name,de.ct_field + ' ' + de.fk_field
            #~ return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
            #~ return ext_elems.GenericForeignKeyField(lh,name,de,**kw)
            de.primary_key = False # for ext_store.Store()
            lh.add_store_field(de)
            return ext_elems.GenericForeignKeyElement(lh,de,**kw)
            
        if isinstance(de,type) and issubclass(de,dd.Table):
            kw.update(master_panel=js_code("this"))
            if isinstance(lh.layout,table.DetailLayout):
                # a Report in a DetailWindow
                kw.update(tools=[
                  js_code("Lino.report_window_button(Lino.%s)" % de.default_action)
                  #~ js_code("Lino.report_window_button(ww,Lino.%s)" % de.default_action)
                ])
                if de.show_slave_grid:
                    e = ext_elems.GridElement(lh,name,de,**kw)
                    return e
                else:
                    # a Table in a DetailWindow, displayed as a summary in a HtmlBox 
                    o = dict(drop_zone="FooBar")
                    a = de.get_action('insert')
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a))
                        kw.update(ls_bbar_actions=[
                          self.a2btn(a),
                          ])
                    field = fields.HtmlBox(verbose_name=de.label,**o)
                    field.name = de.__name__
                    field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    return e
            else:
                #~ field = fields.TextField(verbose_name=de.label)
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de.__name__
                field._return_type_for_method = de.slave_as_summary_meth(self,', ')
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                return e
                
        if isinstance(de,fields.VirtualField):
            return self.create_vurt_element(lh,name,de,**kw)
            
        if callable(de):
            rt = getattr(de,'return_type',None)
            if rt is not None:
                return self.create_meth_element(lh,name,de,rt,**kw)
                
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,table.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                raise KeyError(
                  "Cannot handle value %r in %s.%s." 
                  % (value,lh.layout.__name__,name))
        if hasattr(lh,'rh'):
            msg = "Unknown element %r referred in layout %s of %s." % (
                name,lh.layout,lh.rh.report)
            l = [de.name for de in lh.rh.report.wildcard_data_elems()]
            model = getattr(lh.rh.report,'model',None) # CustomTables don't have a model
            if getattr(model,'_lino_slaves',None):
                l += [str(rpt) for rpt in model._lino_slaves.values()]
            msg += " Possible names are %s." % ', '.join(l)
        else:
            msg = "Unknown element %r referred in layout %s." % (
                name,lh.layout)
        raise KeyError(msg)
        

    def create_vurt_element(self,lh,name,vf,**kw):
        #~ assert vf.get.func_code.co_argcount == 2, (name, vf.get.func_code.co_varnames)
        e = self.create_field_element(lh,vf,**kw)
        if not vf.is_enabled(lh):
            e.editable = False
        return e
        
    def create_meth_element(self,lh,name,meth,rt,**kw):
        #~ if hasattr(rt,'_return_type_for_method'):
            #~ raise Exception(
              #~ "%s.%s : %r has already an attribute '_return_type_for_method'" % (
                #~ lh,name,rt))
        rt.name = name
        rt._return_type_for_method = meth
        if meth.func_code.co_argcount < 2:
            raise Exception("Method %s has %d arguments (must have at least 2)" % (meth,meth.func_code.co_argcount))
            #~ , (name, meth.func_code.co_varnames)
        #~ kw.update(editable=False)
        e = self.create_field_element(lh,rt,**kw)
        #~ if lh.rh.report.actor_id == 'contacts.Persons':
            #~ print 'ext_ui.py create_meth_element',name,'-->',e
        #~ if name == 'preview':
            #~ print 20110714, 'ext_ui.create_meth_element', meth, repr(e)
        return e
        #~ e = lh.main_class.field2elem(lh,return_type,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
            
        #~ if rt is None:
            #~ rt = models.TextField()
            
        #~ e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
          
    def create_field_element(self,lh,field,**kw):
        #~ e = lh.main_class.field2elem(lh,field,**kw)
        e = ext_elems.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh.add_store_field(e.field)
        return e
        #return FieldElement(self,field,**kw)
        

    def main_panel_class(self,layout):
        if isinstance(layout,table.ListLayout) : 
            return ext_elems.GridMainPanel
        if isinstance(layout,table.DetailLayout) : 
            return ext_elems.DetailMainPanel
        if isinstance(layout,table.ParamsLayout) : 
            return ext_elems.ParameterPanel
        raise Exception("No element class for layout %r" % layout)

    
    #~ def save_window_config(self,a,wc):
        #~ self.window_configs[str(a)] = wc
        #~ #a.window_wrapper.config.update(wc=wc)
        #~ a.window_wrapper.update_config(wc)
        #~ f = open(self.window_configs_file,'wb')
        #~ pickle.dump(self.window_configs,f)
        #~ f.close()
        #~ logger.debug("save_window_config(%r) -> %s",wc,a)
        #~ self.build_lino_js()
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    #~ def load_window_config(self,action,**kw):
        #~ wc = self.window_configs.get(str(action),None)
        #~ if wc is not None:
            #~ logger.debug("load_window_config(%r) -> %s",str(action),wc)
            #~ for n in ('x','y','width','height'):
                #~ if wc.get(n,0) is None:
                    #~ del wc[n]
                    #~ #raise Exception('invalid window configuration %r' % wc)
            #~ kw.update(**wc)
        #~ return kw

  
    def get_urls(self):
        #~ urlpatterns = patterns('',
            #~ (r'^$', self.index_view))
        rx = '^'
        urlpatterns = patterns('',
            (rx+'$', self.index_view),
            #~ (rx+r'grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', self.json_report_view),
            (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.grid_config_view),
            (rx+r'detail_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.detail_config_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.api_element_view),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$', self.restful_view),
            (rx+r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.restful_view),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)$', self.choices_view),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', self.choices_view),
        )
        if settings.LINO.use_tinymce:
            urlpatterns += patterns('',
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$', 
                    self.templates_view),
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/(?P<tplname>\w+)$', 
                    self.templates_view),
            )
            
        

        if is_devserver():
          
            from os.path import exists, join, abspath, dirname
          
            logger.info("Running on a development server: install /media URLs ")
            
            def must_exist(s):
                p = getattr(settings.LINO,s)
                if not p:
                    raise Exception("LINO.%s is not set." % s)
                if not exists(p):
                    raise Exception("LINO.%s (%s) does not exist" % (s,p))
                    
            if not exists(join(settings.MEDIA_ROOT,'extjs')):
                #~ if settings.LINO.extjs_root:
                must_exist('extjs_root')
                    
                prefix = settings.MEDIA_URL[1:]
                assert prefix.endswith('/')
                
                urlpatterns += patterns('django.views.static',
                (r'^%sextjs/(?P<path>.*)$' % prefix, 
                    'serve', {
                    'document_root': settings.LINO.extjs_root,
                    'show_indexes': True }))
                    
            if settings.LINO.use_extensible:
                if not exists(join(settings.MEDIA_ROOT,'extensible')):
                    must_exist('extensible_root')
                    urlpatterns += patterns('django.views.static',
                        (r'^%sextensible/(?P<path>.*)$' % prefix, 
                            'serve', {
                            'document_root': settings.LINO.extensible_root,
                            'show_indexes': True }))
                
            if settings.LINO.use_tinymce:
                if not exists(join(settings.MEDIA_ROOT,'tinymce')):
                    #~ if settings.LINO.tinymce_root:
                    must_exist('tinymce_root')
                    urlpatterns += patterns('django.views.static',
                        (r'^%stinymce/(?P<path>.*)$' % prefix, 
                            'serve', {
                            'document_root': settings.LINO.tinymce_root,
                            'show_indexes': True }))
                
            if not exists(join(settings.MEDIA_ROOT,'lino')):
                lino_media = abspath(join(dirname(lino.__file__),'..','media'))
                
                urlpatterns += patterns('django.views.static',
                    (r'^%slino/(?P<path>.*)$' % prefix, 
                        'serve', {
                        'document_root': lino_media,
                        'show_indexes': True }))

            urlpatterns += patterns('django.views.static',
                (r'^%s(?P<path>.*)$' % prefix, 'serve', 
                  { 'document_root': settings.MEDIA_ROOT, 
                    'show_indexes': True }),
            )

        #~ print '\n'.join([repr(i) for i in urlpatterns])
        return urlpatterns

    def html_page(self,*args,**kw):
        return '\n'.join([ln for ln in self.html_lines(*args,**kw)])
        
    def html_lines(self,request,on_ready=[],**kw):
        """Generates the lines of Lino's HTML reponse.
        """
        
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        #~ title = kw.get('title',None)
        #~ if title:
        yield '<title id="title">%s</title>' % settings.LINO.title
        #~ yield '<!-- ** CSS ** -->'
        #~ yield '<!-- base library -->'
        
        def stylesheet(url):
            url = self.media_url() + url
            return '<link rel="stylesheet" type="text/css" href="%s" />' % url
            
        #~ yield '<link rel="stylesheet" type="text/css" href="%s/extjs/resources/css/ext-all.css" />' % self.media_url()
        yield stylesheet('/extjs/resources/css/ext-all.css')
        #~ yield '<!-- overrides to base library -->'
        if settings.LINO.use_extensible:
            yield stylesheet("/extensible/resources/css/extensible-all.css")
          
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/'
            yield '<link rel="stylesheet" type="text/css" href="%sresources/css/htmleditorplugins.css" />' % p
          
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<link rel="stylesheet" type="text/css" href="%s/filterRow.css" />' % p
            
        if settings.LINO.use_gridfilters:
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/statusbar/css/statusbar.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/GridFilters.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/RangeMenu.css" />' % self.media_url() 
            
        yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % self.media_url() 
        
        yield '<link rel="stylesheet" type="text/css" href="%s/lino/extjs/lino.css">' % self.media_url()
        
        if settings.LINO.use_awesome_uploader:
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader.css">' % self.media_url()
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader Progress Bar.css">' % self.media_url()
         
        #~ yield '<!-- ** Javascript ** -->'
        #~ yield '<!-- ExtJS library: base/adapter -->'
        def javascript(url):
            url = self.media_url() + url
            return '<script type="text/javascript" src="%s"></script>' % url
            
        if settings.DEBUG:
            yield javascript('/extjs/adapter/ext/ext-base-debug.js')
            yield javascript('/extjs/ext-all-debug.js')
            if settings.LINO.use_extensible:
                yield javascript('/extensible/extensible-all-debug.js')
        else:
            yield javascript('/extjs/adapter/ext/ext-base.js')
            yield javascript('/extjs/ext-all.js')
            #~ yield '<script type="text/javascript" src="%s/extjs/adapter/ext/ext-base.js"></script>' % self.media_url() 
            #~ yield '<script type="text/javascript" src="%s/extjs/ext-all.js"></script>' % self.media_url()
            
            if settings.LINO.use_extensible:
                yield javascript('/extensible/extensible-all.js')
        if translation.get_language() != 'en':
            yield javascript('/extjs/src/locale/ext-lang-'+translation.get_language()+'.js')
            if settings.LINO.use_extensible:
                yield javascript('/extensible/src/locale/extensible-lang-'+translation.get_language()+'.js')
            
        #~ yield '<!-- ExtJS library: all widgets -->'
        #~ if True:
            #~ yield '<style type="text/css">'
            #~ # http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js 
            #~ yield '.x-grid3-cell-inner, .x-grid3-hd-inner {'
            #~ yield '  white-space: normal;' # /* changed from nowrap */
            #~ yield '}'
            #~ yield '</style>'
        if False:
            yield '<script type="text/javascript" src="%s/extjs/Exporter-all.js"></script>' % self.media_url() 
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/CheckColumn.js"></script>' % self.media_url() 

        yield '<script type="text/javascript" src="%s/extjs/examples/ux/statusbar/StatusBar.js"></script>' % self.media_url()
        
        if settings.LINO.use_tinymce:
            p = self.media_url() + '/tinymce'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/tiny_mce.js"></script>' % p
            yield '<script type="text/javascript" src="%s/lino/tinymce/Ext.ux.TinyMCE.js"></script>' % self.media_url()
            yield '''<script language="javascript" type="text/javascript">
tinymce.init({
        theme : "advanced"
        // , mode : "textareas"
});
</script>'''

        yield '<script type="text/javascript" src="%s/lino/extjs/Ext.ux.form.DateTime.js"></script>' % self.media_url()

        if settings.LINO.use_gridfilters:
            p = self.media_url() + '/extjs/examples/ux/gridfilters'
            #~ yield '<script type="text/javascript" src="%s/extjs/examples/ux/RowEditor.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/menu/RangeMenu.js"></script>' % p
            yield '<script type="text/javascript" src="%s/menu/ListMenu.js"></script>' % p
            yield '<script type="text/javascript" src="%s/GridFilters.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/Filter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/StringFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/DateFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/ListFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/NumericFilter.js"></script>' % p
            yield '<script type="text/javascript" src="%s/filter/BooleanFilter.js"></script>' % p
            
        yield '<script type="text/javascript" src="%s/extjs/examples/ux/fileuploadfield/FileUploadField.js"></script>' % self.media_url()
        
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<script type="text/javascript" src="%s/filterRow.js"></script>' % p
            
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/src/Ext.ux.form.HtmlEditor'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s.MidasCommand.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Divider.js"></script>' % p
            yield '<script type="text/javascript" src="%s.HR.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Image.js"></script>' % p
            yield '<script type="text/javascript" src="%s.RemoveFormat.js"></script>' % p
            yield '<script type="text/javascript" src="%s.IndentOutdent.js"></script>' % p
            yield '<script type="text/javascript" src="%s.SubSuperScript.js"></script>' % p
            yield '<script type="text/javascript" src="%s.FindAndReplace.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Table.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Word.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Link.js"></script>' % p
            yield '<script type="text/javascript" src="%s.SpecialCharacters.js"></script>' % p
            yield '<script type="text/javascript" src="%s.UndoRedo.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Heading.js"></script>' % p
            yield '<script type="text/javascript" src="%s.Plugins.js"></script>' % p
            
        if settings.LINO.use_awesome_uploader:
            p = self.media_url() + '/lino/AwesomeUploader/'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/Ext.ux.XHRUpload.js"></script>' % p
            yield '<script type="text/javascript" src="%s/swfupload.js"></script>' % p
            yield '<!-- <script type="text/javascript" src="%s/swfupload.swfobject.js"></script> -->' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploaderLocalization.js"></script>' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploader.js"></script>' % p

        #~ yield '<!-- overrides to library -->'
        #~ yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % self.media_url()
        yield '<script type="text/javascript" src="%s"></script>' % (
            self.media_url(*self.lino_js_parts()))

        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        #~ yield "console.time('onReady');"
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
          
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          autoScroll=True,
          layout='fit',
          #~ html=self.welcome_template.render(c),
          #~ html=html,
          #~ html=self.site.index_html.encode('ascii','xmlcharrefreplace'),
        )
        
        if not on_ready:
            #~ c = RequestContext(request,dict(site=self.site,lino=lino))
            self.welcome_template.ui = self
            self.welcome_template.request = request
            self.welcome_template.user = request.user
            self.welcome_template.site = settings.LINO # self.site
            self.welcome_template.lino = lino
            #~ main=ext_elems.ExtPanel(
            #~ quicklinks = [dict(text="A")]
            html = unicode(self.welcome_template)
            
            quicklinks = settings.LINO.get_quicklinks(self,request.user)
            if quicklinks.items:
                html = 'Quick Links: ' + ' '.join(
                  [self.action_href_js(mi.action,mi.params) for mi in quicklinks.items]
                  ) + '<br/>' + html
            main.update(html=html)
        
        #~ if quicklinks.items:
            #~ main.update(xtype='panel',tbar=quicklinks)
#~ if not on_ready:
            #~ on_ready = [
              #~ 'new Lino.IndexWrapper({html:%s}).show();' % 
                #~ py2js(self.site.index_html.encode('ascii','xmlcharrefreplace'))]
            #~ main.update(items=dict(layout='fit',html=self.site.index_html.encode('ascii','xmlcharrefreplace')))
        #~ main.update(id='main_area',region='center')
        win = dict(
          layout='fit',
          #~ maximized=True,
          items=main,
          #~ closable=False,
          bbar=dict(xtype='toolbar',items=js_code('Lino.status_bar')),
          #~ title=self.site.title,
          tbar=settings.LINO.get_site_menu(self,request.user),
        )
        
        for ln in jsgen.declare_vars(win):
            yield ln
        yield '  new Ext.Viewport({layout:"fit",items:%s}).render("body");' % py2js(win)
            
        yield '  Ext.QuickTips.init();'
        
        for ln in on_ready:
            yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield '</script></head><body>'
        if settings.LINO.use_davlink:
            yield '<applet name="DavLink" code="davlink.DavLink.class"'
            yield '        archive="%s/lino/applets/DavLink.jar"' % self.media_url()
            yield '        width="1" height="1"></applet>'
            # Note: The value of the ARCHIVE attribute is a URL of a JAR file.
        yield '<div id="body"></div>'
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        #~ yield '<div id="konsole"></div>'
        yield "</body></html>"
        
    def lino_js_lines(self):
        yield """// lino.js --- generated %s by Lino version %s.""" % (time.ctime(),lino.__version__)
        yield "Ext.BLANK_IMAGE_URL = '%s/extjs/resources/images/default/s.gif';" % self.media_url()
        yield "LANGUAGE_CHOICES = %s;" % py2js(list(LANGUAGE_CHOICES))
        yield "STRENGTH_CHOICES = %s;" % py2js(list(STRENGTH_CHOICES))
        yield "KNOWLEDGE_CHOICES = %s;" % py2js(list(KNOWLEDGE_CHOICES))
        yield "MEDIA_URL = %r;" % (self.media_url())
        #~ yield "ROOT_URL = %r;" % settings.LINO.root_url
        yield "ROOT_URL = %r;" % self.root_url
        #~ yield "API_URL = %r;" % self.build_url('api')
        #~ yield "TEMPLATES_URL = %r;" % self.build_url('templates')
        #~ yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
            

    def index_view(self, request,**kw):
        #~ from lino.lino_site import lino_site
        #~ kw.update(title=lino_site.title)
        #~ mnu = py2js(lino_site.get_site_menu(request.user))
        #~ print mnu
        #~ tbar=ext_elems.Toolbar(items=lino_site.get_site_menu(request.user),region='north',height=29)# renderTo='tbar')
        return HttpResponse(self.html_page(request,**kw))
        #~ html = '\n'.join(self.html_page(request,main,konsole,**kw))
        #~ return HttpResponse(html)


    def unused_menu_view(self,request):
        "used only by lino.modlib.dsbe.tests"
        #~ from lino.lino_site import lino_site
        #~ from lino import lino_site
        return json_response_kw(success=True,
          message=(_("Welcome on Lino server %(title)r, user %(user)s") % dict(
            title=settings.LINO.title,
            user=request.user)),
          load_menu=settings.LINO.get_site_menu(request.user))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def form2obj_and_save(self,request,rh,data,elem,is_new,include_rows=None): # **kw2save):
        """
        """
        #~ logger.info('20111217 form2obj_and_save %r', data)
        #~ print 'form2obj_and_save %r' % data
        
        # store normal form data (POST or PUT)
        try:
            rh.store.form2obj(request,data,elem,is_new)
        except exceptions.ValidationError,e:
            #~ raise
            return error_response(e)
           #~ return error_response(e,_("There was a problem while validating your data : "))
        #~ logger.info('store.form2obj passed')
        
        if not is_new:
            dblogger.log_changes(request,elem)
            
        #~ if hasattr(elem,'before_save'): # see :doc:`/blog/2010/0804`, :doc:`/blog/2011/0226`
            #~ elem.before_save()
            
        #~ logger.info('elem.before_save() passed')
        
        #~ print '20101024a', elem.card_valid_from
        try:
            elem.full_clean()
        except exceptions.ValidationError, e:
        #~ except Exception, e:
            return error_response(e) #,_("There was a problem while validating your data : "))
            #~ return json_response_kw(success=False,msg="Failed to save %s : %s" % (elem,e))
            
        #~ logger.info('elem.full_clean() passed')
        #~ print '20101024b', elem.card_valid_from

        kw2save = {}
        #~ kw2resp = {}
        if is_new:
            kw2save.update(force_insert=True)
            #~ kw2resp.update(close=True)
        else:
            kw2save.update(force_update=True)
            #~ kw2resp.update(refresh=True)
            
        try:
            elem.save(**kw2save)
        except IntegrityError,e:
            #~ print unicode(elem)
            #~ logger.exception(e)
            return error_response(e) # ,_("There was a problem while saving your data : "))
            #~ return json_response_kw(success=False,
                  #~ msg=_("There was a problem while saving your data:\n%s") % e)
        kw = dict()
        kw.update(success=True)
        if is_new:
            dblogger.log_created(request,elem)
            kw.update(
                message=_("%s has been created.") % obj2unicode(elem),
                record_id=elem.pk)
        else:
            kw.update(message=_("%s has been saved.") % obj2unicode(elem))
        if include_rows:
            kw.update(rows=[rh.store.row2dict(include_rows,elem)])
        return json_response(kw)
                
            
        #~ return self.success_response(
            #~ _("%s has been saved.") % obj2unicode(elem),
            #~ rows=[elem])


        
    def detail_config_view(self,request,app_label=None,actor=None):
        #~ rpt = actors.get_actor2(app_label,actor)
        rpt = self.requested_report(request,app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden(msg)
        if request.method == 'GET':
            #~ raise Exception("TODO: convert after 20111127")
            tab = int(request.GET.get('tab','0'))
            return json_response_kw(success=True,tab=tab,desc=rpt.get_detail().layouts[tab]._desc)
        if request.method == 'PUT':
            PUT = http.QueryDict(request.raw_post_data)
            tab = int(PUT.get('tab',0))
            desc = PUT.get('desc',None)
            if desc is None:
                return json_response_kw(success=False,message="desc is mandatory")
            rh = rpt.get_handle(self)
            try:
                rh.update_detail(tab,desc)
            except Exception,e:
                logger.exception(e)
                return json_response_kw(success=False,
                    message=unicode(e),alert=True)
            self.build_lino_js(True)
            return json_response_kw(success=True)
            #detail_layout
      
    def grid_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if request.method == 'PUT':
            if not rpt.can_config.passes(request.user):
                msg = _("User %(user)s cannot configure %(report)s.") % dict(
                    user=request.user,report=rpt)
                return error_response(None,msg)
            #~ return http.HttpResponseForbidden(msg)
            PUT = http.QueryDict(request.raw_post_data)
            gc = dict(
              widths=[int(x) for x in PUT.getlist('widths')],
              columns=[str(x) for x in PUT.getlist('columns')],
              hiddens=[(x == 'true') for x in PUT.getlist('hiddens')],
              #~ hidden_cols=[str(x) for x in PUT.getlist('hidden_cols')],
            )
            
            filter = PUT.get('filter',None)
            if filter is not None:
                filter = json.loads(filter)
                gc['filters'] = [ext_requests.dict2kw(flt) for flt in filter]
            
            name = PUT.get('name',None)
            if name is None:
                name = ext_elems.DEFAULT_GC_NAME                 
            else:
                name = int(name)
                
            gc.update(label=PUT.get('label',"Standard"))
            try:
                msg = rpt.save_grid_config(name,gc)
            except IOError,e:
                msg = _("Error while saving GC for %(report)s: %(error)s") % dict(
                    report=rpt,error=e)
                return error_response(None,msg)
            #~ logger.info(msg)
            self.build_lino_js(True)            
            return self.success_response(msg)
            #~ return json_response_kw(success=True)
            
        raise NotImplementedError
        
        
    def api_list_view(self,request,app_label=None,actor=None):
        """
        - GET : List the members of the collection. 
        - PUT : Replace the entire collection with another collection. 
        - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
          The ID created is included as part of the data returned by this operation. 
        - DELETE : Delete the entire collection.
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = self.requested_report(request,app_label,actor)
        #~ rpt = actors.get_actor2(app_label,actor)
        #~ if rpt is None:
            #~ raise Http404("No actor named '%s.%s'." % (app_label,actor))
        #~ rh = rpt.get_handle(self)
        #~ ar = self.build_ar(request,rh)
        
        action_name = request.GET.get(
            ext_requests.URL_PARAM_ACTION_NAME,
            rpt.default_list_action_name)
        a = rpt.get_action(action_name)
        if a is None:
            raise Http404("%s has no action %r" % (rpt,action_name))
        if isinstance(a,actions.ReportAction):
            ar = rpt.request(self,request,a)
            #~ ar = table.TableRequest(self,rpt,request,a)
            rh = ar.ah
            assert rh.report == rpt
        else:
            # e.g. calendar
            ar = tables.ActionRequest(self,a)
            rh = rpt.get_handle(self)
        
        if request.method == 'POST':
            #~ data = rh.store.get_from_form(request.POST)
            #~ instance = ar.create_instance(**data)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.list_action)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
            instance = ar.create_instance()
            # store uploaded files. 
            # html forms cannot send files with PUT or GET, only with POST
            if rh.report.handle_uploaded_files is not None:
                rh.report.handle_uploaded_files(instance,request)
            return self.form2obj_and_save(request,rh,request.POST,instance,True)
            
        if request.method == 'GET':
            
            fmt = request.GET.get(
                ext_requests.URL_PARAM_FORMAT,
                ar.action.default_format)
          
            #~ print '20110714', a, fmt
            
            if fmt == 'html':
                kw = {}
                bp = ar.request2kw(self)
                #~ bp = self.request2kw(ar)
                
                params = dict(base_params=bp)
                
                after_show = {}
                if isinstance(ar.action,actions.InsertRow):
                    elem = ar.create_instance()
                    rec = elem2rec_insert(ar,rh,elem)
                    after_show.update(data_record=rec)

                kw.update(on_ready=[self.action_handler(ar.action,None,params,after_show)])
                #~ kw.update(on_ready=['Lino.%s(undefined,%s,%s);' % (
                    #~ ar.action,
                    #~ py2js(params),
                    #~ py2js(after_show))])
                #~ print '20110714 on_ready', params
                return HttpResponse(self.html_page(request,**kw))
            
            if fmt == 'csv':
                #~ response = HttpResponse(mimetype='text/csv')
                charset = settings.LINO.csv_params.get('encoding','utf-8')
                response = HttpResponse(
                  content_type='text/csv;charset="%s"' % charset)
                if False:
                    response['Content-Disposition'] = \
                        'attachment; filename="%s.csv"' % ar.report
                else:
                    #~ response = HttpResponse(content_type='application/csv')
                    response['Content-Disposition'] = \
                        'inline; filename="%s.csv"' % ar.report
                  
                #~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
                w = ucsv.UnicodeWriter(response,**settings.LINO.csv_params)
                w.writerow(ar.ah.store.column_names())
                for row in ar.data_iterator:
                    w.writerow([unicode(v) for v in rh.store.row2list(ar,row)])
                return response
                
            if fmt == 'pdf':
              
                from lino.utils.appy_pod import setup_renderer
                from appy.pod.renderer import Renderer
                
                tpl_leaf = "Table.odt" 
                #~ tplgroup = rpt.app_label + '/' + rpt.__name__
                tplgroup = None
                tplfile = find_config_file(tpl_leaf,tplgroup)
                if not tplfile:
                    raise Exception("No file %s / %s" % (tplgroup,tpl_leaf))
                    
                target_parts = ['cache', 'appypdf', rpt.app_label + '.' + rpt.__name__ + '.odt']
                target_file = os.path.join(settings.MEDIA_ROOT,*target_parts)
                target_url = self.media_url(*target_parts)
                
                body = self.table2xhtml(ar).toxml()
                #~ logger.info("20120122 body is %s",body)
                context = dict(
                    self=unicode(ar.get_title()),
                    table_body=body,
                    dtos=babel.dtos,
                    dtosl=babel.dtosl,
                    dtomy=babel.dtomy,
                    babelattr=babel.babelattr,
                    babelitem=babel.babelitem,
                    tr=babel.babelitem,
                    #~ iif=iif,
                    settings=settings,
                    #~ restify=restify,
                    #~ site_config = get_site_config(),
                    #~ site_config = settings.LINO.site_config,
                    _ = _,
                    #~ knowledge_text=fields.knowledge_text,
                    )
                #~ lang = str(elem.get_print_language(self))
                logger.info(u"appy.pod render %s -> %s (params=%s",
                    tplfile,target_file,settings.LINO.appy_params)
                renderer = Renderer(tplfile, context, target_file,**settings.LINO.appy_params)
                setup_renderer(renderer)
                #~ renderer.context.update(restify=debug_restify)
                renderer.run()
                return http.HttpResponseRedirect(target_url)
                
            if fmt == 'printer':
                response = HttpResponse(content_type='text/html;charset="utf-8"')
                #~ ar.render_to_html(self,response)
                doc = xhg.HTML()
                doc.set_title(ar.get_title())
                t = self.table2xhtml(ar)
                doc.add_to_body(t)
                doc.__xml__(response)
                return response
                
            if fmt == 'json':
                rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator]
                total_count = len(ar.data_iterator)
                if ar.create_rows:
                    row = ar.create_instance()
                    d = rh.store.row2list(ar,row)
                    rows.append(d)
                    total_count += 1
                return json_response_kw(count=total_count,
                  rows=rows,
                  title=unicode(ar.get_title()),
                  gc_choices=[gc.data for gc in rpt.grid_configs])
                    
            raise Http404("Format %r not supported for GET on %s" % (fmt,rpt))

        raise Http404("Method %s not supported for container %s" % (request.method,rh))
    
    
    def requested_report(self,request,app_label,actor):
        x = getattr(settings.LINO.modules,app_label)
        cl = getattr(x,actor)
        if issubclass(cl,models.Model):
            return cl._lino_model_report
        return cl
        
    def parse_params(self,rh,request):
        return rh.store.parse_params(request)
        
    #~ def rest2form(self,request,rh,data):
        #~ d = dict()
        #~ logger.info('20120118 rest2form %r', data)
        #~ for i,f in enumerate(rh.store.list_fields):
        #~ return d
        
    def delete_element(self,request,rpt,elem):
        assert elem is not None
        #~ if rpt.disable_delete is not None:
        msg = rpt.disable_delete(elem,request)
        if msg is not None:
            return error_response(None,msg)
                
        dblogger.log_deleted(request,elem)
        
        try:
            elem.delete()
        except Exception,e:
            dblogger.exception(e)
            msg = _("Failed to delete %(record)s : %(error)s."
                ) % dict(record=obj2unicode(elem),error=e)
            #~ msg = "Failed to delete %s." % element_name(elem)
            return error_response(None,msg)
            #~ raise Http404(msg)
        return HttpResponseDeleted()
        
    def restful_view(self,request,app_label=None,actor=None,pk=None):
        """
        Used to collaborate with a restful Ext.data.Store.
        """
        rpt = self.requested_report(request,app_label,actor)
        a = rpt.default_action
        
        elem = None
        if pk is not None:
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s." % pk,full_model_name(rpt.model)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
        
        
        if isinstance(a,actions.ReportAction):
            ar = rpt.request(self,request,a)
            rh = ar.ah
        else:
            ar = tables.ActionRequest(self,a)
        
        if request.method == 'GET':
            if pk:
                pass
            else:
                #~ rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator ]
                rows = [ rh.store.row2dict(ar,row,rh.store.list_fields) for row in ar.sliced_data_iterator ]
                #~ rows = [ ar.row2dict(row) for row in ar.queryset ]
                #~ total_count = ar.total_count
                total_count = len(ar.data_iterator)
                #logger.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
                # add extra blank row(s):
                #~ for i in range(0,ar.extra):
                if ar.create_rows:
                    row = ar.create_instance()
                    d = rh.store.row2list(ar,row)
                    #~ logger.info('20111213 %s -> %s -> %s', obj2str(ar.master),row, d)
                    #~ d = ar.row2dict(row)
                    #~ 20100706 d[rh.report.model._meta.pk.name] = -99999
                    rows.append(d)
                    total_count += 1
                return json_response_kw(count=total_count,rows=rows)
        
        if request.method == 'DELETE':
            return self.delete_element(request,rpt,elem)
              
        if request.method == 'POST':
            #~ data = rh.store.get_from_form(request.POST)
            #~ instance = ar.create_instance(**data)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.list_action)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
            instance = ar.create_instance()
            # store uploaded files. 
            # html forms cannot send files with PUT or GET, only with POST
            if rh.report.handle_uploaded_files is not None:
                rh.report.handle_uploaded_files(instance,request)
                
            data = request.POST.get('rows')
            #~ logger.info("20111217 Got POST %r",data)
            data = json.loads(data)
            #~ data = self.rest2form(request,rh,data)
            return self.form2obj_and_save(request,rh,data,instance,True,include_rows=ar)
            
        if request.method == 'PUT':
            if elem:
                data = http.QueryDict(request.raw_post_data).get('rows')
                #~ logger.info('20120118 PUT 1 %r', data)
                data = json.loads(data)
                #~ logger.info('20120118 PUT 2 %r', data)
                #~ data = self.rest2form(request,rh,data)
                #~ print 20111021, data
                #~ fmt = data.get('fmt',None)
                return self.form2obj_and_save(request,ar.ah,data,elem,False) # force_update=True)
            else:
                raise Http404("PUT without element")
          
    def api_element_view(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = self.requested_report(request,app_label,actor)
        #~ if not ah.report.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.report)
            #~ return http.HttpResponseForbidden()
            
        elem = None
        
        if pk != '-99999' and pk != '-99998':
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s." % (pk,rpt)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
        if request.method == 'DELETE':
            return self.delete_element(request,rpt,elem)
            
        if request.method == 'PUT':
            ah = rpt.get_handle(self)
            if elem is None:
                raise Http404('Tried to PUT on element -99999')
            #~ print 20110301, request.raw_post_data
            data = http.QueryDict(request.raw_post_data)
            #~ print 20111021, data
            #~ fmt = data.get('fmt',None)
            return self.form2obj_and_save(request,ah,data,elem,False) # force_update=True)
            
        if request.method == 'GET':
            #~ # before 20110713
            #~ ar = ext_requests.ViewReportRequest(request,ah,ah.report.default_action)
            
            #~ if pk == '-99999':
                #~ elem = ar.create_instance()
            
            #~ fmt = request.GET.get('fmt',None)
            #~ if pk == '-99999':
                #~ datarec = elem2rec_insert(ar,ah,elem)
            #~ else:
                #~ datarec = elem2rec_detailed(ar,ah,elem)
            #~ if fmt is None or fmt == 'json':
                #~ return json_response(datarec)
                    
            action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME,
              rpt.default_elem_action_name)
            #~ if action_name is None:
                #~ a = rpt.default_action
            #~ else:
            a = rpt.get_action(action_name)
            if a is None:
                raise Http404("%s has no action %r" % (rpt,action_name))
                
            fmt = request.GET.get('fmt',a.default_format)
            #~ a = rpt.get_action(fmt)
                
            #~ ar = ViewReportRequest(request,ah,a)
            #~ ar = table.TableRequest(self,rpt,request,a)
            ar = rpt.request(self,request,a)
            ah = ar.ah

            if isinstance(a,actions.OpenWindowAction):
              
                if fmt == 'json':
                    if pk == '-99999':
                        assert elem is None
                        elem = ar.create_instance()
                        datarec = elem2rec_insert(ar,ah,elem)
                    elif pk == '-99998':
                        assert elem is None
                        elem = ar.create_instance()
                        datarec = elem2rec_empty(ar,ah,elem)
                    #~ elif pk  == '-99990':
                        #~ assert elem is None
                        #~ datarec = elem2rec_empty(ar,ah)
                    else:
                        datarec = elem2rec_detailed(ar,ah,elem)
                    
                    return json_response(datarec)
                    
                #~ after_show = dict(data_record=datarec)
                after_show = dict(record_id=pk)
                params = dict()
                bp = ar.request2kw(self)
                #~ bp = self.request2kw(ar)
                
                #~ if a.window_wrapper.tabbed:
                if rpt.get_detail().get_handle(self).tabbed:
                #~ if rpt.model._lino_detail.get_handle(self).tabbed:
                    tab = request.GET.get(ext_requests.URL_PARAM_TAB,None)
                    if tab is not None: 
                        tab = int(tab)
                        after_show.update(active_tab=tab)
                params.update(base_params=bp)
                return HttpResponse(self.html_page(request,
                  on_ready=[self.action_handler(a,None,params,after_show)]))
                #~ return HttpResponse(self.html_page(request,
                  #~ on_ready=['Lino.%s(undefined,%s,%s);' % (
                    #~ a,py2js(params),py2js(after_show))]))
                
                
            if isinstance(a,actions.RedirectAction):
                target = a.get_target_url(elem)
                if target is None:
                    raise Http404("%s failed for %r" % (a,elem))
                return http.HttpResponseRedirect(target)
                
            if isinstance(a,actions.RowAction):
                #~ return a.run(ar,elem)
                if pk == '-99998':
                    assert elem is None
                    elem = ar.create_instance()
                
                try:
                    return a.run(ar,elem)
                except actions.ConfirmationRequired,e:
                    r = dict(
                      success=True,
                      confirm_message='\n'.join([unicode(m) for m in e.messages]),
                      step=e.step)
                    return json_response(r)
                except Exception,e:
                    msg = unicode(e)
                    #~ if elem is None:
                        #~ msg = unicode(e)
                    #~ else:
                        #~ msg = _("Action \"%(action)s\" failed for %(record)s:") % dict(
                            #~ action=a,
                            #~ record=obj2unicode(elem))
                        #~ msg += "\n" + unicode(e)
                      
                    msg += '.\n' + _("An error report has been sent to the system administrator.")
                    logger.warning(msg)
                    logger.exception(e)
                    return error_response(e,msg)
              
            raise NotImplementedError("Action %s is not implemented)" % a)
                
              
        return error_response(None,
            "Method %r not supported for elements of %s." % (
                request.method,ah.report))
        #~ raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        
        
    def error_response(self,*args,**kw):
        kw.update(success=False)
        return error_response(*args,**kw)
        
    def success_response(self,*args,**kw):
        kw.update(success=True)
        return json_response_kw(*args,**kw)
        
    def lino_js_parts(self):
    #~ def js_cache_name(self):
        #~ return ('cache','js','site.js')
        #~ return ('cache','js','lino.js')
        return ('cache','js','lino_'+translation.get_language()+'.js')
        
    def build_lino_js(self,force=False):
        """Generate :xfile:`lino.js`.
        """
        if not force and not settings.LINO.auto_makeui:
            logger.info("NOT generating `lino.js` because `settings.LINO.auto_makeui` is False")
            return 
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.warning("Not generating `lino.js` because "+
            "directory '%s' (settings.MEDIA_ROOT) does not exist.", 
            settings.MEDIA_ROOT)
            return
        
        mtime = codetime()
        
        makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'upload'))
        makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,'webdav'))
        
        for lang in babel.AVAILABLE_LANGUAGES:
            babel.set_language(lang)
            fn = os.path.join(settings.MEDIA_ROOT,*self.lino_js_parts()) 
            if not force and os.path.exists(fn):
                if os.stat(fn).st_mtime > mtime:
                    logger.info("NOT generating %s because it is newer than the code.",fn)
                    continue
                    
            logger.info("Generating %s ...", fn)
            
            makedirs_if_missing(os.path.dirname(fn))
            
            f = codecs.open(fn,'w',encoding='utf-8')
            
            for ln in self.lino_js_lines():
                f.write(ln + '\n')
                
            tpl = self.linolib_template()
            
            f.write(jscompress(unicode(tpl)+'\n'))
            
            #~ for model in models.get_models():
                #~ if model._lino_detail:
                    #~ f.write("Ext.namespace('Lino.%s') // detail\n" % full_model_name(model))
                    #~ for ln in self.js_render_detail_FormPanel(model._lino_detail.get_handle(self)):
                        #~ f.write(ln + '\n')
                        
            actors_list = [rpt for rpt in table.master_reports \
                     + table.slave_reports \
                     + table.generic_slaves.values() \
                     + table.custom_tables \
                     + table.frames ]
                     
            for a in actors_list:
                f.write("Ext.namespace('Lino.%s')\n" % a)
                
            #~ logger.info('20120120 table.all_details:\n%s',
                #~ '\n'.join([str(d) for d in table.all_details]))
            
            for dtl in table.all_details:
                for ln in self.js_render_detail_FormPanel(dtl.get_handle(self)):
                    f.write(ln + '\n')
            
            for rpt in actors_list:
                     
                rh = rpt.get_handle(self) 
                
                if isinstance(rpt,type) and issubclass(rpt,table.AbstractTable):
                    for ln in self.js_render_GridPanel_class(rh):
                        f.write(ln + '\n')
                    
                for a in rpt.get_actions():
                    if isinstance(a,(actions.ShowDetailAction,actions.InsertRow)):
                        for ln in self.js_render_detail_action_FormPanel(rh,a):
                              f.write(ln + '\n')
                    #~ if isinstance(a,(table.WindowAction)):
                    for ln in self.js_render_window_action(rh,a):
                        f.write(ln + '\n')
                            
                    #~ if a.window_wrapper is not None:
                        #~ for ln in a.window_wrapper.js_render():
                            #~ f.write(ln + '\n')
                        #~ f.write('\n')
                        
                  
            #~ f.write("""
#~ Ext.reg('extensible.eventeditwindow', Lino.cal.Event.FormPanel);
#~ """)
            #~ f.write(jscompress(js))
            f.close()
            #~ logger.info("Wrote %s ...", fn)
        logger.info("lino*.js files have been generated.")
        babel.set_language(None)
        
    def make_linolib_messages(self):
        """
        Called from :term:`makedocs`.
        """
        from lino.utils.config import make_dummy_messages_file
        tpl = self.linolib_template()
        messages = set()
        def mytranslate(s):
            #~ settings.LINO.add_dummy_message(s)
            messages.add(s)
            return _(s)
        tpl._ = mytranslate
        unicode(tpl) # just to execute the template. result is not needed
        make_dummy_messages_file(self.linolib_template_name(),messages)
        
    def linolib_template_name(self):
        return os.path.join(os.path.dirname(__file__),'linolib.js')
        
    def linolib_template(self):
        libname = self.linolib_template_name()
        tpl = CheetahTemplate(codecs.open(libname,encoding='utf-8').read())
        tpl.ui = self
            
        tpl._ = _
        #~ tpl.user = request.user
        tpl.site = settings.LINO
        tpl.settings = settings
        tpl.lino = lino
        tpl.ui = self
        tpl.ext_requests = ext_requests
        for k in ext_requests.URL_PARAMS:
            setattr(tpl,k,getattr(ext_requests,k))
        return tpl
            
    def templates_view(self,request,app_label=None,actor=None,pk=None,fldname=None,tplname=None,**kw):
      
        if request.method == 'GET':
            from lino.models import TextFieldTemplate
            if tplname:
                tft = TextFieldTemplate.objects.get(pk=int(tplname))
                return HttpResponse(tft.text)
                
            rpt = actors.get_actor2(app_label,actor)
            if rpt is None:
                model = models.get_model(app_label,actor,False)
                rpt = model._lino_model_report
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s.%s." % (pk,rpt.model._meta.app_label,rpt.model.__name__)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
            #~ TextFieldTemplate.templates
            m = getattr(elem,"%s_templates" % fldname,None)
            #~ m = getattr(rpt.model,"%s_templates" % fldname,None)
            if m is None:
                q = models.Q(user=request.user) | models.Q(user=None)
                #~ q = models.Q(user=request.user)
                qs = TextFieldTemplate.objects.filter(q).order_by('name')
            else:
                qs = m(request)
                
            templates = []
            for obj in qs:
                url = self.build_url('templates',
                    app_label,actor,pk,fldname,unicode(obj.pk))
                templates.append([
                    unicode(obj.name),url,unicode(obj.description)])
            js = "var tinyMCETemplateList = %s;" % py2js(templates)
            return HttpResponse(js,content_type='text/json')
        raise Http404("Method %r not supported" % request.method)
        
    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        """
        Return a JSON object with two attributes `count` and `rows`,
        where `rows` is a list of `(display_text,value)` tuples.
        Used by ComboBoxes or similar widgets.
        If `fldname` is not specified, returns the choices for the `jumpto` widget.
        """
        rpt = self.requested_report(request,app_label,rptname)
        #~ rpt = actors.get_actor2(app_label,rptname)
        if fldname is None:
            #~ rh = rpt.get_handle(self)
            #~ ar = ViewReportRequest(request,rh,rpt.default_action)
            #~ ar = table.TableRequest(self,rpt,request,rpt.default_action)
            ar = rpt.request(self,request,rpt.default_action)
            #~ rh = ar.ah
            #~ qs = ar.get_data_iterator()
            qs = ar.data_iterator
            #~ qs = rpt.request(self).get_queryset()
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                return d
        else:
            #~ field = find_field(rpt.model,fldname)
            field = rpt.get_data_elem(fldname)
            if field is None:
                field = rpt.get_param_elem(fldname)
            chooser = choosers.get_for_field(field)
            if chooser:
                qs = chooser.get_request_choices(request)
                #~ if qs is None:
                    #~ qs = []
                assert isiterable(qs), \
                      "%s.%s_choices() returned %r which is not iterable." % (
                      rpt.model,fldname,qs)
                if chooser.simple_values:
                    def row2dict(obj,d):
                        #~ d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                        return d
                elif chooser.instance_values:
                    # same code as for ForeignKey
                    def row2dict(obj,d):
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                        return d
                else:
                    def row2dict(obj,d):
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                        return d
            elif field.choices:
                qs = field.choices
                def row2dict(obj,d):
                    if type(obj) is list or type(obj) is tuple:
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                    else:
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                    return d
                
            elif isinstance(field,models.ForeignKey):
                m = field.rel.to
                #~ cr = getattr(m,'_lino_choices_table',None)
                t = getattr(m,'_lino_choices_table',m._lino_model_report)
                #~ tblclass = getattr(m,'_lino_choices_table',m._lino_model_report)
                #~ if tblclass is not None:
                    #~ tbl = tblclass()
                #~ else:
                    #~ tbl = m._lino_model_report
                qs = t.request(self,request).data_iterator
                #~ ar = table.TableRequest(self,tbl,request,tbl.default_action)
                #~ qs = ar.get_queryset()
                #~ qs = mr.request(self,**mr.default_params).get_queryset()
                #~ qs = get_default_qs(field.rel.to)
                #~ qs = field.rel.to.objects.all()
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                    return d
            else:
                raise Http404("No choices for %s" % fldname)
                
                
        quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
        if quick_search is not None:
            qs = table.add_quick_search_filter(qs,quick_search)
            
        count = len(qs)
            
        offset = request.GET.get(ext_requests.URL_PARAM_START,None)
        if offset:
            qs = qs[int(offset):]
            #~ kw.update(offset=int(offset))
        limit = request.GET.get(ext_requests.URL_PARAM_LIMIT,None)
        if limit:
            #~ kw.update(limit=int(limit))
            qs = qs[:int(limit)]
            
        rows = [ row2dict(row,{}) for row in qs ]
        return json_response_kw(count=count,rows=rows) 
        #~ return json_response_kw(count=len(rows),rows=rows) 
        #~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
        

    #~ def quicklink(self,request,app_label,actor,**kw):
        #~ rpt = self.requested_report(request,app_label,actor)
        #~ return self.action_href(rpt.default_action,**kw)

    def quick_upload_buttons(self,rr):
        """
        Deserves more documentation.
        """
        params = dict(base_params=rr.request2kw(self))
        after_show = dict()
        #~ params = dict(base_params=self.request2kw(rr))
        if len(rr.data_iterator) == 0:
            #~ return [dict(text="Upload",handler=js_code('Lino.%s' % rr.report.get_action('insert')))]
            a = rr.report.get_action('insert')
            if a is not None:
                elem = rr.create_instance()
                after_show.update(data_record=elem2rec_insert(rr,rr.ah,elem))
                return self.action_href_js(a,params,after_show,_("Upload"))
        if len(rr.data_iterator) == 1:
            #~ return [dict(text="Show",handler=js_code('Lino.%s' % v.report.get_action('detail')))]
            #~ s = unicode(v[0]) + ':'
            s = ''
            s += ' [<a href="%s" target="_blank">show</a>]' % (self.media_url(rr.data_iterator[0].file.name))
            #~ s += ' [<a href="%s" target="_blank">edit</a>]' % (self.get_detail_url(rr[0],fmt='detail'))
            #~ params = dict(data_record=elem2rec1(rr,rr.ah,rr[0]))
            if True:
                #~ params = dict(data_record=elem2rec_detailed(rr,rr.ah,rr[0]))
                after_show.update(record_id=rr.data_iterator[0].pk)
                s += ' ' + self.action_href_js(rr.ah.report.detail_action,params,after_show,_("Edit"))
            else:
                after_show.update(record_id=rr.data_iterator[0].pk)
                s += ' ' + self.action_href_http(rr.ah.report.detail_action,_("Edit"),params,after_show)
            return s
        return '[?!]'
        
    def py2js_converter(self,v):
        """
        Additional converting logic for serializing Python values to json.
        """
        if v is LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if v is STRENGTH_CHOICES:
            return js_code('STRENGTH_CHOICES')
        if v is KNOWLEDGE_CHOICES:
            return js_code('KNOWLEDGE_CHOICES')
        if isinstance(v,choicelists.BabelChoice):
            """
            This is special. We don't render the text but the value. 
            """
            return v.value
        #~ if isinstance(v,babel.BabelText):
            #~ return unicode(v)
        #~ if isinstance(v,Promise):
            #~ return unicode(v)
        if isinstance(v,models.Model):
            return v.pk
        if isinstance(v,Exception):
            return unicode(v)
        if isinstance(v,menus.Menu):
            if v.parent is None:
                return v.items
                #kw.update(region='north',height=27,items=v.items)
                #return py2js(kw)
            return dict(text=prepare_label(v),menu=dict(items=v.items))
        if isinstance(v,menus.MenuItem):
            #~ if v.href is not None:
                #~ if v.parent.parent is None:
                    #~ # special case for href items in main menubar
                    #~ return dict(
                      #~ xtype='button',text=prepare_label(v),
                      #~ handler=js_code("function() {window.location='%s';}" % v.href))
                #~ return dict(text=prepare_label(v),href=v.href)
            if v.href is not None:
                url = v.href
            elif v.params is not None:
                #~ ar = table.TableRequest(self,v.action.actor,None,v.action,**v.params)
                ar = v.action.actor.request(self,None,v.action,**v.params)
                url = self.get_request_url(ar)
            elif v.request is not None:
                url = self.get_request_url(v.request)
            elif v.instance is not None:
                #~ url = self.get_detail_url(v.instance,an='detail')
                url = self.get_detail_url(v.instance)
            elif v.action:
                if True:
                    #~ handler = self.action_handler(v.action,params=v.params)
                    handler = "function(){%s}" % self.action_handler(v.action,params=v.params)
                    #~ handler = "function(btn,evt){Lino.%s(undefined,%s)}" % (
                        #~ v.action,py2js(v.params or {}))
                    return dict(text=prepare_label(v),handler=js_code(handler))
                else:
                    url = self.action_url_http(v.action)
            else:
                # a separator
                #~ return dict(text=v.label)
                return v.label
                #~ url = self.build_url('api',v.action.actor.app_label,v.action.actor.__name__,fmt=v.action.name)
            if v.parent.parent is None:
                # special case for href items in main menubar
                return dict(
                  xtype='button',text=prepare_label(v),
                  #~ handler=js_code("function() { window.location='%s'; }" % url))
                  handler=js_code("function() { location.replace('%s'); }" % url))
            return dict(text=prepare_label(v),href=url)
        return v
        
    def action_handler(self,a,caller=None,params=None,after_show=None):
        if isinstance(a,actions.ShowEmptyTable):
            after_show = dict(record_id=-99998)
        if after_show:
            return "Lino.%s(%s,%s,%s)" % (a,py2js(caller),py2js(params),py2js(after_show))
        if params:
            return "Lino.%s(%s,%s)" % (a,py2js(caller),py2js(params))
        if caller:
            return "Lino.%s(%s)" % (a,py2js(caller))
        return "Lino.%s()" % a

    def action_href_js(self,a,params,after_show=None,label=None):
        """
        Return a HTML chunk for a button that will execute this 
        action using a *Javascript* link to this action.
        """
        label = cgi.escape(force_unicode(label or a.get_button_label()))
        url = self.action_url_js(a,params,after_show)
        return self.href_button(url,label)
        
    def action_url_js(self,a,params,after_show):
        onclick = self.action_handler(a,params,after_show)
        #~ onclick = 'Lino.%s(undefined,%s,%s)' % (
          #~ a,
          #~ py2js(params or {}),
          #~ py2js(after_show or {}))
        #~ print 20110120, onclick
        onclick = cgi.escape(onclick)
        onclick = onclick.replace('"','&quot;')
        return 'javascript:' + onclick

    def action_href_http(self,a,label=None,**params):
        """
        Return a HTML chunk for a button that will execute 
        this action using a *HTTP* link to this action.
        """
        label = cgi.escape(force_unicode(label or a.get_button_label()))
        return '[<a href="%s">%s</a>]' % (self.action_url_http(a,**params),label)
        
    #~ def get_action_url(self,action,*args,**kw):
    def action_url_http(self,action,*args,**kw):
        #~ if not action is action.actor.default_action:
        if action != action.actor.default_action:
            kw.update(an=action.name)
        return self.build_url("api",action.actor.app_label,action.actor.__name__,*args,**kw)
            
    def get_actor_url(self,actor,*args,**kw):
        return self.build_url("api",actor.app_label,actor.__name__,*args,**kw)
        
    def get_request_url(self,rr,*args,**kw):
        kw = rr.request2kw(self,**kw)
        #~ kw = self.request2kw(rr,**kw)
        return self.build_url('api',rr.report.app_label,rr.report.__name__,*args,**kw)
        
    def get_detail_url(self,obj,*args,**kw):
        #~ rpt = obj._lino_model_report
        #~ return self.build_url('api',rpt.app_label,rpt.__name__,str(obj.pk),*args,**kw)
        return self.build_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    def href_to_request(self,rr,text=None):
        return self.href(
            self.get_request_url(rr),
            text or cgi.escape(force_unicode(rr.label)))
            
    def href_to(self,obj,text=None):
        if True:
            a = obj.__class__._lino_model_report.get_action('detail')
            onclick = 'Lino.%s(undefined,{},{record_id:%s})' % (a,py2js(obj.pk))
            onclick = cgi.escape(onclick)
            onclick = onclick.replace('"','&quot;')
            url = "javascript:" + onclick
            return self.href(url,text or cgi.escape(force_unicode(obj)))
        return self.href(
            self.get_detail_url(obj),
            text or cgi.escape(force_unicode(obj)))

    def href(self,url,text):
        return '<a href="%s">%s</a>' % (url,text)
        
    def href_button(self,url,text):
        return '[<a href="%s">%s</a>]' % (url,text)
    
            
    def setup_handle(self,h):
        #~ logger.debug('20120103 ExtUI.setup_handle() %s',h)
        #~ if isinstance(h,layouts.TabPanelHandle):
            #~ h._main = ext_elems.TabPanel([l.get_handle(self) for l in h.layouts])
          
        if isinstance(h,table.DetailHandle): self.setup_detail_handle(h)
        #~ elif isinstance(h,table.FrameHandle):
            #~ for a in h.get_actions():
                #~ a.window_wrapper = self.action_window_wrapper(a,h)
                
        else:
            if isinstance(h,tables.TableHandle):
                if issubclass(h.report,table.Table):
                    if h.report.model is None \
                        or h.report.model is models.Model \
                        or h.report.model._meta.abstract:
                        return
                        
                h.list_layout = table.ListLayoutHandle(h,
                    table.ListLayout(h.report,'main = '+h.report.column_names),
                    hidden_elements=h.report.hidden_columns)
            else:
                h.list_layout = None
                    
            if h.report.parameters:
                if h.report.params_template:
                    params_template = h.report.params_template
                else:
                    #~ params_template= ' '.join([pf.name for pf in h.report.params])
                    params_template= ' '.join(h.report.parameters.keys())
                h.params_layout = table.LayoutHandle(self,
                    table.ParamsLayout(h.report,'main = '+params_template))
                #~ logger.info("20120121 %s params_layout is %s",h,h.params_layout)
            
            h.store = ext_store.Store(h)
            
            #~ if h.store.param_fields:
                #~ logger.info("20120121 %s param_fields is %s",h,h.store.param_fields)
            
            if h.list_layout:
                h.on_render = self.build_on_render(h.list_layout._main)
                
            #~ elif isinstance(h,table.FrameHandle):
                #~ if issubclass(h.report,table.EmptyTable):
                    #~ h.store = ext_store.Store(h)
              
                
                      
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,a,**kw):
        if isinstance(a,actions.SubmitDetail):
            #~ kw.update(panel_btn_handler=js_code('Lino.submit_detail'))
            #~ kw.update(handler=js_code('function() {ww.save()}'))
            kw.update(panel_btn_handler=js_code('function(panel){panel.save()}'))
            
            #~ kw.update(handler=js_code('ww.save'),scope=js_code('ww'))
        #~ elif isinstance(a,table.SubmitInsert):
            #~ kw.update(panel_btn_handler=js_code('function(panel){panel.save()}'))
            #~ kw.update(handler=js_code('function() {ww.save()}'))
            #~ kw.update(handler=js_code('ww.save'),scope=js_code('ww'))
            #~ kw.update(panel_btn_handler=js_code('Lino.submit_insert'))
        #~ elif isinstance(a,actions.UpdateRowAction):
            #~ kw.update(panel_btn_handler=js_code('Lino.update_row_handler(%r)' % a.name))
        elif isinstance(a,actions.ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail_handler'))
            #~ kw.update(panel_btn_handler=js_code('Lino.show_detail_handler()'))
            #~ kw.update(panel_btn_handler=js_code('function(panel){Lino.show_detail(panel)}'))
        elif isinstance(a,actions.InsertRow):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert(panel)}'))
            #~ kw.update(panel_btn_handler=js_code("Lino.show_insert_handler(Lino.%s)" % a))
        elif isinstance(a,actions.DuplicateRow):
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert_duplicate(panel)}'))
        elif isinstance(a,actions.DeleteSelected):
            kw.update(panel_btn_handler=js_code("Lino.delete_selected"))
                #~ "Lino.delete_selected" % a))
        #~ elif isinstance(a,actions.RedirectAction):
            #~ kw.update(panel_btn_handler=js_code("Lino.show_download_handler(%r)" % a.name))
        elif isinstance(a,actions.RowAction):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.name))
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
        kw.update(
          text=a.label,
          name=a.name,
          #~ text=unicode(a.label),
        )
        return kw
        
    def setup_detail_handle(self,dh):
        """
        Adds UI-specific information to a DetailHandle.
        """
        lh_list = dh.lh_list
        if len(lh_list) == 1:
            dh.tabbed = False
            lh = lh_list[0]
            #~ lh.label = None
            dh.main = lh._main
            #~ main.update(autoScroll=True)
        else:
            dh.tabbed = True
            tabs = [lh._main for lh in lh_list]
            #~ for t in tabs: t.update(autoScroll=True)
            dh.main = ext_elems.TabPanel(tabs)
            
        dh.on_render = self.build_on_render(dh.main)
            
    def build_on_render(self,main):
        "dh is a DetailLayout or a ListLayout"
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e,ext_elems.FieldElement):
                field_elems.append(e)
                l = elems_by_field.get(e.field.name,None)
                if l is None:
                    l = []
                    elems_by_field[e.field.name] = l
                l.append(e)
            
        for e in field_elems:
            #~ if isinstance(e,FileFieldElement):
                #~ kw.update(fileUpload=True)
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    for el in elems_by_field.get(f.name,[]):
                        #~ if main.has_field(f):
                        #~ varname = varname_field(f)
                        #~ on_render.append("%s.on('change',Lino.chooser_handler(%s,%r));" % (varname,e.ext_name,f.name))
                        on_render.append(
                            "%s.on('change',Lino.chooser_handler(%s,%r));" % (
                            el.as_ext(),e.as_ext(),f.name))
        return on_render
        
      
    def js_render_detail_FormPanel(self,dh):
        
        yield ""
        #~ yield "// js_render_detail_FormPanel"
        #~ yield "Lino.%s.FormPanel = Ext.extend(Lino.FormPanel,{" % full_model_name(dh.detail.model)
        yield "Lino.%s.FormPanel = Ext.extend(Lino.FormPanel,{" % dh.detail.actor
        
        yield "  layout: 'fit',"
        #~ yield "  content_type: %s," % py2js(dh.content_type)
        if issubclass(dh.detail.actor,table.Table):
            yield "  content_type: %s," % py2js(ContentType.objects.get_for_model(dh.detail.actor.model).pk)

        
        yield "  initComponent : function() {"
            
            
        yield "    var ww = this.containing_window;"
        
        for ln in jsgen.declare_vars(dh.main):
            yield "    " + ln
        yield "    this.items = %s;" % dh.main.as_ext()
        

        yield "    this.before_row_edit = function(record) {"
        for ln in ext_elems.before_row_edit(dh.main):
            yield "      " + ln
        yield "    }"
        if dh.on_render:
            yield "  this.onRender = function(ct, position) {"
            for ln in dh.on_render:
                yield "    " + ln
            #~ yield "    Lino.%s.FormPanel.superclass.onRender.call(this, ct, position);" % full_model_name(dh.detail.model)
            yield "    Lino.%s.FormPanel.superclass.onRender.call(this, ct, position);" % dh.detail.actor
            yield "  }"


        #~ 20111125 see ext_elems.py too
        #~ if self.main.listeners:
            #~ yield "  config.listeners = %s;" % py2js(self.main.listeners)
        #~ yield "  config.before_row_edit = %s;" % py2js(self.main.before_row_edit)
        #~ yield "    Lino.%s.FormPanel.superclass.initComponent.call(this);" % full_model_name(dh.detail.model)
        yield "    Lino.%s.FormPanel.superclass.initComponent.call(this);" % dh.detail.actor
        yield "  }"
        yield "});"
        yield ""
        
        
    def js_render_detail_action_FormPanel(self,rh,action):
        rpt = rh.report
        yield ""
        #~ yield "// js_render_detail_action_FormPanel %s" % action
        #~ yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,full_model_name(rpt.model))
        #~ yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,action.actor)
        if rpt.get_detail() is None:
            raise Exception("action %s on table %r == %r without detail?" % (action,action.actor,rpt))
        yield "Lino.%sPanel = Ext.extend(Lino.%s.FormPanel,{" % (action,rpt.get_detail().actor)
        yield "  empty_title: %s," % py2js(action.get_button_label())
        if not isinstance(action,actions.InsertRow):
            yield "  has_navigator: %s," % py2js(rpt.has_navigator)
            
        if rh.report.params_panel_hidden:
            yield "  params_panel_hidden: true,"
            

        yield "  ls_bbar_actions: %s," % py2js([rh.ui.a2btn(a) for a in rpt.get_actions(action)])
        yield "  ls_url: %s," % py2js(ext_elems.rpt2url(rpt))
        #~ if action != rpt.default_action:
        yield "  action_name: %s," % py2js(action.name)
        yield "  active_fields: %s," % py2js(rpt.active_fields)
        yield "  initComponent : function() {"
        a = rpt.get_action('detail')
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a
        a = rpt.get_action('insert')
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a
            
        yield "    Lino.%sPanel.superclass.initComponent.call(this);" % action
        yield "  }"
        yield "});"
        yield ""
        
    def js_render_GridPanel_class(self,rh):
        
        yield ""
        #~ yield "// js_render_GridPanel_class"
        yield "Lino.%s.GridPanel = Ext.extend(Lino.GridPanel,{" % rh.report
        
        kw = dict()
        #~ kw.update(empty_title=%s,rh.report.get_button_label()
        kw.update(ls_url=ext_elems.rpt2url(rh.report))
        kw.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.list_fields])
        if rh.store.pk is not None:
            kw.update(ls_id_property=rh.store.pk.name)
            kw.update(pk_index=rh.store.pk_index)
            kw.update(content_type=ContentType.objects.get_for_model(rh.report.model).pk)
        kw.update(ls_quick_edit=rh.report.cell_edit)
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(rh.report.default_action)])
        kw.update(ls_grid_configs=[gc.data for gc in rh.report.grid_configs])
        kw.update(gc_name=ext_elems.DEFAULT_GC_NAME)
        #~ if action != rh.report.default_action:
            #~ kw.update(action_name=action.name)
        #~ kw.update(content_type=rh.report.content_type)
        
        
        kw.update(page_length=rh.report.page_length)
        kw.update(stripeRows=True)

        #~ if rh.report.master:
        kw.update(title=rh.report.label)
        
        for k,v in kw.items():
            yield "  %s : %s," % (k,py2js(v))
        
        yield "  initComponent : function() {"
        
        a = rh.report.get_action('detail')
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a
        a = rh.report.get_action('insert')
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a
        
        
        yield "    var ww = this.containing_window;"
        for ln in jsgen.declare_vars(rh.list_layout._main.columns):
            yield "    " + ln
            
            
        yield "    this.before_row_edit = function(record) {"
        for ln in ext_elems.before_row_edit(rh.list_layout._main):
            yield "      " + ln
        yield "    };"
        if rh.on_render:
            yield "    this.onRender = function(ct, position) {"
            for ln in rh.on_render:
                yield "      " + ln
            yield "      Lino.%s.GridPanel.superclass.onRender.call(this, ct, position);" % rh.report
            yield "    }"
            
            
        yield "    this.ls_columns = %s;" % py2js([ 
            ext_elems.GridColumn(i,e) for i,e in enumerate(rh.list_layout._main.columns)])
            
        yield "    this.columns = this.apply_grid_config(this.gc_name,this.ls_grid_configs,this.ls_columns);"

        #~ yield "    this.items = %s;" % rh.list_layout._main.as_ext()
        #~ 20111125 see ext_elems.py too
        #~ if self.main.listeners:
            #~ yield "  config.listeners = %s;" % py2js(self.main.listeners)
        yield "    Lino.%s.GridPanel.superclass.initComponent.call(this);" % rh.report
        yield "  }"
        yield "});"
        yield ""
      
            
    def js_render_window_action(self,rh,action):
      
        rpt = rh.report
        
        if isinstance(action,actions.ShowDetailAction):
            s = "Lino.%sPanel" % action
        elif isinstance(action,actions.InsertRow): # also printable.InitiateListing
            s = "Lino.%sPanel" % action
        elif isinstance(action,actions.GridEdit):
            s = "Lino.%s.GridPanel" % rpt
        elif isinstance(action,actions.Calendar):
            s = "Lino.CalendarPanel"
        #~ elif isinstance(action,table.ShowEmptyTable):
            #~ s = "Lino.FramePanel"
        else:
            return 
            
        if action.actor.parameters:
            params = rh.params_layout._main
            #~ assert params.__class__.__name__ == 'ParameterPanel'
        else:
            params = None
        
        #~ yield "// js_render_window_action (%s)" % action
        yield "Lino.%s_window = null;" % action
        yield "Lino.%s = function(caller,mainConfig,after_show) { " % action
        yield "  if(!caller) caller = Lino.current_window;"
        yield "  if(!mainConfig) mainConfig = {};"
        yield "  if (Lino.%s_window == null) {" % action
        #~ yield "    console.log('20120117 instantiate Lino.%s_window');" % action
        yield "    mainConfig.is_main_window = true;" # workaround for problem 20111206
        if params:
            #~ print "20120115 ext_options", params.ext_options()
            for ln in jsgen.declare_vars(params):
                yield '    '  + ln
            #~ yield "  var pp = new %s(mainConfig);" % params
            yield "    mainConfig.params_panel = %s;" % params
            yield "    mainConfig.params_panel.fields = %s;" % py2js(
              [e for e in params.walk() if isinstance(e,ext_elems.FieldElement)])
            
        yield "    Lino.%s_window = new Lino.Window({" % action
        yield "      caller: caller, "
        yield "      main_item: new %s(mainConfig)" % s
        yield "    });"
        yield "  }"
        yield "  Lino.%s_window.show(after_show);" % action
        yield "};"
            
    def unused_get_actor(self,*args,**kw):
        from lino.core import actors
        a = actors.get_actor(*args,**kw)
        return a.get_handle(self)
        
    def table2xhtml(self,ar):
        t = xhg.TABLE(cellspacing="3px",bgcolor="#ffffff", width="100%")
        headers = [col.label or col.name for col in ar.ah.list_layout._main.columns]
        sums  = [0 for col in ar.ah.store.list_fields]
        cellattrs = dict(align="center",valign="middle",bgcolor="#eeeeee")
        t.add_header_row(*headers,**cellattrs)
        for row in ar.data_iterator:
            cells = [x for x in ar.ah.store.row2html(ar,row,sums)]
            t.add_body_row(*cells,**cellattrs)
        has_sum = False
        for i in sums:
            if i:
                has_sum = True
                break
        if has_sum:
            t.add_body_row(*ar.ah.store.sums2html(ar,sums),**cellattrs)
        return t
            
