# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime
import os

from mock import call, patch

from connect.models import Fulfillment, Asset, Product, Connection, Company, Item, Param, \
    TierAccounts, TierAccount, ContactInfo, Contact, PhoneNumber, Conversation
from .common import load_str, Response


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_fulfillment():
    fulfillments = Fulfillment.deserialize(load_str('response_fulfillment.json'))
    assert isinstance(fulfillments, list)
    assert len(fulfillments) == 1
    fulfillment = fulfillments[0]
    assert isinstance(fulfillment, Fulfillment)

    assert fulfillment.id == 'PR-5620-6510-8214'
    assert fulfillment.type == 'purchase'
    assert fulfillment.created == datetime.datetime(2018, 9, 3, 10, 28, 18)
    assert fulfillment.updated == datetime.datetime(2018, 9, 4, 10, 38, 58)
    assert fulfillment.status == 'approved'
    assert fulfillment.params_form_url is None
    assert fulfillment.activation_key == '###tile'
    assert fulfillment.reason == ''
    assert fulfillment.note is None

    assert isinstance(fulfillment.asset, Asset)
    assert fulfillment.asset.id == 'AS-893-495-635-9'
    assert fulfillment.asset.status == 'new'
    assert fulfillment.asset.external_id == '899'
    assert fulfillment.asset.external_uid is None
    assert isinstance(fulfillment.asset.product, Product)
    assert fulfillment.asset.product.id == 'CN-573-708-587'
    assert fulfillment.asset.product.name == 'Dropbox Test'
    assert isinstance(fulfillment.asset.connection, Connection)
    assert fulfillment.asset.connection.id == 'CT-0000-0000-0000'
    assert fulfillment.asset.connection.type == 'preview'
    assert isinstance(fulfillment.asset.connection.provider, Company)
    assert fulfillment.asset.connection.provider.id == 'PA-473-705'
    assert fulfillment.asset.connection.provider.name == 'ACME Provider'
    assert isinstance(fulfillment.asset.connection.vendor, Company)
    assert fulfillment.asset.connection.vendor.id == 'VA-691-879'
    assert fulfillment.asset.connection.vendor.name == 'Marc FSG'

    assert len(fulfillment.asset.items) == 5
    assert isinstance(fulfillment.asset.items[4], Item)
    assert fulfillment.asset.items[4].id == 'DELETE_TEST'
    assert fulfillment.asset.items[4].mpn == 'DELETE_TEST'
    assert fulfillment.asset.items[4].old_quantity == 200
    assert fulfillment.asset.items[4].quantity == 0

    assert len(fulfillment.asset.params) == 2
    assert isinstance(fulfillment.asset.params[0], Param)
    assert fulfillment.asset.params[0].id == 'howyoufeel'
    assert fulfillment.asset.params[0].name == 'How You feel today?'
    assert fulfillment.asset.params[0].description == 'How customer Feels'
    assert fulfillment.asset.params[0].type == 'dropdown'
    assert fulfillment.asset.params[0].value == 'Good'
    assert fulfillment.asset.params[0].value_error == ''
    assert fulfillment.asset.params[0].value_choice is None

    assert isinstance(fulfillment.asset.tiers, TierAccounts)
    assert isinstance(fulfillment.asset.tiers.customer, TierAccount)
    assert fulfillment.asset.tiers.customer.id == 'TA-0-5870-9239-0029'
    assert fulfillment.asset.tiers.customer.name == 'Kaiser LLC'
    assert fulfillment.asset.tiers.customer.external_id == '889'
    assert isinstance(fulfillment.asset.tiers.customer.contact_info, ContactInfo)
    assert fulfillment.asset.tiers.customer.contact_info.address_line1 == 'Darren Passage'
    assert fulfillment.asset.tiers.customer.contact_info.address_line2 == ''
    assert fulfillment.asset.tiers.customer.contact_info.country == 'us'
    assert fulfillment.asset.tiers.customer.contact_info.state == 'Nevada'
    assert fulfillment.asset.tiers.customer.contact_info.city == 'West Douglas'
    assert fulfillment.asset.tiers.customer.contact_info.postal_code == '30690'
    assert isinstance(fulfillment.asset.tiers.customer.contact_info.contact, Contact)
    assert fulfillment.asset.tiers.customer.contact_info.contact.email \
        == 'markbrooks-0189@VA-691-879.com'
    assert fulfillment.asset.tiers.customer.contact_info.contact.first_name == 'Mark'
    assert fulfillment.asset.tiers.customer.contact_info.contact.last_name == 'Brooks'
    assert isinstance(fulfillment.asset.tiers.customer.contact_info.contact.phone_number,
                      PhoneNumber)
    assert fulfillment.asset.tiers.customer.contact_info.contact.phone_number.country_code \
        == '+252'
    assert fulfillment.asset.tiers.customer.contact_info.contact.phone_number.area_code \
        == '1'
    assert fulfillment.asset.tiers.customer.contact_info.contact.phone_number.phone_number \
        == '474842'
    assert fulfillment.asset.tiers.customer.contact_info.contact.phone_number.extension == ''
    assert isinstance(fulfillment.asset.tiers.tier1, TierAccount)
    assert fulfillment.asset.tiers.tier1.id == 'TA-0-7251-3930-7482'
    assert fulfillment.asset.tiers.tier1.name == 'ACME Reseller'
    assert fulfillment.asset.tiers.tier1.external_id == '1'
    assert isinstance(fulfillment.asset.tiers.tier1.contact_info, ContactInfo)
    assert fulfillment.asset.tiers.tier1.contact_info.address_line1 == 'noname'
    assert fulfillment.asset.tiers.tier1.contact_info.address_line2 == ''
    assert fulfillment.asset.tiers.tier1.contact_info.country == 'us'
    assert fulfillment.asset.tiers.tier1.contact_info.state == 'Alaska'
    assert fulfillment.asset.tiers.tier1.contact_info.city == 'noname'
    assert fulfillment.asset.tiers.tier1.contact_info.postal_code == '12111'
    assert isinstance(fulfillment.asset.tiers.tier1.contact_info.contact, Contact)
    assert fulfillment.asset.tiers.tier1.contact_info.contact.email \
        == 'no-reply@acme.example.com'
    assert fulfillment.asset.tiers.tier1.contact_info.contact.first_name == 'ACME'
    assert fulfillment.asset.tiers.tier1.contact_info.contact.last_name == 'Reseller'
    assert isinstance(fulfillment.asset.tiers.tier1.contact_info.contact.phone_number,
                      PhoneNumber)
    assert fulfillment.asset.tiers.tier1.contact_info.contact.phone_number.country_code \
        == '+1'
    assert fulfillment.asset.tiers.tier1.contact_info.contact.phone_number.area_code \
        == '234'
    assert fulfillment.asset.tiers.tier1.contact_info.contact.phone_number.phone_number \
        == '567890'
    assert fulfillment.asset.tiers.tier1.contact_info.contact.phone_number.extension == ''
    assert isinstance(fulfillment.asset.tiers.tier2, TierAccount)
    assert fulfillment.asset.tiers.tier2.id is None
    assert fulfillment.asset.tiers.tier2.name is None
    assert fulfillment.asset.tiers.tier2.external_id is None
    assert fulfillment.asset.tiers.tier2.contact_info is None

    assert fulfillment.contract is None
    assert fulfillment.marketplace is None

    # Test new items
    new_items = fulfillment.new_items
    assert isinstance(new_items, list)
    assert len(new_items) == 2
    for item in new_items:
        assert isinstance(item, Item)

    # Test changed items
    changed_items = fulfillment.changed_items
    assert isinstance(new_items, list)
    assert len(changed_items) == 2
    for item in changed_items:
        assert isinstance(item, Item)

    # Test removed items
    removed_items = fulfillment.removed_items
    assert isinstance(removed_items, list)
    assert len(removed_items) == 1
    for item in removed_items:
        assert isinstance(item, Item)


def test_fulfillment_needs_migration():
    fulfillments = Fulfillment.deserialize(load_str('response_migration.json'))
    assert isinstance(fulfillments, list)
    assert len(fulfillments) == 1
    fulfillment = fulfillments[0]
    assert isinstance(fulfillment, Fulfillment)

    assert fulfillment.needs_migration()

    fulfillment.asset.get_param_by_id('migration_info').value = ''
    assert not fulfillment.needs_migration()

    fulfillment.asset.params.remove(fulfillment.asset.get_param_by_id('migration_info'))
    assert fulfillment.asset.get_param_by_id('migration_info') is None
    assert not fulfillment.needs_migration()


@patch('requests.get')
def test_fulfillment_get_conversation_ok(get_mock):
    conversation_contents = load_str('conversation.json')
    get_mock.side_effect = [
        Response(True, '[' + conversation_contents + ']', 200),
        Response(True, conversation_contents, 200)
    ]

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id},
            url='http://localhost:8080/api/public/v1/conversations/'),
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            url='http://localhost:8080/api/public/v1/conversations/' + conversation.id)
    ])

    assert isinstance(conversation, Conversation)


@patch('requests.get')
def test_fulfillment_get_conversation_empty(get_mock):
    get_mock.return_value = Response(True, '[]', 200)

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 1
    get_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/conversations/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id}
        )
    ])

    assert conversation is None


@patch('requests.get')
def test_fulfillment_get_conversation_bad_deserialize(get_mock):
    get_mock.side_effect = [
        Response(True, '[' + load_str('conversation.json') + ']', 200),
        Response(True, '', 200)
    ]

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/conversations/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id}),
        call(
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'})
    ])

    assert conversation is None
