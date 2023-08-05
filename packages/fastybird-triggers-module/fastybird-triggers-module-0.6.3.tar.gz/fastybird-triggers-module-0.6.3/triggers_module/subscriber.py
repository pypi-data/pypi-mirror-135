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
Triggers module subscriber module
"""

# Python base dependencies
import datetime
from typing import Dict, Optional, Type

# Library dependencies
from kink import inject
from metadata.routing import RoutingKey
from metadata.types import ModuleOrigin
from sqlalchemy import event

# Library libs
from triggers_module.entities.action import (
    ActionEntity,
    ChannelPropertyActionEntity,
    DevicePropertyActionEntity,
)
from triggers_module.entities.base import Base, EntityCreatedMixin, EntityUpdatedMixin
from triggers_module.entities.condition import (
    ChannelPropertyConditionEntity,
    ConditionEntity,
    DateConditionEntity,
    DevicePropertyConditionEntity,
    TimeConditionEntity,
)
from triggers_module.entities.notification import (
    EmailNotificationEntity,
    SmsNotificationEntity,
)
from triggers_module.entities.trigger import (
    AutomaticTriggerEntity,
    ManualTriggerEntity,
    TriggerControlEntity,
    TriggerEntity,
)
from triggers_module.exchange import IPublisher
from triggers_module.repositories.state import (
    IActionStateRepository,
    IConditionStateRepository,
)


class EntityCreatedSubscriber:
    """
    New entity creation subscriber

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def __init__(self) -> None:
        event.listen(
            Base, "before_insert", lambda mapper, connection, target: self.before_insert(target), propagate=True
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def before_insert(target: Base) -> None:
        """Before entity inserted update timestamp"""
        if isinstance(target, EntityCreatedMixin):
            target.created_at = datetime.datetime.now()


class EntityUpdatedSubscriber:
    """
    Existing entity update subscriber

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def __init__(self) -> None:
        event.listen(
            Base, "before_update", lambda mapper, connection, target: self.before_update(target), propagate=True
        )

    # -----------------------------------------------------------------------------

    @staticmethod
    def before_update(target: Base) -> None:
        """Before entity updated update timestamp"""
        if isinstance(target, EntityUpdatedMixin):
            target.updated_at = datetime.datetime.now()


@inject
class EntitiesSubscriber:
    """
    Data exchanges utils

    @package        FastyBird:TriggersModule!
    @module         subscriber

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    CREATED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGERS_ENTITY_CREATED,
        AutomaticTriggerEntity: RoutingKey.TRIGGERS_ENTITY_CREATED,
        TriggerControlEntity: RoutingKey.TRIGGERS_CONTROL_ENTITY_CREATED,
        DevicePropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_CREATED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_CREATED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_CREATED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_CREATED,
        TimeConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_CREATED,
        DateConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_CREATED,
        SmsNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_CREATED,
        EmailNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_CREATED,
    }

    UPDATED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGERS_ENTITY_UPDATED,
        AutomaticTriggerEntity: RoutingKey.TRIGGERS_ENTITY_UPDATED,
        TriggerControlEntity: RoutingKey.TRIGGERS_CONTROL_ENTITY_UPDATED,
        DevicePropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_UPDATED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_UPDATED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_UPDATED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_UPDATED,
        TimeConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_UPDATED,
        DateConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_UPDATED,
        SmsNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_UPDATED,
        EmailNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_UPDATED,
    }

    DELETED_ENTITIES_ROUTING_KEYS_MAPPING: Dict[Type[Base], RoutingKey] = {
        ManualTriggerEntity: RoutingKey.TRIGGERS_ENTITY_DELETED,
        AutomaticTriggerEntity: RoutingKey.TRIGGERS_ENTITY_DELETED,
        TriggerControlEntity: RoutingKey.TRIGGERS_CONTROL_ENTITY_DELETED,
        DevicePropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_DELETED,
        ChannelPropertyActionEntity: RoutingKey.TRIGGERS_ACTIONS_ENTITY_DELETED,
        DevicePropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_DELETED,
        ChannelPropertyConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_DELETED,
        TimeConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_DELETED,
        DateConditionEntity: RoutingKey.TRIGGERS_CONDITIONS_ENTITY_DELETED,
        SmsNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_DELETED,
        EmailNotificationEntity: RoutingKey.TRIGGERS_NOTIFICATIONS_ENTITY_DELETED,
    }

    __publisher: Optional[IPublisher]

    __action_state_repository: Optional[IActionStateRepository]
    __condition_state_repository: Optional[IConditionStateRepository]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        publisher: IPublisher = None,  # type: ignore[assignment]
        action_state_repository: IActionStateRepository = None,  # type: ignore[assignment]
        condition_state_repository: IConditionStateRepository = None,  # type: ignore[assignment]
    ) -> None:
        self.__publisher = publisher

        self.__action_state_repository = action_state_repository
        self.__condition_state_repository = condition_state_repository

        event.listen(Base, "after_insert", lambda mapper, connection, target: self.after_insert(target), propagate=True)
        event.listen(Base, "after_update", lambda mapper, connection, target: self.after_update(target), propagate=True)
        event.listen(Base, "after_delete", lambda mapper, connection, target: self.after_delete(target), propagate=True)

    # -----------------------------------------------------------------------------

    def after_insert(self, target: Base) -> None:
        """Event fired after new entity is created"""
        if self.__publisher is None:
            return

        routing_key = self.__get_entity_created_routing_key(entity=type(target))

        if routing_key is not None:
            self.__publisher.publish(
                origin=ModuleOrigin.DEVICES_MODULE,
                routing_key=routing_key,
                data={**target.to_dict(), **self.__get_entity_extended_data(entity=target)},
            )

    # -----------------------------------------------------------------------------

    def after_update(self, target: Base) -> None:
        """Event fired after existing entity is updated"""
        if self.__publisher is None:
            return

        routing_key = self.__get_entity_updated_routing_key(entity=type(target))

        if routing_key is not None:
            self.__publisher.publish(
                origin=ModuleOrigin.DEVICES_MODULE,
                routing_key=routing_key,
                data={**target.to_dict(), **self.__get_entity_extended_data(entity=target)},
            )

    # -----------------------------------------------------------------------------

    def after_delete(self, target: Base) -> None:
        """Event fired after existing entity is deleted"""
        if self.__publisher is None:
            return

        routing_key = self.__get_entity_deleted_routing_key(entity=type(target))

        if routing_key is not None:
            self.__publisher.publish(
                origin=ModuleOrigin.DEVICES_MODULE,
                routing_key=routing_key,
                data={**target.to_dict(), **self.__get_entity_extended_data(entity=target)},
            )

    # -----------------------------------------------------------------------------

    def __get_entity_created_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for created entity"""
        for classname, routing_key in self.CREATED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_updated_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for updated entity"""
        for classname, routing_key in self.UPDATED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_deleted_routing_key(self, entity: Type[Base]) -> Optional[RoutingKey]:
        """Get routing key for deleted entity"""
        for classname, routing_key in self.DELETED_ENTITIES_ROUTING_KEYS_MAPPING.items():
            if issubclass(entity, classname):
                return routing_key

        return None

    # -----------------------------------------------------------------------------

    def __get_entity_extended_data(self, entity: Base) -> Dict:
        if isinstance(entity, ActionEntity) and self.__action_state_repository is not None:
            action_state = self.__action_state_repository.get_by_id(property_id=entity.id)

            if action_state is None:
                return {}

            return {
                "is_triggered": action_state.is_triggered,
            }

        if isinstance(entity, ConditionEntity) and self.__condition_state_repository is not None:
            condition_state = self.__condition_state_repository.get_by_id(property_id=entity.id)

            if condition_state is None:
                return {}

            return {
                "is_fulfilled": condition_state.is_fulfilled,
            }

        if (
            isinstance(entity, TriggerEntity)
            and self.__action_state_repository is not None
            and self.__condition_state_repository is not None
        ):
            is_triggered: bool = True

            for action in entity.actions:
                action_state = self.__action_state_repository.get_by_id(property_id=action.id)

                if action_state is None or action_state.is_triggered is False:
                    is_triggered = False

            if isinstance(entity, AutomaticTriggerEntity):
                is_fulfilled = True

                for condition in entity.conditions:
                    condition_state = self.__condition_state_repository.get_by_id(property_id=condition.id)

                    if condition_state is None or condition_state.is_fulfilled is False:
                        is_fulfilled = False

                return {
                    "is_triggered": is_triggered,
                    "is_fulfilled": is_fulfilled,
                }

            return {
                "is_triggered": is_triggered,
            }

        return {}
