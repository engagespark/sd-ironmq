# sd-ironmq

A plugin for [Server Density](https://engagespark.serverdensity.io) that monitors [IronMQ queues](https://www.iron.io/).

Read the [official docs on plugins](https://support.serverdensity.com/hc/en-us/sections/200275866-Plugins) for details how to write one. Or find more, [official plugins](https://github.com/serverdensity/sd-agent-plugins).

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
