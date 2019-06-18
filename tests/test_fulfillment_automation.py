# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os

from mock import patch, MagicMock, call

from connect.config import Config
from connect.exceptions import InquireRequest, FailRequest, SkipRequest
from connect.models import Fulfillment, ActivationTemplateResponse, ActivationTileResponse, Param
from connect.resources import FulfillmentAutomation
from .common import Response, load_str, get_response_tier_config_request


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_filters():
    assert FulfillmentAutomation().filters() == {
        'limit': 1000,
        'status': 'pending',
        'asset.product.id__in': 'CN-631-322-000'
    }


@patch('requests.get', MagicMock(side_effect=get_response_tier_config_request))
def test_dispatch_invalid_product():
    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomation().dispatch(request) == 'Invalid product'


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.get')
def test_dispatch_pass(get_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationPass(config).dispatch(request) == ''

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert info_mock.call_count == 3
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Method `process_request` did not return result')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.get')
def test_dispatch_tile_conversation(get_mock, post_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    conversation_json = load_str('conversation.json')
    get_mock.side_effect = [
        Response(ok=True, text='[{}]'.format(conversation_json), status_code=200),
        Response(ok=True, text=conversation_json, status_code=200)
    ]
    post_mock.side_effect = [
        Response(ok=True, text='Done.', status_code=200),
        Response(ok=True, text=load_str('add_message_response.json'), status_code=200),
    ]

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationTile(config).dispatch(request) == 'Done.'

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/conversations/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': 'PR-5620-6510-8214'}),
        call(
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})
    ])

    assert post_mock.call_count == 2
    post_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/approve/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json={'activation_tile': 'Some text...'}),
        call(
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356/messages/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json={'text': 'Activated using custom activation tile.'})
    ])

    assert info_mock.call_count == 6
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: approve'),
        call('Entering: post'),
        call('Entering: post')
    ])


@patch('connect.resources.fulfillment_automation.logger.error')
@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.get')
def test_dispatch_tile_conversation_wrong(get_mock, post_mock, info_mock, error_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    conversation_json = load_str('conversation.json')
    get_mock.side_effect = [
        Response(ok=True, text='[{}]'.format(conversation_json), status_code=200),
        Response(ok=True, text=conversation_json, status_code=200)
    ]
    post_mock.return_value = Response(ok=True, text='Done.', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationTile(config).dispatch(request) == 'Done.'

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/conversations/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': 'PR-5620-6510-8214'}),
        call(
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})
    ])

    assert post_mock.call_count == 2
    post_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/approve/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json={'activation_tile': 'Some text...'}),
        call(
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356/messages/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json={'text': 'Activated using custom activation tile.'})
    ])

    assert info_mock.call_count == 6
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: approve'),
        call('Entering: post'),
        call('Entering: post')
    ])

    assert error_mock.call_count == 1
    assert error_mock.call_args_list[0][0][0] == \
        'Error updating conversation for request PR-5620-6510-8214: No JSON object could be decoded'


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.get')
def test_dispatch_tile(get_mock, post_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)
    post_mock.return_value = Response(ok=True, text='Done.', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationTile(config).dispatch(request) == 'Done.'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert post_mock.call_count == 1
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/approve/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'activation_tile': 'Some text...'}
    )

    assert info_mock.call_count == 4
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: approve'),
        call('Entering: post')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.get')
def test_dispatch_template(get_mock, post_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)
    post_mock.return_value = Response(ok=True, text='Done.', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationTemplate(config).dispatch(request) == 'Done.'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert post_mock.call_count == 1
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/approve/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'template_id': 'TL-000-000-000'}
    )

    assert info_mock.call_count == 4
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: approve'),
        call('Entering: post')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.get')
def test_dispatch_string(get_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationString(config).dispatch(request) == 'One string'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert info_mock.call_count == 2
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.put')
@patch('requests.get')
def test_dispatch_inquire(get_mock, put_mock, post_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)
    put_mock.return_value = Response(ok=True, text='', status_code=200)
    post_mock.return_value = Response(ok=True, text='Inquired.', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationInquire(config).dispatch(request) == 'Inquired.'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert put_mock.call_count == 1
    put_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'asset': {'params': [{'id': 'param', 'value': 'my_value'}]}}
    )

    assert post_mock.call_count == 1
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/inquire/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={}
    )

    assert info_mock.call_count == 6
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: update_parameters'),
        call('Entering: put'),
        call('Entering: inquire'),
        call('Entering: post')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.post')
@patch('requests.get')
def test_dispatch_fail(get_mock, post_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)
    post_mock.return_value = Response(ok=True, text='Done.', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationFail(config).dispatch(request) == 'Done.'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert post_mock.call_count == 1
    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/PR-5620-6510-8214/fail/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'reason': 'Request failed'}
    )

    assert info_mock.call_count == 4
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
        call('Entering: fail'),
        call('Entering: post')
    ])


@patch('connect.resources.fulfillment_automation.logger.info')
@patch('requests.get')
def test_dispatch_skip(get_mock, info_mock):
    config = Config(api_url=Config.get_instance().api_url, api_key=Config.get_instance().api_key)
    get_mock.return_value = Response(ok=True, text='', status_code=200)

    request = Fulfillment.deserialize(load_str('response_fulfillment.json'))[0]
    assert FulfillmentAutomationSkip(config).dispatch(request) == 'skip'

    assert get_mock.call_count == 1
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/conversations/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'instance_id': 'PR-5620-6510-8214'}
    )

    assert info_mock.call_count == 2
    info_mock.assert_has_calls([
        call('Entering: get'),
        call('Start request process / ID request - PR-5620-6510-8214'),
    ])


@patch('requests.put')
def test_update_parameters(put_mock):
    put_mock.return_value = Response(ok=True, text='Result', status_code=200)

    assert FulfillmentAutomation().update_parameters(
        'REQ_ID',
        params=[Param(id='param', value='my_value')]
    ) == 'Result'

    assert put_mock.call_count == 1
    put_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/requests/REQ_ID',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'asset': {'params': [{'id': 'param', 'value': 'my_value'}]}}
    )


class FulfillmentAutomationPass(FulfillmentAutomation):
    def process_request(self, request):
        pass


class FulfillmentAutomationTile(FulfillmentAutomation):
    def process_request(self, request):
        return ActivationTileResponse('Some text...')


class FulfillmentAutomationTemplate(FulfillmentAutomation):
    def process_request(self, request):
        return ActivationTemplateResponse('TL-000-000-000')


class FulfillmentAutomationString(FulfillmentAutomation):
    def process_request(self, request):
        return 'One string'


class FulfillmentAutomationInquire(FulfillmentAutomation):
    def process_request(self, request):
        raise InquireRequest(params=[Param(id='param', value='my_value')])


class FulfillmentAutomationFail(FulfillmentAutomation):
    def process_request(self, request):
        raise FailRequest()


class FulfillmentAutomationSkip(FulfillmentAutomation):
    def process_request(self, request):
        raise SkipRequest('Value required')
