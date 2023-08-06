########################
Links to rows in a table
########################

.. rst:role:: constdata:link

   Create a link to the row of a table previously listed with the :rst:dir:`constdata:table` directive.

   Takes URI telling which flatfile and ID of a row inside a flatfile as an URI query parameter. For example::

      Set :constdata:link:`conf.yaml?author` configuration parameter.

   will create a link to the row with ID ``author`` inside table listing ``conf.yaml`` file.

   Flatfile path is relative to :confval:`constdata_root` folder (``_constdata`` by default).

Tutorial
********

Link role is the special one. It cannot work without its table directive couterpart.

#. At the project root, create ``_constdata`` folder. External file supported formats are CSV/JSON/YAML. For example, ``conf2.yaml``:

   .. literalinclude:: _constdata/conf2.yaml

#. In the ``conf.py``, set the :ref:`template <templating>` that will be used to render values from the file. We want to print configuration parameter name (column ``Variable``) within ````two backticks```` (literal text)::

      constdata_files = {
         "conf2.yaml": {
            "link": "``{Variable}``"
         }
      }

#. In the ``conf2.yaml``, ID column is *not* called ``id`` (:ref:`default ID column name <conf_id>`). Fix it::

      constdata_files = {
         "conf2.yaml": {
            "link": "``{Variable}``",
            "id": "Variable"
         }
      }

#. Somewhere in the documentation, print the file as a table::

      .. constdata:table:: conf2.yaml

#. Elsewhere in the documentation, create the link to ``author`` row::

      Set :constdata:link:`conf2.yaml?author` configuration parameter.

#. The actual result is:

   .. constdata:table:: conf2.yaml

   Set :constdata:link:`conf2.yaml?author` configuration parameter.

Inline template
***************

The link roles can accept text in either

* ``target`` style and the template must be configured in ``constdata_files``\'s :ref:`label template <conf_label>` attribute in the ``conf.py``. Otherwise, ``WARNING: Missing :constdata:link: template for 'yxz'.`` will appear.
* or ``template <target>`` style, where template is regular :ref:`template <templating>` and ``constdata_files`` template is not required. Inline template takes precedence.

Target is just a path to the flatfile with ID row as a query parameter. For example::

   :constdata:link:`conf2.csv?extensions`

Template may be plain text not using ``{}`` placeholders::

   :constdata:link:`List of extensions <conf2.csv?extensions>`

Using ``{}`` placeholders without |rst|::

   :constdata:link:`{Variable} (from {Category} category) <conf2.csv?extensions>`

Using ``{}`` placeholders and |rst|::

   :constdata:link:`**{Variable}** (from *{Category}* category) <conf2.csv?extensions>`

But inline template could easily become difficult to write due to necessary |rst| quoting::

   :constdata:link:`\`\`{Variable}\`\` (from :guilabel:\`{Category}\` category) <conf2.csv?extensions>`

So, generally, we recommend to write templates in ``constdata_files``. The previous template but in ``conf.py``::

     constdata_files = {
         "conf.csv": {
            "link": "``{Variable}`` (from :guilabel:`{Category}` category)"
         }
      }

Links to multiple times listed tables
*************************************

Link and table work based on the standard |rst| `internal hyperlink targets <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#internal-hyperlink-targets>`_. Each row listed with table directive, is prefixed with a target name based on flatfile and ID value. Link role is actually a standard reference to it.

If you list the same row multiple times::

   The table
   ---------

   .. constdata:table:: conf.json

   Same table again
   ----------------

   .. constdata:table:: conf.json

And, link to it::

   Please see :constdata:link:`conf.json?project_copyright`.

You never know to which table, the link will actually point to. Thus, it is not recommended to print the same table multiple times.

Read more at :ref:`multiple-same-tables`.