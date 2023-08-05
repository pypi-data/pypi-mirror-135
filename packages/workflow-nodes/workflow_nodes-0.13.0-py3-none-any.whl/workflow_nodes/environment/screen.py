# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import shutil
import subprocess
import sys

import click
from xmlhelpy import option

from .main import environment


@environment.environment(
    description="screen node to execute commands or tools detached in background"
)
@option(
    "name",
    char="n",
    default="kadi-workflow-node",
    description="Name the session",
)
@option(
    "resume",
    char="r",
    is_flag=True,
    description="Attempt to reattach previous session, if not existent, start new",
    exclude_from_xml=True,  # resume does not work without a terminal (in workflow)
)
def screen(name, resume, *args, **kwargs):
    """Execute a tool detached in the background using screen."""
    # Check if binaries exist
    binaries = ["screen"]
    for binary_name in binaries:
        if not shutil.which(binary_name):
            click.echo(
                f'"{binary_name}" not found in PATH, please make sure it is installed.'
            )
            sys.exit(1)
    # Assemble command
    cmd = ["screen"]
    if resume:
        cmd += ["-d", "-R"]
        if name:
            cmd += [name]
    else:
        if name:
            cmd += ["-S", name]
        cmd += ["-dm"]
        # screen gobbles up everything by itself and doesn't like the strings
        # parsed by subprocess.call(...). Therefore, split with string manipulation
        cmd += kwargs["env_exec"][0].split(" ")
    # Execute
    click.echo(cmd)
    sys.exit(subprocess.run(cmd).returncode)
