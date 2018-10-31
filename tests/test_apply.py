"""Figcan tests - test configuration applying methods
"""
# Copyright (c) 2018 Shoppimon LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from collections import namedtuple

import pytest

from figcan import Configuration, Extensible


def test_apply_nested_dict(base_config):
    cfg = Configuration(base_config)
    cfg.apply({"foo": "baz", "logging": {"level": 6}})

    assert cfg['foo'] == 'baz'
    assert cfg['logging']['level'] == 6
    assert cfg['logging']['format'] == 'some format'


def test_apply_nested_dict_base_not_modified(base_config):
    cfg = Configuration(base_config)
    cfg.apply({"foo": "baz", "logging": {"level": 6}})
    assert base_config['foo'] == 'bar'


def test_apply_nokey_raises(base_config):
    cfg = Configuration(base_config)
    with pytest.raises(KeyError):
        cfg.apply({"foos": "baz"})


def test_apply_nokey_ignored(base_config):
    cfg = Configuration(base_config)
    cfg.apply({"foos": "baz"}, raise_on_unknown_key=False)
    assert 'foos' not in cfg


def test_apply_nokey_flexible_config_added(base_config):
    base_config['logging']['handlers'] = Extensible(base_config['logging']['handlers'])
    cfg = Configuration(base_config)
    cfg.apply({"foo": "baz", "logging": {"handlers": {"handler3": 'new handler'}}})

    assert cfg['foo'] == 'baz'
    assert cfg['logging']['level'] == 5
    assert cfg['logging']['handlers']['handler1'] == 'some config'
    assert cfg['logging']['handlers']['handler3'] == 'new handler'


def test_apply_flat_dict(base_config):
    cfg = Configuration(base_config)
    flat_overrides = {'foo': 'baz',
                      'is_enabled': True,
                      'logging_level': 6,
                      'logging_handlers_handler1': 'something else'}
    cfg.apply_flat(flat_overrides)

    assert cfg['foo'] == 'baz'
    assert cfg['is_enabled'] is True
    assert cfg['logging']['level'] == 6
    assert cfg['logging']['handlers']['handler1'] == 'something else'


def test_apply_flat_dict_prefix_stripped(base_config):
    cfg = Configuration(base_config)
    flat_overrides = {'foo': 'baz',
                      'figcan_is_enabled': True,
                      'figcan_logging_level': 6,
                      'logging_level': 4}

    cfg.apply_flat(flat_overrides, prefix='figcan_')

    assert cfg['foo'] == 'bar'
    assert cfg['is_enabled'] is True
    assert cfg['logging']['level'] == 6


def test_apply_flat_dict_prefix_stripped_missing_keys(base_config):
    cfg = Configuration(base_config)
    flat_overrides = {'figcan_logging_level': 6,
                      'figcan_logging_shmevel': 9}

    cfg.apply_flat(flat_overrides, prefix='figcan_')

    assert 'shmevel' not in cfg['logging']
    assert 'logging_shmevel' not in cfg


def test_apply_flat_dict_custom_nesting_separator(base_config):
    cfg = Configuration(base_config)
    flat_overrides = {'is_enabled': True,
                      'is.enabled': False,
                      'logging.level': 6,
                      'logging.handlers_handler1': 'something else'}

    cfg.apply_flat(flat_overrides, namespace_separator='.')
    assert cfg['is_enabled'] is True
    assert cfg['logging']['level'] == 6
    assert cfg['logging']['handlers']['handler1'] == 'some config'


def test_apply_object(base_config):
    cfg = Configuration(base_config)
    ConfigOverrides = namedtuple('ConfigOverrides', ('foo', 'is_enabled'))
    cfg.apply_object(ConfigOverrides(foo='blah', is_enabled=True))

    assert cfg['foo'] == 'blah'
    assert cfg['is_enabled'] is True


def test_apply_object_to_subkey(base_config):
    cfg = Configuration(base_config)
    ConfigOverrides = namedtuple('ConfigOverrides', ('level', 'format'))
    cfg.apply_object(ConfigOverrides(level=4, format='this is a format'), apply_on=('logging',))

    assert cfg['logging']['level'] == 4
    assert cfg['logging']['format'] == 'this is a format'


def test_apply_object_from_argparse(base_config):
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=int)
    parser.add_argument('--format', type=str)
    parser.add_argument('--other-flag', action='store_true')
    args = parser.parse_args(['--level', '3', '--format', 'some great format', '--other-flag'])

    cfg = Configuration(base_config)
    cfg.apply_object(args, apply_on=('logging',))

    assert cfg['logging']['level'] == 3
    assert cfg['logging']['format'] == 'some great format'
