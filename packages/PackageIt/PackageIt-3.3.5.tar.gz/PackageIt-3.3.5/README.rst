.. image:: https://img.shields.io/pypi/v/PackageIt
    :alt: PyPi

Managing the scaffolding and VCS for new and existing Python Packages.

    Use a configuration (.ini) file to: 1. Create the "scaffolding" for a new package. 2. Examine existing scaffolding and add missing components like directories and files. 3. Version control 4. Apply PEP8 via Black 5. Update Git and GitHub 6. Upload to PyPi 7. PEP12 doc strings 8. Create a virtual environment for the project 9. Special thanks to Jacob Tomlinson. This application is based on his article `Creating an open source Python project from scratch <https://jacobtomlinson.dev/series/creating-an-open-source-python-project-from-scratch/>`_. 10. Configurations through templates which are easier to change. 11. Step-by-step procedure for beginners as well as connoisseurs. Intention was educational, but also functional. This is a starting block to create the initial structure that can be used to grow it bigger.

=======
Testing
=======

1. This project uses ``pytest`` to run tests and also to test docstring examples.

2. Virtual Environments
    PackageIt rely on virtual environments and also assume (default) any
    creation of a new module.package/library will be in a virtual
    environment.  By convention each of the tests should therefore run in
    it's own freshly created virtual environment.  This is unfortunately
    and expectedly become very expensive.  PackageIt there fore applies
    the following strategy with regards to testing:

    -   It (obviously) assume the PackageIt.create_venv work correctly and is tested properly.
    -   Tests rely on the virtual environment installed for PackageIt.
    -   Fresh virtual environments will only be created if:

        -   The test or any methods it calls will alter the virtual environment or
        -   It requires to operate specifically in the virtual environment for the package begin created.


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
