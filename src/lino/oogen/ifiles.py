﻿#coding: utf-8
"""
this module defines one class for each internal file of an oo document
"""
import os.path
opj = os.path.join

class InternalFile:
	filename = NotImplementedError
	def __init__(self,gen):
		#assert isinstance(gen,OoGenerator)
		self.gen = gen
		
	def writeFile(self):
		f = open(opj(self.gen.tempDir,self.filename),"w")
		self.writeInternalContent(f)
		f.close()
		
	def writeInternalContent(self,f):
		raise NotImplementedError
		

class InternalXmlFile(InternalFile):
	doctype=NotImplementedError
	def writeInternalContent(self,f):
		f.write("""\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE %s PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
""" % self.doctype)
		self.writeXmlContent(f)

	def writeXmlContent(self,f):
		raise NotImplementedError
		
		
class MIMETYPE(InternalFile):
	filename = 'mimetype'
	def writeInternalContent(self,f):
		f.write(self.gen.mimetype+"\n")
		
	
class MANIFEST(InternalXmlFile):
	filename = 'manifest.xml'
	doctype = 'manifest:manifest'
	def writeXmlContent(self,f):
		f.write("""\
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
	<manifest:file-entry manifest:media-type="application/vnd.sun.xml.writer" manifest:full-path="/" />
	<manifest:file-entry manifest:media-type=""manifest:full-path="Pictures/" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml" />
	<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="settings.xml" />
</manifest:manifest>
""")

class META(InternalXmlFile):
	filename = 'meta.xml'
	doctype = 'office:document-meta'
	def writeXmlContent(self,f):
		f.write("""\
<office:document-meta 
xmlns:office="http://openoffice.org/2000/office" xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="http://openoffice.org/2000/meta" office:version="1.0">
<office:meta>
<meta:generator>lino.oogen</meta:generator>
<meta:initial-creator>Luc Saffre</meta:initial-creator>
<meta:creation-date>2004-02-03T11:22:46</meta:creation-date>
<dc:creator>Luc Saffre</dc:creator>
<dc:date>2004-05-20T13:59:07</dc:date>
<dc:language>en-US</dc:language>
<meta:editing-cycles>26</meta:editing-cycles>
<meta:editing-duration>PT5H35M34S</meta:editing-duration>
<meta:user-defined meta:name="Info 1"/>
<meta:user-defined meta:name="Info 2"/>
<meta:user-defined meta:name="Info 3"/>
<meta:user-defined meta:name="Info 4"/>
<meta:document-statistic meta:table-count="3" meta:cell-count="188"/>
</office:meta>
</office:document-meta>
		""")
		
		
		
class SETTINGS(InternalXmlFile):
	filename = 'settings.xml'
	doctype = 'office:document-settings'
	def writeXmlContent(self,f):
		f.write("""\
<office:document-settings 
	xmlns:office="http://openoffice.org/2000/office" 
		xmlns:xlink="http://www.w3.org/1999/xlink" 
		xmlns:config="http://openoffice.org/2001/config" 
	office:version="1.0">
<office:settings>
</office:settings>
</office:document-settings>
		""")
		
		
class STYLES(InternalXmlFile):
	filename = 'styles.xml'
	doctype = 'office:document-styles'
	def writeXmlContent(self,f):
		f.write("""\
<office:document-styles 
xmlns:office="http://openoffice.org/2000/office" 
xmlns:style="http://openoffice.org/2000/style" 
xmlns:text="http://openoffice.org/2000/text" 
xmlns:table="http://openoffice.org/2000/table" 
xmlns:draw="http://openoffice.org/2000/drawing" 
xmlns:fo="http://www.w3.org/1999/XSL/Format" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:number="http://openoffice.org/2000/datastyle" 
xmlns:svg="http://www.w3.org/2000/svg" 
xmlns:chart="http://openoffice.org/2000/chart" 
xmlns:dr3d="http://openoffice.org/2000/dr3d" 
xmlns:math="http://www.w3.org/1998/Math/MathML" 
xmlns:form="http://openoffice.org/2000/form" 
xmlns:script="http://openoffice.org/2000/script" 
office:version="1.0">
""")

		f.write("<office:font-decls>")
		for font in self.gen.doc.fonts:
			font.__xml__(f.write)
		f.write("</office:font-decls>")
		
		f.write("""<office:styles>""")
		for s in self.gen.doc.styles:
			s.__xml__(f.write)
		f.write("""</office:styles>""")
		
		f.write("""<office:automatic-styles>""")
		for s in self.gen.doc.autoStyles:
			s.__xml__(f.write)
		f.write("""</office:automatic-styles>""")
		f.write("""<office:master-styles>""")
		for s in self.gen.doc.masterStyles:
			s.__xml__(f.write)
		f.write("""</office:master-styles>""")
		f.write("""</office:document-styles>""")
		

	
class CONTENT(InternalXmlFile):
	filename = 'content.xml'
	doctype = 'office:document-content'
	
	def writeXmlContent(self,f):
		f.write("""\
<office:document-content 
xmlns:office="http://openoffice.org/2000/office" 
xmlns:style="http://openoffice.org/2000/style" 
xmlns:text="http://openoffice.org/2000/text" 
xmlns:table="http://openoffice.org/2000/table" 
xmlns:draw="http://openoffice.org/2000/drawing" 
xmlns:fo="http://www.w3.org/1999/XSL/Format" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:number="http://openoffice.org/2000/datastyle" 
xmlns:svg="http://www.w3.org/2000/svg" 
xmlns:chart="http://openoffice.org/2000/chart" 
xmlns:dr3d="http://openoffice.org/2000/dr3d" 
xmlns:math="http://www.w3.org/1998/Math/MathML" 
xmlns:form="http://openoffice.org/2000/form" 
xmlns:script="http://openoffice.org/2000/script" 
office:class="%s"
office:version="1.0">
""" % self.gen.officeClass)
		f.write("""\
<office:automatic-styles>
</office:automatic-styles>
""")
		f.write("<office:body>")
		self.gen.writeBody(f.write)
		f.write("</office:body>")
		f.write("</office:document-content>")




IFILES = (MIMETYPE,MANIFEST,SETTINGS,META,STYLES,CONTENT)
