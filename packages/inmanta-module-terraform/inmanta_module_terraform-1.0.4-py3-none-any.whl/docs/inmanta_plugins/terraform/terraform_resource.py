"""
    Copyright 2021 Inmanta

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

import copy
import json
import os
import tempfile
from pathlib import Path

from inmanta_plugins.terraform.helpers.const import TERRAFORM_RESOURCE_STATE_PARAMETER
from inmanta_plugins.terraform.helpers.param_client import ParamClient
from inmanta_plugins.terraform.helpers.utils import (
    build_resource_state,
    parse_resource_state,
)
from inmanta_plugins.terraform.tf.terraform_provider_installer import ProviderInstaller
from inmanta_plugins.terraform.tf.terraform_resource_client import (
    TerraformResourceClient,
)
from inmanta_plugins.terraform.tf.terraform_resource_state import TerraformResourceState

from inmanta import resources
from inmanta.agent import config
from inmanta.agent.agent import AgentInstance
from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.agent.io.local import IOBase
from inmanta.protocol.endpoints import Client
from inmanta.resources import Id, PurgeableResource, resource


@resource(
    "terraform::Resource",
    agent="provider.agent_config.agentname",
    id_attribute="id",
)
class TerraformResource(PurgeableResource):
    fields = (
        "agent_name",
        "provider_namespace",
        "provider_type",
        "provider_version",
        "provider_alias",
        "provider_config",
        "resource_type",
        "resource_name",
        "resource_config",
        "terraform_id",
    )

    @staticmethod
    def get_id(exporter, entity):
        return f"{entity.provider.agent_config.agentname}-{entity.provider.alias}-{entity.type}-{entity.name}"

    @staticmethod
    def get_agent_name(exporter, entity) -> str:
        return entity.provider.agent_config.agentname

    @staticmethod
    def get_provider_namespace(exporter, entity) -> str:
        return entity.provider.namespace

    @staticmethod
    def get_provider_type(exporter, entity) -> str:
        return entity.provider.type

    @staticmethod
    def get_provider_version(exporter, entity) -> str:
        return entity.provider.version

    @staticmethod
    def get_provider_alias(exporter, entity) -> str:
        return entity.provider.alias

    @staticmethod
    def get_provider_config(exporter, entity) -> dict:
        return entity.provider.config

    @staticmethod
    def get_resource_type(exporter, entity) -> str:
        return entity.type

    @staticmethod
    def get_resource_name(exporter, entity) -> str:
        return entity.name

    @staticmethod
    def get_resource_config(exporter, entity) -> dict:
        return {key: value for key, value in entity.config.items() if value is not None}


@provider("terraform::Resource", name="terraform-resource")
class TerraformResourceHandler(CRUDHandler):
    def __init__(self, agent: "AgentInstance", io: "IOBase") -> None:
        super().__init__(agent, io=io)
        self.resource_client = None
        self.log_file_path = ""
        self.private_file_path = ""

    def _agent_state_dir(self, resource: TerraformResource) -> str:
        # Files used by the handler should go in state_dir/cache/<module-name>/<agent-id>/
        base_dir = config.state_dir.get()
        agent_dir = os.path.join(
            base_dir,
            "cache/terraform",
            resource.agent_name,
        )
        if Path(base_dir) not in Path(os.path.realpath(agent_dir)).parents:
            raise Exception(
                f"Illegal path, {agent_dir} is not a subfolder of {base_dir}"
            )

        return agent_dir

    def _provider_state_dir(self, resource: TerraformResource) -> str:
        # In this module, using the above path as root folder, we use one dir by provider
        # with name <provider-namespace>/<provider-type>/<provider-version>, as we have an
        # index on those three values.
        base_dir = self._agent_state_dir(resource)
        provider_dir = os.path.join(
            base_dir,
            resource.provider_namespace,
            resource.provider_type,
            resource.provider_version,
        )
        if Path(base_dir) not in Path(os.path.realpath(provider_dir)).parents:
            raise Exception(
                f"Illegal path, {provider_dir} is not a subfolder of {base_dir}"
            )

        return provider_dir

    def _resource_state_dir(self, resource: TerraformResource) -> str:
        # In this module, using the above path as root folder, we use one dir by resource
        # with name <resource-type>/<resource-name>, as we have an index on those two values.
        base_dir = self._provider_state_dir(resource)
        resource_dir = os.path.join(
            base_dir,
            resource.resource_type,
            resource.resource_name,
        )
        if Path(base_dir) not in Path(os.path.realpath(resource_dir)).parents:
            raise Exception(
                f"Illegal path, {resource_dir} is not a subfolder of {base_dir}"
            )

        return resource_dir

    def _resource_state(self, resource: TerraformResource, id: str) -> dict:
        """
        Some design choice here:
        Context: We need to save a resource state as terraform doesn't allow to get resource values
          based on any identifier amongst the attributes of the resource.  Such attributes can have
          a default value.  If we don't specify any value, Terraform will pick it automatically.
        Concern: If we save as state all the attributes with the values that Terraform picked, this
          saved state will differ from the config of the Inmanta resource.  Then, if we use this
          config in the next read operation, we will trigger an update, even if there were no
          effective changes, as the unspecified value (None) in our model will be compared to the
          the default value picked by Terraform.
        Option: We then decided to save as resource state the values set within Inmanta model with
          the addition of the resource id.  This way, we only compare values from the same origin
          ensuring consistency (as we filter this id before comparison).
        Downside: This implies that we loose track of those default values in the orchestrator.  This
          will however be solved once (if) we generate Inmanta modules automatically, setting those
          default values in the model directly.
        """
        state: dict = copy.deepcopy(resource.resource_config)
        state.update({"id": id})
        return state

    def pre(self, ctx: HandlerContext, resource: TerraformResource) -> None:
        """
        During the pre phase, we have to:
         - Install the provider binary
         - Ensure we have a state file
         - Start the provider process
        """
        provider_installer = ProviderInstaller(
            namespace=resource.provider_namespace,
            type=resource.provider_type,
            version=None
            if resource.provider_version == "latest"
            else resource.provider_version,
        )
        provider_installer.resolve()

        resource.provider_version = provider_installer.version
        # We specify the download path, so that the provider is not downloaded on every handler execution
        download_path = os.path.join(
            self._provider_state_dir(resource),
            "provider.zip",
        )
        provider_installer.download(download_path)
        binary_path, _ = provider_installer.install_dry_run(
            self._provider_state_dir(resource)
        )
        if not Path(binary_path).exists():
            # We only install the binary if it is not there.  This avoids overwritting a binary that
            # might be currently used.
            binary_path = provider_installer.install(self._provider_state_dir(resource))

        # The file in which all logs from the provider will be saved during its execution
        _, self.log_file_path = tempfile.mkstemp(suffix=".log", text=True)

        log_path = Path(self.log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch(exist_ok=True)

        private_file_path = os.path.join(
            self._resource_state_dir(resource),
            "private",
        )
        private_path = Path(private_file_path)
        private_path.parent.mkdir(parents=True, exist_ok=True)
        private_path.touch(exist_ok=True)

        param_client = ParamClient(
            self._agent.environment,
            Client("agent"),
            lambda func: self.run_sync(func),
            TERRAFORM_RESOURCE_STATE_PARAMETER,
            Id.resource_str(resource.id),
        )

        terraform_resource_state = TerraformResourceState(
            private_file_path=private_file_path,
            param_client=param_client,
            type_name=resource.resource_type,
        )

        self.resource_client = TerraformResourceClient(
            binary_path,
            self.log_file_path,
            terraform_resource_state,
        )
        self.resource_client.open(resource.provider_config)

        resource.resource_config = build_resource_state(
            resource.resource_config,
            Client("agent"),
            lambda func: self.run_sync(func),
        )

    def post(self, ctx: HandlerContext, resource: TerraformResource) -> None:
        """
        During the post phase we need to:
         - Stop the provider process
         - Cleanup the logs
        """
        self.resource_client.close()
        with open(self.log_file_path, "r") as f:
            lines = f.readlines()
            if lines:
                ctx.debug("Provider logs", logs="".join(lines))

        Path(self.log_file_path).unlink()

    def read_resource(
        self, ctx: HandlerContext, resource: resources.PurgeableResource
    ) -> None:
        """
        During the read phase, we need to:
         - Read the state, if there is none, we either:
            - Lost it, there is no way to find the resource -> resource considered purged, exit
            - Never created it -> resource considered purged, exit
         - Do a read operation with the provider process, which will return the current state of the resource
            - If it is empty, it couldn't find any -> resource considered purged, exit
            - If it is not empty, we parse the output and set our resource config
         - We save the current state
        """
        current_state = self.resource_client.read_resource()
        if current_state is None and resource.terraform_id is not None:
            self.resource_client.import_resource(resource.terraform_id)
            current_state = self.resource_client.read_resource()

        if not current_state:
            raise ResourcePurged()

        desired_state = resource.resource_config
        current_state = parse_resource_state(
            current_state, self.resource_client.resource_schema.block
        )

        # reduce the current state to only the keys we have a desired state about
        resource.resource_config = {
            k: current_state.get(k) for k in desired_state.keys()
        }

    def create_resource(
        self, ctx: HandlerContext, resource: resources.PurgeableResource
    ) -> None:
        """
        During the create phase, we need to:
         - Create the new resource with the provider process
         - Save the resource config in the state file
        """
        current_state = self.resource_client.create_resource(resource.resource_config)

        if not current_state:
            raise RuntimeError(
                "Something went wrong, the plugin didn't return the current state"
            )

        resource_id = current_state.get("id")
        if not resource_id:
            raise RuntimeError(
                "Something went wrong, the plugin didn't return any id for the created resource"
            )

        ctx.debug("Resource id is %(id)s", id=resource_id)
        ctx.debug(
            "Resource created with config: %(config)s", config=json.dumps(current_state)
        )

        ctx.set_created()

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: resources.PurgeableResource
    ) -> None:
        """
        During the update phase, we need to:
         - Read the current state
         - Update the resource with the provider process
         - Save the new state to the state file
        """
        current_state = self.resource_client.update_resource(resource.resource_config)

        if not current_state:
            raise RuntimeError(
                "Something went wrong, the plugin didn't return the current state"
            )

        resource_id = current_state.get("id")
        if not resource_id:
            raise RuntimeError(
                "Something went wrong, the plugin didn't return any id for the created resource"
            )

        ctx.debug(
            "Resource updated with config: %(config)s", config=json.dumps(current_state)
        )

        ctx.set_updated()

    def delete_resource(
        self, ctx: HandlerContext, resource: resources.PurgeableResource
    ) -> None:
        """
        During the delete phase, we need to:
         - Read the current state
         - Delete the resource with the provider process
         - Delete the state file
        """
        self.resource_client.delete_resource()

        ctx.set_purged()
