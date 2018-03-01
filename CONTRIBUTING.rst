.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/mbhall88/pistis/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

pistis could always use more documentation, whether as part of the
official pistis docs, in docstrings, or even on the web in blog posts,
articles, and such.
Please ensure that all functions include a `google-style docstring <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_.
Additionally, please make sure type annotations are included for all functions.
For an example of this please refer to `this line<https://github.com/mbhall88/pistis/blob/f53a83c2dc38d7fb05c81bd9c9c7b9150cab694d/pistis/utils.py#L65>`_ in ``pistis``.
Please ensure you update the docstrings and/or type annotations if you change a
pre-existing function.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/mbhall88/pistis/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `pistis` for local development.

1. Fork the `pistis` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pistis.git

3. Install your local copy into a virtualenv. Assuming you are happy to use pipenv, this is how you set up your fork for local development::

    $ cd pistis/
    $ make init
    $ make install

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ make lint
    $ make test
    $ make test-all

   flake8 and tox should be already installed at step 3.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 2.7 and 3.6. Check
   https://travis-ci.org/mbhall88/pistis/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

$ pipenv run pytest tests.test_pistis


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed.
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
