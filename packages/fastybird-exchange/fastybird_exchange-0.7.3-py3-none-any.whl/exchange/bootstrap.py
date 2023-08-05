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
Exchange plugin DI container
"""

# pylint: disable=no-value-for-parameter

# Library dependencies
from typing import List

# Library dependencies
from kink import di, inject

# Library libs
from exchange.consumer import Consumer, IConsumer
from exchange.publisher import IPublisher, Publisher


def create_container() -> None:
    """Create exchange plugin services"""
    di[Publisher] = Publisher()
    di["fb-exchange_publisher"] = di[Publisher]

    di[Consumer] = Consumer()
    di["fb-exchange_consumer"] = di[Consumer]

    @inject
    def register_publishers(publishers: List[IPublisher] = None) -> None:  # type: ignore[assignment]
        if publishers is None:
            return

        for publisher in publishers:
            di[Publisher].register_publisher(publisher=publisher)

    @inject
    def register_consumers(consumers: List[IConsumer] = None) -> None:  # type: ignore[assignment]
        if consumers is None:
            return

        for consumer in consumers:
            di[Consumer].register_consumer(consumer=consumer)

    register_publishers()
    register_consumers()
