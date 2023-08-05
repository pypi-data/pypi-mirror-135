import argparse
import logging as log
import json
import sys
import importlib
import time

from knowledge_mapper.knowledge_mapper import KnowledgeMapper

from knowledge_mapper.data_source import DataSource
from knowledge_mapper.sparql_source import SparqlSource
from knowledge_mapper.sql_source import SqlSource

log.basicConfig(level=log.INFO)


DATA_SOURCE_MAX_CONNECTION_ATTEMPTS = 5
DATA_SOURCE_WAIT_BEFORE_RETRY = 2

def test_data_source(data_source: DataSource):
    success = False
    attempts = 0
    while not success:
        try:
            data_source.test()
            success = True
        except Exception as e:
            attempts += 1
            if attempts < DATA_SOURCE_MAX_CONNECTION_ATTEMPTS:
                log.warning(f'Request to data source failed. Retrying in {DATA_SOURCE_WAIT_BEFORE_RETRY} s.')
                time.sleep(DATA_SOURCE_WAIT_BEFORE_RETRY)
            else:
                log.error(f'Request to data source failed.')
                raise e


def main():
    from . import __version__
    log.info(f'Running Knowledge Mapper {__version__}')
    parser = argparse.ArgumentParser(description='Expose an endpoint to a knowledge network.')
    parser.add_argument('config')
    args = parser.parse_args()
    with open(args.config) as config_file:
        config = json.load(config_file)

        if 'sparql' in config:
            endpoint = config['sparql']['endpoint']
            username = None
            password = None
            if 'username_environment_var' in config['sparql'] and 'password_environment_var' in config['sparql']:
                username = config['sparql']['username_environment_var']
                password = config['sparql']['password_environment_var']
            data_source = SparqlSource(endpoint, username, password)
        elif 'sql_host' in config:
            data_source = SqlSource(config['sql_host'], config['sql_port'], config['sql_database'], config['sql_user'], config['sql_password'])
        elif 'plugin' in config:
            plugin_cfg = config['plugin']
            module_name, class_name = plugin_cfg['class'].rsplit(".", 1)
            plugin_module = importlib.import_module(module_name)
            plugin_class = getattr(plugin_module, class_name)
            if 'args' in plugin_cfg:
                data_source = plugin_class(*plugin_cfg['args'])
            else:
                data_source = plugin_class()
        else:
            log.error('Invalid config.')
            sys.exit(1)

        test_data_source(data_source)

        if 'authorization_enabled' in config:
            auth_enabled = config['authorization_enabled']
        else:
            auth_enabled = False
        
        km = KnowledgeMapper(
            data_source,
            auth_enabled,
            config['knowledge_engine_endpoint'],
            config['knowledge_base']['id'],
            config['knowledge_base']['name'],
            config['knowledge_base']['description']
        )
        for ki in config['knowledge_interactions']:
            km.add_knowledge_interaction(ki)

        try:
            km.start()
        except KeyboardInterrupt:
            log.info('Shutting down gracefully...')
        finally:
            km.clean_up()

        log.info('Goodbye.')
        exit(0)

if __name__ == '__main__':
    main()
