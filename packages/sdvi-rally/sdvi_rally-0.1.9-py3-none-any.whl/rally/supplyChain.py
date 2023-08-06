""" Rally Supply Chain support.

Provides management of Rally supply chains

Import example:

>>> from rally import supplyChain
"""
__all__ = [
    'SupplyChainStep',
    'SupplyChainSplit',
    'SupplyChainSequence',
    'SupplyChainCancel',
    'start_new_supply_chain',
    'set_scheduled_supply_chain',
    'get_scheduled_supply_chain',
    'create_supply_chain_marker',
    'get_supply_chain_metadata',
    'set_supply_chain_metadata'
]
import datetime
import functools
import uuid

from rally import exceptions
from rally._utils import _datetimeToTimestamp, _toDatetime
from rally.context import context, ASSET_ID, BASE_ASSET_ID, JOB_UUID, ORG_ID, USER_ID, WORKFLOW_BASE_ID, WORKFLOW_ID, \
    WORKFLOW_RULE_ID, WORKFLOW_PARENT_ID
from ._session import _getSession, _getAssetByName


# TODO We need real examples for working with SupplyChains


class SupplyChainStep:
    """ A step in a supply chain. Return an instance of this class for the next step in the supply chain

    :param name: The name of the supply chain step
    :type name: str
    :param dynamic_preset_data: Dynamic preset data passed to the supply chain step. Defaults to `None`
    :type dynamic_preset_data: dict, optional
    :param fail_step_name: Including this argument makes this SupplyChainStep a conditional when part of a
        SupplyChainSequence: `fail_step_name` will be executed instead of `name` if the immediately preceding step fails.
        Note: `fail_step_name` has no effect outside of a SupplyChainSequence.
    :type fail_step_name: str, optional
    :param preset: Overrides the step's preset with the preset of this name. Defaults to `None`
    :type preset: str, optional
    :param priority: Job priority for remainder of the supply chain, defaults to `None` (meaning that the supply chain's
        priority will not be changed). String values must be one of (shown ranked from greatest to least urgency):

        - `urgent`
        - `high`
        - `med_high`
        - `normal`
        - `med_low`
        - `low`
        - `background`
    :type priority:  int or str, optional
    :param supply_chain_deadline: SupplyChain deadline override for remainder of the supply chain. Defaults to `None`
    :type supply_chain_deadline: :py:class:`~datetime.datetime`, optional
    :param step_deadline: SupplyChain deadline override for the supply chain step. Defaults to `None`
    :type step_deadline: :py:class:`~datetime.datetime`, optional
    :param provider_filter: Provider tag for the supply chain step. Constrains provider used to those tagged with this
        TagName. Defaults to not constraining the provider
    :type provider_filter: str, optional
    :param retry_policy: Job retry policy for remainder of the supply chain. Must be
       a list of non-negative ints where each int is retry hold time in seconds. Defaults to `None`
    :type retry_policy: list(int), optional
    :param step_deadline_lic_only: Deadline for restricting to licensed managed providers. Specified either as a
       datetime as an absolute date, a timedelta as an offset before the normal job deadline, or as an integer number
       of hours as an offset before the normal job deadline.  Note, this deadline is ignored for jobs with priority
       higher than Normal.
    :type step_deadline_lic_only: :py:class:`~datetime.datetime`, :py:class:`~datetime.timedelta` or int, optional
    """

    def __init__(self, name, dynamic_preset_data=None, preset=None, priority=None, supply_chain_deadline=None,
                 step_deadline=None, provider_filter=None, retry_policy=None, step_deadline_lic_only=None,
                 fail_step_name=None):
        self.stepName = name
        self.dynamicPresetData = dynamic_preset_data
        self.presetName = preset
        self.workflowJobPriority = _get_job_priority(priority)
        self.movieDeadline = _datetimeToTimestamp(supply_chain_deadline) if supply_chain_deadline else None
        self.movieDeadlineNextStep = _datetimeToTimestamp(step_deadline) if step_deadline else None
        self.workflowJobRetryPolicy = retry_policy
        self.deadlineLicOnly = step_deadline_lic_only
        self.providerTag = provider_filter

        if fail_step_name:
            if isinstance(fail_step_name, str):
                self.failStepName = fail_step_name
            else:
                raise TypeError(f"invalid type for step: {type(fail_step_name).__name__}, expected: str")

        if isinstance(self.deadlineLicOnly, (int, float)):
            # convert from hours to mS
            # a negative value indicates a relative time before job deadline
            self.deadlineLicOnly = 0 - max(int(self.deadlineLicOnly * 60 * 60 * 1000), 0)
        elif isinstance(self.deadlineLicOnly, datetime.timedelta):
            # convert to number of hours for next conversion
            self.deadlineLicOnly = 0 - max(int(self.deadlineLicOnly.total_seconds() * 1000), 0)
        elif isinstance(self.deadlineLicOnly, datetime.datetime):
            # convert from hours to mS
            # a positive value indicates an absolute time
            self.deadlineLicOnly = _datetimeToTimestamp(self.deadlineLicOnly)

    def _toJson(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class _SupplyChainMixin:
    def _validateStep(self, step):
        if isinstance(step, str):
            return SupplyChainStep(step)

        validTypes = (SupplyChainStep,) if isinstance(self, SupplyChainSequence) else\
            (SupplyChainStep, SupplyChainSequence)

        if not isinstance(step, validTypes):
            raise TypeError(f"invalid type for step: {type(step).__name__}, expected:"
                            f" str, {', '.join([x.__name__ for x in validTypes])}")

        return step


class SupplyChainSplit(_SupplyChainMixin):
    """ An object to represent a split in a supply chain. Return this object to create a split in the supply chain.

    :param resume_step:
    :type resume_step: str, :class:`~rally.supplyChain.SupplyChainStep`, or :class:`~rally.supplyChain.SupplyChainSequence`
    """
    def __init__(self, resume_step):
        self.resumeStep = self._validateStep(resume_step)
        self.splitSteps = []

    def add_split(self, step, run_async=False):
        """ Add a split step.

        :param step: Initial supply chain step of a split in the parent supply chain.
        :type step: str, :class:`~rally.supplyChain.SupplyChainStep` or :class:`~rally.supplyChain.SupplyChainSequence`
        :param run_async: Set true to make this split path asynchronous.
        :type run_async: :boolean:
        """
        self.splitSteps.append({'isNewChildWorkflow': True, 'async': run_async, 'wfId': str(uuid.uuid4()),
                                'stepName': self._validateStep(step)})

    def _toJson(self):
        if all([split.get('async') for split in self.splitSteps]):
            raise Exception('all paths of a split cannot be async')
        return self.splitSteps + [self.resumeStep]


class SupplyChainSequence(_SupplyChainMixin):
    """
    An object to represent a sequence in a supply chain. Return this object to specify a list of next steps
    in the supply chain.

    """
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        """ Add a step the to sequence.

        :param step: Supply chain step
        :type step: str or :class:`~rally.supplyChain.SupplyChainStep`
        """
        self.steps.append(self._validateStep(step))

    def _toJson(self):
        return [x._toJson() for x in self.steps]


class SupplyChainCancel(_SupplyChainMixin):
    """
    Cancels all running and scheduled jobs associated with this supply chain. Supply chain continues at the
    specified SupplyChainStep.

    :param resume_step:
    :type resume_step: str, :class:`~rally.supplyChain.SupplyChainStep` or :class:`~rally.supplyChain.SupplyChainSequence`:
    """
    def __init__(self, resume_step):
        self.resumeStep = self._validateStep(resume_step)

    def _toJson(self):
        return {'cancelAllSubWorkflowsAndResumeAtStep': self.resumeStep}


def start_new_supply_chain(asset, step, dynamic_preset_data=None, preset_name=None, supply_chain_job_priority=None,
                           deadline=None, supply_chain_deadline_step_name=None, retry_policy=None,
                           client_resource_id=None):
    """ Start a new supply chain on the specified asset.

    :param asset: Name of the asset. The asset is created if it does not already exist.
    :type asset: str
    :param step: First step to execute in the new supply chain.
    :type step: str or :class:`~rally.supplyChain.SupplyChainStep`
    :param dynamic_preset_data: Dynamic preset data passed to the first step. Defaults to `None` (meaning no preset data
    :type dynamic_preset_data: dict, optional
    :param preset_name: First step preset name override. Defaults to `None`
    :type preset_name: str, optional
    :param supply_chain_job_priority: Job priority override for all steps in the supply chain, defaults to `None`
        (meaning the default priorities are preserved). String values must be one of (shown ranked from greatest to
        least urgency):

        - `urgent`
        - `high`
        - `med_high`
        - `normal`
        - `med_low`
        - `low`
        - `background`
    :type supply_chain_job_priority: int or str, optional
    :param deadline: Supply chain deadline time. Defaults to `None` (meaning this SupplyChain has no
        deadline)
    :type deadline: :py:class:`~datetime.datetime`, optional
    :param supply_chain_deadline_step_name: Name of the first step to execute in another supply chain. This step is
        provided with dynamicPresetData containing the following keys:

        - 'baseWorkflowId'
        - 'workflowId'
        - 'deadlineTime'
        - 'alertTime'

        This new SupplyChain is created and started only when the deadline is reached. It is not created or started
        if the original SupplyChain finishes before the deadline or if the supply-chain_deadline_time and/or the
        supply_chain_deadline_step_name is removed. Note it is possible this new SupplyChain could run after the
        original SupplyChain finishes if the finish time is near the deadline time. Defaults to `None` (meaning no new
        SupplyChain or SupplyChainStep is created upon reaching the deadline).
    :type supply_chain_deadline_step_name: str, optional
    :param retry_policy: Job retry policy override for all steps in the supply chain. Must be
           a list of non-negative ints where each int is retry hold time in seconds. Defaults to `None` (meaning the
           default policy is adhered to).
    :type retry_policy: list(int), optional
    :param client_resource_id: An identifier for the SupplyChain that is meaningful to the creator.  This identifier
        will be by default applied to all jobs in the SupplyChain and to descendent SupplyChains
    :type client_resource_id: str, optional

    Usage:

    >>> supplyChain.start_new_supply_chain('Yeti Corps', 'Vanguard')
    """
    if isinstance(step, (str, SupplyChainStep)):
        step = step if isinstance(step, str) else step._toJson()
    else:
        raise TypeError(f"invalid type for step: {type(step).__name__}, expected: str or SupplyChainStep")

    payload = {'assetName': asset,
               'firstStep': step,
               'dynamicPresetData': dynamic_preset_data,
               'presetName': preset_name,
               'jobPriority': _get_job_priority(supply_chain_job_priority),
               'jobRetryPolicy': retry_policy,
               'deadlineTime': _datetimeToTimestamp(deadline) if deadline else None,
               'deadlineStepName': supply_chain_deadline_step_name,
               'fromWfRuleId': context(WORKFLOW_RULE_ID),
               'clientResourceId': client_resource_id}

    if not context(ASSET_ID):
        payload['jobUuidForMovieId'] = context(JOB_UUID)

    s = _getSession()
    s.post('v1.0/workflow/new', json=payload)


def set_scheduled_supply_chain(step, asset_name=None, creation_delay=None, deadline_delay=None, idle_delay=None,
                               date_after=None):
    """

    .. warning::
        :func:`rally.supplyChain.set_scheduled_supply_chain` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    Set a scheduled supply chain for a given asset.

    .. note::
       At least one of 'creationDelay', 'deadlineDelay', 'idleDelay', or 'dateAfter' must be specified

    :param step: the name of the supply chain step to execute when the schedule condition is met
    :type step: str, :class:`~rally.supplyChain.SupplyChainStep`
    :param asset_name: the name of the asset to which to attach the scheduled supply chain, defaults to current supply chain's asset
    :type asset_name: str, optional
    :param creation_delay: the number of days after creation of the asset to trigger execution, defaults to not executing based on creation date
    :type creation_delay: int, optional
    :param deadline_delay: the number of days after the asset's deadline that the scheduled supply chain is executed, defaults to not executing based on deadline
    :type deadline_delay: int, optional
    :param idle_delay: the number of days of asset inactivity before running the scheduled supply chain, defaults to not executing based on idle time
    :type idle_delay: int, optional
    :param date_after: a timezone-aware :py:class:`datetime.datetime` on which to execute scheduled supply chain, defaults to not executing based on a date
    :type date_after: str, optional

    Usage:

    >>> supplyChain.set_scheduled_supply_chain('YakDelete', idle_delay=2)

    """
    # Validate inputs
    asset_id = _getAssetByName(asset_name) if asset_name else context(ASSET_ID)
    if not asset_id:
        raise exceptions.NotFound(asset_name or 'asset')

    payload = {
        'stepName': step.stepName if isinstance(step, SupplyChainStep) else step,
        'creationDelay': creation_delay if creation_delay else None,
        'deadlineDelay': deadline_delay if deadline_delay else None,
        'idleDelay': idle_delay if idle_delay else None,
        'dateAfter': _datetimeToTimestamp(date_after) if date_after else None,
    }

    _getSession().post(f'v1.0/scheduledWorkflow/{asset_id}', json=payload)


def get_scheduled_supply_chain(asset_name=None):
    """

    .. warning::
        :func:`rally.supplyChain.get_scheduled_supply_chain` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    Return a dict containing a representation of an asset's scheduled supply chain. Note that attributes whose values
    are `None` are not included in the return

    Scheduled Supply Chain dict attributes:
        - asset_id (:py:class:`int`)
        - creation_delay, days: (:py:class:`int`)
        - deadline_delay, days: (:py:class:`int`)
        - idle_delay, days: (:py:class:`int`)
        - date_after, date: (:py:class:`datetime.datetime`)
        - step_name: (:py:class:`str`)

    :param asset_name: the name of the asset, defaults to this asset
    :type asset_name: str, optional

    Usage:

    >>> supplyChain.get_scheduled_supply_chain()
    {
        'asset_id': 1,
        'idle_delay': 2,
        'step_name': 'YakDelete',
    }

    """
    asset_id = _getAssetByName(asset_name) if asset_name else context(ASSET_ID)
    if not asset_id:
        raise exceptions.NotFound(asset_name or 'asset')

    try:
        resp = _getSession().get(f'v1.0/scheduledWorkflow/{asset_id}')
        res = {}
        # Remove None values and Convert unix date to tz-aware datetime
        for key, value in resp.json().items():
            if value is not None:
                if key == 'date_after':
                    res[key] = _toDatetime(value)
                else:
                    res[key] = value
        return res
    except exceptions.RallyApiError as e:
        if e.code == 404:
            raise exceptions.NotFound(asset_name or 'asset')
        raise


def create_supply_chain_marker(description, icon, color):
    """
    Create a supply chain marker.

    :param description: Text description to be displayed with the marker, max 50 characters.
    :type description: str
    :param icon: CSS class name for the icon to be used as the marker.
    :type icon: str
    :param color: the icon color, one of:

        - 'pass': equivalent to `green`
        - 'fail': equivalent to `red`
        - a hex value (`#xxxxxx`), or
        - a web color name
    :type color: str

    Usage:

    >>> supplyChain.create_supply_chain_marker('Yeti-Marker', 'fa-thumb-tack', 'burlywood')

    .. seealso::
        `Font Awesome <https://fontawesome.com/icons?d=gallery>`_ documentation for available icons

        `Color keyword <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_ MDN documentation
    """
    description = description or ''

    if len(description) > 50:
        raise ValueError('description must be < 51 characters')
    if not isinstance(color, str):
        raise TypeError('color argument must be a string')

    payload = {
        'success': False if color.lower() == 'fail' else True,
        'desc': description,
        'icon': icon,
        'color': None if color.lower() in ('pass', 'fail') else color,
        'userId': context(USER_ID),
        'orgId': context(ORG_ID),
        'jobId': context(JOB_UUID),
        'assetId': context(ASSET_ID),
        'assetBaseId': context(BASE_ASSET_ID),
        'wfRuleId': context(WORKFLOW_RULE_ID),
        'wfId': context(WORKFLOW_ID),
        'wfBaseId': context(WORKFLOW_BASE_ID),
        'wfParentId': context(WORKFLOW_PARENT_ID),
    }

    s = _getSession()
    s.post('v1.0/workflow/marker', json=payload)


@functools.lru_cache()
def get_supply_chain_metadata(name=None):
    """ Return a dict containing an Asset's SupplyChain metadata. Raises a :class:`~rally.exceptions.NotFound` if the
    asset does not exist.

    .. warning::
        :func:`rally.supplyChain.get_supply_chain_metadata` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    :param name: the asset name, defaults to this Asset
    :type name: str, optional

    Usage:

    >>> supplyChain.get_supply_chain_metadata()
    {'spam': 'eggs', 'yaks': 5}
    """
    assetId = _getAssetByName(name) if name else context(ASSET_ID)
    if not assetId:
        raise exceptions.NotFound(name or 'asset')
    try:
        resp = _getSession().get(f'v2/supplyChainMetadata/{assetId}')
        return resp.json()['data']['attributes']['metadata']
    except exceptions.RallyApiError as err:
        if err.code == 404:
            return {}
        raise


# TODO limit size
def set_supply_chain_metadata(metadata):
    """ Set an Asset's SupplyChain metadata. Note this will replace any existing metadata

    .. warning::
        :func:`rally.supplyChain.set_supply_chain_metadata` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    .. warning::
        Altering supply chain metadata can seriously impact the function of a supply chain. Proceed at your own risk.

    :param metadata: metadata to set on the Asset
    :type metadata: dict

    Usage:

    >>> supplyChain.set_supply_chain_metadata({'spam': 'eggs'})
    """
    _getSession().put(f'v1.0/movie/{context(ASSET_ID)}/workflowMetadata2', json={'metadata': metadata})

    get_supply_chain_metadata.cache_clear()


def _get_job_priority(priority):
    priority_map = {
        'urgent': 'PriorityUrgent',
        'high': 'PriorityHigh',
        'med_high': 'PriorityMedHigh',
        'normal': 'PriorityNorm',
        'med_low': 'PriorityMedLow',
        'low': 'PriorityLow',
        'background': 'PriorityBackground'
    }

    if isinstance(priority, (int, type(None))):
        return priority
    # Normalize str priorities into something the API can understand (PascalCase `urgent` => `PriorityUrgent`)
    try:
        return priority_map[priority.lower()]
    except KeyError:
        raise ValueError(f'{priority} is not a valid priority')
