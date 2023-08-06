<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
  xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
  xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
  xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
  xmlns:math="http://www.w3.org/1998/Math/MathML" 
  xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
  xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
  xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" 
  xmlns:ooo="http://openoffice.org/2004/office" 
  xmlns:ooow="http://openoffice.org/2004/writer" 
  xmlns:oooc="http://openoffice.org/2004/calc" 
  xmlns:dom="http://www.w3.org/2001/xml-events" 
  xmlns:xforms="http://www.w3.org/2002/xforms" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:rpt="http://openoffice.org/2005/report" 
  xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" 
  xmlns:xhtml="http://www.w3.org/1999/xhtml" 
  xmlns:grddl="http://www.w3.org/2003/g/data-view#" 
  xmlns:officeooo="http://openoffice.org/2009/office" 
  xmlns:tableooo="http://openoffice.org/2009/table" 
  xmlns:drawooo="http://openoffice.org/2010/draw" 
  xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" 
  xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" 
  xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" 
  xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" 
  xmlns:css3t="http://www.w3.org/TR/css3-text/"
  xmlns="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="office style text table draw fo xlink dc meta number svg chart  dr3d math form script config ooo ooow oooc dom xforms xsd xsi rpt of xhtml grddl officeooo tableooo drawooo calcext loext field formx css3t">
    
<xsl:output method="xml" encoding="UTF-8" indent="no"/>
    
<xsl:template name="teiHeader">
    <teiHeader>
      <fileDesc>
        <titleStmt>
        <!-- surtitre -->
            <xsl:if test="//text:p[@text:style-name='TEI_title:sup']">
                <title type="sup"><xsl:apply-templates select="//text:p[@text:style-name='TEI_title:sup']" mode="teiHeader"/></title>
            </xsl:if>
        <!-- titre principal -->
          <title type="main"><xsl:apply-templates select="//text:h[@text:outline-level='0']" mode="teiHeader"/></title>
        <!-- titre courant -->
        <!-- sous-titre -->
            <xsl:if test="//text:p[@text:style-name='TEI_title:sub']">
                <title type="sub"><xsl:apply-templates select="//text:p[@text:style-name='TEI_title:sub']" mode="teiHeader"/></title>
            </xsl:if>
        <!-- titre traduit -->
            <xsl:if test="//text:p[contains(@text:style-name,'TEI_title:trl')]">
                <xsl:for-each select="//text:p[contains(@text:style-name,'TEI_title:trl')]">
                    <title type="trl">
                        <xsl:attribute name="xml:lang">
                            <xsl:value-of select="substring-after(@text:style-name,'TEI_title:trl:')"/>
                        </xsl:attribute>
                        <xsl:apply-templates mode="teiHeader"/></title>
                </xsl:for-each>
            </xsl:if>
            <!-- bloc auteur -->
            <xsl:for-each select="//text:p[contains(@text:style-name,'TEI_author:aut')]">
                <xsl:call-template name="author"/>
            </xsl:for-each>
            <!-- bloc collaborateur -->
            <xsl:for-each select="//text:p[contains(@text:style-name,'TEI_editor')]">
                <xsl:call-template name="editor"/>
            </xsl:for-each>
        </titleStmt>
        <publicationStmt>
          <publisher></publisher>
          <!-- date de réception -->
          <xsl:if test="//text:p[@text:style-name='TEI_date_reception']">
              <date type="received"><xsl:value-of select="//text:p[@text:style-name='TEI_date_reception']"/></date>
          </xsl:if>
          <!-- date d'acceptation' -->
          <xsl:if test="//text:p[@text:style-name='TEI_date_acceptance']">
              <date type="accepted"><xsl:value-of select="//text:p[@text:style-name='TEI_date_acceptance']"/></date>
          </xsl:if>
<!-- blocs <ab> Métopes [todo] -->
            <ab type="online">
    <!-- /!\ distributor cause l'invalidité du fichier TEI (schéma TEI all) 
                <distributor></distributor>
                -->            
                <date type="publishing" when="">
                    <xsl:comment>Date de publication en ligne</xsl:comment>
                </date>
                <date type="embargoend" when="">
                    <xsl:comment>Date de fin d'embargo</xsl:comment>
                </date>
                <idno>
                    <xsl:comment>Numéro du document</xsl:comment>
                </idno>
                <idno type="DOI"></idno>
                <idno type="URL"></idno>
    <!-- /!\ élément availability invalide ici en TEI (pour Métopes) -->
<!--                <availability><xsl:comment>Licence</xsl:comment></availability>-->
            </ab>
            <ab type="print">
    <!-- /!\ distributor cause l'invalidité du ficheir TEI (schéma TEI all) 
                <distributor></distributor>
                -->  
                <date type="publishing" when="">
                    <xsl:comment>Date de publication papier</xsl:comment>
                </date>
                <dimensions>
                    <dim type="pagination">
                        <xsl:value-of select="//text:p[@text:style-name='TEI_pagination']"/>
                    </dim>
                </dimensions>
                <idno type="book"></idno>
            </ab>
        </publicationStmt>
        <sourceDesc>
          <p>Version métopes : 3.0</p>
        </sourceDesc>
      </fileDesc>
      <encodingDesc>
        <p>L'encodage de ce fichier a été produit au moyen des outils Métopes.</p>
        <appInfo>
            <xsl:comment>Version du modèle de stylage documentée ici ? <xsl:value-of select="//meta:user-defined[@meta:name='tplVersion']"/></xsl:comment>
            <application ident="circe" version="1.0">
                <label>Circé</label>
                <desc>Document converti en TEI avec l'application Circé</desc>
                <ref target="##"/>
            </application>
        </appInfo>
    <!-- génération conditionnelle du tagsDecl : ajouter test table -->
          <xsl:if test="//text:list">
            <tagsDecl>
            <xsl:comment>l'élément tagsDecl peut-il être vide ? sinon, conditionner à la présence de listes ou de tableaux</xsl:comment>
              <rendition scheme="css" xml:id="none">color:black;</rendition>
            <!-- liste des valeurs : disc, square, circle | decimal, lower-roman, upper-roman, lower-alpha, upper-alpha -->
              <xsl:if test="//text:list/@style:num-format='1'"><rendition scheme="css" xml:id="list-decimal">list-style-type:decimal;</rendition></xsl:if>
              <xsl:if test="//text:list/@style:num-format='i'"><rendition scheme="css" xml:id="list-lower-roman">list-style-type:lower-roman;</rendition></xsl:if>
              <xsl:if test="//text:list/@style:num-format='I'"><rendition scheme="css" xml:id="list-upper-roman">list-style-type:upper-roman;</rendition></xsl:if>
              <xsl:if test="//text:list/@style:num-format='a'"><rendition scheme="css" xml:id="list-lower-alpha">list-style-type:lower-alpha;</rendition></xsl:if>
              <xsl:if test="//text:list/@style:num-format='A'"><rendition scheme="css" xml:id="list-upper-alpha">list-style-type:upper-alpha;</rendition></xsl:if>
              <xsl:if test="//text:list/@text:bullet-char='■'"><rendition scheme="css" xml:id="list-square">list-style-type:square;</rendition></xsl:if>
              <xsl:if test="//text:list/@text:bullet-char='○'"><rendition scheme="css" xml:id="list-circle">list-style-type:circle;</rendition></xsl:if>
              <xsl:if test="//text:list/@text:bullet-char='●'"><rendition scheme="css" xml:id="list-disc">list-style-type:disc;</rendition></xsl:if>
              <!-- définir un comportement si autre cas rencontré ? -->
            </tagsDecl>
        </xsl:if>
        <editorialDecl>
            <normalization rendition="notes">
                <p rendition="note" select="restart"/>
                <p rendition="table" select="restart"/>
                <p rendition="annexe" select="restart"/>
                <p rendition="floatingText" select="restart"/>
            </normalization>
        </editorialDecl>
      </encodingDesc>
      <profileDesc>
        <langUsage>
          <language>
              <!-- diff Métopes/OE : combien de code de langue -->
              <xsl:attribute name="ident">
                  <xsl:value-of select="//text:p[@text:style-name='TEI_language']"/>
              </xsl:attribute>
          </language>
        </langUsage>
        <!-- mots-clés -->
        <xsl:if test="//text:p[starts-with(@text:style-name,'TEI_keywords')]">
            <textClass>
                <xsl:for-each select="//text:p[starts-with(@text:style-name,'TEI_keywords')]">
                    <xsl:call-template name="keywords"/>
                </xsl:for-each>
            </textClass>
        </xsl:if>
      </profileDesc>
      <revisionDesc>
          <listChange>
              <change type="##">
                  <xsl:attribute name="when">
                      <xsl:value-of select="current-date()"/>
                  </xsl:attribute>
                  <xsl:text>XML-TEI file created</xsl:text>
              </change>
          </listChange>
      </revisionDesc>
    </teiHeader>
</xsl:template>

<xsl:template name="author">
    <author>
        <xsl:attribute name="role" select="substring-after(@text:style-name,':')"/>
        <persName>
            <forename>
                <xsl:value-of select="substring-before(.,tokenize(.,' ')[last()])"/>
            </forename>
            <surname>
                <xsl:value-of select="tokenize(.,' ')[last()]"/>
            </surname>
        </persName>
        <xsl:if test="following-sibling::text:p[1][@text:style-name='TEI_authority_affiliation']">
            <affiliation><orgName><xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='TEI_authority_affiliation']/node()"/></orgName></affiliation>
        </xsl:if>
    </author>
</xsl:template>
    
<xsl:template name="editor">
    <editor>
        <xsl:attribute name="role" select="substring-after(@text:style-name,':')"/>
        <persName>
            <forename>
                <xsl:value-of select="substring-before(.,tokenize(.,' ')[last()])"/>
            </forename>
            <surname>
                <xsl:value-of select="tokenize(.,' ')[last()]"/>
            </surname>
        </persName>
        <xsl:if test="following-sibling::text:p[1][@text:style-name='TEI_authority_affiliation']">
            <affiliation><orgName><xsl:apply-templates select="following-sibling::text:p[1][@text:style-name='TEI_authority_affiliation']/node()"/></orgName></affiliation>
        </xsl:if>
    </editor>
</xsl:template>

<xsl:template name="keywords">
    <keywords scheme="keywords">
        <xsl:attribute name="xml:lang" select="substring-after(@text:style-name,'keywords:')"/>
        <list>
            <xsl:variable name="list">
                <xsl:choose>
                    <xsl:when test="contains(.,':')">
                        <xsl:value-of select="substring-after(., ': ')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:call-template name="keyWordsList">
                <xsl:with-param name="list">
                    <xsl:value-of select="$list"/>
                </xsl:with-param>
            </xsl:call-template>
        </list>
    </keywords>
</xsl:template>

<xsl:template name="keyWordsList">
    <xsl:param name="list"/>
    <xsl:variable name="first" select="substring-before($list, ', ')" />
    <xsl:variable name="remaining" select="substring-after($list, ', ')" />
    <xsl:choose>
        <xsl:when test="$first">
            <item><xsl:value-of select="$first"/></item>
            <xsl:if test="$remaining">
                <xsl:call-template name="keyWordsList">
                    <xsl:with-param name="list" select="$remaining" />
                </xsl:call-template>
            </xsl:if>
        </xsl:when>
        <xsl:otherwise>
            <item><xsl:value-of select="$list"/></item>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
    
<xsl:template match="//text:h[@text:outline-level='0']"/>
<xsl:template match="//text:p[@text:style-name='adSousTitre']"/>
<xsl:template match="//text:p[@text:style-name='adTitreTraduit']"/>
<xsl:template match="//text:p[@text:style-name='title-sup']"/>
<xsl:template match="//text:p[starts-with(@text:style-name,'TEI_author:')]"/>
<xsl:template match="//text:p[starts-with(@text:style-name,'TEI_editor')]"/>
<xsl:template match="//text:p[@text:style-name='TEI_authority_affiliation']"/>
<xsl:template match="//text:p[@text:style-name='TEI_date_reception']"/>
<xsl:template match="//text:p[@text:style-name='TEI_date_acceptance']"/>
<xsl:template match="//text:p[starts-with(@text:style-name,'TEI_keywords')]"/>
<xsl:template match="//text:p[@text:style-name='TEI_language']"/>
<xsl:template match="//text:p[@text:style-name='TEI_pagination']"/>
    
</xsl:stylesheet>