##########
Flatfiles
##########

Flatfiles are external text files in CSV, JSON or YAML format that appear in the documentation thanks to |project|. Flatfiles are during build `cached <Caching_>`_ as table in a database, thus we talk about tables, column, rows, cells etc.

The requirements to all formats are:

* first row contains column names
* if not :ref:`overriden <conf_id>`, there must exist a column named ``id`` (case-sensitive)
* ID column must contain unique values across the table (will become primary key)

***
CSV
***

Traditional and concise data exchange format is CSV.

However, CSV is not very human-friendly, especially if it comes to multilines values. For example:

.. literalinclude:: ../tests/samples/conf.csv

.. _flatfiles-csv-format:

CSV format
==========

The CSV (Comma Separated Values) format is very common import/export format. CSV file standard is described in :rfc:`4180`. Unfortunatelly, many applications don't adhere to this stadnard. They use different delimiters, support/doesn't support comments, quoting characters, etc. The most terrifying example is Microsoft Excel that produce different CSVs depending on its version and language.

|project| uses standard Python 3 csv module which allows to customize the format of *your* CSV files. See csv module `Formatting Parameters <https://docs.python.org/3/library/csv.html#csv-fmt-params>`_ documentation for list of attributes.

Enter these attributes as a dict pairs of :confval:`constdata_csv_format`. For example, to change delimiter to ``;`` and disable doubling quoting:

::

    constdata_csv_format = {
        "delimiter": ";",
        "doublequote": False
    }

****
JSON
****

Popular JSON format is also supported.

* Top-level value of a JSON must be an array.
* Array items are objects representing individual rows.
* Comments are not supported.

JSON is more human-frendly, but verbose and has difficult newlines handling. For example:

.. literalinclude:: ../tests/samples/conf.json

****
YAML
****

YAML is likely the most suitable format for external data. Editing it is human-friendly, is relatively concise, and multilines strings are easy.

* File may have both ``.yaml`` and ``.yml`` suffix.
* Top-level of YAML document is a list.
* List items are mappings representing rows.

.. literalinclude:: ../tests/samples/conf.yaml

********
Caching
********

For faster operation and querying functionality, |project| stores all flatfiles to a internal Sqlite database. On the initial build, every file found in :confval:`constdata_root` is cached as a table in the database.

Database file is ``<outdir>/constdata.db`` (e.g. ``_build/html/constdata.db`` for HTML builder). Table name is flatfile path relative to :confval:`constdata_root` including an extension (e.g. ``chat/menuselection.csv`` is path and table name too)

All paths in label, link and table markup are actually table names in cache DB.

.. caution::

   If you modify a flatfile, the change is *not* automatically detected and reflected on the next Sphinx build. You have to peform a clean build (e.g., delete ``_build/html`` output) to update all affected documents where external data were used.

   `We know <https://gitlab.com/documatt/sphinxcontrib-constdata/-/issues/5>`_ it is annoying flaw and hopefully fix it soon. Thanks for your patience!

.. _flatfiles-encoding:

*********
Encoding
*********

By default, flatfiles are read in platform default encoding. It is likely UTF-8 for most Linux and macOS users. Windows platform encoding varies according to the Windows language.For example, central European Windows uses Windows-1250 (ISO-8859-2).

In all cases, we recommend to use and force the single encoding via :confval:`constdata_files_encoding`.

::

    constdata_files_encoding = "utf-8"