#############
Configuration
#############

|project| expects configuration via multiple ``constdata_*`` variables in ``conf.py``.

constdata_root
**************

.. confval:: constdata_root

Relative path to a folder with external flatfiles in CSV, JSON or YAML format. Path is relative to ``conf.py``. Default value is ``_costdata``.

constdata_files
***************

.. confval:: constdata_files

Configuration of individual flatfiles. It is a dict (a mapping) of flatfiles to their configuration. The key is path to a flatfile (including suffix), relative to :confval:`constdata_root`.

::

    constdata_files = {
        "menu.yaml": {
            # ..configuration..
        },
        "path/to/shortcuts.yaml": {
            # ..configuration..
        }
    }

The value is actual configuration for a flatfile (the most important are templates). It is also a dict. Available keys are:

* .. _conf_id:

  ``id`` -- name of ID column. By default it is ``id``. If ID column has different name, you have to tell it here.

  The ID column name is case sensitive. E.g., if you set ``Variable``, but the file contains ``variable``, "ID column not found" error will appear. It also applies to the default value ``id`` - ``ID``, ``iD``, etc. will all cause the error.

  ::

      constdata_files = {
        "conf.yaml": {
            "id": "Variable"
        }

* .. _conf_label:

  ``label`` -- |rst| template for :rst:role:`constdata:label` role. See :ref:`templating`.

  E.g., labels coming from ``shortcuts.yaml`` should be rendered with values from columns ``pc`` and ``mac`` on matching row.

  ::

      constdata_files = {
        "shortcuts.yaml": {
            "label": ":kbd:`{pc}` (PC) or :kbd:`{mac}` (Mac)"
        }

* ``link`` -- |rst| template for :rst:role:`constdata:link` role. See :ref:`templating`.

  E.g., links to table listing ``conf.yaml`` should have the link title (link text) from ``id`` column rendered as :doc:`inline literal <rstref:element/inline-literal>`.

  ::

      constdata_files = {
        "conf.yaml": {
            "link": "``{id}``"
        }

.. include:: table-templates-not-supported.inc.rst

constdata_files_encoding
************************

.. confval:: constdata_files_encoding

Encoding used for reading flatfiles. By default, it is platform specific. We recommend set it to standard UTF-8.

::

    constdata_files_encoding = "utf-8"

See :ref:`flatfiles-encoding`.

constdata_csv_format
********************

.. confval:: constdata_csv_format

Customize the format of CSV files. Value is a dict of attributes and values.

|project| uses standard Python 3 csv module which allows to customize the format of *your* CSV files. See csv module `Formatting Parameters <https://docs.python.org/3/library/csv.html#csv-fmt-params>`_ documentation for list of attributes.

::

    constdata_csv_format = {
        "delimiter": ";",
        "doublequote": False
    }

See :ref:`flatfiles-csv-format`.