Title as a template
===================

Custom title is a template. Not using ``{}`` placeholders: (expected_link7.html)

:constdata:link:`List of extensions <conf2.csv?extensions>`

Custom title is a template. Using ``{}`` placeholders without RST: (expected_link8.html)

:constdata:link:`{Variable} (from {Category} category) <conf2.csv?extensions>`

Custom title is a template. Using ``{}`` placeholders and RST: (expected_link9.html)

:constdata:link:`**{Variable}** (from *{Category}* category) <conf2.csv?extensions>`

Even more complex.... (expected_link10.html)

:constdata:link:`\`\`{Variable}\`\` (from :guilabel:\`{Category}\` category) <conf2.csv?extensions>`