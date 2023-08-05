#!/usr/bin/python3
# -*- coding: utf-8 -*-
from enum import Enum


class SubscribeType(Enum):
    Undefined = 0
    Events = 1
    EventsStore = 2
    Commands = 3
    Queries = 4


class EventsStoreType(Enum):
    Undefined = 0
    StartNewOnly = 1
    StartFromFirst = 2
    StartFromLast = 3
    StartAtSequence = 4
    StartAtTime = 5
    StartAtTimeDelta = 6


class RequestType(Enum):
    Undefined = 0
    Command = 1
    Query = 2


class StreamRequestType(Enum):
    Undefined = 0
    ReceiveMessage = 1
    AckMessage = 2
    RejectMessage = 3
    ModifyVisibility = 4
    ResendMessage = 5
    SendModifiedMessage = 6
