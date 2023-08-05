"""
Implements backend-related functionality.
"""

import dataclasses
import itertools
import json
import os
import pathlib
from typing import Optional, Any

import ansible_runner
import datafiles.formats
import rich.prompt
import temppathlib
import yaml
from plumbum import local, FG, BG

from pqrs import paths
from pqrs.config import config
from pqrs.version import Version


@dataclasses.dataclass
class Role:
    """
    A collection of metadata related to a single ansible role.
    """

    name: str
    collection: str
    description: list[str]
    variables: dict[str, Any]
    available_version: Version
    installed_version: Optional[Version] = None
    selected: bool = False

    @classmethod
    def from_path(cls, path, collection):
        # type: (pathlib.Path, str) -> Role
        """
        Construct a Role object from a given filesystem path. The information
        about the role is loaded from the meta/pqrs.yml file.
        """

        name = path.stem

        metadata = {}
        metadata_path = path / 'meta/pqrs.yml'

        if metadata_path.exists():
            with open(path / 'meta/pqrs.yml') as f:
                metadata = yaml.safe_load(f)

        description = metadata.get('description', '')
        available = Version(metadata.get('version', '0.0.0'))
        installed = (config.channels[collection]['roles'] or {}).get(name)
        config_vars = metadata.get('config', {})

        return cls(
            name,
            collection,
            [line.strip() for line in description.splitlines()],
            config_vars,
            available,
            Version(installed) if installed else None,
        )

    @property
    def is_outdated(self):
        # type: () -> bool
        """
        Returns True if role should be run.
        """

        return self.installed_version is None or self.available_version > self.installed_version


def discover_roles():
    # type: () -> dict[str, list[Role]]
    """
    Discovers PQRS-enabled roles on the filesystem.
    """

    # Discover the PQRS-enabled collections
    pqrs_collections = {
        f"{path.parent.parent.stem}.{path.parent.stem}": path.parent
        for path in paths.COLLECTIONS.glob('*/*/MANIFEST.json')
        if len(list(path.parent.glob('roles/*/meta/pqrs.yml'))) > 0
    }

    # Locate the roles for each collection
    return {
        collection: [
            Role.from_path(p, collection)
            for p in path.glob('roles/*')
            if (p / 'meta/pqrs.yml').exists()
        ]
        for collection, path in pqrs_collections.items()
    }

def bump_role_version(role, version=None):
    """
    Bumps the version of the role in the config to the given version. Defaults
    to latest.
    """

    # Default to the bump to the last version
    version = version or role.available_version

    # Create role dict if it does not exist
    if not config.channels[role.collection].get("roles"):
        config.channels[role.collection]["roles"] = {}

    config.channels[role.collection]["roles"][role.name] = version


def execute_roles(roles_to_run, status, stderr):
    # type: (list[str]) -> None
    """
    Executes the given roles using ansible-runner.
    """

    role_paths = [
        str(paths.COLLECTIONS / f"{collection.replace('.', '/')}/roles")
        for collection in roles_to_run
    ]

    with temppathlib.TemporaryDirectory(prefix="pqrs-", dont_delete=True) as tmpdir:
        # Dump the configuration values into a temp file
        with open(tmpdir.path / "vars.yml", "w") as f:
            # We need to use datafiles serializer directly to turn just one
            # attribute of the class into yaml
            content = datafiles.formats.YAML.serialize(config.variables)
            f.write(content)

        # Prepare the playbook. The playbook consists of a single play, which
        # configures all roles that need to be executed (=the ones that have
        # new tasks to be applied).

        # The role application is performed via the 'include_role' task
        # (instead of the simpler 'role:' play parameter), because this allows
        # us to create a try-except analogue, the "block-rescue", which will ensure
        # that subsequent roles continue executing even if the given role errors out.
        playbook = [{
            'hosts': 'localhost',
            'tasks': [
                {
                    'name': f"pqrs-meta: Wrapper for {role.name}",
                    'block': [
                        {
                            'name': f"pqrs-meta: Execute {role.name}",
                            'include_role': {'name': role.name},
                            'vars': {'role_version': role.installed_version or '0.0.0'}
                        },
                        {
                            # Use 'debug' task as a signal for us that the role successfully completed
                            'name': f"pqrs-meta: Termination guard for {role.name} - success",
                            'debug': {'msg': f"{role.name} success"},
                        },
                    ],
                    'rescue': [
                        {
                            # Use 'debug' task as a signal for us that the role failed
                            'name': f"pqrs-meta: Termination guard for {role.name} - failure",
                            'debug': {'msg': f"{role.name} failure"},
                        }
                    ]
                }
                for role in itertools.chain(*roles_to_run.values())
            ],
            'vars_files': str(tmpdir.path / "vars.yml")
        }]

        with open(tmpdir.path / "play.yml", "w") as f:
            content = datafiles.formats.YAML.serialize(playbook)
            f.write(content)

        current_role = None
        roles_by_name = {role.name: role for role in itertools.chain(*roles_to_run.values())}
        roles_success = {}

        def ensure_role_header(role_name):
            nonlocal current_role
            if role_name == current_role or role_name is None:
                return

            current_role = role_name
            role = roles_by_name.get(role_name)
            if role is not None:
                stderr.print(f"\n[magenta]{role_name}:[/] {role.installed_version or '0.0.0'} -> {role.available_version}")

        def check_event_handler(data, **kwargs):
            event_type = data.get("event")

            if event_type.startswith("runner_on_"):
                event_type = event_type.removeprefix("runner_on_")

                role = data["event_data"].get("role", "")
                task = data["event_data"].get("task", "")
                changed = data["event_data"].get("res", {}).get("changed")

                # Supress pqrs-meta: tasks
                if task.startswith("pqrs-meta:"):
                    return

                if event_type == "start":
                    # Start of the task
                    ensure_role_header(role)
                    status.update(f"{task} [dim](analyzing..)[/]")
                elif event_type == "ok":
                    # Do not print a line for built-in fact collection
                    if task == "Gathering Facts":
                        return

                    # End of the task
                    ensure_role_header(role)
                    stderr.print(f"[yellow]-[/] {task} {'[dim](no change)[/]' if not changed else ''}")
                elif event_type == "skipped":
                    # Do not print anything for skipped tasks
                    pass

        def event_handler(data, **kwargs):
            event_type = data.get("event")

            if event_type == "verbose":
                # Supress verbose messages for now
                pass
            elif event_type.startswith("playbook_on"):
                # Playbook events don't contain interesting information
                pass
            elif event_type.startswith("runner_on"):
                role = data["event_data"].get("role", "")
                task = data["event_data"].get("task", "")
                changed = data["event_data"].get("res", {}).get("changed")
                ensure_role_header(role)

                # Record success / failure from "pqrs-meta: Termination guard"(s)
                if task.startswith("pqrs-meta: Termination guard") and event_type == "runner_on_ok":
                    # The termination guard(s) are not a part of the role, so
                    # we have to extract the relevant role (and completion
                    # status) from the debug message of the guard
                    reported_role, reported_status = data["event_data"]["res"]["msg"].split()
                    roles_success[reported_role] = (reported_status == "success")

                    if roles_success[reported_role]:
                        bump_role_version(roles_by_name[reported_role])

                # Supress pqrs-meta: tasks
                if task.startswith("pqrs-meta:"):
                    return

                if event_type == "runner_on_start":
                    # Start of the task
                    status.update(f"{task} [dim](executing..)[/]")
                elif event_type == "runner_on_ok":
                    # Do not print a line for built-in fact collection
                    if task == "Gathering Facts":
                        return

                    # End of the task
                    symbol = "" if changed else "[blue]↻[/]"
                    stderr.print(f"[green]✔[/] {task} {'[dim](no change)[/]' if not changed else ''}")
                elif event_type == "runner_on_failed":
                    # Catastrohpic end of the task
                    stderr.print(f"[red][bold]✗[/] {task}")


        # Execute the playbook, using private role vars switch to ensure
        # role_version variables are not overwriting each other
        os.environ["ANSIBLE_PRIVATE_ROLE_VARS"] = "True"

        # Supress colorful output (and cows) in the stdout
        os.environ["ANSIBLE_NOCOLOR"] = "True"
        os.environ["ANSIBLE_NOCOWS"] = "True"

        # Collect all the tasks to execute and await confirmation
        stderr.print("[bold]Analyzing system for applicable updates[/]")
        runner = ansible_runner.interface.run(
            private_data_dir=str(tmpdir.path),
            project_dir=str(tmpdir.path),
            roles_path=role_paths,
            playbook="play.yml",
            event_handler=check_event_handler,
            quiet=True
        )

        current_role = None

        status.stop()
        if not rich.prompt.Confirm.ask("Do you wish to apply the updates?"):
            return

        status.update("Applying configuration updates...")
        status.start()
        stderr.print("\n\n[bold]Applying configuration updates[/]")

        runner = ansible_runner.interface.run(
            private_data_dir=str(tmpdir.path),
            project_dir=str(tmpdir.path),
            roles_path=role_paths,
            playbook="play.yml",
            event_handler=event_handler,
            quiet=True
        )

        # Print summary
        successes = [roles_by_name[role] for role, status in roles_success.items() if status is True]
        failures = [roles_by_name[role] for role, status in roles_success.items() if status is False]

        if successes or failures:
            stderr.print("\n\n[bold]Summary[/]")

        if successes:
            stderr.print(
                f"Successfully applied {len(successes)} role{'s' if len(successes) > 1 else ''}: " +
                ", ".join([f'{role.name} ({role.available_version})' for role in successes])
            )
        if failures:
            stderr.print(
                f"The following {len(failures)} role{'s' if len(failures) > 1 else ''} failed: " +
                ", ".join([f'{role.name} ({role.available_version})' for role in failures])
            )
            stdout_path = list(tmpdir.path.glob("artifacts/*/stdout"))
            if stdout_path:
                stderr.print(f"For more details, please refer to the log file: '{stdout_path[0]}'.")
