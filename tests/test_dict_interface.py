"""Unit tests for Figcan - test the base dictionary access interface
"""
import pytest

from figcan import Configuration


def test_can_read_existing_items(base_config):
    cfg = Configuration(base_config)
    assert cfg['is_enabled'] is False
    assert cfg['items'][2] == 3
    assert cfg['logging']['handlers']['handler1'] == 'some config'


def test_throw_if_read_nonexisting_items(base_config):
    cfg = Configuration(base_config)
    with pytest.raises(KeyError):
        assert cfg['is_fababled'] is False

    with pytest.raises(TypeError):
        assert cfg['items']['item_foo'] == 3


def test_can_read_nonexisting_key_with_default(base_config):
    cfg = Configuration(base_config)
    assert cfg.get('is_fababled', 'foo') == 'foo'


def test_throw_on_write(base_config):
    cfg = Configuration(base_config)
    with pytest.raises(TypeError):
        cfg['is_enabled'] = True

    with pytest.raises(TypeError):
        cfg['new_key'] = 'new value'


def test_can_check_for_items_in(base_config):
    cfg = Configuration(base_config)
    assert 'items' in cfg
    assert 'format' in cfg['logging']


def test_is_iterable(base_config):
    cfg = Configuration(base_config)
    cfg_keys = [k for k in cfg]
    assert len(cfg_keys) == 5
    assert len(cfg.keys()) == 5
    assert len(cfg.values()) == 5
    assert len(cfg.items()) == 5


def test_has_len(base_config):
    cfg = Configuration(base_config)
    assert len(cfg) == 5
