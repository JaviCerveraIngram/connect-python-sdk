# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import six

from connect.exceptions import Message, FailRequest, InquireRequest, SkipRequest, ServerError, \
    AcceptUsageFile, CloseUsageFile, DeleteUsageFile, RejectUsageFile, SubmitUsageFile, \
    FileCreationError, FileRetrievalError
from connect.models import Param, ServerErrorResponse


def test_message():
    message = Message('Hello', 'code', object())
    assert str(message) == 'Hello'
    assert message.code == 'code'
    assert isinstance(message.obj, object)


def test_message_unicode():
    # noinspection PyTypeChecker
    message = Message(u'A unicode \u018e string \xf1')
    if six.PY2:
        assert str(message) == 'A unicode \xc6\x8e string \xc3\xb1'
    else:
        assert str(message) == 'A unicode \u018e string \xf1'


def test_fail():
    fail = FailRequest('Hello')
    assert str(fail) == 'Hello'
    assert fail.code == 'fail'
    assert fail.obj is None


def test_inquire():
    inquire = InquireRequest('Hello', params=[Param(name='name', value='test')])
    assert str(inquire) == 'Hello'
    assert inquire.code == 'inquire'
    assert isinstance(inquire.obj, list)
    assert len(inquire.params) == 1
    assert inquire.params[0].name == 'name'
    assert inquire.params[0].value == 'test'


def test_skip():
    skip = SkipRequest('Hello')
    assert str(skip) == 'Hello'
    assert skip.code == 'skip'
    assert skip.obj is None


def test_server_error():
    error_str = '{"error_code": "404"}'
    error = ServerErrorResponse(error_code='404')
    server_error = ServerError(error)
    assert str(server_error) == "('{}', '404')".format(error_str)
    assert len(server_error.args) == 2
    assert server_error.args[0] == error_str
    assert server_error.args[1] == '404'


def test_accept_usage_file():
    accept = AcceptUsageFile('This is the note')
    assert str(accept) == 'Usage data is correct'
    assert accept.code == 'accept'
    assert isinstance(accept.obj, dict)
    assert accept.obj['acceptance_note'] == 'This is the note'


def test_close_usage_file():
    close = CloseUsageFile()
    assert str(close) == 'Usage File Closed'
    assert close.code == 'close'
    assert close.obj is None


def test_delete_usage_file():
    delete = DeleteUsageFile()
    assert str(delete) == 'Usage File Deleted'
    assert delete.code == 'delete'
    assert delete.obj is None


def test_reject_usage_file():
    reject = RejectUsageFile('This is the note')
    assert str(reject) == 'Usage data is not correct'
    assert reject.code == 'reject'
    assert isinstance(reject.obj, dict)
    assert reject.obj['rejection_note'] == 'This is the note'


def test_submit_usage_file():
    submit = SubmitUsageFile()
    assert str(submit) == 'Usage File Submitted'
    assert submit.code == 'submit'
    assert submit.obj is None


def test_file_creation_error():
    file_creation_error = FileCreationError('Hello')
    assert str(file_creation_error) == 'Hello'
    assert file_creation_error.code == 'filecreation'
    assert file_creation_error.obj is None


def test_file_retrieval_error():
    file_retrieval_error = FileRetrievalError('Hello')
    assert str(file_retrieval_error) == 'Hello'
    assert file_retrieval_error.code == 'fileretrieval'
    assert file_retrieval_error.obj is None
