# -*- coding: UTF-8 -*-
import os
import sys
if sys.version_info.major == 2:
    # python2
    import ConfigParser as configparser
else:
    # python3
    import configparser

from .plugin import PytestXrayPlugin


def pytest_addoption(parser):
    group = parser.getgroup('xray')
    group.addoption(
        '--xray',
        action='store_true',
        default=False)
    group.addoption(
        '--username',
        action='store')
    group.addoption(
        '--password',
        action='store')
    group.addoption(
        '--testplan',
        action='store')
    group.addoption(
        '--test_execution',
        action='store',
        default=None,)
    group.addoption(
        '--xray-config',
        default='xray.cfg',
        action='store',)


def pytest_configure(config):
    if config.getoption('--xray'):
        cfg_file_path = config.getoption('--xray-config')
        config_manager = ConfigManager(cfg_file_path, config)
        config.pluginmanager.register(
            PytestXrayPlugin(
                username=config_manager.getoption('username', 'username', 'XRAY'),
                password=config_manager.getoption('password', 'password', 'XRAY'),
                testplan=config_manager.getoption('testplan', 'testplan', 'XRAY'),
                test_execution=config_manager.getoption('test_execution', 'test_execution', 'XRAY'),
            ),
            # Name of plugin instance (allow to be used by other plugins)
            name="pytest-xray-instance"
        )


class ConfigManager(object):
    def __init__(self, cfg_file_path, config):
        '''
        Handles retrieving configuration values. Config options set in flags are given preferance over options set in the
        config file.

        :param cfg_file_path: Path to the config file containing information about the TestRail server.
        :type cfg_file_path: str or None
        :param config: Config object containing commandline flag options.
        :type config: _pytest.config.Config
        '''
        self.cfg_file = None
        if os.path.isfile(cfg_file_path) or os.path.islink(cfg_file_path):
            self.cfg_file = configparser.ConfigParser()
            self.cfg_file.read(cfg_file_path)

        self.config = config

    def getoption(self, flag, cfg_name, section=None, is_bool=False, default=None):
        # priority: cli > config file > default

        # 1. return cli option (if set)
        value = self.config.getoption('--{}'.format(flag))
        if value is not None:
            return value

        # 2. return default if not config file path is specified
        if section is None or self.cfg_file is None:
            return default

        if self.cfg_file.has_option(section, cfg_name):
            # 3. return config file value
            return self.cfg_file.getboolean(section, cfg_name) if is_bool else self.cfg_file.get(section, cfg_name)
        else:
            # 4. if entry not found in config file
            return default
