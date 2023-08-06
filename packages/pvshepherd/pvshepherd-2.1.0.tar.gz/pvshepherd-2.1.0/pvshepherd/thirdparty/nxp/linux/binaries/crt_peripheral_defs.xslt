<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>Peripherals</h2>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>Peripherals</EM></Caption>
    <tr bgcolor="#9acd32">
      <th align="left">Name</th>
      <th align="left">PartOf</th>
      <th align="left">Size</th>
      <th align="left">Enable</th>
      <th align="left">Description</th>
    </tr>
    <xsl:for-each select="System/peripheral">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="@partOf"/></td>
      <td><xsl:value-of select="@size"/></td>
      <td><xsl:value-of select="@enable"/></td>
      <td><xsl:value-of select="@description"/></td>
    </tr>
    <xsl:if test="group">
    <tr>
      <td></td>
      <td colspan="5">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">GroupID</th>
          <th align="left">Offset</th>
          <th align="left">Size</th>
          <th align="left">EnableReg</th>
          <th align="left">Description</th>
        </tr>
	<xsl:for-each select="group">
	<tr>
	  <td><xsl:value-of select="@id"/></td>
	  <td><xsl:value-of select="@offset"/></td>
	  <td><xsl:value-of select="@size"/></td>
	  <td><xsl:value-of select="@enable"/></td>
	  <td><xsl:value-of select="@description"/></td>
	</tr>
        <xsl:call-template name="register" />
	</xsl:for-each>
     </table>
     </td>
    </tr>
    </xsl:if>
    <xsl:if test="register">
    <tr>
      <td></td>
      <td colspan="5">
        <xsl:call-template name="register" />
      </td>
    </tr>
    </xsl:if>

    </xsl:for-each>
    </table>
    <p>---</p>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>Peripheral Instances</EM></Caption>
    <tr bgcolor="lightblue">
      <th align="left">Name</th>
      <th align="left">DerivedFrom</th>
      <th align="left">Location</th>
      <th align="left">Enable</th>
    </tr>
    <xsl:for-each select="System/peripheralInstance">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="@derived_from"/></td>
      <td><xsl:value-of select="@location"/></td>
      <td><xsl:value-of select="@enable"/></td>
    </tr>
    </xsl:for-each>
    </table>

  </body>
  </html>
</xsl:template>
    <xsl:template name="register">
        <tr>
	  <td></td>
	  <td colspan="5">
	  <table border="1" cellspacing="0" width="850">
          <tr valign="top">
	    <th align="left">Register</th>
	    <th align="left">Offset</th>
	    <th align="left">Size</th>
	    <th align="left">Format</th>
	    <th align="left">RO</th>
	    <th align="left">Volatile</th>
	    <th align="left">WO</th>
	    <th align="left">Description</th>
          </tr>
	  <xsl:for-each select="register">
	  <tr valign="top">
	    <td><xsl:value-of select="@id"/></td>
	    <td><xsl:value-of select="@offset"/></td>
	    <td><xsl:value-of select="@size"/></td>
  	    <td><xsl:value-of select="@format"/></td>
	    <td><xsl:value-of select="@readOnly"/></td>
	    <td><xsl:value-of select="@readVolatile"/></td>
	    <td><xsl:value-of select="@writeOnly"/></td>
	    <td><xsl:value-of select="@description"/></td>
	  </tr>
	    <tr>
	      <td></td>
	      <td colspan="5">
	      <table bgcolor="lightgrey" border="1" cellspacing="0" width="800">
	      <xsl:if test="field">
	      <tr valign="top">
		<th align="left">Field</th>
		<th align="left">Position</th>
		<th align="left">Format</th>
		<th align="left">Enum</th>
		<th align="left">IsReg</th>
		<th align="left">Description</th>
	      </tr>
              </xsl:if>
	      <xsl:for-each select="field">
	      <tr valign="top">
		<td><xsl:value-of select="@id"/></td>
		<td><xsl:value-of select="@offset"/></td>
		<td><xsl:value-of select="@format"/></td>
		<td><xsl:value-of select="@enum"/></td>
		<td><xsl:value-of select="@makeRegister"/></td>
		<td><xsl:value-of select="@description"/></td>
	      </tr>
	      </xsl:for-each>
	      </table>
	      </td>
	    </tr>
	  </xsl:for-each>
	  </table>
	  </td>
         </tr>
   </xsl:template>


</xsl:stylesheet>
