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

@resource("docker::Container", agent = "service.host.name", id_attribute = "name")
class Container(Resource):
    """
        This class represents a docker container
    """
    fields = ("name", "enabled", "description", "admin_token", "url", "purged",
              "admin_user", "admin_password", "admin_tenant", "auth_url")
