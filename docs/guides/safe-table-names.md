# Table names are trusted configuration

The loader currently interpolates `table_name` into CREATE TABLE and INSERT
statements using f-strings. A table name is an SQL identifier, not a regular
bound value. The command-line table argument must therefore come from trusted
configuration, never directly from a web request, uploaded filename, or other
untrusted input.

Until the SQL builder is hardened, use a reviewed simple identifier such as
`sales` or `sales_archive`. A conservative application-side allowlist can be:

```python
import re
name = "sales_archive"
if re.fullmatch(r"[a-z_][a-z0-9_]*", name) is None:
    raise ValueError("untrusted destination table name")
```

This example is an operational restriction, not a patch already applied by
the pipeline. It intentionally excludes schema-qualified names, quoted
identifiers, uppercase names, and punctuation. An allowlist of a few known
destinations is even easier to audit than accepting arbitrary names.

A proper implementation should compose identifiers using psycopg2's SQL
composition facilities and define schema/table handling explicitly. Parameter
placeholders protect data values but cannot simply stand in for identifiers.
Include regression coverage for malicious-looking and quoted names before
broadening the accepted interface. Restrict database privileges as a second
layer; an input validation convention alone is not a permission boundary.
