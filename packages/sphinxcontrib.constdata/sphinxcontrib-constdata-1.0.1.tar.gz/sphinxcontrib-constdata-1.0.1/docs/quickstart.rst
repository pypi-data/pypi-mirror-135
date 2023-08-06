##########
Quickstart
##########

An typical app contains tons of various labels shown in UI (form fields labels, button labels, menu selection labels, ...), configuration parameter names, permission names, business object states, and many other *constant and externally managed data*.

If you document an app, you often write something like::

   To save a document, you can either

   * choose menu item File --> Save As
   * press Shift+Ctrl+S (PC) or Shift+Cmd+S (Mac)

   Document's author will be set to a value of the author configuration parameter.

   Available configuration parameters are:

   +-------------------+-------------------------------------+
   |   Parameter       |                Description          |
   +===================+=====================================+
   | author            | The author name(s) of the document. |
   +-------------------+-------------------------------------+
   | project_copyright | An alias of ``copyright``.          |
   +-------------------+-------------------------------------+

Above fragment contains many hard-coded values that are out-of-control of you, a tech writer, like "File", "Save As", "Shift+Ctrl+S", configuration parameters names and their description.

Developers or translators may change them without noticing you. Huh, yes - if the app supports multiple languages, you have to find out and hard-code translation of these constants for each language! Nightmare.

*********
Flatfiles
*********

This is where |project| comes to the rescue. Developers gave you all app strings in one or more text CSV/JSON/YAML files that you refer from the docs. It allows you to reuse values from external file in the documentation. If the file has changed, the documentation is updated too. From this point, we will refer external files as *flatfiles*.

Create ``_constdata`` folder under your sources (in the folder with ``conf.py``) and put flatfiles here. (This place can be changed with :confval:`constdata_root` configuration value.)

In above example, we will work with three flatfiles - menu selections, keyboard shortcuts, and configuration parameters. It doesn't matter if one is CSV, second JSON and third in YAML. CSV is the most concise, but YAML the most human-friendly - just use the format you prefer.

.. tabs::

   .. group-tab:: CSV

      .. literalinclude:: ../tests/samples/menu.csv
         :caption: menu.csv

   .. group-tab:: JSON

      .. literalinclude:: ../tests/samples/menu.json
         :caption: menu.json

   .. group-tab:: YAML

      .. literalinclude:: ../tests/samples/menu.yaml
         :caption: menu.yaml

.. tabs::

   .. group-tab:: CSV

      .. literalinclude:: ../tests/samples/shortcuts.csv
         :caption: shortcuts.csv

   .. group-tab:: JSON

      .. literalinclude:: ../tests/samples/shortcuts.json
         :caption: shortcuts.json

   .. group-tab:: YAML

      .. literalinclude:: ../tests/samples/shortcuts.yaml
         :caption: shortcuts.yaml

.. tabs::

   .. group-tab:: CSV

      .. literalinclude:: ../tests/samples/conf.csv
         :caption: shortcuts.csv

   .. group-tab:: JSON

      .. literalinclude:: ../tests/samples/conf.json
         :caption: conf.json

   .. group-tab:: YAML

      .. literalinclude:: ../tests/samples/conf.yaml
         :caption: conf.yaml

Read more in :doc:`flatfiles`.

************
Added markup
************

|project| adds three new markup constructions to the Sphinx:

* role :rst:role:`constdata:label` to print a single value from flatfile
* role :rst:role:`constdata:link` to create a link inside table from flatfile
* directive :rst:dir:`constdata:table` to print a table from flatfile

Both :rst:role:`constdata:label` and :rst:role:`constdata:link` takes URI telling which flatfile and ID of a row inside a flatfile as an URI query parameter. For example:

::

    * choose menu item :constdata:label:`menu.yaml?FileSaveAs`

and

::

   Document's author will be set to a value of the :constdata:link:`conf.yaml?author` configuration parameter.

Read more in :doc:`label` and :doc:`link`.

:rst:dir:`constdata:table` accept URI to flatfile only and prints it content as-is. For example::

   .. constdata:table:: conf.yaml

If you want to print only specific rows, sort differently, etc. pass SQL SELECT to its ``:query:`` option::

   .. constdata:table:: conf.yaml
      :query: select * from "conf.yaml" where "group" = 'meta'

Read more in :doc:`table`.

*********
ID column
*********

Back to basics. You need to learn how things work on the most common markup - the label role. E.g.,:

::

    * choose menu item :constdata:label:`menu.yaml?FileSaveAs`
    * press :constdata:label:`shortcuts.yaml?FileSaveAs`

will lookup row with ID ``FileSaveAs`` in ``menu.yaml`` and ``shortcuts.yaml``.

Every flatfile needs an *ID column*. In ``menu.yaml`` and ``shortcuts.yaml``, ID column has name ``id``. This is default value, but if the column has different name, as in ``conf.yaml``, you need to set it ``conf.py`` within :confval:`constdata_files` variable::

   constdata_files = {
      "conf.yaml": {
         "id": "Variable"
      }
   }

.. _templating:

**********
Templating
**********

We will have to tell what column of a matching row to print. Without configuration

::

   * choose menu item :constdata:label:`menu.yaml?FileSaveAs`
   * press :constdata:label:`shortcuts.yaml?FileSaveAs`

will result to::

   * choose menu item menu.yaml?FileSaveAs
   * press shortcuts.yaml?FileSaveAs

Not very useful. Also, warnings like this will appear in log::

   WARNING: Missing :constdata:label: template for 'menu.yaml'.
   WARNING: Missing :constdata:link: template for 'menu.yaml'.

What are *templates*? It is a |rst| string that will be injected instead of |project| markup, then rendered by Sphinx as if it would be written in the document. It can contain variable parts within ``{`` and ``}`` that will be replaced with a value from flatfile.

Label templates
===============

Let's define templates for label role, i.e. a |rst| fragment you want to actually write instead of label role. In your ``conf.py``, in :confval:`constdata_files` variable::

   constdata_files = {
      "menu.yaml": {
         "label": ":menuselection:`{Path}`"
      },
      "shortcuts.yaml": {
         "label": ":kbd:`{pc}` (PC) or :kbd:`{mac}` (Mac)"
      }
   }

As said above, columns from flatfile are in ``{curly}`` brackets, the rest is plain |rst|. I.e., the previous example says that

* labels coming from ``menu.yaml`` should be rendered with value in column ``Path`` on matching row, wrapped into ``:menuselection:`` role.
* labels coming from ``shortcuts.yaml`` should be rendered with values from columns ``pc`` and ``mac`` on matching row.

.. important::

   * Column name in ``{curly}`` brackets is case sensitive. If a flatfile contains ``mac`` column, ``{Mac}`` will not work!
   * Only curly brackets style (``{column}``) is supported. A dollar brackets (``${column}``) is the dollar character and a column placeholder. E.g. ``Hello ${name}`` will become ``Hello $Joe``, not ``Hello Joe``.

Actual output (before Sphinx will render it) will be now::

   * choose menu item :menuselection:`File --> Save As...`
   * press :kbd:`Shift+Ctrl+S` (PC) or :kbd:`Shift+Cmd+S` (Mac)

Link templates
==============

Similarly, the link role

::

   Document's author will be set to a value of the :constdata:link:`conf.yaml?author` configuration parameter.

without its template will warn and produce

::

   Document's author will be set to a value of the conf.yaml?author configuration parameter.

Setting |rst| template for link role will help::

   constdata_files = {
      ...
      "conf.yaml": {
         "link": "``{id}``"
      }
   }

It will instruct |project| to create a link pointing to a row inside table with ``author`` ID. The link title (link text) will be value from ``id`` column displayed as :doc:`inline literal <rstref:element/inline-literal>`.

.. important:: |project| allows inline element nesting :ref:`normally impossible <rstref:no-nested-inlines>` in |rst|.

The result in (not a valid |rst|!) could looks like::

   Document's author will be set to a value of the :ref:```author`` <conf-author>` configuration parameter.

Table templates
===============

.. include:: table-templates-not-supported.inc.rst

******
Tables
******

Last added markup, :rst:dir:`constdata:table` directive, prints a table from a flatfile::

   .. constdata:table:: permissions.yaml

or, result of a query to the flatfile::

   .. constdata:table:: permissions.yaml
      :query: select * from "permissions.yaml" where "group" = 'meta'

Query syntax is actually `SQLite SELECT <https://www.sqlite.org/lang_select.html>`_ syntax.

Please note strict quoting tables and column names in ``"`` (double quotes) and values with ``'`` (single quotes). Any identifier containing ``.`` (dot) needs to be, in Sqlite, quoted in double quotes. See `SQLite manpage on keywords <https://www.sqlite.org/lang_keywords.html>`_.

****************
Tables and links
****************

Tables and links are tight companions. :constdata:link: creates links to rows inside constdata:table:. In other words, to make links to a table, it is necessary to list it as a table.

.. note:: Indeed, you might have table that has no links to it.

Put table directive on a proper place in your documentation. For example, in ``reference.rst`` page or "Reference" section.

::

   .. constdata:table:: conf.yaml

Now, the rows printed in a table could be referred anywhere else with link role.

::

   Document's author will be set to a value of the :constdata:link:`conf.yaml?author` configuration parameter.

Links may appear in the text before tables, or vice-versa. The important is to have both link and table that shows row reffered from a link.

************
Localization
************

Many documentations are multilingual and constant data will be different for different languages. Hopefully, |project| includes localization of flatfiles.

It handles it similarly as Sphinx handles translating regular ``.rst`` files. |project| integrates with Sphinx standard gettext builder (invoked by ``make gettext``), and creates ``constdata.pot`` with extracted values from flatfiles. Extracted strings are translated with the same `Sphinx internationalization <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`_ mechanism as the rest of the documentation.

Translatable string is anything between ``_('``/``_('''``/``_("``/``_("""`` and ``')``/``'')``/``")``/``""")``, i.e. single and triple quotes.

For example, assume all menu selection paths in ``menu.yaml`` are language sensitive:

.. literalinclude:: ../tests/samples/menu_gettext.yaml

Workflow is identical as if localizing the docs itself - you invoke gettext builder (e.g., ``make gettext``). Beside ``.pot``\s created by Sphinx from the docs, a new ``constdata.pot`` file will appear along with them.

::

    $ make gettext
    $ cd build/gettext
    $ ls
    calling.pot
    configuration.pot
    constdata.pot
    glossary.pot
    index.pot
    ...

************
Naked syntax
************

You can use shorted "naked" syntax - ``:label:`` instead of ``:constdata:label:``, ``:link:`` instead of ``:constdata:link:``, and ``.. table::`` instead of ``.. constdata:table::`` if you set constdata as `default Sphinx domain <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-primary_domain>`_.

Globally, in ``conf.py`` set::

   primary_domain = "constdata"

Or, for particular point in document and bellow with `default-domain <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-default-domain>`_ directive:

.. literalinclude:: ../tests/roots/test-naked-syntax/index.rst

*********
Thats all
*********

Now you understand the basic usage. Previous fragment, but rewritten with |project|:

.. tabs::

   .. tab:: full domain syntax

      ::

         To save a document, you can either

         * choose menu item :constdata:label:`menu.yaml?FileSaveAs`
         * press :constdata:label:`shortcuts.yaml?FileSaveAs`

         Document's author will be set to a value of the :constdata:link:`conf.yaml?author` configuration parameter.

         Available configuration parameters are:

         .. constdata:table:: conf.yaml

   .. tab:: naked syntax

      ::

         To save a document, you can either

         * choose menu item :label:`menu.yaml?FileSaveAs`
         * press :label:`shortcuts.yaml?FileSaveAs`

         Document's author will be set to a value of the :link:`conf.yaml?author` configuration parameter.

         Available configuration parameters are:

         .. table:: conf.yaml

Now, the docs are independent of the current names for UI control labels, config param names, etc. If somebody decides that a better name for "Advanced" button label is "Expert", and you or script update the flatfile, the docs will reflect the change on the next build. The ideal is to fetch constdata files directly from DB or source code repository provided by the developers during docs CI/CD build.