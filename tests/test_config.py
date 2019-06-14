# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os

import pytest

from connect.config import Config


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_global():
    _assert_config(Config.get_instance())


def test_immutable():
    config = Config.get_instance()
    with pytest.raises(AttributeError):
        config.api_url = 'http://localhost:8080/api/public/v1/'
    with pytest.raises(AttributeError):
        config.api_key = 'ApiKey XXXX:YYYYY'
    with pytest.raises(AttributeError):
        config.products = ['CN-631-322-000']


def test_file_ok():
    _assert_config(Config(file='config.json'))


def test_file_ko():
    with pytest.raises(IOError):
        Config(file='non_existing_config.json')


def test_file_ko2():
    with pytest.raises(TypeError):
        try:
            Config(file='data/plain.txt')
        except TypeError as ex:
            assert str(ex).startswith('Invalid config file `data/plain.txt`\nERROR: ')
            raise


def test_args_ko():
    with pytest.raises(ValueError):
        try:
            Config()
        except ValueError as ex:
            assert str(ex) == 'Expected file or api_key and api_url in Config initialization'
            raise


def test_products_str():
    _assert_config(Config(
        api_url='http://localhost:8080/api/public/v1/',
        api_key='ApiKey XXXX:YYYYY',
        products='CN-631-322-000',
    ))


def test_products_arr():
    _assert_config(Config(
        api_url='http://localhost:8080/api/public/v1/',
        api_key='ApiKey XXXX:YYYYY',
        products=['CN-631-322-000'],
    ))


def test_products_ko():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        Config(
            api_url='http://localhost:8080/api/public/v1/',
            api_key='ApiKey XXXX:YYYYY',
            products=0,
        )


def _assert_config(config):
    assert isinstance(config, Config)
    assert config.api_url == 'http://localhost:8080/api/public/v1/'
    assert config.api_key == 'ApiKey XXXX:YYYYY'
    assert isinstance(config.products, list)
    assert len(config.products) == 1
    assert config.products[0] == 'CN-631-322-000'
