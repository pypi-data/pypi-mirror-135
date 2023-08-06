
# xmldt

This python 3 module is a reimplementation of the long living Perl module `XML::DT`.
It was rewritten taking in mind the pythonic way of writing code, but
guaranteeing the Down-Translate approach to process XML.

### Installing

Use `pip` to install the stable version

    $ pip install xmldt

### Synopsis

Start bootstrapping a processor using the `pydt` script:

    $ pydt -s sample.xml > sample_processor.py

### Contributing

 * to test: `pytest`
 * to check coverage: `pytest --cov`
 * to generate coverage report in HTML: `pytest --cov --cov-report=html`

### TODO

 * process multiple XML files at once
 * access parent from pcdata
 * look to the possibility of a `__begin__`
