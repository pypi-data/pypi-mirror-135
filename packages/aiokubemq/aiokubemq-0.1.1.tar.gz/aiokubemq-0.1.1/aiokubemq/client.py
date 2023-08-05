#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import typing
from typing import AsyncIterator

import grpc

from aiokubemq.enums import SubscribeType
from aiokubemq.proto import kubemq_pb2, kubemq_pb2_grpc
from aiokubemq.requests import (
    Event,
    EventStream,
    QueueMessageStream,
    Subscription,
    AckAllQueueMessages,
    QueueMessage,
    QueueMessageBatch,
    ReceiveQueueMessages,
    RPCRequest,
    RPCResponse,
    Request,
    StreamQueueMessagesRequest,
)


class KubeMQClient:
    def __init__(
        self,
        client_id: str,
        url: str,
        authentication: str = None,
        metadata: dict = None,
        credentials: grpc.ChannelCredentials = None,
    ):
        self.client_id = client_id
        if credentials is None:
            self._channel = grpc.aio.insecure_channel(url)
        else:
            self._channel = grpc.aio.secure_channel(url, credentials=credentials)
        self._stub = kubemq_pb2_grpc.kubemqStub(self._channel)
        self._metadata = {}

        if metadata is not None:
            self._metadata.update(metadata)

        if authentication is not None:
            self._metadata["authorization"] = authentication

    @property
    def metadata(self) -> list[tuple]:
        return [(key, val) for key, val in self._metadata.items()]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._channel.close()

    @typing.overload
    async def send(self, request: Event) -> kubemq_pb2.Result:
        ...

    @typing.overload
    async def send(
        self, request: Subscription
    ) -> AsyncIterator[typing.Union[kubemq_pb2.Request, kubemq_pb2.EventReceive]]:
        ...

    @typing.overload
    async def send(
        self, request: QueueMessageStream
    ) -> AsyncIterator[kubemq_pb2.StreamQueueMessagesResponse]:
        ...

    @typing.overload
    async def send(self, request: EventStream) -> AsyncIterator[kubemq_pb2.Result]:
        ...

    @typing.overload
    async def send(
        self, request: AckAllQueueMessages
    ) -> kubemq_pb2.AckAllQueueMessagesResponse:
        ...

    @typing.overload
    async def send(self, request: QueueMessage) -> kubemq_pb2.SendQueueMessageResult:
        ...

    @typing.overload
    async def send(
        self, request: QueueMessageBatch
    ) -> kubemq_pb2.QueueMessagesBatchResponse:
        ...

    @typing.overload
    async def send(
        self, request: ReceiveQueueMessages
    ) -> kubemq_pb2.ReceiveQueueMessagesResponse:
        ...

    @typing.overload
    async def send(self, request: RPCRequest) -> kubemq_pb2.Response:
        ...

    @typing.overload
    async def send(self, request: RPCResponse) -> None:
        ...

    async def send(
        self, request: Request
    ) -> typing.Union[
        kubemq_pb2.Result,
        kubemq_pb2.Response,
        kubemq_pb2.ReceiveQueueMessagesResponse,
        kubemq_pb2.QueueMessagesBatchResponse,
        kubemq_pb2.SendQueueMessageResult,
        kubemq_pb2.AckAllQueueMessagesResponse,
        AsyncIterator[
            typing.Union[
                kubemq_pb2.Request,
                kubemq_pb2.EventReceive,
                kubemq_pb2.StreamQueueMessagesResponse,
                kubemq_pb2.Result,
            ]
        ],
        None,
    ]:
        if isinstance(request, EventStream):

            async def request_converter(stream):
                async for req in stream:
                    req: Event
                    yield req.to_lowlevel_object(client_id=self.client_id)

            streamer = self._stub.SendEventsStream(
                request_converter(request.stream), metadata=self.metadata
            )
            return streamer
        elif isinstance(request, Event):
            return await self._stub.SendEvent(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, QueueMessage):
            return await self._stub.SendQueueMessage(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, QueueMessageBatch):
            return await self._stub.SendQueueMessagesBatch(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, QueueMessageStream):

            async def request_converter(stream):
                async for req in stream:
                    req: StreamQueueMessagesRequest
                    yield req.to_lowlevel_object(client_id=self.client_id)

            streamer = self._stub.StreamQueueMessage(
                request_converter(request.stream), metadata=self.metadata
            )
            return streamer
        elif isinstance(request, ReceiveQueueMessages):
            return await self._stub.ReceiveQueueMessages(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, AckAllQueueMessages):
            return await self._stub.AckAllQueueMessages(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, RPCRequest):
            return await self._stub.SendRequest(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, RPCResponse):
            return await self._stub.SendResponse(
                request.to_lowlevel_object(client_id=self.client_id),
                metadata=self.metadata,
            )
        elif isinstance(request, Subscription):
            if (
                request.typ == SubscribeType.Events
                or request.typ == SubscribeType.EventsStore
            ):
                return self._stub.SubscribeToEvents(
                    request.to_lowlevel_object(client_id=self.client_id),
                    metadata=self.metadata,
                )
            elif (
                request.typ == SubscribeType.Queries
                or request.typ == SubscribeType.Commands
            ):
                return self._stub.SubscribeToRequests(
                    request.to_lowlevel_object(client_id=self.client_id),
                    metadata=self.metadata,
                )
            else:
                raise ValueError("Unknown SubscribeType")
        else:
            raise ValueError("Unknown request")

    async def ping(self) -> kubemq_pb2.PingResult:
        return await self._stub.Ping(kubemq_pb2.Empty())
