Label role
==========

Default template (from settings): (expected1.html)

:constdata:label:`shortcuts.csv?FileSaveAs`

.. the following is not supported at this moment but kept for later "todo"

Custom title is a template. Not using ``{}`` placeholders: (expected2.html)

.. :constdata:label:`save as <menu.csv?FileSaveAs>`

Custom title is a template. Using ``{}`` placeholders without RST: (expected3.html)

.. :constdata:link:`{pc} (or {mac} on macOS) <menu.csv?FileSaveAs>`

Custom title is a template. Using ``{}`` placeholders and RST: (expected4.html)

.. :constdata:link:`**{pc}** (or *{mac}* on macOS) <menu.csv?FileSaveAs>`

Even more complex.... (expected5.html)

.. :constdata:link:`\`\`{pc}\`\` (or :kbd:\`{mac}\` on macOS) <menu.csv?FileSaveAs>`