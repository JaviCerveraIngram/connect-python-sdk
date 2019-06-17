# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from connect.models import ActivationTileResponse, ActivationTemplateResponse


def test_activation_tile_response():
    assert ActivationTileResponse().tile == 'Activation succeeded'
    assert ActivationTileResponse('# Hello, world!').tile == '# Hello, world!'


def test_activation_template_response():
    assert ActivationTemplateResponse('TL-000-000-000').template_id == 'TL-000-000-000'
