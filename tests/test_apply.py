"""Figcan tests - test configuration applying methods
"""
import argparse
from collections import namedtuple

import pytest

from figcan import Configuration


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
