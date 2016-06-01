"""
    Copyright 2016 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

from inmanta.agent.handler import provider, ResourceHandler
from inmanta.execute.util import Unknown
from inmanta.resources import Resource, resource, ResourceNotFoundExcpetion
from inmanta import methods

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

    def list_changes(self, resource: Container) -> dict:
        """
            List the changes that are required to the vm
        """
        container_id, current = self.check_resource(resource)
        return self._diff(current, resource)

    def __init__(self, agent, io=None):
        super().__init__(agent, io)

        self._client = None

    def pre(self, resource: Container):
        self._client = Client(base_url="unix://var/run/docker.sock")

    def post(self, resource: Container):
        self._client.close()

    def check_resource(self, resource: Container):
        current = resource.clone()
        containers = self._client.containers(all=True)

        docker_resource = None
        for container in containers:
            names = container["Names"]
            search_name = resource.name
            if search_name[0] != "/":
                search_name = "/" + search_name

            if search_name in names:
                docker_resource = container


        if docker_resource is None:
            current.state = "purged"
        else:
            data = self._client.inspect_container(docker_resource["Id"])
            current.state = data["State"]["Status"]

        return current

    def do_changes(self, resource: Container) -> bool:
        """
            Enforce the changes
        """
        container_id, current = self.check_resource(resource)
        changes = self._diff(current, resource)
        changed = False

        if "state" in changes:
            state = changes["state"]
            if state[0] == "purged" and state[1] == "running":
                # ensure the image is pulled
                images = self._client.images(name=resource.image)
                if len(images) == 0:
                    msg = self._client.pull(resource.image)
                    if "not found" in msg:
                        raise Exception("Failed to pull image %s: %s" % (resource.image, msg))

                cont = self._client.create_container(image=resource.image, command=resource.command, detach=resource.detach,
                                                     host_config={"memory_limit": resource.memory_limit})
                self._client.start(cont["Id"])
                self._client.rename(cont["Id"], resource.name)

                changed = True

            elif state[1] == "purged":
                if state[0] == "running":
                    self._client.stop(container_id)

                self._client.remove_container(container_id)

        return changed

    def facts(self, resource : Container):
        """
            Get facts about this resource
        """
        return {}

