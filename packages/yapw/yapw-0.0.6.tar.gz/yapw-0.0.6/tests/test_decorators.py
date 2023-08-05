import logging
import signal
from collections import namedtuple
from unittest.mock import Mock, patch

import pytest

from yapw.decorators import default_decode, discard, requeue

# https://pika.readthedocs.io/en/stable/modules/spec.html#pika.spec.Basic.Deliver
Deliver = namedtuple("Deliver", "delivery_tag redelivered routing_key")
# https://pika.readthedocs.io/en/stable/modules/spec.html#pika.spec.BasicProperties
BasicProperties = namedtuple("BasicProperties", "content_type")


def raises(*args):
    raise Exception("message")


def passes(*args):
    pass


def closes(*args):
    global opened
    opened = True
    try:
        raise Exception("message")
    finally:
        opened = False


@patch("yapw.decorators.nack")
def test_decode_json(nack, caplog):
    caplog.set_level(logging.DEBUG)

    method = Deliver(1, False, "key")
    properties = BasicProperties("application/json")
    callback = Mock()

    discard(default_decode, callback, "state", "channel", method, properties, b'{"message": "value"}')

    callback.assert_called_once_with("state", "channel", method, properties, {"message": "value"})
    nack.assert_not_called()

    assert len(caplog.records) == 1
    assert caplog.records[-1].levelname == "DEBUG"
    assert (
        caplog.records[-1].message
        == 'Received message b\'{"message": "value"}\' with routing key key and delivery tag 1'
    )


@patch("yapw.decorators.nack")
def test_decode_bytes(nack, caplog):
    caplog.set_level(logging.DEBUG)

    method = Deliver(1, False, "key")
    properties = BasicProperties("application/octet-stream")
    callback = Mock()

    discard(default_decode, callback, "state", "channel", method, properties, b"message value")

    callback.assert_called_once_with("state", "channel", method, properties, b"message value")
    nack.assert_not_called()

    assert len(caplog.records) == 1
    assert caplog.records[-1].levelname == "DEBUG"
    assert caplog.records[-1].message == "Received message b'message value' with routing key key and delivery tag 1"


def test_decode_invalid(caplog):
    caplog.set_level(logging.DEBUG)

    function = Mock()
    signal.signal(signal.SIGUSR2, function)

    method = Deliver(1, False, "key")
    properties = BasicProperties("application/json")

    discard(default_decode, passes, "state", "channel", method, properties, b"invalid")

    function.assert_called_once()
    assert function.call_args[0][0] == signal.SIGUSR2

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[0].message == "Received message b'invalid' with routing key key and delivery tag 1"
    assert caplog.records[-1].levelname == "ERROR"
    assert caplog.records[-1].message == "b'invalid' can't be decoded, sending SIGUSR2"
    assert caplog.records[-1].exc_info


@patch("yapw.decorators.nack")
def test_discard(nack, caplog):
    caplog.set_level(logging.DEBUG)

    method = Deliver(1, False, "key")
    properties = BasicProperties("application/json")

    discard(default_decode, raises, "state", "channel", method, properties, b'"body"')

    nack.assert_called_once_with("state", "channel", 1, requeue=False)

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[0].message == "Received message b'\"body\"' with routing key key and delivery tag 1"
    assert caplog.records[-1].levelname == "ERROR"
    assert caplog.records[-1].message == "Unhandled exception when consuming b'\"body\"', discarding message"
    assert caplog.records[-1].exc_info


@pytest.mark.parametrize("redelivered,requeue_kwarg", [(False, True), (True, False)])
@patch("yapw.decorators.nack")
def test_requeue(nack, redelivered, requeue_kwarg, caplog):
    caplog.set_level(logging.DEBUG)

    method = Deliver(1, redelivered, "key")
    properties = BasicProperties("application/json")

    requeue(default_decode, raises, "state", "channel", method, properties, b'"body"')

    nack.assert_called_once_with("state", "channel", 1, requeue=requeue_kwarg)

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "DEBUG"
    assert caplog.records[0].message == "Received message b'\"body\"' with routing key key and delivery tag 1"
    assert caplog.records[-1].levelname == "ERROR"
    assert caplog.records[-1].message == f"Unhandled exception when consuming b'\"body\"' (requeue={requeue_kwarg})"
    assert caplog.records[-1].exc_info


@patch("yapw.decorators.nack")
def test_finally(nack):
    method = Deliver(1, False, "key")
    properties = BasicProperties("application/json")

    discard(default_decode, closes, "state", "channel", method, properties, b'"body"')

    global opened
    assert opened is False
