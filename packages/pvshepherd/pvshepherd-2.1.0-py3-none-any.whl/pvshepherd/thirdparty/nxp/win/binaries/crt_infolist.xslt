<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
    <h2>List of Chips and Boards for one vendor</h2>
    <table border="1" width="1000" cellspacing="0"><Caption><EM>Chips and Boards</EM></Caption>
    <tr bgcolor="#9acd32">
      <th align="left">Vendor</th>
      <th align="left">Name</th>
      <th align="left">Chip</th>
      <th align="left">Version</th>
      <th align="left">Family</th>
      <th align="left">Proc</th>
      <th align="left">Vendor Full Name</th>
      <th align="left">Stub</th>
    </tr>
    <xsl:for-each select="infoList/info">
    <tr>
      <td><xsl:value-of select="../@vendor"/></td>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="@chip"/></td>
      <td><xsl:value-of select="chip/name/@ver"/></td>
      <td><xsl:value-of select="chip/family"/></td>
      <td><xsl:value-of select="@proc"/></td>
      <td><xsl:value-of select="chip/vendor"/></td>
      <td><xsl:value-of select="@stub"/></td>
    </tr>
    <tr>
      <td></td>
      <td colspan="6">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">Rst Board</th>
          <th align="left">Rst Sys</th>
          <th align="left">Rst Proc</th>
	  <th align="left">Clock freq</th>
	  <th align="left">Changeable</th>
	  <th align="left">Accurate</th>
          <th align="left">Chip Name</th>
        </tr>
	<xsl:for-each select="chip">
	<tr>
	  <td><xsl:value-of select="reset/@board"/></td>
	  <td><xsl:value-of select="reset/@sys"/></td>
	  <td><xsl:value-of select="reset/@core"/></td>
	  <td><xsl:value-of select="clock/@freq"/></td>
	  <td><xsl:value-of select="clock/@changeable"/></td>
	  <td><xsl:value-of select="clock/@is_accurate"/></td>
	  <td><xsl:value-of select="name"/></td>
	</tr>
	</xsl:for-each>
     </table>
     </td>
    </tr>
    <tr>
      <td></td>
      <td colspan="6">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">Memory</th>
          <th align="left">ID</th>
          <th align="left">Type</th>
	  <th align="left">Size</th>
	  <th align="left">RO</th>
	  <th align="left">WO</th>
          <th align="left">Volatile</th>
          <th align="left">Can Program</th>
        </tr>
	<xsl:for-each select="chip/memory">
	<tr>
	  <td><xsl:value-of select="../memory"/></td>
	  <td><xsl:value-of select="@id"/></td>
	  <td><xsl:value-of select="@type"/></td>
	  <td><xsl:value-of select="@size"/></td>
	  <td><xsl:value-of select="@is_ro"/></td>
	  <td><xsl:value-of select="@is_wo"/></td>
	  <td><xsl:value-of select="@is_volatile"/></td>
	  <td><xsl:value-of select="@can_program"/></td>
	</tr>
	</xsl:for-each>
     </table>
     </td>
    </tr>
    <tr>
      <td></td>
      <td colspan="6">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">Memory Instance ID</th>
          <th align="left">Derived From</th>
          <th align="left">Location</th>
	  <th align="left">Size</th>
	  <th align="left">Enable</th>
        </tr>
	<xsl:for-each select="chip/memoryInstance">
	<tr>
	  <td><xsl:value-of select="@id"/></td>
	  <td><xsl:value-of select="@derived_from"/></td>
	  <td><xsl:value-of select="@location"/></td>
	  <td><xsl:value-of select="@size"/></td>
	  <td><xsl:value-of select="@enable"/></td>
	</tr>
	</xsl:for-each>
     </table>
     </td>
    </tr>
    <tr>
      <td></td>
      <td colspan="6">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">Prog Flash</th>
          <th align="left">Location</th>
          <th align="left">Size</th>
	  <th align="left">Block Size</th>
	  <th align="left">Word Size</th>
	  <th align="left">Self Erase</th>
	  <th align="left">Read While prog</th>
	  <th align="left">Prog with Code</th>
	  <th align="left">Algorithm Name</th>
	  <th align="left">Max Prog Buff</th>
        </tr>
	<xsl:for-each select="chip/prog_flash">
	<tr>
	  <td><xsl:value-of select="../prog_flash"/></td>
	  <td><xsl:value-of select="@location"/></td>
	  <td><xsl:value-of select="@size"/></td>
	  <td><xsl:value-of select="@blocksz"/></td>
	  <td><xsl:value-of select="@wordsz"/></td>
	  <td><xsl:value-of select="@self_erase"/></td>
	  <td><xsl:value-of select="@readwhileprog"/></td>
	  <td><xsl:value-of select="@progwithcode"/></td>
	  <td><xsl:value-of select="@algoName"/></td>
	  <td><xsl:value-of select="@maxPrgBuff"/></td>
	</tr>
	</xsl:for-each>
     </table>
     </td>
    </tr>
    <tr>
      <td></td>
      <td colspan="6">
      <table border="1" cellspacing="0" width="900">
        <tr>
          <th align="left">Peripheral Instance ID</th>
          <th align="left">Derived From</th>
          <th align="left">Location</th>
	  <th align="left">Enable</th>
        </tr>
	<xsl:for-each select="chip/peripheralInstance">
	<tr>
	  <td><xsl:value-of select="@id"/></td>
	  <td><xsl:value-of select="@derived_from"/></td>
	  <td><xsl:value-of select="@location"/></td>
	  <td><xsl:value-of select="@enable"/></td>
	</tr>
	</xsl:for-each>
     </table>
     </td>
    </tr>


    </xsl:for-each>

    </table>

  </body>
  </html>
</xsl:template>
</xsl:stylesheet>
