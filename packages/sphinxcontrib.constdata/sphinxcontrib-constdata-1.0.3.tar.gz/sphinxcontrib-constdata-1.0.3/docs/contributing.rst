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

**************
How to release
**************

#. Tag commit that is new release with "vX.Y.Z".
#. Update tho this version in

   * the last line of ``sphinxcontrib/constdata/__ini__.py``::

        return {"version": "1.0.2", "parallel_read_safe": True}

   * ``version`` key in ``setup.cfg``::

        version =  1.0.2

#. Prepare to build and release::

        $ pip install build wheel twine
        $ rm -rf build
        $ python3 -m build
        $ twine check dist/sphinxcontrib_constdata_.....whl
        $ twine upload dist/*