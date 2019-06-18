# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import pytest
from mock import patch

from connect.config import Config
from connect.exceptions import ServerError
from connect.models import BaseModel
from connect.resources.base import ApiClient, BaseResource
from .common import Response, BinaryResponse


def test_api_client():
    assert ApiClient.urljoin('one', 'two', 'three') == 'one/two/three'
    assert ApiClient.urljoin('one/', 'two/', 'three/') == 'one/two/three/'
    assert ApiClient._check_and_pack_response(Response(ok=True, text='Text', status_code=200)) \
        == ('Text', 200)
    with pytest.raises(AttributeError):
        try:
            ApiClient._check_and_pack_response(BinaryResponse(ok=True, content='', status_code=200))
        except AttributeError as ex:
            assert str(ex) == 'Response does not have attribute `text`. ' \
                              'Check your request params. Response status - 200'
            raise
    with pytest.raises(ServerError):
        ApiClient._check_and_pack_response(Response(
            ok=False,
            text='{"error_code": "ERR"}',
            status_code=400
        ))

    # Env config
    # noinspection PyTypeChecker
    client = ApiClient(None, 'base_path')
    assert client.base_path == 'base_path'
    assert client.config == Config.get_instance()
    assert client.headers == {
        'Authorization': 'ApiKey XXXX:YYYYY',
        'Content-Type': 'application/json'
    }
    assert client.get_url('hello') == 'http://localhost:8080/api/public/v1/base_path/hello'

    # Arg config
    config = Config(api_url='url', api_key='000')
    assert ApiClient(config, 'path').config == config

    # Bad config
    with pytest.raises(ValueError):
        try:
            # noinspection PyTypeChecker
            ApiClient('Nothing', 'path')
        except ValueError as ex:
            assert str(ex) == 'A valid Config object must be passed or globally configured.'
            raise


def test_create():
    # Base class
    with pytest.raises(AttributeError):
        try:
            BaseResource()
        except AttributeError as ex:
            assert str(ex) == 'Resource name not specified in class BaseResource. ' \
                              'Add an attribute `resource` with the name of the resource'
            raise

    # Env config
    assert BaseResourceHelper().config == Config.get_instance()

    # Arg config
    config = Config(api_url='url', api_key='key')
    assert BaseResourceHelper(config).config == config


def test_filters():
    resource = BaseResourceHelper()
    assert resource.filters() == {'limit': 100}
    assert resource.filters(limit=0) == {'limit': 0}
    assert resource.filters(extra=True) == {'limit': 100, 'extra': True}


@patch('requests.get')
def test_list(get_mock):
    get_mock.return_value = Response(ok=True, text='[{"id": "TEST_ID"}]', status_code=200)

    result = BaseResourceHelper().list()
    assert len(result) == 1
    assert isinstance(result[0], BaseModel)
    assert result[0].id == 'TEST_ID'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/resource/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'limit': 100},
    )


@patch('requests.get')
def test_get(get_mock):
    get_mock.return_value = Response(ok=True, text='[{"id": "TEST_ID"}]', status_code=200)

    result = BaseResourceHelper().get('TEST_ID')
    assert isinstance(result, BaseModel)
    assert result.id == 'TEST_ID'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/resource/TEST_ID',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey XXXX:YYYYY'},
    )

    # Empty return
    get_mock.return_value = Response(ok=True, text='[]', status_code=200)
    result = BaseResourceHelper().get('TEST_ID')
    assert result is None


class BaseResourceHelper(BaseResource):
    resource = 'resource'
