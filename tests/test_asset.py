# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from connect.models import Asset, Param, Item


def test_asset_get_param_by_id():
    asset = Asset(params=[Param(id='id', value='qwerty')])

    # Ok
    param = asset.get_param_by_id('id')
    assert isinstance(param, Param)
    assert param.id == 'id'
    assert param.value == 'qwerty'

    # KO
    param = asset.get_param_by_id('invalid')
    assert param is None


def test_asset_get_item_by_mpn():
    asset = Asset(items=[Item(mpn='1q2w3e')])

    # Ok
    item = asset.get_item_by_mpn('1q2w3e')
    assert isinstance(item, Item)
    assert item.mpn == '1q2w3e'

    # KO
    item = asset.get_item_by_mpn('invalid')
    assert item is None
