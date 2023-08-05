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
import os
import subprocess
import sys
from pathlib import Path

import click
from xmlhelpy import Choice
from xmlhelpy import option

from workflow_nodes.config.main import config


@config.command()
@option(
    "shell",
    char="s",
    description="Your shell type.",
    required=True,
    param_type=Choice(["bash", "zsh", "fish"]),
)
def activate_autocompletion(shell):
    """Activate the autocompletion for bash, zsh or fish."""

    name = "workflow-nodes"
    name_upper = name.replace("-", "_").upper()

    if shell in ["bash", "zsh"]:
        config_path = Path.home().joinpath(f".{shell}rc")
        target_path = Path.home().joinpath(f".{name}-complete.{shell}")

    elif shell == "fish":
        target_path = Path.home().joinpath(
            ".config", "fish", "completions", f"{name}.fish"
        )
        folder = os.path.dirname(target_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Due to choices, we should never go into else.
    else:
        click.echo(f"Your shell {shell} is currently not supported for autocompletion.")
        sys.exit(1)

    if os.path.exists(target_path):
        click.echo("Autocompletion is already activated.")
        sys.exit(0)

    my_env = os.environ.copy()
    my_env[f"_{name_upper}_COMPLETE"] = f"{shell}_source"

    with open(target_path, mode="w", encoding="utf-8") as f:
        subprocess.run(name, env=my_env, stdout=f)

    if shell != "fish":

        add_import = True
        with open(config_path, encoding="utf-8") as f:
            if str(target_path) in f.read():
                add_import = False

        # Add line only if not already present.
        if add_import:
            with open(config_path, "a", encoding="utf-8") as file:
                file.write("\n")
                file.write(f". {target_path}")
                file.write("\n")

    click.echo(
        f"Successfully installed {shell} completion at '{target_path}'. To use it,"
        " start a new shell."
    )
