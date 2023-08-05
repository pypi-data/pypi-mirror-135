import os
import json
import tornado.web
from typing import Union
from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import APIHandler
from epi2melabs_wfpage.config import Epi2melabsWFPage
from epi2melabs.workflows.launcher import get_workflow_launcher


class LauncherAPIHandler(APIHandler):

    def __init__(self, application, request, launcher, **kwargs):
        super().__init__(application, request, **kwargs)
        self.launcher = launcher


class Workflows(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, name: Union[str, None] = None) -> None:
        """Get workflow(s)"""
        if not name:
            self.finish(json.dumps(
                self.launcher.workflows))
            return

        workflow = self.launcher.get_workflow(name)
        self.finish(json.dumps(workflow))


class Logs(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, instance_id: str) -> None:
        """Get logs(s)"""
        if instance := self.launcher.get_instance(instance_id):
            log_file = os.path.join(
                self.launcher.instance_dir,
                instance['name'], 'nextflow.stdout')

            if not os.path.exists(log_file):
                self.finish(json.dumps({}))
                return

            lines = []
            with open(log_file) as lf:
                lines = lf.readlines()
                lines = [line.rstrip() for line in lines]
                self.finish(json.dumps({'logs': lines}))
            return

        self.finish(json.dumps({}))


class Params(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, instance_id: str) -> None:
        """Get params(s)"""
        if instance := self.launcher.get_instance(instance_id):
            params_file = os.path.join(
                self.launcher.instance_dir,
                instance['name'], self.launcher.PARAMS)

            if not os.path.exists(params_file):
                self.finish(json.dumps({}))
                return

            with open(params_file, 'r') as pf:
                params = json.load(pf)
                self.finish(json.dumps({'params': params}))
            return
        self.finish(json.dumps({}))


class Path(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get path"""
        exists, error = self.launcher.validate_path(path)
        self.finish(json.dumps({
            'exists': exists,
            'error': error}))


class File(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get file"""
        exists, error = self.launcher.validate_file_path(path)
        self.finish(json.dumps({
            'exists': exists,
            'error': error}))


class Directory(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get directory"""
        exists, error = self.launcher.validate_directory_path(path)
        resp = {'exists': exists, 'error': error}
        if self.get_argument("contents", None, True) and exists:
            contents = self.launcher.list_dir(path)
            resp['contents'] = contents
        self.finish(json.dumps(resp))


class Instance(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, instance_id: Union[str, None] = None) -> None:
        """Get workflow instance(s)"""
        if instance_id:
            instance = self.launcher.get_instance(instance_id)

            # Todo: stop hacking
            instance['path'] = os.path.join(
                self.launcher.orig_dir, 'instances',
                instance['name'])

            self.finish(json.dumps(instance))
            return
        
        payload = self.get_json_body() or {}
        all_instances = self.launcher.instances

        if instance_ids := payload.get('instances'):
            self.finish(json.dumps({ 
                    k: v for (k,v) in x.items() 
                    if k in instance_ids 
                } for x in all_instances
            ))
            return

        self.finish(json.dumps(all_instances))

    @tornado.web.authenticated
    def post(self) -> None:
        """Create a new instance"""
        payload = self.get_json_body()

        if not payload:
            self.finish(json.dumps({}))
            return
        
        name = payload['workflow']
        params = payload['params']

        created, instance = self.launcher.create_instance(
            name, params)

        self.finish(json.dumps({
            'created': created, 
            'instance': instance
        }))

    @tornado.web.authenticated
    def delete(self, instance_id: Union[str, None] = None) -> None:
        """Create a new instance"""
        if not instance_id:
            self.finish(json.dumps({'deleted': False}))
            return

        payload = self.get_json_body() or {}

        self.launcher.delete_instance(
            instance_id, delete=payload.get('delete', False))
        self.finish(json.dumps({'deleted': True}))


def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    epi2melabs_wfpage = "epi2melabs-wfpage"

    # Create the launcher
    config = Epi2melabsWFPage(
        config=web_app.settings['config_manager'].config)

    launcher = {'launcher': get_workflow_launcher(
        base_dir=config.base_dir, workflows_dir=config.workflows_dir,
        remote=config.remote, ip=config.ip, port=config.port)}

    # Workflow get
    workflow_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"workflows/([-A-Za-z0-9]+)")
    workflows_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"workflows/?")

    # Instance crd
    instance_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"instances/([-A-Za-z0-9]+)")
    instances_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"instances/?")

    # Instance extras
    logs_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"logs/([-A-Za-z0-9]+)")
    params_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"params/([-A-Za-z0-9]+)")

    # Filesystem
    path_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"path/([-A-Za-z0-9_%.]+)")
    file_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"file/([-A-Za-z0-9_%.]+)")
    directory_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"directory/([-A-Za-z0-9_%.]+)")

    handlers = [
        (path_pattern, Path, launcher),
        (file_pattern, File, launcher),
        (directory_pattern, Directory, launcher),
        (workflow_pattern, Workflows, launcher),
        (workflows_pattern, Workflows, launcher),
        (instance_pattern, Instance, launcher),
        (instances_pattern, Instance, launcher),
        (logs_pattern, Logs, launcher),
        (params_pattern, Params, launcher),
    ]

    web_app.add_handlers(host_pattern, handlers)
