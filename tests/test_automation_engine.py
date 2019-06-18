# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

import pytest
from mock import patch, MagicMock

from connect.models import BaseModel, ActivationTileResponse
from connect.resources.automation_engine import AutomationEngine
from .common import Response


def test_filters():
    assert AutomationEngineHelper().filters() == {'limit': 1000, 'status': 'pending'}


@patch('requests.get', MagicMock(return_value=Response(ok=True, text='[]', status_code=200)))
def test_process_empty():
    # This should not raise an exception
    AutomationEngineHelper().process()


@patch('requests.get', MagicMock(return_value=Response(ok=True, text='[{"id": "TEST_ID"}]',
                                                       status_code=200)))
def test_process_exception():
    with pytest.raises(NotImplementedError):
        try:
            AutomationEngineHelper().process()
        except NotImplementedError as ex:
            assert str(ex) == 'Please implement `AutomationEngineHelper.dispatch` method'
            raise


def test_dispatch():
    with pytest.raises(NotImplementedError):
        try:
            AutomationEngineHelper().dispatch(BaseModel())
        except NotImplementedError as ex:
            assert str(ex) == 'Please implement `AutomationEngineHelper.dispatch` method'
            raise


def test_process_request():
    with pytest.raises(NotImplementedError):
        try:
            AutomationEngineHelper().process_request(BaseModel())
        except NotImplementedError as ex:
            assert str(ex) == 'Please implement `AutomationEngineHelper.process_request` method'
            raise


@patch('requests.post')
def test_approve(post_mock):
    post_mock.return_value = Response(ok=True, text='OK', status_code=200)
    AutomationEngineHelper().approve('ID', {'activation_tile': 'Hello...'})
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/automation_engine/ID/approve/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'activation_tile': 'Hello...'}
    )


@patch('requests.post')
def test_inquire(post_mock):
    post_mock.return_value = Response(ok=True, text='OK', status_code=200)
    AutomationEngineHelper().inquire('ID')
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/automation_engine/ID/inquire/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={}
    )


@patch('requests.post')
def test_fail(post_mock):
    post_mock.return_value = Response(ok=True, text='OK', status_code=200)
    AutomationEngineHelper().fail('ID', 'Something went wrong...')
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/automation_engine/ID/fail/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'reason': 'Something went wrong...'}
    )


@patch('requests.get', MagicMock(return_value=
                                 Response(ok=True, text='Some response', status_code=200)))
def test_render_template():
    result = AutomationEngineHelper().render_template('ID', template_id='TL-000-000-000')
    assert isinstance(result, ActivationTileResponse)
    assert result.tile == 'Some response'


class AutomationEngineHelper(AutomationEngine):
    __metaclass__ = ABCMeta
    resource = 'automation_engine'
