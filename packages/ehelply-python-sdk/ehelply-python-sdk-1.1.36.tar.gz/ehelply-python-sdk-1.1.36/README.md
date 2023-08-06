# ehelply-python-sdk

Note: This SDK is generated, built, and published automatically by eHelply.

- API version: 1.1.36
- Package version: 1.1.36

## Requirements.

Python >= 3.6

## Installation
### Install from PyPi (Recommended)
```sh
pip install ehelply-python-sdk
```

Then import the package:
```python
import ehelply_python_sdk
```

### Install from repository

```sh
pip install git+https://github.com/eHelply/Python-eHelply-SDK.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/eHelply/Python-eHelply-SDK.git`)

Then import the package:
```python
import ehelply_python_sdk
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ehelply_python_sdk
```

## Getting Started and Usage

```python

import time
import ehelply-python-sdk
from pprint import pprint
from ehelply-python-sdk.api import access_api
from ehelply-python-sdk.model.access_group_db import AccessGroupDB
from ehelply-python-sdk.model.access_group_get import AccessGroupGet
from ehelply-python-sdk.model.access_limit_create import AccessLimitCreate
from ehelply-python-sdk.model.access_node_create import AccessNodeCreate
from ehelply-python-sdk.model.access_node_db import AccessNodeDB
from ehelply-python-sdk.model.access_node_get import AccessNodeGet
from ehelply-python-sdk.model.access_role_db import AccessRoleDB
from ehelply-python-sdk.model.access_role_get import AccessRoleGet
from ehelply-python-sdk.model.access_type_db import AccessTypeDB
from ehelply-python-sdk.model.access_type_get import AccessTypeGet
from ehelply-python-sdk.model.body_create_group_access_partitions_partition_identifier_who_groups_post import BodyCreateGroupAccessPartitionsPartitionIdentifierWhoGroupsPost
from ehelply-python-sdk.model.body_create_role_access_partitions_partition_identifier_roles_post import BodyCreateRoleAccessPartitionsPartitionIdentifierRolesPost
from ehelply-python-sdk.model.body_create_type_access_partitions_partition_identifier_permissions_types_post import BodyCreateTypeAccessPartitionsPartitionIdentifierPermissionsTypesPost
from ehelply-python-sdk.model.body_make_rgt_access_partitions_partition_identifier_rgts_roles_role_uuid_groups_group_uuid_targets_target_identifier_post import BodyMakeRgtAccessPartitionsPartitionIdentifierRgtsRolesRoleUuidGroupsGroupUuidTargetsTargetIdentifierPost
from ehelply-python-sdk.model.body_update_group_access_partitions_partition_identifier_who_groups_group_uuid_put import BodyUpdateGroupAccessPartitionsPartitionIdentifierWhoGroupsGroupUuidPut
from ehelply-python-sdk.model.body_update_limits_for_entity_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_entities_entity_identifier_post import BodyUpdateLimitsForEntityOnTargetAccessPartitionsPartitionIdentifierLimitsTargetsTargetIdentifierEntitiesEntityIdentifierPost
from ehelply-python-sdk.model.body_update_limits_for_key_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_keys_post import BodyUpdateLimitsForKeyOnTargetAccessPartitionsPartitionIdentifierLimitsTargetsTargetIdentifierKeysPost
from ehelply-python-sdk.model.body_update_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_put import BodyUpdateNodeAccessPartitionsPartitionIdentifierPermissionsNodesNodeUuidPut
from ehelply-python-sdk.model.body_update_role_access_partitions_partition_identifier_roles_role_uuid_put import BodyUpdateRoleAccessPartitionsPartitionIdentifierRolesRoleUuidPut
from ehelply-python-sdk.model.body_update_type_access_partitions_partition_identifier_permissions_types_type_uuid_put import BodyUpdateTypeAccessPartitionsPartitionIdentifierPermissionsTypesTypeUuidPut
from ehelply-python-sdk.model.http_validation_error import HTTPValidationError
from ehelply-python-sdk.model.page import Page
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ehelply-python-sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with ehelply-python-sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = access_api.AccessApi(api_client)
    partition_identifier = "partition_identifier_example" # str
group_uuid = "group_uuid_example" # str
entity_identifier = "entity_identifier_example" # str
x_access_token = "x-access-token_example" # str (optional)
x_secret_token = "x-secret-token_example" # str (optional)
authorization = "authorization_example" # str (optional)
ehelply_active_participant = "ehelply-active-participant_example" # str (optional)
ehelply_project = "ehelply-project_example" # str (optional)
ehelply_data = "ehelply-data_example" # str (optional)

    try:
        # Add Entity To Group
        api_response = api_instance.add_entity_to_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_post(partition_identifier, group_uuid, entity_identifier, x_access_token=x_access_token, x_secret_token=x_secret_token, authorization=authorization, ehelply_active_participant=ehelply_active_participant, ehelply_project=ehelply_project, ehelply_data=ehelply_data)
        pprint(api_response)
    except ehelply-python-sdk.ApiException as e:
        print("Exception when calling AccessApi->add_entity_to_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_post: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.prod.ehelply.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccessApi* | [**add_entity_to_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_post**](docs/AccessApi.md#add_entity_to_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_post) | **POST** /sam/access/partitions/{partition_identifier}/who/groups/{group_uuid}/entities/{entity_identifier} | Add Entity To Group
*AccessApi* | [**add_node_to_key_access_partitions_partition_identifier_keys_key_uuid_nodes_node_uuid_post**](docs/AccessApi.md#add_node_to_key_access_partitions_partition_identifier_keys_key_uuid_nodes_node_uuid_post) | **POST** /sam/access/partitions/{partition_identifier}/keys/{key_uuid}/nodes/{node_uuid} | Add Node To Key
*AccessApi* | [**add_node_to_role_access_partitions_partition_identifier_roles_role_uuid_nodes_node_uuid_post**](docs/AccessApi.md#add_node_to_role_access_partitions_partition_identifier_roles_role_uuid_nodes_node_uuid_post) | **POST** /sam/access/partitions/{partition_identifier}/roles/{role_uuid}/nodes/{node_uuid} | Add Node To Role
*AccessApi* | [**attach_key_to_entity_access_partitions_partition_identifier_who_entities_entity_identifier_keys_key_uuid_post**](docs/AccessApi.md#attach_key_to_entity_access_partitions_partition_identifier_who_entities_entity_identifier_keys_key_uuid_post) | **POST** /sam/access/partitions/{partition_identifier}/who/entities/{entity_identifier}/keys/{key_uuid} | Attach Key To Entity
*AccessApi* | [**create_group_access_partitions_partition_identifier_who_groups_post**](docs/AccessApi.md#create_group_access_partitions_partition_identifier_who_groups_post) | **POST** /sam/access/partitions/{partition_identifier}/who/groups | Create Group
*AccessApi* | [**create_node**](docs/AccessApi.md#create_node) | **POST** /sam/access/partitions/{partition_identifier}/permissions/types/{type_uuid}/nodes | Createnode
*AccessApi* | [**create_role_access_partitions_partition_identifier_roles_post**](docs/AccessApi.md#create_role_access_partitions_partition_identifier_roles_post) | **POST** /sam/access/partitions/{partition_identifier}/roles | Create Role
*AccessApi* | [**create_type_access_partitions_partition_identifier_permissions_types_post**](docs/AccessApi.md#create_type_access_partitions_partition_identifier_permissions_types_post) | **POST** /sam/access/partitions/{partition_identifier}/permissions/types | Create Type
*AccessApi* | [**delete_group_access_partitions_partition_identifier_who_groups_group_uuid_delete**](docs/AccessApi.md#delete_group_access_partitions_partition_identifier_who_groups_group_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/who/groups/{group_uuid} | Delete Group
*AccessApi* | [**delete_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_delete**](docs/AccessApi.md#delete_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/permissions/nodes/{node_uuid} | Delete Node
*AccessApi* | [**delete_role_access_partitions_partition_identifier_roles_role_uuid_delete**](docs/AccessApi.md#delete_role_access_partitions_partition_identifier_roles_role_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/roles/{role_uuid} | Delete Role
*AccessApi* | [**delete_type_access_partitions_partition_identifier_permissions_types_type_uuid_delete**](docs/AccessApi.md#delete_type_access_partitions_partition_identifier_permissions_types_type_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/permissions/types/{type_uuid} | Delete Type
*AccessApi* | [**destroy_rgt_access_partitions_partition_identifier_rgts_roles_role_uuid_groups_group_uuid_targets_target_identifier_delete**](docs/AccessApi.md#destroy_rgt_access_partitions_partition_identifier_rgts_roles_role_uuid_groups_group_uuid_targets_target_identifier_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/rgts/roles/{role_uuid}/groups/{group_uuid}/targets/{target_identifier} | Destroy Rgt
*AccessApi* | [**dettach_key_from_entity_access_partitions_partition_identifier_who_entities_entity_identifier_keys_key_uuid_delete**](docs/AccessApi.md#dettach_key_from_entity_access_partitions_partition_identifier_who_entities_entity_identifier_keys_key_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/who/entities/{entity_identifier}/keys/{key_uuid} | Dettach Key From Entity
*AccessApi* | [**get_entity_access_partitions_partition_identifier_who_entities_entity_identifier_get**](docs/AccessApi.md#get_entity_access_partitions_partition_identifier_who_entities_entity_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/who/entities/{entity_identifier} | Get Entity
*AccessApi* | [**get_entity_for_key_access_partitions_partition_identifier_who_entities_keys_key_uuid_get**](docs/AccessApi.md#get_entity_for_key_access_partitions_partition_identifier_who_entities_keys_key_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/who/entities/keys/{key_uuid} | Get Entity For Key
*AccessApi* | [**get_entity_keys_access_partitions_partition_identifier_who_entities_entity_identifier_keys_get**](docs/AccessApi.md#get_entity_keys_access_partitions_partition_identifier_who_entities_entity_identifier_keys_get) | **GET** /sam/access/partitions/{partition_identifier}/who/entities/{entity_identifier}/keys | Get Entity Keys
*AccessApi* | [**get_group_access_partitions_partition_identifier_who_groups_group_uuid_get**](docs/AccessApi.md#get_group_access_partitions_partition_identifier_who_groups_group_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/who/groups/{group_uuid} | Get Group
*AccessApi* | [**get_groups_for_entity_access_partitions_partition_identifier_who_groups_entities_entity_identifier_get**](docs/AccessApi.md#get_groups_for_entity_access_partitions_partition_identifier_who_groups_entities_entity_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/who/groups/entities/{entity_identifier} | Get Groups For Entity
*AccessApi* | [**get_limits_for_entity_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_entities_entity_identifier_get**](docs/AccessApi.md#get_limits_for_entity_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_entities_entity_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/limits/targets/{target_identifier}/entities/{entity_identifier} | Get Limits For Entity On Target
*AccessApi* | [**get_limits_for_key_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_keys_get**](docs/AccessApi.md#get_limits_for_key_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_keys_get) | **GET** /sam/access/partitions/{partition_identifier}/limits/targets/{target_identifier}/keys | Get Limits For Key On Target
*AccessApi* | [**get_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_get**](docs/AccessApi.md#get_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/nodes/{node_uuid} | Get Node
*AccessApi* | [**get_nodes_for_entity_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_get**](docs/AccessApi.md#get_nodes_for_entity_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/nodes/entities/{entity_identifier} | Get Nodes For Entity
*AccessApi* | [**get_nodes_for_entity_key_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_keys_key_uuid_get**](docs/AccessApi.md#get_nodes_for_entity_key_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_keys_key_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/nodes/entities/{entity_identifier}/keys/{key_uuid} | Get Nodes For Entity Key
*AccessApi* | [**get_nodes_for_entity_target_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_targets_target_identifier_get**](docs/AccessApi.md#get_nodes_for_entity_target_access_partitions_partition_identifier_permissions_nodes_entities_entity_identifier_targets_target_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/nodes/entities/{entity_identifier}/targets/{target_identifier} | Get Nodes For Entity Target
*AccessApi* | [**get_rgt_access_partitions_partition_identifier_rgts_rgt_uuid_get**](docs/AccessApi.md#get_rgt_access_partitions_partition_identifier_rgts_rgt_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/rgts/{rgt_uuid} | Get Rgt
*AccessApi* | [**get_role_access_partitions_partition_identifier_roles_role_uuid_get**](docs/AccessApi.md#get_role_access_partitions_partition_identifier_roles_role_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/roles/{role_uuid} | Get Role
*AccessApi* | [**get_type_access_partitions_partition_identifier_permissions_types_type_uuid_get**](docs/AccessApi.md#get_type_access_partitions_partition_identifier_permissions_types_type_uuid_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/types/{type_uuid} | Get Type
*AccessApi* | [**is_allowed_for_entity_on_target_with_node_access_partitions_partition_identifier_auth_targets_target_identifier_nodes_node_entities_entity_identifier_get**](docs/AccessApi.md#is_allowed_for_entity_on_target_with_node_access_partitions_partition_identifier_auth_targets_target_identifier_nodes_node_entities_entity_identifier_get) | **GET** /sam/access/partitions/{partition_identifier}/auth/targets/{target_identifier}/nodes/{node}/entities/{entity_identifier} | Is Allowed For Entity On Target With Node
*AccessApi* | [**make_rgt_access_partitions_partition_identifier_rgts_roles_role_uuid_groups_group_uuid_targets_target_identifier_post**](docs/AccessApi.md#make_rgt_access_partitions_partition_identifier_rgts_roles_role_uuid_groups_group_uuid_targets_target_identifier_post) | **POST** /sam/access/partitions/{partition_identifier}/rgts/roles/{role_uuid}/groups/{group_uuid}/targets/{target_identifier} | Make Rgt
*AccessApi* | [**remove_entity_from_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_delete**](docs/AccessApi.md#remove_entity_from_group_access_partitions_partition_identifier_who_groups_group_uuid_entities_entity_identifier_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/who/groups/{group_uuid}/entities/{entity_identifier} | Remove Entity From Group
*AccessApi* | [**remove_node_from_key_access_partitions_partition_identifier_keys_key_uuid_nodes_node_uuid_delete**](docs/AccessApi.md#remove_node_from_key_access_partitions_partition_identifier_keys_key_uuid_nodes_node_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/keys/{key_uuid}/nodes/{node_uuid} | Remove Node From Key
*AccessApi* | [**remove_node_from_role_access_partitions_partition_identifier_roles_role_uuid_nodes_node_uuid_delete**](docs/AccessApi.md#remove_node_from_role_access_partitions_partition_identifier_roles_role_uuid_nodes_node_uuid_delete) | **DELETE** /sam/access/partitions/{partition_identifier}/roles/{role_uuid}/nodes/{node_uuid} | Remove Node From Role
*AccessApi* | [**search_groups_access_partitions_partition_identifier_who_groups_get**](docs/AccessApi.md#search_groups_access_partitions_partition_identifier_who_groups_get) | **GET** /sam/access/partitions/{partition_identifier}/who/groups | Search Groups
*AccessApi* | [**search_nodes_access_partitions_partition_identifier_permissions_types_type_uuid_nodes_get**](docs/AccessApi.md#search_nodes_access_partitions_partition_identifier_permissions_types_type_uuid_nodes_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/types/{type_uuid}/nodes | Search Nodes
*AccessApi* | [**search_roles_access_partitions_partition_identifier_roles_get**](docs/AccessApi.md#search_roles_access_partitions_partition_identifier_roles_get) | **GET** /sam/access/partitions/{partition_identifier}/roles | Search Roles
*AccessApi* | [**search_types_access_partitions_partition_identifier_permissions_types_get**](docs/AccessApi.md#search_types_access_partitions_partition_identifier_permissions_types_get) | **GET** /sam/access/partitions/{partition_identifier}/permissions/types | Search Types
*AccessApi* | [**update_group_access_partitions_partition_identifier_who_groups_group_uuid_put**](docs/AccessApi.md#update_group_access_partitions_partition_identifier_who_groups_group_uuid_put) | **PUT** /sam/access/partitions/{partition_identifier}/who/groups/{group_uuid} | Update Group
*AccessApi* | [**update_limits_for_entity_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_entities_entity_identifier_post**](docs/AccessApi.md#update_limits_for_entity_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_entities_entity_identifier_post) | **POST** /sam/access/partitions/{partition_identifier}/limits/targets/{target_identifier}/entities/{entity_identifier} | Update Limits For Entity On Target
*AccessApi* | [**update_limits_for_key_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_keys_post**](docs/AccessApi.md#update_limits_for_key_on_target_access_partitions_partition_identifier_limits_targets_target_identifier_keys_post) | **POST** /sam/access/partitions/{partition_identifier}/limits/targets/{target_identifier}/keys | Update Limits For Key On Target
*AccessApi* | [**update_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_put**](docs/AccessApi.md#update_node_access_partitions_partition_identifier_permissions_nodes_node_uuid_put) | **PUT** /sam/access/partitions/{partition_identifier}/permissions/nodes/{node_uuid} | Update Node
*AccessApi* | [**update_role_access_partitions_partition_identifier_roles_role_uuid_put**](docs/AccessApi.md#update_role_access_partitions_partition_identifier_roles_role_uuid_put) | **PUT** /sam/access/partitions/{partition_identifier}/roles/{role_uuid} | Update Role
*AccessApi* | [**update_type_access_partitions_partition_identifier_permissions_types_type_uuid_put**](docs/AccessApi.md#update_type_access_partitions_partition_identifier_permissions_types_type_uuid_put) | **PUT** /sam/access/partitions/{partition_identifier}/permissions/types/{type_uuid} | Update Type
*DefaultApi* | [**playground_notes_playground_get**](docs/DefaultApi.md#playground_notes_playground_get) | **GET** /notes/notes/playground | Playground
*LoggingApi* | [**get_logs_logging_logs_get**](docs/LoggingApi.md#get_logs_logging_logs_get) | **GET** /sam/logging/logs | Get Logs
*LoggingApi* | [**get_service_logs_logging_logs_services_service_get**](docs/LoggingApi.md#get_service_logs_logging_logs_services_service_get) | **GET** /sam/logging/logs/services/{service} | Get Service Logs
*LoggingApi* | [**get_subject_logs_logging_logs_services_service_subjects_subject_get**](docs/LoggingApi.md#get_subject_logs_logging_logs_services_service_subjects_subject_get) | **GET** /sam/logging/logs/services/{service}/subjects/{subject} | Get Subject Logs
*MetaApi* | [**delete_meta_from_uuid_meta_meta_meta_uuid_delete**](docs/MetaApi.md#delete_meta_from_uuid_meta_meta_meta_uuid_delete) | **DELETE** /meta/meta/meta/{meta_uuid} | Delete Meta From Uuid
*MetaApi* | [**delete_meta_meta_meta_service_service_type_type_entity_entity_uuid_delete**](docs/MetaApi.md#delete_meta_meta_meta_service_service_type_type_entity_entity_uuid_delete) | **DELETE** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Delete Meta
*MetaApi* | [**get_meta_from_uuid_meta_meta_meta_uuid_get**](docs/MetaApi.md#get_meta_from_uuid_meta_meta_meta_uuid_get) | **GET** /meta/meta/meta/{meta_uuid} | Get Meta From Uuid
*MetaApi* | [**get_meta_meta_meta_service_service_type_type_entity_entity_uuid_get**](docs/MetaApi.md#get_meta_meta_meta_service_service_type_type_entity_entity_uuid_get) | **GET** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Get Meta
*MetaApi* | [**make_slug_meta_meta_slug_post**](docs/MetaApi.md#make_slug_meta_meta_slug_post) | **POST** /meta/meta/meta/slug | Make Slug
*MetaApi* | [**post_meta_meta_meta_service_service_type_type_str_entity_entity_uuid_post**](docs/MetaApi.md#post_meta_meta_meta_service_service_type_type_str_entity_entity_uuid_post) | **POST** /meta/meta/meta/service/{service}/type/{type_str}/entity/{entity_uuid} | Post Meta
*MetaApi* | [**touch_meta_meta_meta_service_service_type_type_entity_entity_uuid_touch_post**](docs/MetaApi.md#touch_meta_meta_meta_service_service_type_type_entity_entity_uuid_touch_post) | **POST** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid}/touch | Touch Meta
*MetaApi* | [**update_meta_from_uuid_meta_meta_meta_uuid_put**](docs/MetaApi.md#update_meta_from_uuid_meta_meta_meta_uuid_put) | **PUT** /meta/meta/meta/{meta_uuid} | Update Meta From Uuid
*MetaApi* | [**update_meta_meta_meta_service_service_type_type_entity_entity_uuid_put**](docs/MetaApi.md#update_meta_meta_meta_service_service_type_type_entity_entity_uuid_put) | **PUT** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Update Meta
*MonitorApi* | [**ack_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_acknowledge_post**](docs/MonitorApi.md#ack_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_acknowledge_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/acknowledge | Ack Alarm
*MonitorApi* | [**assign_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_assign_post**](docs/MonitorApi.md#assign_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_assign_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/assign | Assign Alarm
*MonitorApi* | [**attach_alarm_note_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_note_post**](docs/MonitorApi.md#attach_alarm_note_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_note_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/note | Attach Alarm Note
*MonitorApi* | [**attach_alarm_ticket_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_ticket_post**](docs/MonitorApi.md#attach_alarm_ticket_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_ticket_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/ticket | Attach Alarm Ticket
*MonitorApi* | [**clear_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_clear_post**](docs/MonitorApi.md#clear_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_clear_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/clear | Clear Alarm
*MonitorApi* | [**get_service_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_get**](docs/MonitorApi.md#get_service_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_get) | **GET** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid} | Get Service Alarm
*MonitorApi* | [**get_service_alarms_monitor_services_service_uuid_stages_stage_alarms_get**](docs/MonitorApi.md#get_service_alarms_monitor_services_service_uuid_stages_stage_alarms_get) | **GET** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms | Get Service Alarms
*MonitorApi* | [**get_service_heartbeats_monitor_services_service_uuid_stages_stage_heartbeats_get**](docs/MonitorApi.md#get_service_heartbeats_monitor_services_service_uuid_stages_stage_heartbeats_get) | **GET** /sam/monitor/services/{service_uuid}/stages/{stage}/heartbeats | Get Service Heartbeats
*MonitorApi* | [**get_service_kpis_monitor_services_service_uuid_kpis_get**](docs/MonitorApi.md#get_service_kpis_monitor_services_service_uuid_kpis_get) | **GET** /sam/monitor/services/{service_uuid}/kpis | Get Service Kpis
*MonitorApi* | [**get_service_monitor_services_service_uuid_get**](docs/MonitorApi.md#get_service_monitor_services_service_uuid_get) | **GET** /sam/monitor/services/{service_uuid} | Get Service
*MonitorApi* | [**get_service_vitals_monitor_services_service_uuid_stages_stage_vitals_get**](docs/MonitorApi.md#get_service_vitals_monitor_services_service_uuid_stages_stage_vitals_get) | **GET** /sam/monitor/services/{service_uuid}/stages/{stage}/vitals | Get Service Vitals
*MonitorApi* | [**get_services_monitor_services_get**](docs/MonitorApi.md#get_services_monitor_services_get) | **GET** /sam/monitor/services | Get Services
*MonitorApi* | [**hide_service_monitor_services_service_uuid_stages_stage_hide_post**](docs/MonitorApi.md#hide_service_monitor_services_service_uuid_stages_stage_hide_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/hide | Hide Service
*MonitorApi* | [**ignore_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_ignore_post**](docs/MonitorApi.md#ignore_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_ignore_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/ignore | Ignore Alarm
*MonitorApi* | [**register_service_monitor_services_post**](docs/MonitorApi.md#register_service_monitor_services_post) | **POST** /sam/monitor/services | Register Service
*MonitorApi* | [**search_alarms_monitor_services_service_uuid_alarms_get**](docs/MonitorApi.md#search_alarms_monitor_services_service_uuid_alarms_get) | **GET** /sam/monitor/services/{service_uuid}/alarms | Search Alarms
*MonitorApi* | [**show_service_monitor_services_service_uuid_stages_stage_show_post**](docs/MonitorApi.md#show_service_monitor_services_service_uuid_stages_stage_show_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/show | Show Service
*MonitorApi* | [**terminate_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_terminate_post**](docs/MonitorApi.md#terminate_alarm_monitor_services_service_uuid_stages_stage_alarms_alarm_uuid_terminate_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms/{alarm_uuid}/terminate | Terminate Alarm
*MonitorApi* | [**trigger_alarm_monitor_services_service_uuid_stages_stage_alarms_post**](docs/MonitorApi.md#trigger_alarm_monitor_services_service_uuid_stages_stage_alarms_post) | **POST** /sam/monitor/services/{service_uuid}/stages/{stage}/alarms | Trigger Alarm
*NotesApi* | [**create_note_notes_notes_post**](docs/NotesApi.md#create_note_notes_notes_post) | **POST** /notes/notes/notes | Create Note
*NotesApi* | [**delete_note_notes_notes_note_id_delete**](docs/NotesApi.md#delete_note_notes_notes_note_id_delete) | **DELETE** /notes/notes/notes/{note_id} | Delete Note
*NotesApi* | [**get_note_notes_notes_note_id_get**](docs/NotesApi.md#get_note_notes_notes_note_id_get) | **GET** /notes/notes/notes/{note_id} | Get Note
*NotesApi* | [**update_note_notes_notes_note_id_put**](docs/NotesApi.md#update_note_notes_notes_note_id_put) | **PUT** /notes/notes/notes/{note_id} | Update Note
*ProjectsApi* | [**add_member_to_project_projects_projects_project_uuid_members_entity_uuid_post**](docs/ProjectsApi.md#add_member_to_project_projects_projects_project_uuid_members_entity_uuid_post) | **POST** /sam/projects/projects/{project_uuid}/members/{entity_uuid} | Add Member To Project
*ProjectsApi* | [**add_permission_to_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_node_uuid_post**](docs/ProjectsApi.md#add_permission_to_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_node_uuid_post) | **POST** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys/{key_uuid}/permissions/{node_uuid} | Add Permission To Key
*ProjectsApi* | [**archive_project_projects_projects_project_uuid_delete**](docs/ProjectsApi.md#archive_project_projects_projects_project_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid} | Archive Project
*ProjectsApi* | [**cloud_participant_projects_cloud_participant_post**](docs/ProjectsApi.md#cloud_participant_projects_cloud_participant_post) | **POST** /sam/projects/cloud_participant | Cloud Participant
*ProjectsApi* | [**create_project_key_projects_projects_project_uuid_members_entity_uuid_keys_post**](docs/ProjectsApi.md#create_project_key_projects_projects_project_uuid_members_entity_uuid_keys_post) | **POST** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys | Create Project Key
*ProjectsApi* | [**create_project_projects_projects_post**](docs/ProjectsApi.md#create_project_projects_projects_post) | **POST** /sam/projects/projects | Create Project
*ProjectsApi* | [**create_usage_type_projects_usage_types_post**](docs/ProjectsApi.md#create_usage_type_projects_usage_types_post) | **POST** /sam/projects/usage/types | Create Usage Type
*ProjectsApi* | [**delete_usage_type_projects_usage_types_usage_type_key_delete**](docs/ProjectsApi.md#delete_usage_type_projects_usage_types_usage_type_key_delete) | **DELETE** /sam/projects/usage/types/{usage_type_key} | Delete Usage Type
*ProjectsApi* | [**get_all_project_usage_projects_projects_project_uuid_usage_get**](docs/ProjectsApi.md#get_all_project_usage_projects_projects_project_uuid_usage_get) | **GET** /sam/projects/projects/{project_uuid}/usage | Get All Project Usage
*ProjectsApi* | [**get_member_projects_projects_members_entity_uuid_projects_get**](docs/ProjectsApi.md#get_member_projects_projects_members_entity_uuid_projects_get) | **GET** /sam/projects/members/{entity_uuid}/projects | Get Member Projects
*ProjectsApi* | [**get_permissions_for_entity_projects_projects_project_uuid_members_entity_uuid_permissions_get**](docs/ProjectsApi.md#get_permissions_for_entity_projects_projects_project_uuid_members_entity_uuid_permissions_get) | **GET** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/permissions | Get Permissions For Entity
*ProjectsApi* | [**get_permissions_for_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_get**](docs/ProjectsApi.md#get_permissions_for_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_get) | **GET** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys/{key_uuid}/permissions | Get Permissions For Key
*ProjectsApi* | [**get_permissions_type_projects_projects_project_uuid_members_entity_uuid_permissions_types_type_uuid_get**](docs/ProjectsApi.md#get_permissions_type_projects_projects_project_uuid_members_entity_uuid_permissions_types_type_uuid_get) | **GET** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/permissions/types/{type_uuid} | Get Permissions Type
*ProjectsApi* | [**get_project_keys_projects_projects_project_uuid_members_entity_uuid_keys_get**](docs/ProjectsApi.md#get_project_keys_projects_projects_project_uuid_members_entity_uuid_keys_get) | **GET** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys | Get Project Keys
*ProjectsApi* | [**get_project_members_projects_projects_project_uuid_members_get**](docs/ProjectsApi.md#get_project_members_projects_projects_project_uuid_members_get) | **GET** /sam/projects/projects/{project_uuid}/members | Get Project Members
*ProjectsApi* | [**get_project_projects_projects_project_uuid_get**](docs/ProjectsApi.md#get_project_projects_projects_project_uuid_get) | **GET** /sam/projects/projects/{project_uuid} | Get Project
*ProjectsApi* | [**get_specific_project_usage_projects_projects_project_uuid_usage_usage_type_key_get**](docs/ProjectsApi.md#get_specific_project_usage_projects_projects_project_uuid_usage_usage_type_key_get) | **GET** /sam/projects/projects/{project_uuid}/usage/{usage_type_key} | Get Specific Project Usage
*ProjectsApi* | [**get_usage_type_projects_usage_types_usage_type_key_get**](docs/ProjectsApi.md#get_usage_type_projects_usage_types_usage_type_key_get) | **GET** /sam/projects/usage/types/{usage_type_key} | Get Usage Type
*ProjectsApi* | [**remove_member_from_project_projects_projects_project_uuid_members_entity_uuid_delete**](docs/ProjectsApi.md#remove_member_from_project_projects_projects_project_uuid_members_entity_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid}/members/{entity_uuid} | Remove Member From Project
*ProjectsApi* | [**remove_permission_from_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_node_uuid_delete**](docs/ProjectsApi.md#remove_permission_from_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_permissions_node_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys/{key_uuid}/permissions/{node_uuid} | Remove Permission From Key
*ProjectsApi* | [**remove_project_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_delete**](docs/ProjectsApi.md#remove_project_key_projects_projects_project_uuid_members_entity_uuid_keys_key_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid}/members/{entity_uuid}/keys/{key_uuid} | Remove Project Key
*ProjectsApi* | [**search_projects_projects_projects_get**](docs/ProjectsApi.md#search_projects_projects_projects_get) | **GET** /sam/projects/projects | Search Projects
*ProjectsApi* | [**search_usage_type_projects_usage_types_get**](docs/ProjectsApi.md#search_usage_type_projects_usage_types_get) | **GET** /sam/projects/usage/types | Search Usage Type
*ProjectsApi* | [**update_project_projects_projects_project_uuid_put**](docs/ProjectsApi.md#update_project_projects_projects_project_uuid_put) | **PUT** /sam/projects/projects/{project_uuid} | Update Project
*ProjectsApi* | [**update_usage_type_projects_usage_types_usage_type_key_put**](docs/ProjectsApi.md#update_usage_type_projects_usage_types_usage_type_key_put) | **PUT** /sam/projects/usage/types/{usage_type_key} | Update Usage Type
*SecurityApi* | [**create_encryption_key_security_encryption_categories_category_keys_post**](docs/SecurityApi.md#create_encryption_key_security_encryption_categories_category_keys_post) | **POST** /sam/security/encryption/categories/{category}/keys | Create Encryption Key
*SecurityApi* | [**create_key_security_keys_post**](docs/SecurityApi.md#create_key_security_keys_post) | **POST** /sam/security/keys | Create Key
*SecurityApi* | [**delete_key_security_keys_key_uuid_delete**](docs/SecurityApi.md#delete_key_security_keys_key_uuid_delete) | **DELETE** /sam/security/keys/{key_uuid} | Delete Key
*SecurityApi* | [**generate_token_security_tokens_post**](docs/SecurityApi.md#generate_token_security_tokens_post) | **POST** /sam/security/tokens | Generate Token
*SecurityApi* | [**get_encryption_key_security_encryption_categories_category_keys_get**](docs/SecurityApi.md#get_encryption_key_security_encryption_categories_category_keys_get) | **GET** /sam/security/encryption/categories/{category}/keys | Get Encryption Key
*SecurityApi* | [**get_key_security_keys_key_uuid_get**](docs/SecurityApi.md#get_key_security_keys_key_uuid_get) | **GET** /sam/security/keys/{key_uuid} | Get Key
*SecurityApi* | [**search_keys_security_keys_get**](docs/SecurityApi.md#search_keys_security_keys_get) | **GET** /sam/security/keys | Search Keys
*SecurityApi* | [**verify_key_security_keys_verify_post**](docs/SecurityApi.md#verify_key_security_keys_verify_post) | **POST** /sam/security/keys/verify | Verify Key
*SupportApi* | [**create_contact_support_contact_post**](docs/SupportApi.md#create_contact_support_contact_post) | **POST** /sam/support/contact | Create Contact
*SupportApi* | [**create_ticket_support_projects_project_uuid_members_member_uuid_tickets_post**](docs/SupportApi.md#create_ticket_support_projects_project_uuid_members_member_uuid_tickets_post) | **POST** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets | Create Ticket
*SupportApi* | [**delete_contact_support_contact_delete**](docs/SupportApi.md#delete_contact_support_contact_delete) | **DELETE** /sam/support/contact | Delete Contact
*SupportApi* | [**list_tickets_support_projects_project_uuid_members_member_uuid_tickets_get**](docs/SupportApi.md#list_tickets_support_projects_project_uuid_members_member_uuid_tickets_get) | **GET** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets | List Tickets
*SupportApi* | [**update_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_put**](docs/SupportApi.md#update_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_put) | **PUT** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets/{ticket_id} | Update Ticket
*SupportApi* | [**view_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_get**](docs/SupportApi.md#view_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_get) | **GET** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets/{ticket_id} | View Ticket


## RecursionError
When APIs/SDKs are large, imports in ehelply-python-sdk.apis and ehelply-python-sdk.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from ehelply_python_sdk.api.default_api import DefaultApi`
- `from ehelply_python_sdk.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:

```python
import sys
sys.setrecursionlimit(1500)

import ehelply_python_sdk
from ehelply_python_sdk.apis import *
from ehelply_python_sdk.models import *
```

