#!/usr/bin/python3
# -*- coding: utf-8 -*-
import dataclasses
import time
import typing
from typing import Optional

from aiokubemq.enums import (
    StreamRequestType,
    RequestType,
    EventsStoreType,
    SubscribeType,
)
from aiokubemq.proto import kubemq_pb2
from aiokubemq.types import QueueMessageAttributes, QueueMessagePolicy


@dataclasses.dataclass
class Request:
    channel: str
    metadata: str = ""
    body: Optional[bytes] = None
    request_id: Optional[str] = None
    tags: Optional[dict] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


class Event(Request):
    event_id: str
    persistent: bool

    def __init__(self, *args, **kwargs):
        self.event_id = kwargs.pop("event_id", "")
        self.persistent = kwargs.pop("persistent", False)
        super(Event, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.Event(
            Channel=self.channel,
            ClientID=kwargs.get("client_id"),
            Store=self.persistent,
            EventID=self.event_id,
            Body=self.body,
            Tags=self.tags,
            Metadata=self.metadata,
        )


class EventStream(Request):
    def __init__(self, stream: typing.AsyncGenerator):
        self.stream = stream


class QueueMessage(Request):
    message_id: str
    attributes: QueueMessageAttributes
    policy: QueueMessagePolicy

    def __init__(self, *args, **kwargs):
        self.message_id = kwargs.pop("message_id", "")
        self.attributes = kwargs.pop("attributes", QueueMessageAttributes())
        self.policy = kwargs.pop("policy", QueueMessagePolicy())
        super(QueueMessage, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.QueueMessage(
            MessageID=self.message_id,
            ClientID=kwargs.pop("client_id"),
            Channel=self.channel,
            Metadata=self.metadata,
            Body=self.body,
            Tags=self.tags,
            Attributes=self.attributes.to_lowlevel_object(**kwargs),
            Policy=self.policy.to_lowlevel_object(**kwargs),
        )


class QueueMessageBatch(Request):
    messages: typing.List[QueueMessage]
    batch_id: Optional[str] = None

    def __init__(self, messages: typing.List[QueueMessage], batch_id: str = None):
        self.messages = messages
        self.batch_id = batch_id

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.QueueMessagesBatchRequest(
            BatchID=self.batch_id,
            Messages=(
                message.to_lowlevel_object(**kwargs) for message in self.messages
            ),
        )


class QueueMessageStream(Request):
    def __init__(self, stream: typing.AsyncGenerator):
        self.stream = stream


class StreamQueueMessagesRequest(Request):
    typ: StreamRequestType
    visibility_time: int
    wait_time: int
    ref_sequence: int
    modified_message: QueueMessage

    def __init__(self, *args, **kwargs):
        self.typ = kwargs.pop("typ", StreamRequestType.Undefined)
        self.visibility_time = kwargs.pop("visibility_seconds", 10)
        self.wait_time = kwargs.pop("wait_time", 60)
        self.ref_sequence = kwargs.pop("ref_sequence", 0)
        self.modified_message = kwargs.pop("modified_message", None)
        super(StreamQueueMessagesRequest, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.StreamQueueMessagesRequest(
            RequestID=self.request_id,
            ClientID=kwargs.pop("client_id"),
            Channel=self.channel,
            StreamRequestTypeData=self.typ.value,
            VisibilitySeconds=self.visibility_time,
            RefSequence=self.ref_sequence,
            ModifiedMessage=self.modified_message,
            WaitTimeSeconds=self.wait_time,
        )


class ReceiveQueueMessages(Request):
    max_messages: int
    wait_time: int
    peak: bool

    def __init__(self, *args, **kwargs):
        self.max_messages = kwargs.pop("max_messages", 1)
        self.wait_time = kwargs.pop("wait_time", 60)
        self.peak = kwargs.pop("peak", False)
        super(ReceiveQueueMessages, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.ReceiveQueueMessagesRequest(
            RequestID=self.request_id,
            ClientID=kwargs.pop("client_id"),
            Channel=self.channel,
            MaxNumberOfMessages=self.max_messages,
            WaitTimeSeconds=self.wait_time,
            IsPeak=self.peak,
        )


class AckAllQueueMessages(Request):
    wait_time: int

    def __init__(self, *args, **kwargs):
        self.wait_time = kwargs.pop("wait_time", 60)
        super(AckAllQueueMessages, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.AckAllQueueMessagesRequest(
            RequestID=self.request_id,
            Channel=self.channel,
            ClientID=kwargs.get("client_id"),
            WaitTimeSeconds=self.wait_time,
        )


class RPCRequest(Request):
    typ: RequestType
    timeout: int

    def __init__(self, *args, **kwargs):
        self.typ = kwargs.pop("typ", RequestType.Undefined)
        self.timeout = kwargs.pop("timeout", 30)
        super(RPCRequest, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.Request(
            ClientID=kwargs.get("client_id"),
            RequestID=self.request_id,
            Channel=self.channel,
            Body=self.body,
            RequestTypeData=self.typ.value,
            Timeout=self.timeout * 1000,  # convert to ms
            Metadata=self.metadata,
            Tags=self.tags,
        )


class RPCResponse(Request):
    executed: bool
    timestamp: int

    def __init__(self, *args, **kwargs):
        self.executed = kwargs.pop("executed", True)
        self.timestamp = kwargs.pop("timestamp", time.time())
        super(RPCResponse, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.Response(
            ClientID=kwargs.get("client_id"),
            RequestID=self.request_id,
            ReplyChannel=self.channel,
            Body=self.body,
            Executed=self.executed,
            Timestamp=int(self.timestamp),
            Metadata=self.metadata,
            Tags=self.tags,
        )


class Subscription(Request):
    typ: SubscribeType
    group: str
    events_store_type_data: EventsStoreType
    events_store_type_value: int

    def __init__(self, *args, **kwargs):
        self.typ = kwargs.pop("typ", SubscribeType.Undefined)
        self.group = kwargs.pop("group", None)
        self.events_store_type_data = kwargs.pop(
            "events_store_type_data", EventsStoreType.Undefined
        )
        self.events_store_type_value = kwargs.pop("events_store_type_value", None)
        super(Subscription, self).__init__(*args, **kwargs)

    def to_lowlevel_object(self, **kwargs):
        return kubemq_pb2.Subscribe(
            Channel=self.channel,
            ClientID=kwargs.get("client_id"),
            Group=self.group or "",
            EventsStoreTypeValue=self.events_store_type_value,
            EventsStoreTypeData=self.events_store_type_data.value,
            SubscribeTypeData=self.typ.value,
        )
