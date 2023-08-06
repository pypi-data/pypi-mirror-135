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

# language_level=3

"""
Codec for AMQP 1.0 messages.

Why custom codec:

    >>> import proton
    >>> proton.VERSION
    (0, 35, 0)
    >>> timeit proton.Message(body='abcd').encode()
    13.2 µs ± 31.6 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

    >>> import uamqp
    >>> uamqp.__version__
    '1.4.3'
    >>> timeit uamqp.Message(body='abcd').encode_message()
    6.63 µs ± 45.1 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

    >>> from rbfly.amqp._message import Message, encode_amqp
    >>> buff = bytearray(1024)
    >>> timeit encode_amqp(Message(b'abcd'))
    113 ns ± 3.31 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

RbFly codec adds little overhead to basic, binary message, which allows to
use AMQP 1.0 by default for all use cases.
"""

import array
import cython
import logging
from cpython cimport array, PyUnicode_CheckExact, PyBytes_CheckExact

from libc.stdint cimport uint32_t
from libc.string cimport memcpy

from .._codec cimport pack_uint32, unpack_uint32
from ..types import AMQPBody

logger = logging.getLogger(__name__)

DEF DESCRIPTOR_START = 0x00
DEF DESCRIPTOR_MESSAGE_BINARY = 0x75
DEF DESCRIPTOR_MESSAGE_VALUE = 0x77
DEF TYPE_ULONG = 0x53
DEF TYPE_BINARY_SHORT = 0xa0
DEF TYPE_BINARY_LONG = 0xb0
DEF TYPE_STRING_SHORT = 0xa1
DEF TYPE_STRING_LONG = 0xb1

@cython.no_gc_clear
@cython.final
@cython.freelist(1000)
cdef class Message:
    def __cinit__(self, object body, *, int stream_offset=0, float stream_timestamp=0):
        self.body = body

        self.stream_offset = stream_offset
        self.stream_timestamp = stream_timestamp

    def __eq__(self, other: Message):
        return self.body == other.body \
            and self.stream_offset == other.stream_offset \
            and self.stream_timestamp == other.stream_timestamp

    def __repr__(self) -> str:
        return 'Message(body={!r}, stream_offset={}, stream_timestamp={})'.format(
            self.body[:10] if self.body else None,
            self.stream_offset,
            self.stream_timestamp,
        )

def encode_amqp(buffer: bytearray, message: Message) -> int:
    return c_encode_amqp(<char*> buffer, message)

def decode_amqp(char *buffer) -> Message:
    return c_decode_amqp(buffer)

# NOTE: callee checks for buffer overflow
cdef Message c_decode_amqp(char *buffer):
    cdef:
        uint32_t code
        object body
        Py_ssize_t body_len
        Py_ssize_t offset = 0
        unsigned char is_str = 0
        unsigned char valid = 1

    code = unpack_uint32(&buffer[offset])
    offset += sizeof(uint32_t)

    if code == 0x005375b0 or code == 0x005377b1:
        body_len = unpack_uint32(&buffer[offset])
        offset += sizeof(uint32_t)
        is_str = code % 2 == 1
    elif code == 0x005375a0 or code == 0x005377a1:
        body_len = buffer[offset]
        offset += 1
        is_str = code % 2 == 1
    else:
        valid = 0
        logger.warning('cannot decode message for code: 0x{:04x}'.format(code))

    if not valid:
        body = None
    elif is_str:
        body = buffer[offset:offset + body_len].decode('utf-8')
    else:
        body = <bytes> buffer[offset:offset + body_len]

    return Message(body)

cdef Py_ssize_t c_encode_amqp(char *buffer, object message) except -1:
    cdef:
        Py_ssize_t offset = 0
        Py_ssize_t size
        object body = (<Message> message).body

    if PyBytes_CheckExact(body):
        size = len(body)

        offset += _encode_descriptor_start(&buffer[offset], DESCRIPTOR_MESSAGE_BINARY)
        offset += _encode_strb(
            &buffer[offset],
            body, size,
            TYPE_BINARY_SHORT, TYPE_BINARY_LONG
        )

    elif PyUnicode_CheckExact(body):
        body_bin = body.encode('utf-8')
        size = len(body_bin)

        offset += _encode_descriptor_start(&buffer[offset], DESCRIPTOR_MESSAGE_VALUE)
        offset += _encode_strb(
            &buffer[offset],
            body_bin, size,
            TYPE_STRING_SHORT, TYPE_STRING_LONG
        )

    else:
        raise TypeError('Cannot encode message with body of type: {}'.format(type(body)))

    return offset

cdef inline Py_ssize_t _encode_descriptor_start(char *buffer, unsigned char descriptor_code):
    buffer[0] = DESCRIPTOR_START
    buffer[1] = TYPE_ULONG
    buffer[2] = descriptor_code
    return 3

cdef inline Py_ssize_t _encode_strb(
        char *buffer,
        char *body,
        Py_ssize_t size,
        unsigned char code_short,
        unsigned char code_long,
    ) except -1:

    cdef Py_ssize_t offset = 0

    if size < 256:
        buffer[offset] = code_short
        offset += 1
        buffer[offset] = size
        offset += 1
    elif size < 2 ** 32:
        buffer[offset] = code_long
        offset += 1
        pack_uint32(&buffer[offset], size)
        offset += 4
    else:
        raise ValueError('Data too long, size={}'.format(size))

    memcpy(&buffer[offset], <char*> body, size)
    return offset + size

# vim: sw=4:et:ai
