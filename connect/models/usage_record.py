# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UsageRecordSchema


class UsageRecord(BaseModel):
    """ Usage Record Object. """

    _schema = UsageRecordSchema()

    record_id = None  # type: str
    """ (str) Unique identifier od the usage record. """

    record_note = None  # type: str
    """ (str) Optional note. """

    item_search_criteria = None  # type: str
    """ (str) Macro that will be used to find out respective item in product. """

    item_search_value = None  # type: str
    """ (str) Value that will be used to identify item within product with the help of filter
    specified on 'item_search_criteria'. """

    amount = None  # type: float
    """ (float) Usage amount corresponding to a item of an asset.
    Only needed for CR, PR and TR Schemas. """

    quantity = None  # type: float
    """ (float) Usage quantity. """

    start_time_utc = None  # type: str
    """ (str) Start Time in UTC. """

    end_time_utc = None  # type: str
    """ (str) End Time in UTC. """

    asset_search_criteria = None  # type: str
    """ (str) Macro that will be used to find out respective asset belonging to the product. """

    asset_search_value = None  # type: str
    """ (str) alue that will be used to identify Asset belonging to the product with the help of
    filter specified on 'asset_search_criteria'. """

    item_name = None  # type: str
    """ (str) Item name to which usage record belongs to, only for reporting items that was
    not part of product definition. Items are reported and created dynamically. """

    item_mpn = None  # type: str
    """ (str) Item MPN to which usage record belongs to, only for reporting items that was
    not part of product definition. Items are reported and created dynamically. """

    item_unit = None  # type: str
    """ (str) Only for reporting items that was not part of product definition. Items are reported
    and created dynamically. """

    item_precision = None  # type: str
    """ (str) Precision of the item for which usage record belong to. Input data should be one of:
    integer, decimal(1), decimal(2), decimal(4), decimal(8). Only for reporting items that was
    not part of product definition. Items are reported and created dynamically. """

    category_id = None  # type: str
    """ (str) Category id to link this usage record with a category. """

    asset_recon_id = None  # type: str
    """ (str) Optional: Asset reconciliation ID provided by vendor. This value comes from a
    parameter value of the asset that is marked as recon id by vendor."""

    tier = None  # type: int
    """ (int) Tier level specified for linking usage record with a tier account of Asset in case
    of TR schema. """
