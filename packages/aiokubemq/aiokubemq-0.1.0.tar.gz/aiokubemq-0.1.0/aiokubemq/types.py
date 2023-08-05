#!/usr/bin/python3
# -*- coding: utf-8 -*-
import dataclasses
from typing import Optional

from aiokubemq.proto import kubemq_pb2


@dataclasses.dataclass
class QueueMessageAttributes:
    timestamp: Optional[int] = None
    sequence: Optional[int] = None
    md5: Optional[str] = None
    receive_count: Optional[int] = None
    rerouted: Optional[bool] = None
    rerouted_from_queue: Optional[str] = None
    expiration_at: Optional[int] = None
    delayed_to: Optional[int] = None

    def to_lowlevel_object(self, **_):
        return kubemq_pb2.QueueMessageAttributes(
            Timestamp=self.timestamp,
            Sequence=self.sequence,
            MD5OfBody=self.md5,
            ReceiveCount=self.receive_count,
            ReRouted=self.rerouted,
            ReRoutedFromQueue=self.rerouted_from_queue,
            ExpirationAt=self.expiration_at,
            DelayedTo=self.delayed_to,
        )


@dataclasses.dataclass
class QueueMessagePolicy:
    expiration: Optional[int] = None
    delay: Optional[int] = None
    max_receive_count: Optional[int] = None
    max_receive_queue: Optional[str] = None

    def to_lowlevel_object(self, **_):
        return kubemq_pb2.QueueMessagePolicy(
            ExpirationSeconds=self.expiration,
            DelaySeconds=self.delay,
            MaxReceiveCount=self.max_receive_count,
            MaxReceiveQueue=self.max_receive_queue,
        )
