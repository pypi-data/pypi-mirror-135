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
from xmlhelpy import Integer
from xmlhelpy import option

from .main import environment


@environment.environment(
    description="ssh node to execute commands or tools on remote computers"
)
@option(
    name="user",
    description="Username",
)
@option(
    name="host",
    description="Specifies the host address",
)
@option(
    name="confighost",
    description="Use a predefined host from the ssh config",
)
@option(
    name="port",
    description="Specifiy a certain port",
    param_type=Integer,
)
@option(
    "x-server",
    char="X",
    description="Enables X11-forwarding",
    is_flag=True,
)
@option(
    "disable-shell-sourcing",
    char="u",
    is_flag=True,
    description="Disables sourcing the configuration files ~/.profile and ~/.bashrc",
)
def ssh(*args, **kwargs):
    """Execute a tool on a remote computer using ssh"""

    binaries = ["ssh-askpass", "setsid"]

    for binary_name in binaries:
        if not shutil.which(binary_name):
            click.echo(
                f'"{binary_name} not found in PATH, please make sure it is installed.'
            )
            sys.exit(1)

    if kwargs["confighost"] and (kwargs["user"] or kwargs["host"]):
        click.echo("Please set either a confighost OR a user-host combination")
        sys.exit(1)

    cmd = ["setsid", "ssh"]

    if kwargs["user"] and kwargs["host"]:
        address = f'{kwargs["user"]}@{kwargs["host"]}'
        cmd += [address]
    elif kwargs["confighost"]:
        cmd += [kwargs["confighost"]]
    if kwargs["port"]:
        cmd += ["-p", kwargs["port"]]
    if kwargs["x_server"]:
        cmd += ["-X"]
    if not kwargs["disable_shell_sourcing"]:
        cmd += [
            f"for FILE in /etc/bash.bashrc /etc/profile $HOME/.bashrc "
            f"$HOME/.profile; do test -f $FILE && source $FILE; done && "
            f"{kwargs['env_exec'][0]}"
        ]
    else:
        cmd += [kwargs["env_exec"][0]]

    click.echo(cmd)
    sys.exit(subprocess.call(cmd))
