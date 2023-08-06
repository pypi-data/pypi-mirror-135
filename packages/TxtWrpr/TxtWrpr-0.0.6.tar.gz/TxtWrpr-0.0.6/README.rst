A wrapper for fixed column text files

    This module copies a fixed column TXT file into a dictionary to manipulate, and enrich. It can also be exported into a TXT file with a different structure than the original file.

=======
Testing
=======

This project uses ``pytest`` to run tests and also to test docstring examples.

Install the test dependencies.

.. code-block:: bash

    $ pip install -r requirements_test.txt

Run the tests.

==========
Developing
==========

This project uses ``black`` to format code and ``flake8`` for linting. We also support ``pre-commit`` to ensure these have been run. To configure your local environment please install these development dependencies and set up the commit hooks.

.. code-block:: bash

    $ pip install black flake8 pre-commit
    $ pre-commit install

=========
Releasing
=========

Releases are published automatically when a tag is pushed to GitHub.

.. code-block:: bash

    # Set next version number
    export RELEASE = x.x.x

    # Create tags
    git commit --allow -empty -m "Release $RELEASE"
    git tag -a $RELEASE -m "Version $RELEASE"

    # Push
    git push upstream --tags

