#
# Copyright (c) 2019 UAVCAN Development Team
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

from __future__ import annotations
import enum
import typing
import dataclasses
from ._timestamp import Timestamp


FragmentedPayload = typing.Sequence[memoryview]
"""
Transfer payload is allowed to be segmented to facilitate zero-copy implementations.
The format of the memoryview object should be 'B'.
We're using Sequence and not Iterable to permit sharing across multiple consumers.
"""


class Priority(enum.IntEnum):
    """
    Transfer priority enumeration follows the recommended names provided in the UAVCAN specification.
    We use integers here in order to allow usage of static lookup tables for conversion into transport-specific
    priority values. The particular integer values used here may be meaningless for some transports.
    """
    EXCEPTIONAL = 0
    IMMEDIATE   = 1
    FAST        = 2
    HIGH        = 3
    NOMINAL     = 4
    LOW         = 5
    SLOW        = 6
    OPTIONAL    = 7


@dataclasses.dataclass
class Transfer:
    """
    UAVCAN transfer representation.
    """
    timestamp: Timestamp
    """
    For output (tx) transfers this field contains the transfer creation timestamp.
    For input (rx) transfers this field contains the first frame reception timestamp.
    """

    priority: Priority
    """
    See :class:`Priority`.
    """

    transfer_id: int
    """
    When transmitting, the appropriate modulus will be computed by the transport automatically.
    Higher layers shall use monotonically increasing transfer-ID counters.
    """

    fragmented_payload: FragmentedPayload
    """
    See :class:`FragmentedPayload`. This is the serialized application-level payload.
    Fragmentation may be completely arbitrary.
    Received transfers usually have it fragmented such that one fragment corresponds to one received frame.
    Outgoing transfers usually fragment it according to the structure of the serialized data object.
    The purpose of fragmentation is to eliminate unnecessary data copying within the protocol stack.
    :func:`pyuavcan.util.refragment` is designed to facilitate regrouping when sending a transfer.
    """


@dataclasses.dataclass
class TransferFrom(Transfer):
    """
    Specialization for received transfers.
    """
    source_node_id: typing.Optional[int]
    """
    None indicates anonymous transfers.
    """
