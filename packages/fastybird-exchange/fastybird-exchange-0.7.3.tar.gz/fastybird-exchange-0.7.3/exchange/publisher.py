#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Exchange plugin publisher
"""

# Python base dependencies
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union

# Library dependencies
from metadata.routing import RoutingKey
from metadata.types import ModuleOrigin, PluginOrigin


class IPublisher(ABC):  # pylint: disable=too-few-public-methods
    """
    Data exchange publisher interface

    @package        FastyBird:Exchange!
    @module         publisher

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def publish(
        self,
        origin: Union[ModuleOrigin, PluginOrigin],
        routing_key: RoutingKey,
        data: Optional[Dict],
    ) -> None:
        """Publish data to exchange bus"""


class Publisher:
    """
    Data exchange publisher proxy

    @package        FastyBird:Exchange!
    @module         publisher

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __publishers: Set[IPublisher]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        publishers: Optional[List[IPublisher]] = None,
    ) -> None:
        if publishers is None:
            self.__publishers = set()

        else:
            self.__publishers = set(publishers)

    # -----------------------------------------------------------------------------

    def publish(
        self,
        origin: Union[ModuleOrigin, PluginOrigin],
        routing_key: RoutingKey,
        data: Optional[Dict],
    ) -> None:
        """Call all registered publishers and publish data"""
        for publisher in self.__publishers:
            publisher.publish(origin=origin, routing_key=routing_key, data=data)

    # -----------------------------------------------------------------------------

    def register_publisher(
        self,
        publisher: IPublisher,
    ) -> None:
        """Register new publisher to proxy"""
        self.__publishers.add(publisher)
