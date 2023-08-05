# Python client SDK for Tutti.ai

## Installation

```
pip install tutti-client
```

## Importing Module

```python
from tutti_client import TuttiDuct
duct = TuttiDuct()
```

## Usage

For example, to obtain a list of your Tutti projects:

```python
import asyncio
from tutti_client import TuttiDuct

import logging
logger = logging.getLogger(__name__)

class MyPlayground:
    def __init__(self):
        self.tutti = TuttiDuct()

    async def catchall_event_handler(self, rid, eid, data):
        print(eid, data)

    async def on_open(self):
        await self.tutti.controllers["resource"].list_projects()

    async def main(self):
        self.tutti.add_onopen_handler(self.on_open)
        self.tutti.event_listeners["resource"].on("list_projects", self.on_list_projects)

        await self.tutti.open("http://localhost/ducts/wsd")

    async def on_list_projects(self, data, is_error):
        if is_error:
            # handle error here

            '''
            data = {
                Status: "Error",
                Reason: str,
                Timestamp: {
                  "Requested": int,
                  "Responded": int
                }
            }
            '''
        else:
            print(data)
            # do anything here

            '''
            data = {
              Contents: {
                 ...
              },
              Timestamp: {
                "Requested": int,
                "Responded": int
              }
            }
            '''


if __name__=="__main__":
    pg = MyPlayground()
    asyncio.run(pg.main())
```

## Handling Events with Event Listeners

`tutti.event_listeners["{source}"].on("{method}", handler_func)`

## Executing Methods with Controllers

`tutti.controllers["{source}"].{method}([ ... args])`

## Sources

- `resource` ... Tutti-relevant resources (projects, templates, nanotasks, answers, ...)
- `mturk` ... Amazon Mechanical Turk-relevant operations (wrapper methods for [Python Boto3 MTurk API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html))

## Methods

### Resource

#### get_event_history
- Parameters: None
- Gets all input parameter histories set by setEventHistory.

#### set_event_history
- Parameters: `eid`, `query`
- Sets input parameters to a history.

#### list_projects
- Parameters: None
- Lists Tutti projects.

#### create_project
- Parameters: `ProjectName`
- Creates a Tutti project.

#### list_templates
- Parameters: `ProjectName`
- Lists Tutti templates for the specified project.

#### get_responses_for_template
- Parameters: `ProjectName`, `TemplateName`
- Lists all worker responses for the specified template.

#### get_responses_for_nanotask
- Parameters: `NanotaskId`

#### create_templates
- Parameters: `ProjectName`, `TemplateNames`, `PresetEnvName`, `PresetTemplateName`

#### list_template_presets
- Parameters: None

#### get_project_scheme
- Parameters: `ProjectName`, `Cached`

#### get_nanotasks
- Parameters: `ProjectName`, `TemplateName`

#### delete_nanotasks
- Parameters: `ProjectName`, `TemplateName`, `NanotaskIds`

#### update_nanotask_num_assignable
- Parameters: `ProjectName`, `TemplateName`, `NanotaskId`, `NumAssignable`

#### upload_nanotasks
- Parameters: `ProjectName`, `TemplateName`, `Nanotasks`, `NumAssignable`, `Priority`, `TagName`

#### get_template_node
- Parameters: `Target`, `WorkSessionId`, `NodeSessionId`

#### create_session
- Parameters: `ProjectName`, `PlatformWorkerId`, `ClientToken`, `Platform`

#### set_response
- Parameters: `WorkSessionId`, `NodeSessionId`, `Answers`

#### check_platform_worker_id_existence_for_project
- Parameters: `ProjectName`, `Platform`, `PlatformWorkerId`


  
### MTurk

#### get_credentials
- Parameters: None

#### set_credentials
- Parameters: `AccessKeyId`, `SecretAccessKey`

#### set_sandbox
- Parameters: `Enabled`

#### clear_credentials
- Parameters: None

#### delete_qualifications
- Parameters: `QualificationTypeIds`

#### list_qualifications
- Parameters: None

#### list_workers_with_qualification_type
- Parameters: `QualificationTypeId`

#### create_qualification
- Parameters: `QualificationTypeParams`

#### associate_qualifications_with_workers
- Parameters: `AssociateQualificationParams`

#### list_workers
- Parameters: None

#### notify_workers
- Parameters: `Subject`, `MessageText`, `SendEmailWorkerIds`

#### create_hit_type
- Parameters: `CreateHITTypeParams`, `HITTypeQualificationTypeId`

#### create_hits_with_hit_type
- Parameters: `ProjectName`, `NumHITs`, `CreateHITsWithHITTypeParams`

#### get_hit_types
- Parameters: `HITTypeIds`

#### expire_hits
- Parameters: `HITIds`

#### delete_hits
- Parameters: `HITIds`

#### list_hits
- Parameters: `Cached`

#### list_hits_for_hit_type
- Parameters: `HITTypeId=null`, `Cached=true`

#### list_assignments
- Parameters: `Cached`

#### list_assignments_for_hits
- Parameters: `HITIds`

#### approve_assignments
- Parameters: `AssignmentIds`, `RequesterFeedback`

#### reject_assignments
- Parameters: `AssignmentIds`, `RequesterFeedback`

#### get_assignments
- Parameters: `AssignmentIds`
