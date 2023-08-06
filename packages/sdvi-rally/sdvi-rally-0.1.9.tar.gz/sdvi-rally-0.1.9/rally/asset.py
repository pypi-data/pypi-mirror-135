""" Asset support.

Provides functions for managing Rally assets

Importing the asset module:

>>> from rally import asset
"""

__all__ = [
    'create_asset',
    'get_asset',
    'rename_asset',
    'get_asset_tags',
    'add_asset_tags',
    'remove_asset_tags',
    'set_asset_deadline',
    'search_for_asset',
    'get_user_metadata',
    'set_user_metadata',
    'set_media_attribute_source',
    'get_asset_status_indicators',
    'add_asset_status_indicator',
    'clear_asset_status_indicator',
    'clear_all_asset_status_indicators'
]

import datetime
import functools
import json

from .context import context, ASSET_ID, JOB_UUID
from ._session import _getSession, _getAssetByName
from ._utils import _toDatetime, _datetimeToTimestamp
from . import exceptions


def create_asset(name, deadline=None):
    """ Create a new Asset

    :param name: The asset name. Must be unique in Rally
    :type name: str
    :param deadline: a timezone aware deadline, defaults to `None` (meaning this asset has no deadline)

        .. note::
            If used, the deadline must be a timezone aware :py:class:`~datetime.datetime` which Rally will process in UTC.

    :type deadline: :py:class:`~datetime.datetime`, optional

    >>> asset.create_asset('Yak Corps')
    """
    # ..TODO WHAT happens if name is x***5, or if name is a dict not a string
    #  we need some kind of validation on all arguments for types and legitimate data bounds

    if deadline:
        deadline = _datetimeToTimestamp(deadline)
    payload = {'data': {'type': 'assets', 'attributes': {'name': name, 'deadline': deadline}}}

    try:
        _getSession().post(f'v2/assets', json=payload)
    except exceptions.RallyApiError as err:
        if err.code == 409:
            raise exceptions.AlreadyExists(name) from err
        raise


def get_asset(name=None):
    """ Returns a :py:class:`dict` representation of an Asset. Raises :class:`~rally.exceptions.NotFound` if the asset does not exist

    :param name: The asset name, defaults to this Asset
    :type name: str, optional

    Usage:

    >>> asset.get_asset('Yak Corps')
    {'createdAt': datetime.datetime(..., tzinfo=datetime.timezone.utc), 'deadline': None, 'mediaAttributesLabel': None, 'name': 'Yak Corps'}
    """
    if name is None:
        if not context(ASSET_ID):
            raise exceptions.NotFound('Rally context asset')
        resp = _getSession().get(f'v2/assets/{context(ASSET_ID)}')
        resp = resp.json()['data']['attributes']
    else:
        try:
            resp = _getAssetByName(name, fullRep=True)['attributes']
        except exceptions.RallyApiError as e:
            if e.code == 404:
                raise exceptions.NotFound(name)
            raise

    def toDatetime(ts):
        return _toDatetime(ts) if ts else None

    # Asset Rules
    # When adding items to the set of Asset attributes run these tests,
    #  if the attribute is a collection (e.g. tags) then it should be retrieved with a separate function calls
    #  if the attribute is of no apparent value to SupplyChains (e.g. favorite) then do not include it
    #  if the attribute is in a non-pythonic type (e.g. Posix Epoch timestamp) then convert it (e.g. Datetime)
    #  if the attribute is used as an argument in other functions then include it
    #  if the attribute has a use case and does not incur additional API traffic then include it
    #  else do not include it
    attrs = {'createdAt': toDatetime,
             'deadline': toDatetime,
             'mediaAttributesLabel': lambda x: x,
             'name': lambda x: x}

    result = {}
    for k, v in resp.items():
        if k in attrs:
            result[k] = attrs[k](v)
    return result


# TODO LOREN- the API needs to paginate this stuff
def get_asset_tags(name=None):
    """ Returns a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ containing the tags for an Asset

    :param name: the asset name, defaults to the current asset.
    :type name: str, optional

    Usage:

    >>> next(asset.get_asset_tags())
    'Fantastic'
    """
    assetId = _getAssetByName(name) if name else context(ASSET_ID)

    resp = _getSession().get(f'v2/assets/{assetId}')
    return (tag for tag in resp.json()['data']['attributes']['tagList'])


def set_asset_deadline(deadline):
    """ Set a deadline on an Asset

    :param deadline: a timezone aware Asset deadline

        .. note::
            The deadline must be a timezone aware :py:class:`~datetime.datetime` which Rally will process in UTC.

    :type deadline: :py:class:`~datetime.datetime`

    Usage:

    >>> asset.set_asset_deadline(datetime.datetime.now(tz=datetime.timezone.utc))
    """
    s = _getSession()
    payload = {'data': {'type': 'assets', 'attributes': {'deadline': _datetimeToTimestamp(deadline)}}}
    s.patch(f'v2/assets/{context(ASSET_ID)}', json=payload)


def rename_asset(new_name):
    """ Renames an Asset

    :param new_name: the new name
    :type new_name: str

    .. warning::

        **Care should be taken when renaming Assets.**

        Names are the handle for an Asset.

        If another client (API, Evaluate, etc) has persisted or is actively working with the current name the rename
        operation *will* cause havok.

        You have been warned

    Usage:

    >>> asset.get_asset()['name']
    'Yak'
    >>> asset.rename_asset('Yeti')
    >>> asset.get_asset()['name']
    'Yeti'
    """
    s = _getSession()

    payload = {'data': {'type': 'assets', 'attributes': {'name': new_name}}}
    try:
        if not context(ASSET_ID):
            raise exceptions.NotFound('Rally context asset')
        s.patch(f'v2/assets/{context(ASSET_ID)}', json=payload)
    except exceptions.RallyApiError as err:
        if err.code == 409:
            raise exceptions.AlreadyExists(new_name)
        raise


def add_asset_tags(tags):
    """ Add tags to the current Asset. An Asset can only have 25 tags.

    :param tags: tag(s) to add to the Asset, maximum 25
    :type tags: collection (str), or `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ (str)

    >>> asset.add_asset_tags(['red', 'green'])
    """
    if isinstance(tags, str):
        raise TypeError('tags must be an iterator')
    tags = set(tags)
    if len(tags) > 25:
        raise ValueError('cannot set more than 25 tags')
    tags = {t: True for t in tags}
    payload = {'data': {'type': 'assets', 'attributes': {'tags': tags}}}
    _getSession().patch(f'v2/assets/{context(ASSET_ID)}', json=payload)


def remove_asset_tags(tags):
    """ Removes the given tags from the current Asset

    :param tags: tag(s) to remove from the Asset, maximum 25
    :type tags: collection (str), or `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ (str)

    >>> asset.remove_asset_tags(['red', 'green'])

    Remove all tags:

    >>> asset.remove_asset_tags(asset.get_asset_tags())
    """
    if isinstance(tags, str):
        raise TypeError('tags must be an iterator')
    tags = set(tags)
    if len(tags) > 25:
        raise ValueError('cannot remove more than 25 tags')
    tags = {t: False for t in tags}

    payload = {'data': {'type': 'assets', 'attributes': {'tags': tags}}}
    _getSession().patch(f'v2/assets/{context(ASSET_ID)}', json=payload)


# TODO don't let users search for things that are really expensive, over time.
#  These need to be very specific tunable queries
def search_for_asset(criterion):
    """ Returns a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ containing asset dictionaries matching the given criterion

    .. warning::

        :func:`rally.asset.search_for_asset` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :param criterion: the search parameters

        You can search for assets using only a single criteria, specified as a dictionary containing ``{ DOMAIN: {KEY: VALUE} }``:
            - ``'inventory'`` DOMAIN: search for assets by inventory contents
                - ``'label'``: search for inventory containing a label
                - ``'tag'``: search for inventory containing a File Tag
                - ``'uri'``: search for inventory containing a URI
            - ``'asset'`` DOMAIN: search for assets by their attributes
                - ``'tag'``: search for an Asset with tag

        .. note::
            Inventory domain searches are currently limited to the first 1000 results.

    :type criterion: dict

    Usage:

    >>> next(asset.search_for_asset({'inventory': {'uri': 's3://bucket/prefix/file'}}))
    'Sasquatch One'
    """
    # TODO (note?) this does not work with "rsl://" schemes but elsewhere we ONLY work with rsl://
    if 'inventory' in criterion:
        resp = _getSession().get(f'v1.0/movie/search', json=criterion)
        # TODO This currently is not a paged search -- we are limiting to 1000.
        for x in resp.json()['assets']:
            yield x

    elif 'asset' in criterion:
        # the V2 api error checking is lacking, just returning an empty list if filter criteria isn't understood
        # to compensate for that we do the error checking here
        query = criterion['asset']
        if len(query) > 1:
            raise ValueError(f'too many criteria: {list(query.keys())}')

        qKey, qValue = next(iter(query.items()))

        if qKey not in ('tag', ):  # list of queries we can send to the V2
            raise NotImplementedError(f'unsupported criteria "{qKey}"')

        if not isinstance(qValue, str):
            raise TypeError(f'{qValue} must be of type str')

        marker = None

        while True:
            if marker:
                path = marker
            else:
                path = f'v2/assets?page=1p100&filter={qKey}%3D{qValue}'
            page = _getSession().get(path).json()
            marker = page['links']['next']
            for asset in page['data']:
                yield asset['attributes']['name']

            if not marker:
                break

    else:
        raise ValueError(f'invalid criteria: {list(criterion.keys())}')


@functools.lru_cache()
def get_user_metadata(name=None):
    """ Returns a dictionary containing the given Asset's metadata. Raises NotFound if the asset is not found

    .. warning::

        :func:`rally.asset.get_user_metadata` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :param name: Desired asset name, defaults to the current Asset.
    :type name: str, optional

    Usage:

    >>> asset.get_user_metadata()
    {'spam': 'eggs', 'yaks': 5}
    """
    assetId = _getAssetByName(name) if name else context(ASSET_ID)
    if not assetId:
        raise exceptions.NotFound(name or 'Rally context asset')
    try:
        resp = _getSession().get(f'v2/userMetadata/{assetId}')
    except exceptions.RallyApiError as err:
        if err.code == 404:
            return {}
        raise

    return resp.json()['data']['attributes']['metadata']


# TODO max size for metadata, TBD, but we want one
def set_user_metadata(metadata):
    """ Set the metadata for an Asset

    .. warning::

        :func:`rally.asset.set_user_metadata` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :type metadata: dict
    :param metadata: metadata to set on the Asset

    Usage:

    >>> asset.set_user_metadata({'spam': 'eggs'})
    """
    if not isinstance(metadata, dict):
        raise TypeError('metadata must be of type dict')

    assetId = context(ASSET_ID)

    _getSession().put(f'v1.0/movie/{assetId}/metadata', json=metadata, params={'replace': True})

    get_user_metadata.cache_clear()


def set_media_attribute_source(label):
    """ Sets the source for this asset's media attributes. Setting this value to `None` removes the source and forces
    Rally to assign attributes using the "old" way

    .. warning::

        :func:`rally.asset.set_media_attribute_source` is in Alpha Preview and is not considered suitable for Production
        use.  Experimentation in lower environments is encouraged.

    :param label: The label of an inventory item to be used as the source of this asset's media attributes
    :type label: str or None

    Usage:

    >>> asset.set_media_attribute_source('Yak')
    """
    assetId = context(ASSET_ID)
    payload = {'data': {'type': 'assets', 'attributes': {'mediaAttributesLabel': label}}}
    _getSession().patch(f'v2/assets/{assetId}', json=payload)


def get_asset_status_indicators(group=None, asset_name=None):
    """ Return a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ of dicts
    containing attributes of asset status indicators. The dict has the following keys:

        :id: (int) the id of the indicator
        :message: (str) the message associated with the indicator
        :group: (str) the group in which the indicator is included
        :icon: (str) the name of the `Font Awesome <https://fontawesome.com/icons?d=gallery>`_ icon class
        :color: (str) a hex value or color name for the icon
        :createdAt: (datetime) when the indicator was created
        :cleared: (bool) current cleared status
        :clearedAt:  (datetime, or None) when the indicator was cleared, if applicable

    :param group: The name of the group to filter on
    :type group: str, optional
    :param asset_name: The name of an asset to filter on, defaults to current asset
    :type asset_name: str, optional

    """
    indicatorAttributes = ('message', 'group', 'icon', 'color', 'createdAt', 'cleared')

    paramFilter = {}

    assetId = _getAssetByName(asset_name) if asset_name else context(ASSET_ID)

    if not assetId:
        raise exceptions.NotFound(f'asset {asset_name}')
    else:
        paramFilter['assetId'] = assetId

    if group:
        if not isinstance(group, str):
            raise TypeError('group must be a string')
        paramFilter['group'] = group

    marker = None

    while True:
        if marker:
            path = marker
            params = None
        else:
            path = 'v2/assetStatusIndicators'
            params = {'page': '1p100', 'filter': json.dumps(paramFilter)}

        page = _getSession().get(path, params=params).json()
        marker = page['links']['next']

        for i in page['data']:
            indicator = {'id': i.get('id')}
            attributes = i.get('attributes', {})
            for attr in indicatorAttributes:
                if attr == 'createdAt':
                    indicator[attr] = _toDatetime(attributes.get(attr))
                else:
                    indicator[attr] = attributes.get(attr)
            yield indicator

        if not marker:
            return


def add_asset_status_indicator(message, group, icon, color, asset_name=None, curate_message=False, curate_group=False):
    """ Create a status indicator, optionally adding the group and/or message to the curated lists

    :param message: The message to be displayed with the indicator icon
    :type message: str
    :param group: The group in which the indicator should be included
    :type group: str
    :param icon: The name of the `Font Awesome <https://fontawesome.com/icons?d=gallery>`_ icon class
    :type icon: str
    :param color: A hex value or `Color keyword <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_
    :type color: str
    :param asset_name: The asset to which to add the indicator, defaults to the current asset
    :type asset_name: str, optional
    :param curate_message: Whether to save the message as a curated Asset Status Message, defaults to False
    :type curate_message: bool, optional
    :param curate_group: Whether to save the group as a curated Asset Status Group, defaults to False
    :type curate_group: bool, optional

    """
    assert isinstance(message, str), 'message must be a string'
    assert isinstance(group, str), 'group must be a string'
    assert isinstance(icon, str), 'icon must be a string'
    assert isinstance(color, str), 'color must be a string'

    assetId = _getAssetByName(asset_name) if asset_name else context(ASSET_ID)
    if not assetId:
        raise exceptions.NotFound()

    indicator_payload = {'data': {
        'type': 'assetStatusIndicators',
        'attributes': {
            'group': group,
            'icon': icon,
            'message': message,
            'color': color,
            'curate_message': curate_message,
            'curate_group': curate_group
        },
        'relationships': {
            'asset': {'data': {'id': assetId, 'type': 'assets'}},
            'job': {'data': {'id': context(JOB_UUID), 'type': 'jobs'}}
        }
    }}

    path = f'v2/assetStatusIndicators'
    _getSession().post(path, data=json.dumps(indicator_payload))


def clear_asset_status_indicator(indicator_id):
    """ Sets the `cleared` flag on the given Asset Status Indicator

    :param indicator_id: The id of the indicator to clear
    :type indicator_id: int

    """
    indicator_id = int(indicator_id)
    payload = {
        'data': {
            'type': 'assetStatusIndicators',
            'attributes': {'cleared': True}
        }
    }
    _getSession().patch(f'v2/assetStatusIndicators/{indicator_id}', data=json.dumps(payload))


def clear_all_asset_status_indicators(group=None, asset_name=None):
    """ Sets the `cleared` flag on: all indicators or all indicators in the named group associated with an asset.

    :param group: The name of the group from which to clear all indicators, defaults to clearing all of the asset's indicators
    :type group: str, optional
    :param asset_name: The name of a different asset from which to clear all indicators, defaults to the current asset
    :type asset_name: str, optional

    """
    indicatorIds = [indicator['id'] for indicator in get_asset_status_indicators(group=group, asset_name=asset_name)]
    for indicator_id in indicatorIds:
        clear_asset_status_indicator(indicator_id)
