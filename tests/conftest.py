"""Shared testing configuration and utilities
"""
import pytest


@pytest.fixture()
def base_config():
    return {
        'foo': 'bar',
        'logging': {
            'level': 5,
            'format': 'some format',
            'handlers': {
                'handler1': 'some config',
                'handler2': 'other config'
            }
        },
        'items': [1, 2, 3],
        'is_enabled': False,
        'has_value': None
    }
