# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os

from mock import patch

from connect.models import TierConfig, Param, TierConfigRequest
from .common import Response, load_str


def _get_response_tier_config_request(*_, **__):
    return Response(ok=True, text=load_str('response_tier_config_request.json'), status_code=200)


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


def teardown_module(module):
    os.chdir(module.prev_dir)


@patch('requests.get')
def test_get(get_mock):
    get_mock.return_value = _get_response_tier_config_request()

    tier_config = TierConfig.get('tier_id', 'product_id')
    assert isinstance(tier_config, TierConfig)

    param = tier_config.get_param_by_id('param_a')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/tier/config-requests/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey XXXX:YYYYY'},
        params={
            'status': 'approved',
            'configuration.product.id': 'product_id',
            'configuration.account.id': 'tier_id'})

    get_mock.return_value = Response(ok=True, text='[]', status_code=200)
    assert not TierConfig.get('', '')


def test_get_param_by_id():
    tier_config_requests = TierConfigRequest.deserialize(
        load_str('response_tier_config_request.json'))
    assert len(tier_config_requests) == 1
    tier_config_request = tier_config_requests[0]
    assert isinstance(tier_config_request, TierConfigRequest)

    # TierConfigRequest Ok
    param = tier_config_request.get_param_by_id('param_a')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'

    # TierConfigRequest KO
    param = tier_config_request.get_param_by_id('invalid')
    assert param is None

    # TierConfig Ok
    param = tier_config_request.configuration.get_param_by_id('param_a')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'

    # TierConfig KO
    param = tier_config_request.configuration.get_param_by_id('invalid')
    assert param is None
