# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import pytest

from connect import FulfillmentAutomation, TierConfigAutomation
from connect.exceptions import Message


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
