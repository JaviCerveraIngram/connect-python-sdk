# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import json

import pytest

from connect.models import BaseModel


def test_base_model():
    base_model = BaseModel(one='1', two=2)

    # Test attributes
    assert not hasattr(base_model, 'other')
    assert base_model.id is None
    assert getattr(base_model, 'one') == '1'
    assert getattr(base_model, 'two') == 2

    # Test json properties
    model_dict = {"one": "1", "two": 2}
    model_str = json.dumps(model_dict)
    assert base_model.json == model_dict
    assert base_model.json_str == model_str

    # Assert deserialize
    deserialized_model = BaseModel.deserialize('{"id": "obj_id"}')
    assert isinstance(deserialized_model, BaseModel)
    assert deserialized_model.id == 'obj_id'

    # Assert deserialize_json
    deserialized_model = BaseModel.deserialize_json({'id': 'obj_id'})
    assert isinstance(deserialized_model, BaseModel)
    assert deserialized_model.id == 'obj_id'

    # Assert wrong deserialize_json
    with pytest.raises(TypeError):
        try:
            BaseModel.deserialize_json({'id': None})
        except TypeError as ex:
            assert str(ex).startswith('Invalid structure for initialization of `BaseModel`')
            raise
