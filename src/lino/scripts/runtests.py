## Copyright 2004-2005 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import sys
import types
import unittest

from lino.misc import tsttools
from lino.misc.my_import import my_import

from lino.console.application import Application

from lino.forms import gui
gui.choose("testkit")

class StoppingTestResult(unittest._TextTestResult):

    def stopTest(self, test):
        "Called when the given test has been run"
        if len(self.errors) or len(self.failures):
            self.stop()


class StoppingTestRunner(unittest.TextTestRunner):
    
    def _makeResult(self):
        return StoppingTestResult(self.stream,
                                  self.descriptions,
                                  self.verbosity)


class Runtests(Application):

    name="Lino/runtests"
    years='2004-2005'
    author='Luc Saffre'
    
    usage="usage: %prog [options] [TESTS]"
    
    description="""\
scans a directory tree for .py files containing test cases and run
them.  TESTS specifies the tests to run. Default is all. Other
possible values e.g. `1` or `1-7`.
"""
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-i", "--ignore-failures",
                          help="""\
continue testing even if failures or errors occur""",
                          action="store_true",
                          dest="ignore",
                          default=False)
    
    def makeSuite(self,sess,argv,root='.'):

        sess.status("Collecting test cases")
        suites=[]
        cases = []
        #skipped=[]
        sys.path.append(root)
        for dirpath, dirnames, filenames in os.walk(root):
            prefix=".".join(dirpath.split(os.path.sep)[1:])
            if len(prefix):
                prefix+="."
            #print dirpath
            for filename in filenames:
                sess.status(os.path.join(dirpath,filename))
                modname,ext = os.path.splitext(filename)
                if ext == '.py':
                    doit = (len(argv) == 0)
                    for arg in argv:
                        a = arg.split('-')
                        if len(a) == 2:
                            if a[0].isdigit() and a[1].isdigit():
                                if modname.isdigit():
                                    if int(modname) >= int(a[0]) \
                                          and int(modname) <= int(a[1]):
                                        doit = True
                            else:
                                if modname >= a[0] and modname <= a[1]:
                                    doit = True
                        elif len(a) == 1:
                            if modname == a[0]:
                                doit = True
                        else:
                            sess.warning("Unrecognized argument %s",
                                         arg)
                    if doit:
                        modname=prefix+modname
                        sess.verbose("Loading cases from %s...",
                                     modname)
                        
                        self.findTestCases(sess,modname,cases,suites)
        sys.path.remove(root)

        sess.notice("found %d cases and %d suites.",
                    len(cases),len(suites))
        for tcl in cases:
            if hasattr(tcl,"todo"):
                sess.notice("Todo %s : %s", tcl.__module__,tcl.todo)
            else:
                suites.append(unittest.makeSuite(tcl))
                
        return unittest.TestSuite(suites)
     
    def findTestCases(self,sess,modname,cases,suites):
        mod = my_import(modname)
        #cases=[]
        if hasattr(mod,"suite"):
            #print modname + ".suite()"
            suites.append(mod.suite())
        for (k,v) in mod.__dict__.items():
            # Python 2.2 if type(v) == types.ClassType:
            if type(v) == types.TypeType: # since 2.3
                if issubclass(v,unittest.TestCase) \
                      and v != unittest.TestCase \
                      and v != tsttools.TestCase:
                    if hasattr(v,"skip") and v.skip:
                        sess.notice("Skipping %s.%s",
                                    modname,v.__name__)
                    else:
                        cases.append(v)
        return cases
    
    
    def run(self,sess):
        suite = self.makeSuite(sess,self.args)
        sess.status("")
        if self.options.ignore:
            runner = unittest.TextTestRunner()
        else:
            runner = StoppingTestRunner()
        runner.run(suite)
        

# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = Runtests

if __name__ == '__main__':
    consoleApplicationClass().main() 
    



