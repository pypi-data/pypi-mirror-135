import functools

from ducts_client import Duct
from .controllers import ResourceController, MTurkController
from .event_listeners import ResourceEventListener, MTurkEventListener

class TuttiDuct(Duct):
    def __init__(self):
        super().__init__()
        self.onopen_handlers = [];
        self.controllers = {
            "resource": ResourceController(self),
            "mturk": MTurkController(self)
        }
        self.event_listeners = {
            "resource": ResourceEventListener(),
            "mturk": MTurkEventListener()
        }

    def add_onopen_handler(self, handler_coro):
        self.onopen_handlers.append(handler_coro)

    async def _onopen(self, event):
        await super()._onopen(event)

        self.setup_handlers()
        for handler in self.onopen_handlers:
            await handler()

    def setup_handlers(self):
        self.set_event_handler( self.EVENT["EVENT_HISTORY"], self.handle_for_event_history )

        self.set_event_handler( self.EVENT["LIST_PROJECTS"],
                                    functools.partial(self.handle_for, "resource", "list_projects") )
        self.set_event_handler( self.EVENT["CREATE_PROJECT"],
                                    functools.partial(self.handle_for, "resource", "create_project") )
        self.set_event_handler( self.EVENT["GET_PROJECT_SCHEME"],
                                    functools.partial(self.handle_for, "resource", "get_project_scheme") )
        self.set_event_handler( self.EVENT["CREATE_TEMPLATES"],
                                    functools.partial(self.handle_for, "resource", "create_templates") )
        self.set_event_handler( self.EVENT["LIST_TEMPLATE_PRESETS"],
                                    functools.partial(self.handle_for, "resource", "list_template_presets") )
        self.set_event_handler( self.EVENT["LIST_TEMPLATES"],
                                    functools.partial(self.handle_for, "resource", "list_templates") )
        self.set_event_handler( self.EVENT["GET_RESPONSES_FOR_TEMPLATE"],
                                    functools.partial(self.handle_for, "resource", "get_responses_for_template") )
        self.set_event_handler( self.EVENT["GET_RESPONSES_FOR_NANOTASK"],
                                    functools.partial(self.handle_for, "resource", "get_responses_for_nanotask") )
        self.set_event_handler( self.EVENT["GET_NANOTASKS"],
                                    functools.partial(self.handle_for, "resource", "get_nanotasks") )
        self.set_event_handler( self.EVENT["UPLOAD_NANOTASKS"],
                                    functools.partial(self.handle_for, "resource", "upload_nanotasks") )
        self.set_event_handler( self.EVENT["DELETE_NANOTASKS"],
                                    functools.partial(self.handle_for, "resource", "delete_nanotasks") )
        self.set_event_handler( self.EVENT["UPDATE_NANOTASK_NUM_ASSIGNABLE"],
                                    functools.partial(self.handle_for, "resource", "update_nanotask_num_assignable") )
        self.set_event_handler( self.EVENT["SESSION"], self.handle_for_session )
        self.set_event_handler( self.EVENT["CHECK_PLATFORM_WORKER_ID_EXISTENCE_FOR_PROJECT"],
                                    functools.partial(self.handle_for, "resource", "check_platform_worker_id_existence_for_project") )

        self.set_event_handler( self.EVENT["MTURK_GET_CREDENTIALS"],
                                    functools.partial(self.handle_for, "mturk", "get_credentials") )
        self.set_event_handler( self.EVENT["MTURK_SET_CREDENTIALS"],
                                    functools.partial(self.handle_for, "mturk", "set_credentials") )
        self.set_event_handler( self.EVENT["MTURK_CLEAR_CREDENTIALS"],
                                    functools.partial(self.handle_for, "mturk", "clear_credentials") )
        self.set_event_handler( self.EVENT["MTURK_SET_SANDBOX"],
                                    functools.partial(self.handle_for, "mturk", "set_sandbox") )
        self.set_event_handler( self.EVENT["MTURK_GET_HIT_TYPES"],
                                    functools.partial(self.handle_for, "mturk", "get_hit_types") )
        self.set_event_handler( self.EVENT["MTURK_CREATE_HIT_TYPE"],
                                    functools.partial(self.handle_for, "mturk", "create_hit_type") )
        self.set_event_handler( self.EVENT["MTURK_CREATE_HITS_WITH_HIT_TYPE"],
                                    functools.partial(self.handle_for, "mturk", "create_hits_with_hit_type") )
        self.set_event_handler( self.EVENT["MTURK_LIST_QUALIFICATIONS"],
                                    functools.partial(self.handle_for, "mturk", "list_qualifications") )
        self.set_event_handler( self.EVENT["MTURK_LIST_HITS"],
                                    functools.partial(self.handle_for, "mturk", "list_hits") )
        self.set_event_handler( self.EVENT["MTURK_LIST_HITS_FOR_HIT_TYPE"],
                                    functools.partial(self.handle_for, "mturk", "list_hits_for_hit_type") )
        self.set_event_handler( self.EVENT["MTURK_EXPIRE_HITS"],
                                    functools.partial(self.handle_for, "mturk", "expire_hits") )
        self.set_event_handler( self.EVENT["MTURK_DELETE_HITS"],
                                    functools.partial(self.handle_for, "mturk", "delete_hits") )
        self.set_event_handler( self.EVENT["MTURK_CREATE_QUALIFICATION"],
                                    functools.partial(self.handle_for, "mturk", "create_qualification") )
        self.set_event_handler( self.EVENT["MTURK_ASSOCIATE_QUALIFICATIONS_WITH_WORKERS"],
                                    functools.partial(self.handle_for, "mturk", "associate_qualifications_with_workers") )
        self.set_event_handler( self.EVENT["LIST_WORKERS"],
                                    functools.partial(self.handle_for, "mturk", "list_workers") )
        self.set_event_handler( self.EVENT["MTURK_LIST_WORKERS_WITH_QUALIFICATION_TYPE"],
                                    functools.partial(self.handle_for, "mturk", "list_workers_with_qualification_type") )
        self.set_event_handler( self.EVENT["MTURK_DELETE_QUALIFICATIONS"],
                                    functools.partial(self.handle_for, "mturk", "delete_qualifications") )
        self.set_event_handler( self.EVENT["MTURK_LIST_ASSIGNMENTS"],
                                    functools.partial(self.handle_for, "mturk", "list_assignments") )
        self.set_event_handler( self.EVENT["MTURK_LIST_ASSIGNMENTS_FOR_HITS"],
                                    functools.partial(self.handle_for, "mturk", "list_assignments_for_hits") )
        self.set_event_handler( self.EVENT["MTURK_APPROVE_ASSIGNMENTS"],
                                    functools.partial(self.handle_for, "mturk", "approve_assignments") )
        self.set_event_handler( self.EVENT["MTURK_REJECT_ASSIGNMENTS"],
                                    functools.partial(self.handle_for, "mturk", "reject_assignments") )
        self.set_event_handler( self.EVENT["MTURK_GET_ASSIGNMENTS"],
                                    functools.partial(self.handle_for, "mturk", "get_assignments") )


    async def handle_for(self, _type, event_name, rid, eid, data):
        await self._handle(_type, event_name, data)

    async def handle_for_event_history(self, rid, eid, data):
        if "AllHistory" in data["Contents"]:  await self._handle("resource", "get_event_history", data)
        elif "History" in data["Contents"]:   await self._handle("resource", "set_event_history", data)

    async def handle_for_session(self, rid, eid, data):
        if data["Contents"]["Command"]=="Create":  await self._handle("resource", "create_session", data)
        elif data["Contents"]["Command"]=="Get":  await self._handle("resource", "get_template_node", data)
        elif data["Contents"]["Command"]=="SetResponse":  await self._handle("resource", "set_response", data)

    async def _handle(self, _type, name, data):
        if data["Status"]=="Success":
            for func in self.event_listeners[_type].get_handlers(name):  await func(data["Contents"], is_error=False)
        else:
            for func in self.event_listeners[_type].get_handlers(name):  await func(data, is_error=True)
