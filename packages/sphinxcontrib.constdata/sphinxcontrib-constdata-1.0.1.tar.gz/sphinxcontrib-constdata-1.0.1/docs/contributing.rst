############
Contributing
############

We are looking to grow the project and get more contributors. Feel free to file bug reports, merge requests and feature requests.

*****************
Local development
*****************

#. Clone repository to your local computer.
#. Create and activate virtual environment::

    $ python3 -m venv venv
    $ . venv/bin/activate

#. Install dev dependencies::

    $ pip3 install -r dev-requirements.txt

#. Install pre-commit Git hook scripts::

    $ pre-commit install

Before push, do checks that CI do::

    # run mypy checks
    $ tox -e mypy

    # run tests
    $ tox

    # run style fix
    $ tox -e style