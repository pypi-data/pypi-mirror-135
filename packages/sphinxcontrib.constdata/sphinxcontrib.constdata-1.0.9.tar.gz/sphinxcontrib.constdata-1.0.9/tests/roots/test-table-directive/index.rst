Table directive
===============

.. Many identical menu.csv is symlinked under names menuN.csv to
   - prevent "Duplicate explicit target name: xxx" error
   - identify particular table directive usage in HTML output

Basic usage
***********

No options: (expected1.html)

.. constdata:table:: menu1.csv

Query
*****

"select \*" query: (expected2.html)

.. constdata:table:: menu2.csv
   :query: select * from "menu2.csv"

Query excluding non-ID column: (expected3.html)

.. constdata:table:: menu3.csv
   :query: select "id" from "menu3.csv"

Query excluding ID column will cause "no ID column with name 'id'": (expected4.html)

.. constdata:table:: menu4.csv
   :query: select "Path" from "menu4.csv"

Query renaming non-ID column "Path": (expected5.html)

.. constdata:table:: menu5.csv
   :query: select "id", "Path" as "Menu" from "menu5.csv"

Query renaming ID column "id" causes error "no ID column with name 'id'": (expected6.html)

.. constdata:table:: menu6.csv
   :query: select "id" as "Code", "Path" from "menu6.csv"

Query re-ordering rows: (expected7.html)

.. constdata:table:: menu7.csv
   :query: select * from "menu7.csv" order by "Path"

Query limiting rows: (expected8.html)

.. constdata:table:: menu8.csv
   :query: select * from "menu8.csv" where "Path" = 'File --> Save As...'

Options
*******

Options: (expected9.html)

.. constdata:table:: menu9.csv
   :title: Custom title
   :header-rows: 2
   :stub-columns: 1
   :widths: 30,70
   :width: 50%
   :align: right

Errors
******

Query with empty result: (expected10.html)

.. constdata:table:: menu10.csv
   :query: select * from "menu10.csv" where "id" = 'nonexisting'

The same table again causes error "Duplicate explicit target name" for each row:

.. constdata:table:: menu1.csv