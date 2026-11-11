# Run regression tests

Install runtime dependencies in an isolated environment, then use unittest's
explicit start directory from the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The existing tests exercise input-frame preservation, invalid numeric
filtering, and JSON root validation. They are ordinary Python unittest tests;
no pytest installation is required. Discovery with `-s tests` avoids depending
on whether the tests directory is an importable package.

For a focused investigation, discover one filename:

```bash
python -m unittest discover -s tests -p test_02_skip_invalid_numbers.py -v
```

Favor observable contracts: accepted and rejected rows, preserved source
values, input shape, and clear failure behavior. Use temporary input files
for reader tests. Mock the connection boundary when a unit test targets
orchestration; such a test does not establish that PostgreSQL accepts real
parameters or that privileges are correct.

Run database integration checks only against a disposable database with
explicit configuration. Keep synthetic fixtures small and avoid production
credentials. Record interpreter and package versions when reporting failures,
because `requirements.txt` currently has no version pins. A passing cleaner
test is not evidence that a nonempty database load succeeds.
