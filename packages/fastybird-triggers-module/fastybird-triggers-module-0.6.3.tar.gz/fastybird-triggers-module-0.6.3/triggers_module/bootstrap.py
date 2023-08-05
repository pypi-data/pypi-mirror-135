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
Triggers module DI container
"""

# pylint: disable=no-value-for-parameter

# Library dependencies
from kink import di
from sqlalchemy.orm import Session as OrmSession

# Library libs
from triggers_module.managers.action import ActionsManager
from triggers_module.managers.condition import ConditionsManager
from triggers_module.managers.notification import NotificationsManager
from triggers_module.managers.trigger import TriggerControlsManager, TriggersManager
from triggers_module.repositories.action import ActionsRepository
from triggers_module.repositories.condition import ConditionsRepository
from triggers_module.repositories.notification import NotificationsRepository
from triggers_module.repositories.trigger import (
    TriggersControlsRepository,
    TriggersRepository,
)
from triggers_module.subscriber import EntitiesSubscriber, EntityCreatedSubscriber


def create_container(database_session: OrmSession) -> None:
    """Register triggers module services"""
    di[TriggersRepository] = TriggersRepository(session=database_session)
    di["fb-triggers-module_trigger-repository"] = di[TriggersRepository]
    di[TriggersControlsRepository] = TriggersControlsRepository(session=database_session)
    di["fb-triggers-module_trigger-control-repository"] = di[TriggersControlsRepository]
    di[ActionsRepository] = ActionsRepository(session=database_session)
    di["fb-triggers-module_action-repository"] = di[ActionsRepository]
    di[ConditionsRepository] = ConditionsRepository(session=database_session)
    di["fb-triggers-module_condition-repository"] = di[ConditionsRepository]
    di[NotificationsRepository] = NotificationsRepository(session=database_session)
    di["fb-triggers-module_notification-repository"] = di[NotificationsRepository]

    di[TriggersManager] = TriggersManager(session=database_session)
    di["fb-triggers-module_triggers-manager"] = di[TriggersManager]
    di[TriggerControlsManager] = TriggerControlsManager(session=database_session)
    di["fb-triggers-module_trigger-controls-manager"] = di[TriggerControlsManager]
    di[ActionsManager] = ActionsManager(session=database_session)
    di["fb-triggers-module_actions-manager"] = di[ActionsManager]
    di[ConditionsManager] = ConditionsManager(session=database_session)
    di["fb-triggers-module_actions-manager"] = di[ConditionsManager]
    di[NotificationsManager] = NotificationsManager(session=database_session)
    di["fb-triggers-module_actions-manager"] = di[NotificationsManager]

    di[EntitiesSubscriber] = EntitiesSubscriber()
    di["fb-devices-module_entities-subscriber"] = di[EntitiesSubscriber]
    di[EntityCreatedSubscriber] = EntityCreatedSubscriber()
    di["fb-devices-module_entity-created-subscriber"] = di[EntityCreatedSubscriber]
