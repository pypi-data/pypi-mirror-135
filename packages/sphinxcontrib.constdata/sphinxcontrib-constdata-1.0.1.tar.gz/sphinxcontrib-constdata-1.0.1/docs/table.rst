###############
Listing a table
###############

.. rst:directive:: .. constdata:table:: path/to/flatfile

   List a flatfile in the argument as a table. For example::

       .. constdata:table:: conf.yaml

   Flatfile path is relative to :confval:`constdata_root` folder (``_constdata`` by default).

   Directive accepts a number of additional options - ``:query:``, ``:title:``, ``:header-rows:``, ``:stub-columns:``, ``:widths:``, ``:width:``, ``:align:`` - all optional and better described bellow.

Tutorial
********

Often, you need to print a table from external data.

#. At the project root, create ``_constdata`` folder. External file supported formats are CSV/JSON/YAML. For example, ``conf.yaml``:

   .. literalinclude:: _constdata/conf.yaml

#. In the ``conf.yaml``, ID column is *not* called ``id`` (:ref:`default ID column name <conf_id>`). Fix it::

      constdata_files = {
         "conf.yaml": {
            "id": "Variable"
         }
      }

#. In a |rst| document, use table directive to print the file as a table::

      Incididunt occaecat irure dolore voluptate occaecat officia magna mollit.

      .. constdata:table:: conf.yaml

      Minim aliqua sit officia mollit dolore Lorem.

#. It will print a table from the file as-is:

   Incididunt occaecat irure dolore voluptate occaecat officia magna mollit.

   .. constdata:table:: conf.yaml

   Minim aliqua sit officia mollit dolore Lorem.

Templating
**********

.. include:: table-templates-not-supported.inc.rst

Query
*****

The basic usage ``.. constdata:table:: conf.yaml`` will print the table as 1:1 to the flatfile - columns and rows are as found in the flatfile.

The most common option is ``:query:`` that specify `SQLite SELECT <https://sqlite.org/lang_select.html>`_ for the table.

If you omit the query, it is actually

::

    .. constdata:table:: conf.yaml
       :query: select * from "conf.yaml"

.. important::

   Even if you use ``:query:`` option, you can't omit directive argument. I.e.

   ::

      .. constdata:table::
         :query: select * from "conf.yaml"

   will cause en error.

.. important::

   Query allows you to specify any "from" table. However, use the same table as in the argument, please.

The query must returns *some rows*, otherwise a warning will appear.

Quoting
-------

The SQLite SELECT needs proper quoting of values, and table and column names:

* table name, because it contains a dot, has to be in double quotes
* best practice is to double quote all table and column names
* values are in single quotes

For example::

   .. constdata:table:: conf.yaml
      :query: select * from "conf.yaml" where "Category" = 'Project information'

Without double quoting a table name, the "table not found" error will raise.

Query examples
--------------

Row ordering and filtering::

    .. constdata:table:: conf.json
       :query: select "Variable", "Description" from "conf.json" where "Category" = 'Project information' order by "Description"

Reorder or exclude columns::

    .. constdata:table:: conf.json
       :query: select "Category", "Variable" from "conf.json"

You can use |rst| in columns, but values are not :ref:`templates <templating>` (can't use ``{}`` placeholders to refer other columns). Also, it breaks possibility to :doc:`translate files <l10n>` in multilingual documentations.

::

    .. constdata:table:: conf.json
       :query: select "Variable", "Description" as "Help text (*shortened*)" from "conf.json" where "Category" = 'Project information' order by "Description"

Be aware of renaming and excluding ID column! If you do it, the error "no ID column" will appear. E.g., we omit ID column ``Variable``::

    .. constdata:table:: menu3.csv
       :query: select "Path" from "menu3.csv"

Other options
*************

title
-----

Optional table title, default none.

::

    .. constdata:table:: conf.yaml
       :title: Configuration parameters

header-rows
-----------

Number of rows in the file considered as header, default 1.

stub-columns
------------

Number of columns (from the left) in the file considered as header, default 0.

align
-----

Values: ``left``, ``center``, or ``right``.

The horizontal alignment of the table.

width
-----

Values: length or percentage.

Sets the width of the table to the specified length or percentage of the line width. If omitted, the renderer determines the width of the table based on its contents or the column widths.

widths
------

Values: ``auto``, ``grid``, or a list of integers.

A list of relative column widths. The default is the width of the input columns (in characters).

* ``auto`` delegates the determination of column widths to the backend (LaTeX, the HTML browser, ...).
* ``grid`` restores the default, overriding a table_style or class value "colwidths-auto".

.. _multiple-same-tables:

The same table multiple times
*****************************

You can list the file as a table on multiple places across the project, but it is not a recommended practice.

.. rubric:: Same table across different pages

If the file is multiple times listed as table across the project, the links will point to "random" of them. You can't guarantee to what table links will actually point to.

``one.rst``:

.. code-block::

   Please see :constdata:link:`conf.json?project_copyright`.

   .. constdata:table:: conf.yaml

   Please see :constdata:link:`conf.json?project_copyright`.

``second.rst``:

.. code-block::

   Please see :constdata:link:`conf.json?project_copyright`.

   .. constdata:table:: conf.yaml

   Please see :constdata:link:`conf.json?project_copyright`.

.. rubric:: Same table on the same page

Listing the same table on the same page is even worse. E.g.:

::

    .. constdata:table:: conf.yaml

    .. constdata:table:: conf.yaml

Second occurence will cause warning like :samp:`WARNING: Duplicate explicit target name: "constdata-conf-yaml-{<id>}".` for each row.

Wrong error line number
***********************

If table (flatfile) has invalid |rst|, the reported warning has wrong line number.

.. note:: We are aware of this issue and, hopefully, `fix it soon <https://gitlab.com/documatt/sphinxcontrib-constdata/-/issues/4>`_.

For example, you did a typo in ``:doc:`` link in a CSV file::

    "extensions","General configuration","A list of :doc:`extensions <extensionx>`."

It causes in output ``index.rst:17:unknown document: extensionx``, but table directive is on line 10.