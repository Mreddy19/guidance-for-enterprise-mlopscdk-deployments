Developer Guide
===============

.. important::

    Unless stated otherwise, all the instructions on this page assumes ``GITROOT/`` as your current
    directory.

.. note::

    This project is still in private preview and is hosted on https://github.com/awslabs/guidance-for-enterprise-mlops-deployments

Pre-Requisites
--------------

The Python packages required for building the documentation is specified in
``requirements-docs.txt``. Please install those dependencies as follows:

.. code-block::

    pip install -r requirements-docs.txt

Hygiene Practice
----------------

.. important:: **Insist on the highest standards**

    Leaders have relentlessly high standards --- many people may think these standards are
    unreasonably high. Leaders are continually raising the bar and drive their teams to deliver high
    quality products, services, and processes. Leaders ensure that defects do not get sent down the
    line and that problems are fixed so they stay fixed.

To ensure high-quality merge requests (MR) and shorten the code-review cycle, you're strongly
recommended to perform these tasks before creating an MR.

Although the project repository also runs the same checks as CI on your MR as a pre-cautionary
measure, you're still strongly recommended to run these tasks locally to quickly catch and fix
low-hanging-fruit violations.

Linters
~~~~~~~

The code-base comes with a set of git pre-commit hooks listed in the ``.pre-commit-config.yaml``
file.

.. note::

    For those who are mandated to use
    `Code Defender <https://w.amazon.com/bin/view/AWS/Teams/Proserve/SRC/ACE/SEAT/CodeDefender/>`_
    [#f1]_, please follow
    `this <https://w.amazon.com/bin/view/AWS/Teams/Proserve/SRC/ACE/SEAT/CodeDefender/UserHelp/#18>`_
    to setup your pre-commit hooks, which as of this writing is as follows:

    .. code-block:: bash

        git defender --precommit_tool_setup

    .. [#f1] The internal AWS tool created by AWS Sales & Marketing (SAM) Engagement security
        service

HTML Docs
---------

First, make sure your operating system has ``make`` CLI. Then, generate the html documentations as
follows:

.. code-block:: bash

    cd docs
    make clean
    make html

On a multi-core machine, you can also pass the ``-j <num>`` to speed-up the build process.

.. code-block:: bash

    cd docs
    make clean

    # Instruct make to run 4 jobs (commands) in parallel.
    make -j 4 html

Once completed, you can view the generated html pages at ``docs/_build/html/index.html``.

.. tip::

    `VS Code <https://code.visualstudio.com/>`_ users may consider the
    `Live Preview <https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server>`_
    extension to auto-refresh the preview of the generated HTML pages after every ``make html``.
