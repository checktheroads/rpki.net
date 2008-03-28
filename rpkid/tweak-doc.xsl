<!-- $Id$
 -
 -  Copyright (C) 2008  American Registry for Internet Numbers ("ARIN")
 - 
 -  Permission to use, copy, modify, and distribute this software for any
 -  purpose with or without fee is hereby granted, provided that the above
 -  copyright notice and this permission notice appear in all copies.
 - 
 -  THE SOFTWARE IS PROVIDED "AS IS" AND ARIN DISCLAIMS ALL WARRANTIES WITH
 -  REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
 -  AND FITNESS.  IN NO EVENT SHALL ARIN BE LIABLE FOR ANY SPECIAL, DIRECT,
 -  INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
 -  LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
 -  OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 -  PERFORMANCE OF THIS SOFTWARE.
 -->	

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

  <xsl:template match="div[@class = 'navigation']">
    <p>[Converted from HTML, see rpki/__init__.py for source]</p>
  </xsl:template>

  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="node() | @*"/>
    </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>
