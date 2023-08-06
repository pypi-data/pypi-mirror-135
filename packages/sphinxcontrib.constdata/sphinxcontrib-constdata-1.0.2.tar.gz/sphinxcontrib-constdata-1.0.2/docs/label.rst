**********************
Getting a single value
**********************

.. rst:role:: constdata:label

   Lookup and print a single value in the file by its ID.

   Takes URI telling which flatfile and ID of a row inside a flatfile as an URI query parameter. For example::

      Go to the :constdata:label:`menu.yaml?FileSaveAs` option.

   will lookup row with ID ``FileSaveAs`` in ``menu.yaml``.

   Flatfile path is relative to :confval:`constdata_root` folder (``_constdata`` by default).

Tutorial
********

.. todo: link to rst ref

Label role is the most common markup added by |project|.

#. At the project root, create ``_constdata`` folder. External file supported formats are CSV/JSON/YAML. For example, ``menu.yaml``:

   .. literalinclude:: _constdata/menu.yaml

#. In ``conf.py``, set the :ref:`template <templating>` that will be used to render values from the file. We want to print menu path (column ``Path``) within ``:menuselection:``::

      constdata_files = {
         "menu.yaml": {
            "label": ":menuselection:`{Path}`"
         }
      }

#. Somewhere in a |rst| document, use link role to print a value from ``menu.yaml``::

      Go to the :constdata:label:`menu.yaml?FileSaveAs` option.

#. This says that labels coming from ``menu.yaml`` should be rendered with value in column ``Path`` wrapped into ``:menuselection:`` role. Actual output (before Sphinx will process it) will be now::

      Go to the :menuselection:`File --> Save As...` option.

#. The result is:

   Go to the :constdata:label:`menu.yaml?FileSaveAs` option.


.. Label does not support inline templates (inside role text).