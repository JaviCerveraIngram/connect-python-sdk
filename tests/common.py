# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os
from collections import namedtuple

Response = namedtuple('Response', ('ok', 'text', 'status_code'))
BinaryResponse = namedtuple('BinaryResponse', ('ok', 'content', 'status_code'))


def load_str(filename):
    # type: (str) -> str
    with open(filename) as file_handle:
        return file_handle.read()


def get_response_tier_config_request(*_, **__):
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'response_tier_config_request.json')
    return Response(ok=True, text=load_str(filename), status_code=200)
