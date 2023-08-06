Warnings has wrong number
=========================

If table, or template has invalid RST, the reported warning has line number to a table/link/label.

The warning should be without a line and message should mention it is the error inside the table/temple, optionally with the line number inside a table/template.

Error in flatfile
-----------------

Actual warnings is ``Inline literal start-string without end-string."``.

.. constdata:table:: invalid_conf.yaml

Error in templates
------------------

Actual warning is ``Unknown interpreted text role "gui".``

Please see :constdata:label:`invalid_conf.yaml?project_copyright`.

Actual warning is ``Inline literal start-string without end-string.``

Please see :constdata:link:`invalid_conf.yaml?project_copyright`.