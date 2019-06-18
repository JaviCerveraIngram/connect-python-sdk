# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os

import pytest
from mock import patch, MagicMock

from connect import FulfillmentAutomation, TierConfigAutomation
from connect.exceptions import Message, FailRequest, InquireRequest, SkipRequest
from connect.models import TierConfig
# noinspection PyDeprecation
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from .common import Response, get_response_tier_config_request


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_message():
    with pytest.deprecated_call():
        # noinspection PyStatementEffect
        Message('Hello').message


def test_fulfillment_automation():
    with pytest.deprecated_call():
        FulfillmentAutomation()


def test_tier_config_automation():
    with pytest.deprecated_call():
        TierConfigAutomation()


def test_deprecated_exceptions():
    assert isinstance(FulfillmentFail(), FailRequest)
    assert isinstance(FulfillmentInquire(), InquireRequest)
    assert isinstance(Skip(), SkipRequest)


@patch('requests.get', MagicMock(side_effect=get_response_tier_config_request))
def test_get_tier_config():
    with pytest.deprecated_call():
        assert isinstance(FulfillmentAutomation().get_tier_config('', ''), TierConfig)


@patch('requests.get', MagicMock(return_value=Response(ok=True, text='[]', status_code=200)))
def test_get_tier_config_none():
    with pytest.deprecated_call():
        assert FulfillmentAutomation().get_tier_config('', '') is None
