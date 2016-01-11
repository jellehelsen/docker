"""
    Copyright 2016 Impera

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: bart@impera.io
"""

from impera.agent.handler import provider, ResourceHandler
from impera.execute.util import Unknown
from impera.export import resource_to_id
from impera.resources import Resource, resource, ResourceNotFoundExcpetion
from impera import methods

from docker import Client


@resource("docker::Container", agent="service.host.name", id_attribute="name")
class Container(Resource):
    """
        This class represents a docker container
    """
    fields = ("name", "image", "state", "detach", "memory_limit", "command", "entrypoint")


@provider("docker::Container", name="docker")
class ContainerHandler(ResourceHandler):
    @classmethod
    def is_available(self, io):
        return True

    def __init__(self, agent, io=None):
        super().__init__(agent, io)

        self._client = None

    def pre(self, resource: Container):
        self._client = Client(base_url="unix://var/run/docker.sock")

    def post(self, resource: Container):
        self._client.close()

    def check_resource(self, resource: Container):
        current = resource.clone()
        return current

    def do_changes(self, resource: Container) -> bool:
        """
            Enforce the changes
        """
        changes = self.list_changes(resource)

        return changed

    def facts(self, resource : Container):
        """
            Get facts about this resource
        """
        return {}

