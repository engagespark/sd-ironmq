"""Server Density Plugin to monitor IronMQ queues.

Copyright engageSPARK <info@engageSPARK.com>
Published under MIT license, see LICENSE file.

"""

import iron_mq
import requests

PLUGIN_NAME = 'IronMQ Plugin'
CONFIG_SECTION = "IronMQ"
CONFIG_PARAMS = [
    # ('config key', 'name', 'required'),
    ('project_ids', 'ProjectIDs', True),
    ('token', 'Token', True),
    ('host', 'Host', True),
]


class ConfigError(Exception):
    pass


class IronMQ(object):
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.log = checks_logger

        # get config options
        try:
            self._read_config(raw_config)
        except ConfigError:
            # Just don't create any clients.
            self.log.exception("Could not read config, doing nothing.")
            self.agent_config['ProjectIDs'] = ""

        self.iron_clients = [
            iron_mq.IronMQ(
                api_version=3,
                host=self.agent_config['Host'],
                name=project_id,
                port=443,
                project_id=project_id,
                protocol="https",
                token=self.agent_config.get('Token'),
            )
            for project_id
            in self.agent_config.get('ProjectIDs').split(" ")
        ]

    def run(self):
        stats = {}
        for client in self.iron_clients:
            try:
                stats.update(**self._get_data_for_client(client))
            except requests.HTTPError:
                self.log.exception(
                    "Could not fetch details for client {}. Ignoring."
                )
        return stats

    def _read_config(self, raw_config):
        if raw_config.get(CONFIG_SECTION, False):
            for key, name, required in CONFIG_PARAMS:
                if key not in raw_config[CONFIG_SECTION] and required:
                    raise ConfigError(
                        "Expected to find key '{}' in section '{}'".format(
                            key, CONFIG_SECTION))
                self.agent_config[name] = raw_config[
                    CONFIG_SECTION].get(key, None)
        else:
            raise ConfigError(
                '{}: IronMQ config section missing: [{}]'.format(
                    PLUGIN_NAME, CONFIG_SECTION))

    def _get_data_for_client(self, client):
        stats = {}
        for queue_name in client.getQueues():
            stats.update(**self._get_data_for_queue(client, queue_name))
        return stats

    def _get_data_for_queue(self, client, queue_name):
        details = client.getQueueDetails(queue_name)
        return {
            "{}:{}:size".format(
                client.name,
                queue_name,
            ): details['size'],
            "{}:{}:total_messages".format(
                client.name,
                queue_name,
            ): details['total_messages'],
        }


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    import pprint

    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('example.cfg')
    fake_config = {
        section: dict(config.items(section))
        for section in config.sections()
    }
    pprint.pprint(IronMQ({}, logging, fake_config).run())
