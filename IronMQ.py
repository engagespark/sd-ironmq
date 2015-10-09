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
    ('host', 'Host', True),
    ('project_ids', 'ProjectIDs', True),
    ('token', 'Token', True),
]


class ConfigError(Exception):
    pass


class IronMQ(object):
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.log = checks_logger

        # get config options
        try:
            self._set_agent_config(raw_config)
        except ConfigError:
            self.log.exception("Could not read config, doing nothing.")
            self.iron_clients = []
            return

        self.log.info("Querying queues for {}".format(
            ", ".join([p["name"] for p in self.agent_config.get('Projects')])))
        self.iron_clients = [
            iron_mq.IronMQ(
                api_version=3,
                host=self.agent_config['Host'],
                name=project['name'],
                port=443,
                project_id=project['id'],
                protocol="https",
                token=self.agent_config.get('Token'),
            )
            for project in self.agent_config.get('Projects')
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

    def _set_agent_config(self, raw_config):
        self._copy_validated_config(raw_config)
        self._set_projects(raw_config)

    def _copy_validated_config(self, raw_config):
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

    def _set_projects(self, raw_config):
        project_ids_string = self.agent_config.get('ProjectIDs')
        self.agent_config['Projects'] = [
            {
                "id": project_id,
                "name": raw_config[CONFIG_SECTION].get(
                    u"{}.name".format(project_id), project_id)
            }
            for project_id in (
                [i.strip() for i in project_ids_string.split(" ")]
                if project_ids_string
                else []
            )
        ]

    def _get_data_for_client(self, client):
        stats = {}
        for queue_name in client.getQueues():
            results = self._get_data_for_queue(client, queue_name)
            self.log.debug(u"Got result: {}".format(results))
            stats.update(**results)
        return stats

    def _get_data_for_queue(self, client, queue_name):
        details = client.getQueueDetails(queue_name)
        self.log.debug(
            u"Querying information for project '{}'s queue '{}'".format(
                client.name, queue_name))
        return {
            u":".join([
                client.name,
                queue_name,
                "size",
            ]): details['size'],
            u":".join([
                client.name,
                queue_name,
                "total_messages",
            ]): details['total_messages'],
        }


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    import pprint

    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('example.cfg')
    fake_config = {
        section: dict(config.items(section))
        for section in config.sections()
    }
    pprint.pprint(IronMQ({}, logging, fake_config).run())
