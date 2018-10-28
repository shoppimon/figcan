"""Figcan tests - test mapping interface access
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
