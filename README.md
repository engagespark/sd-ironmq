# sd-ironmq

A plugin for [Server Density](https://engagespark.serverdensity.io) that monitors [IronMQ queues](https://www.iron.io/).

Read the [official docs on plugins](https://support.serverdensity.com/hc/en-us/sections/200275866-Plugins) for details how to write one. Or find more, [official plugins](https://github.com/serverdensity/sd-agent-plugins).

## Features

* Given one or more projects, the plugin monitors all queues of the given size.
* Recorded metrics:
  * size (key: <projectid/-name>:<queuename>:size)
  * total_messages (key: <projectid/-name>:<queuename>:size)

Example for metric keys:

    billingproject:invoicequeue:size
    billingproject:invoicequeue:total_messages

## How to use

### Install

Get it from pypi, installing it somewhere

    pip install sd-ironmq

Symlink it to your plugin directory, on Debian/Ubuntu by default: `/usr/bin/sd-agent/plugins`

### Configure

Add this section to your `/etc/sd-agent/config.cfg`:

    [IronMQ]
    host=mq-aws-eu-west-1-1.iron.io
    # comma separated list of project IDs
    project_ids=<your-project-ids>
    token=<your-token>

### Restart the agent

On Debian/Ubuntu:

    service sd-agent restart

## Other configuration options

### Metric Keys: Use Project Names instead of IDs

Let's say you configured the queues of your billing project to be monitored:

    project_ids=2342934839ai239ai89i

For a queue `invoices`, the metric keys would look like so:

    2342934839ai239ai89i:invoices:size
    2342934839ai239ai89i:invoices:total_messages

That's not beautiful, nor understandable. Also it exposes IronMQ internals unnecessarily. Configure a name for the project ID like so:

    2342934839ai239ai89i.name=billing

The name is then used in the keys:

    billing:invoices:size
    billing:invoices:total_messages

## Test locally

Create an example.cfg in the working directory:

    [IronMQ]
    host=mq-aws-eu-west-1-1.iron.io
    project_ids=<your-project-ids>
    token=<your-token>

Run the plugin:

    python IronMQ.py


## License

MIT, see LICENSE file, Copyright engageSPARK
