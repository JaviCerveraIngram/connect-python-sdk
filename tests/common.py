# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from collections import namedtuple

Response = namedtuple('Response', ('ok', 'text', 'status_code'))
BinaryResponse = namedtuple('BinaryResponse', ('ok', 'content', 'status_code'))


def load_str(filename):
    # type: (str) -> str
    with open(filename) as file_handle:
        return file_handle.read()
