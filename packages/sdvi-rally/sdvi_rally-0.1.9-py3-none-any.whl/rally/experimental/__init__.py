""" Support for new or experimental features. These features may be moved into other sub-modules as their behaviors
 are finalized

Importing the experimental module:

>>> from rally.experimental import <feature> [as <alias>]

.. warning::

    **DEPRECATION WARNING**: `rally.experimental.asset_status` methods will move out of the experimental
    submodule in a future release. They are now found in the `asset` submodule.

"""
from rally.experimental.asset_status import *
