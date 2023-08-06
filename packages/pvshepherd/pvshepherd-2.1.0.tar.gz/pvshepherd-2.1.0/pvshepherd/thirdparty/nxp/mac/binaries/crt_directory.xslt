<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:xi="http://www.w3.org/2001/XInclude">

<xsl:template match="/">
  <html>
  <body>
  <xsl:apply-templates/> 
  </body>
  </html>
</xsl:template>

<xsl:template match="directory">
    <h2>List of available Chips and Boards by vendor</h2>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>Boards</EM></Caption>
    <tr bgcolor="#9acd32">
      <th align="left">For Chip Vendor</th>
      <th align="left">Name</th>
      <th align="left">Using Chip</th>
      <th align="left">File</th>
      <th align="left">Proc</th>
      <th align="left">Description</th>
    </tr>
    <xsl:for-each select="boards/board">
    <tr>
      <td><xsl:value-of select="../@chipVendor"/></td>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="@chip"/></td>
      <td><xsl:value-of select="@xml_file"/></td>
      <td><xsl:value-of select="@proc"/></td>
      <td><xsl:value-of select="@description"/></td>
    </tr>

    </xsl:for-each>
    </table>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>Chips</EM></Caption>
    <tr bgcolor="#9acd32">
      <th align="left">Vendor</th>
      <th align="left">Name</th>
      <th align="left">File</th>
      <th align="left">Proc</th>
      <th align="left">Description</th>
    </tr>
    <xsl:for-each select="chips/chip">
    <tr>
      <td><xsl:value-of select="../@chipVendor"/></td>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="@xml_file"/></td>
      <td><xsl:value-of select="@proc"/></td>
      <td><xsl:value-of select="@description"/></td>
    </tr>
    </xsl:for-each>

    <xsl:for-each select="xi:include">
      <xsl:variable name="block" select="@href" />
      <xsl:variable name="stuff" select="document($block)" />
      <xsl:for-each select="$stuff/chips/chip">
      <tr>
	<td><xsl:value-of select="../@chipVendor"/></td>
	<td><xsl:value-of select="@name"/></td>
	<td><xsl:value-of select="@xml_file"/></td>
	<td><xsl:value-of select="@proc"/></td>
	<td><xsl:value-of select="@description"/></td>
      </tr>
      </xsl:for-each>
    </xsl:for-each>
    </table>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>RTOSes</EM></Caption>
    <tr bgcolor="#9acd32">
      <th align="left">For Chip Vendor</th>
      <th align="left">Name</th>
      <th align="left">For Board</th>
      <th align="left">For Chip</th>
      <th align="left">File</th>
      <th align="left">Sym to Match</th>
      <th align="left">Description</th>
    </tr>
    <xsl:for-each select="rtoses/rtos">
    <tr>
      <td><xsl:value-of select="../@chipVendor"/></td>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="@board"/></td>
      <td><xsl:value-of select="@chip"/></td>
      <td><xsl:value-of select="@xml_file"/></td>
      <td><xsl:value-of select="@sym_match"/></td>
      <td><xsl:value-of select="@description"/></td>
    </tr>

    </xsl:for-each>
    </table>

</xsl:template>
</xsl:stylesheet>
