# coding: latin1

## Copyright Luc Saffre 2003-2005

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

"""
"""


import os
from lino import adamo
from lino.schemas.sprl.sprl import makeSchema



def populate(sess):
    from lino.schemas.sprl.data import demo1
    #std.populate(sess,big)
    demo1.populate(sess)


        
def beginSession(populator=populate,
                 filename=None,
                 langs=None,
                 isTemporary=True,
                 **kw):
    schema = makeSchema(**kw)
    sess = adamo.beginQuickSession(schema,
                                   langs=langs,
                                   filename=filename,
                                   isTemporary=True,
                                   )
    
    sess.populate()
    if populator:
        populator(sess)
        
    return sess


# deprecated name for beginSession:
# getDemoDB = beginSession

