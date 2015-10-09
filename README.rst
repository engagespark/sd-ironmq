===========
 sd-ironmq
===========

A plugin for the `Server Density <https://engagespark.serverdensity.io>`_ agent that monitors `IronMQ queues <https://www.iron.io/>`_ **using API version 3**.

`PyPI page <https://pypi.python.org/pypi/sd-ironmq/>`_ | `GitHub project <https://github.com/engagespark/sd-ironmq/>`_

For details how to write one, read the `official docs on plugins <https://support.serverdensity.com/hc/en-us/sections/200275866-Plugins>`_. Or find more `official plugins <https://github.com/serverdensity/sd-agent-plugins>`_.

Features
========

- Monitors all queues of the given projects.
- Recorded metrics:
    - size (key: <projectid/-name>:<queuename>:size)
    - total_messages (key: <projectid/-name>:<queuename>:size)

Example for metric keys::

  billingproject:invoicequeue:size
  billingproject:invoicequeue:total_messages

How to use
==========

Install via PyPI or …
---------------------

Get it from pypi, installing it somewhere::

    pip install sd-ironmq

Symlink it to your plugin directory, on Debian/Ubuntu by default: `/usr/bin/sd-agent/plugins`

Install via curl
----------------

`curl` the latest version from GitHub directly into your Plugin directory::

    curl https://raw.githubusercontent.com/engagespark/sd-ironmq/master/IronMQ.py > /usr/bin/sd-agent/plugins/IronMQ.py

Configure
---------

Add this section to your `/etc/sd-agent/config.cfg`::

    [IronMQ]
    host=mq-aws-eu-west-1-1.iron.io
    # comma separated list of project IDs
    project_ids=<your-project-ids>
    token=<your-token>

Restart the agent
-----------------

On Debian/Ubuntu::

    service sd-agent restart

Other configuration options
===========================

Metric Keys: Use Project Names instead of IDs
---------------------------------------------

Let's say you configured the queues of your billing project to be monitored::

    project_ids=2342934839ai239ai89i

For a queue `invoices`, the metric keys would look like so::

    2342934839ai239ai89i:invoices:size
    2342934839ai239ai89i:invoices:total_messages

That's not beautiful, nor understandable. Also it exposes IronMQ internals unnecessarily. Configure a name for the project ID like so::

    2342934839ai239ai89i.name=billing

The name is then used in the keys::

    billing:invoices:size
    billing:invoices:total_messages

Test locally
============

Create an example.cfg in the working directory::

    [IronMQ]
    host=mq-aws-eu-west-1-1.iron.io
    project_ids=<your-project-ids>
    token=<your-token>

Run the plugin::

    python IronMQ.py


Releasing
=========

Prepare
-------

#. Install `twine <https://github.com/pypa/twine>`_ and `wheel <https://pypi.python.org/pypi/wheel>`_::

    $ pip install -r requirements_dev.txt

#. Setup your `.pypirc <https://docs.python.org/2/distutils/packageindex.html#pypirc>`_.

Release a new version
---------------------

#. Update CHANGELOG.
#. Update version in setup.py, commit, push.
#. Tag as that version, see `git tag`, `push --tags`
#. Build distributables::

    $ python setup.py sdist bdist_wheel

#. Upload distributable to PyPI::

    $ twine upload --sign dist/*


License
=======

MIT, see `LICENSE <https://github.com/engagespark/sd-ironmq/blob/master/LICENSE>`_ file, Copyright `engageSPARK <https://www.engagespark.com>`_
