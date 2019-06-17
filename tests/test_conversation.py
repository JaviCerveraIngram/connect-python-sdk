# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime
import os

from mock import patch

from connect.models import Conversation, ConversationMessage, User
from .common import Response, load_str


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_conversation_attributes():
    conversation = Conversation.deserialize(load_str('conversation.json'))
    assert isinstance(conversation, Conversation)
    assert conversation.id == 'CO-750-033-356'
    assert conversation.instance_id == 'LST-038-662-242'
    assert conversation.created == datetime.datetime(2018, 12, 18, 12, 49, 34)
    assert conversation.topic == 'Topic'
    assert isinstance(conversation.messages, list)
    assert len(conversation.messages) == 1

    message = conversation.messages[0]
    assert isinstance(message, ConversationMessage)
    assert message.id == 'ME-506-258-087'
    assert message.conversation == conversation.id
    assert message.created == datetime.datetime(2018, 12, 18, 13, 3, 30)
    assert isinstance(message.creator, User)
    assert message.creator.id == 'UR-922-977-649'
    assert message.creator.name == 'Some User'
    assert message.text == 'Hi, check out'

    assert isinstance(conversation.creator, User)
    assert conversation.creator.id == 'UR-922-977-649'
    assert conversation.creator.name == 'Some User'


@patch('requests.post')
def test_add_message(post_mock):
    post_mock.return_value = Response(True, load_str('add_message_response.json'), 200)

    text = 'Hi, please see my listing request'

    conversation = Conversation.deserialize(load_str('conversation.json'))
    message = conversation.add_message(text)

    post_mock.assert_called_with(
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'text': text},
        url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356/messages/')

    assert isinstance(message, ConversationMessage)
    assert message.id == 'ME-000-000-000'
    assert message.conversation == 'CO-000-000-000'
    assert message.created == datetime.datetime(2018, 12, 18, 13, 3, 30)
    assert isinstance(message.creator, User)
    assert message.creator.id == 'UR-000-000-000'
    assert message.creator.name == 'Some User'
    assert message.text == text
