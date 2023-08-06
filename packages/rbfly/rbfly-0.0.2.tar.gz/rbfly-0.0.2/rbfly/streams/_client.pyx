#
# rbfly - a library for RabbitMQ Streams using Python asyncio
#
# Copyright (C) 2021-2022 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# cython: boundscheck=False, wraparound=False, initializedcheck=False, profile=False, language_level=3

"""
RabbitMQ Streams publishers (producers) and subscribers (consumers).

Publishers sending messages in AMQP format for two scenarios are implemented

- sending single message
- sending batch of messages

There are also publishers for sending opaque binary data implemented. These
are used to measure overhead of AMQP 1.0 encoding with the official
publishers. While these are not part of official API, they still can be
used and are supported.

Subscriber class implements RabbitMQ Streams message consumer. It supports
both AMQP 1.0 message format and opaque binary data.
"""

import cython
import typing as tp
from collections import deque

from ..amqp._message cimport Message
from ..types import AMQPBody
from .offset import Offset

class PublisherConstr(tp.Protocol):
    """
    Interface for publisher classes constructor.
    """
    def __init__(self, client, stream, id, message_id):
        ...

cdef class PublisherTrait:
    cdef:
        public int id
        public str stream
        public int message_id
        object client
    """
    Trait with basic publisher funcionality.

    :var client: RabbitMQ Streams client.
    :var stream: RabbitMQ stream name.
    :var id: Publisher id.
    :var message_id: Last value of published message id.
    """
    def __cinit__(self, object client, str stream, int id, int message_id):
        """
        Create publisher.

        :param client: RabbitMQ Streams client.
        :param stream: RabbitMQ stream name.
        :param id: Publisher id.
        :param message_id: Last value of published message id.
        """
        self.client = client
        self.stream = stream
        self.id = id
        self.message_id = message_id

    cpdef int next_message_id(self, int inc=1):
        """
        Get next value of message id.

        :param inc: Value by which to increase the message id.
        """
        self.message_id += inc
        return self.message_id

    async def _publish(self, message_id: int, *data: Message | bytes, amqp: bool=True) -> None:
        """
        Publish multiple messages to RabbitMQ stream.

        Connection error is ignored and then sending of messages is
        retried.

        :param message_id: Starting message id of published messages.
        :param data: Collection of messages to publish.
        :param amqp: Send messages in AMQP format or just opaque data.
        """
        while True:
            protocol = await self.client.get_protocol()
            try:
                await protocol.publish(self.id, self.message_id, *data, amqp=amqp)
            except ConnectionError:
                pass
            else:
                break

cdef class PublisherBatchTrait:
    """
    RabbitMQ Streams publisher trait for sending messages in batches.
    """
    def __init__(self, client, stream: str, id: cython.int, message_id: cython.int):
        """
        Create batch publisher for sending messages in AMQP format.
        """
        self._data: cython.list = []

cdef class Publisher(PublisherTrait):
    """
    RabbitMQ Streams publisher for sending single message in AMQP format.

    .. seealso:: :py:class:`rbfly.streams.PublisherBatch`
    """
    async def send(self, body: AMQPBody) -> None:
        """
        Send AMQP message to RabbitMQ stream.

        :param body: AMQP message body.
        """
        msg = Message(body)
        await self._publish(self.message_id, msg)
        self.next_message_id()

class PublisherBatch(PublisherTrait, PublisherBatchTrait):
    """
    RabbitMQ Streams publisher for sending batch of messages in
    AMQP format.

    .. seealso:: :py:class:`rbfly.streams.Publisher`
    """
    def batch(self, body: AMQPBody) -> None:
        """
        Enqueue single message for batch processing.

        :param body: Body of AMQP message.

        .. seealso:: :py:meth:`.PublisherBatch.flush`
        """
        self._data.append(body)

    async def flush(self) -> None:
        """
        Flush all enqueued messages.

        .. seealso:: :py:meth:`.PublisherBatch.batch`
        """
        data = (Message(v) for v in self._data)
        await self._publish(self.message_id, *data)

        self.next_message_id(len(self._data))
        self._data.clear()

#
# purely binary publishers; application is reponsible for data encoding and
# decoding; their implementation is for performance comparision purposes
# only
#

cdef class PublisherBin(PublisherTrait):
    """
    RabbitMQ Streams publisher for sending single message of binary data.

    An application is responsible for encoding and decoding the format of
    the data.

    .. seealso:: `Publisher`
    """
    async def send(self, message: bytes) -> None:
        """
        Send message binary data to RabbitMQ stream.

        :param message: Message binary data.
        """
        await self._publish(self.message_id, message, amqp=False)
        self.next_message_id()

class PublisherBinBatch(PublisherTrait, PublisherBatchTrait):
    """
    RabbitMQ Streams publisher for sending batch of messages in
    application's binary format.

    An application is responsible for encoding and decoding the format of
    the data.

    .. seealso:: `Publisher`
    """
    def batch(self, message: bytes) -> None:
        """
        Enqueue single message for batch processing.

        :param message: Binary message to send.

        .. seealso:: :py:meth:`.PublisherBinBatch.flush`
        """
        self._data.append(message)

    async def flush(self) -> None:
        """
        Flush all enqueued messages.

        .. seealso:: `batch`
        """
        await self._publish(self.message_id, *self._data, amqp=False)
        self.next_message_id(len(self._data))
        self._data.clear()

class Subscriber:
    """
    RabbitMQ Streams subscriber.

    Use subscriber to iterate over messages read from a stream.

    :var client: RabbitMQ Streams client.
    :var stream: RabbitMQ stream name.
    :var subscription_id: RabbitMQ stream subscription id.
    :var offset: RabbitMQ Streams offset specification.
    :var message: Last received message or null.
    :var amqp: Messages are in AMQP 1.0 format if true. Otherwise no AMQP decoding.
    """
    def __init__(self, client, stream: str, subscription_id: int, offset: Offset, amqp: bool) -> None:
        self.client = client
        self.stream = stream
        self.subscription_id = subscription_id
        self.offset = offset
        self.amqp = amqp
        self.message: Message | None = None

        self._buffer = deque

    async def __aiter__(self) -> tp.AsyncIterator[Message]:
        """
        Iterate over messages read from a stream.
        """
        while True:
            try:
                protocol = await self.client.get_protocol()
                messages = await protocol.read_stream(self.subscription_id, self.amqp)
            except ConnectionError:
                pass
            else:
                while messages:
                    self.message = messages.popleft()
                    yield self.message

# vim: sw=4:et:ai
